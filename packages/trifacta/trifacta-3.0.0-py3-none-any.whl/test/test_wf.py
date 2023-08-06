from trifacta.util import tfrequests as tfr
import requests
import pdftotext


class TestWfClass:
    # runJob: exercised by tfobjects

    def test_profile(self, wf):
        prof = wf.profile()
        wf.profile() # exercise the cache line
        assert(len(prof['profilerTypeCheckHistograms']) == 2)
        assert(len(prof['columnTypes']) == 2)
        assert(len(prof['profilerValidValueHistograms']) == 2)

    def test_profile2(self, wf2):
        prof = wf2.profile()
        wf2.profile() # exercise the cache line
        assert(len(prof['profilerTypeCheckHistograms']) == 2)
        assert(len(prof['columnTypes']) == 2)
        assert(len(prof['profilerValidValueHistograms']) == 2)

    def test_dqBars(self, wf):
        dq = wf.dqBars()
        cols = set(dq.columns)
        assert(len(dq) == 2) # one per column of df
        assert(len(cols) == 3) # VALID, INVALID, EMPTY
        assert(cols == set(['VALID', 'INVALID', 'EMPTY']))

        dq = wf.dqBars(False)
        cols = set(dq.columns)
        assert(len(dq) == 2) # one per column of df
        assert(len(cols) == 3) # VALID, INVALID, EMPTY
        assert(cols == set(['VALID', 'INVALID', 'EMPTY']))

    def test_colTypes(self, wf):
        types = wf.colTypes()
        assert(types['type'][0] == 'Integer')
        assert(types['type'][1] == 'String')
 
    def test_barsDfList(self, wf):
        columns = wf.barsDfList()
        assert(len(columns) == 2)
        assert(columns[0]['count'].sum() == 3)
        assert(len(columns[0].columns) == 1)
        assert(columns[1]['count'].sum() == 3)
        assert(len(columns[1].columns) == 1)

    def test_summary(self, wf):
        s = wf.summary()
        assert(len(s) == 2)
        assert(set(s.columns) == set(['type','roundMin','roundMax','max','min','q1','q2','q3','ub','c','k']))
        assert(s['roundMin'].count() == 1) # only 1 numeric column
        assert(s['ub'].count() == 1) # only 1 categorical

    def test_pdfProfile(self, wf, tmpdir):
        filepath = tmpdir.join("output.pdf")
        wf.pdfProfile(filepath)
        wf.pdfProfile(filepath) # exercise cached case
        with open(filepath, "rb") as f:
            pdf = pdftotext.PDF(f)
        assert(pdf[0][0:6] == 'Report')

    def test_output(self, df, wf, tmpdir):
        assert(wf.output(tmpdir.join("output.csv")).to_csv() == df.reset_index().to_csv())
        wf.cache['outDf'] = None # reset the df cache to test the tempfile construction
        assert(wf.output().to_csv() == df.reset_index().to_csv())
        assert(wf.output().to_csv() == df.reset_index().to_csv())

    # run last, as it forces recomputing tfobjects on next call
    def test_open(self, wf):
        url = wf.open(True)
        r = requests.get(url, auth=tfr.get_auth())
        assert(r.status_code == 200)


 
