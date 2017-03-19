import unittest
import softwareprocess.dispatch as d

class DispatchTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

# -----------------------------------------------------------------------
# ---- Acceptance Tests
# 100 dispatch
#   Desired level of confidence: boundary value analysis
#       inputs:     values ->   dictionary of one or more key values
#       outputs:    dictionary of params and result
#   Happy Path Analysis
#       values:         predict op  {'op':'predict'}
#                       adjust op   {'op':'adjust'}
#                       correct op  {'op':'correct'}
#                       locate op   {'op':'locate'}
#   Sad Path Analysis
#       op:             no op       {}
#                       not dict    42
#                       not op      {'op':'unknown'}
#                       missing value
#Happy Path
    def test100_001_Success_AdjustOp(self):
        result = d.dispatch({'op':'adjust'})
        self.assert_(not ('error' in result), "adjust op not recognized")

    def test100_002_Success_PredictOp(self):
        result = d.dispatch({'op':'predict'})
        self.assert_(not ('error' in result), "predict op not recognized")

    def test100_003_Success_CorrectOp(self):
        result = d.dispatch({'op':'correct'})
        self.assert_(not ('error' in result), "correct op not recognized")

    def test100_004_Success_LocateOp(self):
        result = d.dispatch({'op':'locate'})
        self.assert_(not ('error' in result), "locate op not recognized")

#Sad Path
    def test100_010_Error_EmptyDict(self):
        result = d.dispatch({})
        self.assert_(result['error'] == 'no op is specified')

    def test100_011_Error_NotDict(self):
        result = d.dispatch(42)
        self.assert_(result['error'] == 'parameter is not a dictionary')

    def test100_012_Error_NotValidOp(self):
        result = d.dispatch({'op':'unknown'})
        self.assert_(result['error'] == 'op is not a legal operation')

    def test100_013_Error_noDict(self):
        result = d.dispatch()
        self.assert_(result['error'] == 'dictionary is missing')



# 200 adjust
#   Happy Path Analysis:
#       observation:    low value   0d0.0
#                       nom value   45d30.0
#                       high value  89d59.9
#       height:         low value   0
#                       nom value   300
#                       missing value
#       temperature:    low value   -20
#                       nom value   60
#                       high value  120
#       pressure:       low value   100
#                       nom value   600
#                       high value  1100
#       horizon:        value1      artificial
#                       value2      natural
#                       value3      ArtiFICIal
#                       value4      NatuRAL
#                       missing value