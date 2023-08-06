import os
from time import sleep
import pandas as pd
import numpy as np
import webbrowser
from functools import reduce
from tqdm.auto import tqdm

from trifacta.util import tfrequests
from trifacta.util.tffiles import downloadGet


class WrangleFlow:
    """
    This is the class we use to capture state of a flow
    """
    def __init__(
        self,
        conf,
        importedDataset,
        wrangledDataset,
        user,
        awsConfig,
        flowId,
        flowName,
        outputObjectId
    ):
        self.conf = conf
        self.importedDataset = importedDataset
        self.wrangledDataset = wrangledDataset
        self.user = user
        self.awsConfig = awsConfig
        self.flowId = flowId
        self.flowName = flowName
        self.outputObjectId = outputObjectId
        self.cache = {}
        return

    def _cacheGet(self, k):
        if k in self.cache:
            return self.cache[k]
        else:
            return None

    def _cachePut(self, k, v):
        self.cache[k] = v

    def _createOutputObjectId(self, execution='photon'):
        # create an output object
        payload = {
            "profiler": True,
            "execution": execution,
            "flowNodeId": self.wrangledDataset["id"],
            "isAdhoc": True,
        }

        oObj = tfrequests.post(url="/v4/outputObjects/", json=payload).json()
        awsConfig = self.awsConfig

        # establish write settings
        payload = {
            "action": "create",
            "format": "csv",
            "compression": "none",
            "header": True,
            "asSingleFile": True,
            "suffix": "_increment",
            "outputObjectId": oObj["id"],
        }
        if awsConfig:
            payload.update(
                {
                    "path": "s3://"
                    + awsConfig["defaultBucket"]
                    + self.user["outputHomeDir"]
                    + "/"
                    + self.flowName
                    + ".csv"
                }
            )
        else:
            payload.update(
                {
                    "path": "file://"
                    + self.user["outputHomeDir"]
                    + "/"
                    + self.flowName
                    + ".csv"
                }
            )

        wsObj = tfrequests.post(url="/v4/writeSettings", json=payload)

        return oObj["id"]

    def _runFlow(self):
        payload = {
            "wrangledDataset": {"id": self.wrangledDataset["id"]},
            "overrides": {
                # "execution": "emrSpark",
                "profiler": True,
            },
            # "ranfrom": "ui",
            # "testMode": False,
            # "isCanceled": False
        }
        if not self.awsConfig:
            payload["overrides"].update({"execution": "photon"})
        jobGroup = tfrequests.post(url="/v4/jobGroups/", json=payload).json()
        return jobGroup

    def _getoutputUrl(self):
        # Assumes there is only one filewriter for this jobGroup,
        # and only one scriptResult for this filewriter!
        outs = tfrequests.get(
            f"/v4/jobGroups/{self.cache['jobGroup']['id']}?embed=jobs.scriptResults"
        ).json()["jobs"]["data"]
        fw = list(filter(lambda x: x["jobType"] == "filewriter", outs))
        if len(fw) > 1:
            raise (Exception("ambiguous output; multiple filewriters for job!"))
        sr = fw[0]["scriptResults"]["data"]
        if len(sr) > 1:
            raise (Exception("ambiguous output; multiple scriptResults for job!"))
        sr0 = sr[0]
        srId = sr0["id"]
        return f"/v4/scriptResults/{srId}/download"

    def open(self, do_not_open = False):
        # open the flow for editing and return the opened url
        # if do_not_open == TRUE, just return the url
        flow = tfrequests.get(
            url="/v4/flows/" + str(self.flowId), params={"embed": "flowNodes"}
        )
        nodes = flow.json()["flowNodes"]["data"]
        lastNode = reduce((lambda x, y: x if x["id"] > y["id"] else y), nodes)
        url = (
            str(self.conf["endpoint"])
            + "/data/"
            + str(self.flowId)
            + "/"
            + str(lastNode["id"])
            + "?minimalView=true"
        )

        # assume that opening the file requires us to invalidate the result cache
        self.cache = {}
        if not do_not_open:
            print("Opening " + url)
            webbrowser.open_new(url)
        return(url)

    def runJob(self, pbar=None, execution='photon'):
        # run the flow, return the jobGroup object. this is a blocking call.
        # as a side-effect, cache the outputObjectId and outputUrl
        # We repeatedly increment the pbar by 10% of the remainder as we poll.
        # If the pbar is passed in, the caller is then responsible
        # to complete and close the bar.
        close_pbar = False
        if not pbar:
            close_pbar = True
            pbar = tqdm(total=100)
        wf = self
        if wf.outputObjectId is None:
            wf.outputObjectId = wf._createOutputObjectId(execution=execution)

        if pbar:
            pbar.set_description("starting flow")
            # increment by 10% of the remainder
            pbar.update((pbar.total - pbar.n) / 10)
        jobGroup = wf._runFlow()
        self._cachePut("jobGroup", jobGroup)

        if pbar:
            pbar.set_description("transforming and profiling data")
            # increment by 10% of the remainder
            pbar.update((pbar.total - pbar.n) / 10)
        url = f"/v4/jobgroups/{jobGroup['id']}/status"
        resp = None
        while resp is None or resp.json() != "Complete":
            resp = tfrequests.get(url)
            if resp.json() != "Complete":
                sleep(1)
                if pbar and pbar.n < (pbar.total - 1):
                    # increment by 10% of the remainder
                    pbar.update((pbar.total - pbar.n) / 10)

        self._cachePut("outputUrl", self._getoutputUrl())

        if close_pbar:
            pbar.update(pbar.total - pbar.n)
            pbar.close()
        return jobGroup

    def profile(self):
        if self._cacheGet("prof"):
            return self._cacheGet("prof")

        jobGroup = self._cacheGet("jobGroup")
        if jobGroup is None:
            jobGroup = self.runJob()

        url = f"/v4/jobgroups/{jobGroup['id']}/profile"
        resp = tfrequests.get(url)

        self._cachePut("prof", resp.json())
        return self._cacheGet("prof")

    def dqBars(self, showTypes=True):
        hist = self.profile()["profilerTypeCheckHistograms"]
        if showTypes:
            types = self.colTypes()
            rows = [
                {
                    **{"column": f"{h} ({t})"},
                    **{cat["key"]: cat["count"] for cat in hist[h]},
                }
                for h, t in zip(hist, types["type"])
            ]
        else:
            rows = [
                {**{"column": h}, **{cat["key"]: cat["count"] for cat in hist[h]}}
                for h in hist
            ]
        df = pd.DataFrame(columns=["column", "VALID", "INVALID", "EMPTY"])
        df = pd.DataFrame(rows)
        df = df.reindex(columns=["column", "VALID", "INVALID", "EMPTY"]).set_index(
            "column"
        )
        df = df.replace(np.nan, 0)
        return df

    def colTypes(self):
        return pd.DataFrame(
            [(k, v[0]) for (k, v) in self.profile()["columnTypes"].items()],
            columns=["name", "type"],
        )

    def _numericBarsDf(self, col, name):
        # min = col['min']
        # max = col['max']
        # roundMin = col['roundMin']
        # roundMax = col['roundMax']
        # quartiles = col['quartiles']
        df = (
            pd.DataFrame(col["buckets"])
            .rename(columns={"pos": name, "b": "count"})
            .set_index(name)
        )
        return df

    def _categoricalBarsDf(self, col, name):
        # k = col['k']
        # c = col['c']
        # ub = col['ub']
        df = pd.DataFrame(col["topk"]).rename(columns={"key": name}).set_index(name)
        return df

    def _barsDf(self, col, name):
        if "buckets" in col:
            df = self._numericBarsDf(col, name)
        elif "topk" in col:
            df = self._categoricalBarsDf(col, name)
        else:
            raise (
                TypeError(f"neither buckets not topk given for bar chart in {name}!")
            )
        return df

    def barsDfList(self):
        hist = self.profile()["profilerValidValueHistograms"]
        return [self._barsDf(hist[col], col) for col in hist]

    def _numericSummaryDf(self, col, name):
        schema = col.keys() - ["buckets", "quartiles"]
        row = {"column": name, "type": self.profile()["columnTypes"][name]}
        row.update({k: col[k] for k in schema})
        row.update(col["quartiles"])
        return row

    def _categoricalSummaryDf(self, col, name):
        schema = col.keys() - ["topk"]
        row = {"column": name, "type": self.profile()["columnTypes"][name]}
        row.update({k: col[k] for k in schema})
        return row

    def summary(self):
        hist = self.profile()["profilerValidValueHistograms"]
        data = []
        for col in hist:
            if "buckets" in hist[col]:
                data.append(self._numericSummaryDf(hist[col], col))
            elif "topk" in hist[col]:
                data.append(self._categoricalSummaryDf(hist[col], col))
            else:
                raise (
                    TypeError(f"neither buckets not topk given for summary of {col}!")
                )
        data
        df = pd.DataFrame(data).set_index("column")
        return df

    def pdfProfile(self, filename=None):
        if self._cacheGet("pdfProf"):
            return self._cacheGet("pdfProf")
        if self._cacheGet("jobGroup") is None:
            self.runJob()
        jobGroup = self._cacheGet("jobGroup")
        url = f"/v4/jobgroups/{jobGroup['id']}/pdfResults"
        resp = None
        # poll until job completes, sleeping between polls
        while resp is None or resp.status_code == 404:
            resp = tfrequests.raw_get(url)
            if resp.status_code == 404:
                sleep(1)
        self._cachePut("pdfProf", resp)
        if filename:
            with open(filename, "wb") as fd:
                for chunk in resp.iter_content(chunk_size=128):
                    fd.write(chunk)
        return resp

    def output(self, filename=None, noDf=False):
        if (filename is None) and (noDf == False) and not (self._cacheGet("outDf") is None):
            return self._cacheGet("outDf")
        if not self._cacheGet("jobGroup"):
            self.runJob()
        result = downloadGet(self._cacheGet("outputUrl"), filename)
        if not noDf:
            df = pd.read_csv(result)
            self._cachePut("outDf", df)
        if not filename:
            # clean up tempfile created by downloadGet
            os.remove(result)
        return df

    def _tf_cleanup(self):
        # garbage collect state in Trifacta
        # first the flow; presumably this cascades delete to
        # OutputObject, writeSettings, and wrangledDataset
        tfrequests.delete(f"/v4/flows/{self.flowId}")

        # then the importedDataset
        tfrequests.delete(f"/v4/importedDatasets/{self.importedDataset}")

    def open_profile(self):
        if self._cacheGet('jobGroup') is None:
            self.runJob()
        url = (
                str(self.conf["endpoint"])
                + "/jobs/"
                + str(self._cacheGet('jobGroup')['id'])
                + "?activeTab=profile"
        )
        print("Opening " + url)
        webbrowser.open_new(url)
        return url

    def get_pandas(self, column_names, add_to_next_cell=False):
        if self.outputObjectId is None:
            self.outputObjectId = self._createOutputObjectId()

        request_params = {
            "orderedColumns": ",".join([name.strip() for name in column_names])
        }
        response = tfrequests.post(
            '/v4/outputObjects/{0}/wrangleToPython'.format(self.outputObjectId),
            json=request_params
        ).json()

        if add_to_next_cell:
            self._add_source_to_next_notebook_cell(response["pythonScript"])
        else:
            return response["pythonScript"]

    @staticmethod
    def _add_source_to_next_notebook_cell(contents):
        from IPython.core.getipython import get_ipython
        shell = get_ipython()
        shell.set_next_input(contents, replace=False)

    def __del__(self):
        self._tf_cleanup()
