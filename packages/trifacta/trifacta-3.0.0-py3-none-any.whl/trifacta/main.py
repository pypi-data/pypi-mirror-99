import os
import tempfile
from slugify import slugify
import pandas as pd
from tqdm.auto import tqdm

from trifacta.util import tfrequests
from trifacta.util.tffiles import uploadFile
from trifacta.tfobjects.wrangle_flow import WrangleFlow


def _createWrangleFlow(infile, dsName, pkg=None, flow_execution='photon'):
    pbar = tqdm(total=100)
    if pbar:
        pbar.update(0)

    # get current user and configuration info
    pbar.set_description("getting config info")
    user = tfrequests.get(url="/v4/people/current").json()
    conf = dict(tfrequests.get_config())
    awsConfig = None
    r = tfrequests.raw_get(url="/v4/awsConfigs/current", params={"limit": 1})
    if r.status_code == 200:
        data = r.json()
        if data:
            awsConfig = data
    if pbar:
        pbar.update(20)

    # upload infile to trifacta
    pbar.set_description("uploading data")
    resp = uploadFile(
        path=infile, filename=os.path.basename(infile), user=user, awsConfig=awsConfig
    )
    if pbar:
        pbar.update(20)
    up = resp

    # create importedDataset
    if awsConfig:
        uri = up["type"] + "://" + up["bucket"] + up["path"]
    else:
        uri = up["type"] + "://" + up["path"]

    pbar.set_description("finishing data import")
    importedDataset = tfrequests.post(
        "/v4/importedDatasets", json={"name": up["name"], "uri": uri}
    ).json()["id"]
    if pbar:
        pbar.update(20)

    # create a flow
    pbar.set_description("creating flow")
    if not dsName:
        dsName = os.path.basename(str(infile))
    slugname = slugify(dsName)
    payload = {
        # "workspaceId": 1, ## do we need this param?  I'm not sure!
        "name": slugname,
        "description": "python-generated flow",
    }
    resp = tfrequests.post(url="/v4/flows/", json=payload).json()
    flowId = resp["id"]
    flowName = slugify(resp["name"])
    if pbar:
        pbar.update(20)

    # create a wrangledDataset within this flow based on our importedDataset ds
    pbar.set_description("creating output staging")
    payload = {
        "name": flowName,
        "importedDataset": {"id": importedDataset},
        "flow": {"id": flowId},
    }
    wrangledDataset = tfrequests.post(url="/v4/wrangledDatasets/", json=payload).json()
    if pbar:
        pbar.update(20)

    # create the WrangleFlow object
    wf = WrangleFlow(
        conf, importedDataset, wrangledDataset, user, awsConfig, flowId, flowName, None
    )
    pbar.set_description("wrangle flow established")
    pbar.close()
    return wf


def wrangleDf(df, pkg=None, dsName=None, index=False, flow_execution='photon'):
    with tempfile.NamedTemporaryFile() as tmp:
        df.to_csv(tmp.name, index=index, quoting=1)
        wf = _createWrangleFlow(tmp.name, dsName="dataframe", flow_execution=flow_execution)
    return wf


def wrangleFile(infile, pkg=None, dsName=None, flow_execution='photon'):
    return _createWrangleFlow(infile, pkg, dsName, flow_execution=flow_execution)


def wrangle(input, pkg=None, dsName=None, flow_execution='photon'):
    if type(input) == pd.core.frame.DataFrame:
        return wrangleDf(input, pkg, dsName, flow_execution=flow_execution)
    else:
        return wrangleFile(input, pkg, dsName, flow_execution=flow_execution)
