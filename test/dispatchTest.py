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
        self.assert_(not (d.ERROR_OP_NOT_LEGAL in result), "adjust op not recognized")

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
    def test100_100_Error_EmptyDict(self):
        result = d.dispatch({})
        self.assert_(result['error'] == d.ERROR_OP_NOT_SPECIFIED)

    def test100_101_Error_NotDict(self):
        result = d.dispatch(42)
        self.assert_(result['error'] == d.ERROR_PARAM_NOT_DICTIONARY)

    def test100_102_Error_NotValidOp(self):
        result = d.dispatch({'op':'unknown'})
        self.assert_(result['error'] == d.ERROR_OP_NOT_LEGAL)

    def test100_103_Error_noDict(self):
        result = d.dispatch()
        self.assert_(result['error'] == d.ERROR_DICTIONARY_MISSING)



# 200 adjust
#   Desired level of confidence: boundary value analysis
#       inputs:     values -> dictionary of key values, passed from dispatch
#       outputs:    dictionary of params and result of calculation
#   Happy Path Analysis:
#       observation:    low value       0d0.0
#                       nom value       45d30.0
#                       high value      89d59.9
#       height:         low value       0
#                       nom value       300
#                       missing value
#       temperature:    low value        -20
#                       nom value       60
#                       high value      120
#                       missing value
#       pressure:       low value       100
#                       nom value       600
#                       high value      1100
#                       missing value
#       horizon:        value1          artificial
#                       value2          natural
#                       value3          ArtiFICIal
#                       value4          NatuRAL
#                       missing value
#
#   Sad Path Analysis:
#       observation:    low violation   -1d-1.1
#                       high violation  90d60.0
#                       missing value
#       height:         low violation   -1
#       temp:           low violation   -21
#                       high violation  121
#       pressure:       low violation   99
#                       high violation  1101
#       horizon:        invalid param   unknown

# Happy Path
#Observation param
    def test200_001_Success_ObsLowbound(self):
        result = d.adjust({'op':'adjust','observation':'0d0.0'})
        self.assert_(not (d.ERROR_INVALID_OBSERVATION in result))

    def test200_002_Success_ObsNom(self):
        result = d.adjust({'op':'adjust','observation':'45d30.0'})
        self.assert_(not (d.ERROR_INVALID_OBSERVATION in result))

    def test200_003_Success_ObsHighbound(self):
        result = d.adjust({'op':'adjust','observation':'89d59.9'})
        self.assert_(not (d.ERROR_INVALID_OBSERVATION in result))

#Height param
    def test200_011_Success_HeightLowbound(self):
        result = d.adjust({'op':'adjust','observation':'0d0.0','height':'0'})
        if('error' in result):
            self.assert_(result['error'] != d.ERROR_INVALID_HEIGHT)
        else:
            self.assert_(True)

    def test200_012_Success_HeightNom(self):
        result = d.adjust({'op':'adjust','observation':'0d0.0','height':'300'})
        if ('error' in result):
            self.assert_(result['error'] != d.ERROR_INVALID_HEIGHT)
        else:
            self.assert_(True)

    def test200_013_Success_HeightNotGiven(self):
        result = d.adjust({'op':'adjust','observation':'0d0.0'})
        self.assert_(result['height'] == '0')

#Pressure param
    def test200_021_Success_PressureLowbound(self):
        result = d.adjust({'op':'adjust','observation':'0d0.0','pressure':'100'})
        if ('error' in result):
            self.assert_(result['error'] != d.ERROR_INVALID_PRESSURE)
        else:
            self.assert_(True)

    def test200_021_Success_PressureNom(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0', 'pressure': '600'})
        if ('error' in result):
            self.assert_(result['error'] != d.ERROR_INVALID_PRESSURE)
        else:
            self.assert_(True)

    def test200_021_Success_PressureHighbound(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0', 'pressure': '1100'})
        if ('error' in result):
            self.assert_(result['error'] != d.ERROR_INVALID_PRESSURE)
        else:
            self.assert_(True)

    def test200_021_Success_PressureNotGiven(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0'})
        self.assert_(result['pressure'] == '1010')

#Sad Path
#Observation Param
    def test200_101_Error_ObsLowboundViolation(self):
        result = d.adjust({'op':'adjust','observation':'-1d-1.1'})
        self.assert_(result['error'] == d.ERROR_INVALID_OBSERVATION)

    def test200_102_Error_ObsHighboundViolation(self):
        result = d.adjust({'op':'adjust','observation':'90d60.0'})
        self.assert_(result['error'] == d.ERROR_INVALID_OBSERVATION)

    def test200_103_Error_ObsNotIncluded(self):
        result = d.adjust({'op':'adjust'})
        self.assert_(result['error'] == d.ERROR_MANDATORY_INFO_MISSING)

#Height param
    def test200_111_Error_HeightLowboundViolation(self):
        result = d.adjust({'op':'adjust','observation':'0d0.0','height':'-1'})
        self.assert_(result['error'] == d.ERROR_INVALID_HEIGHT)

#Pressure param
    def test300_121_Error_PressureLowboundViolation(self):
        result = d.adjust({'op':'adjust','observation':'0d0.0','pressure':'99'})
        self.assert_(result['error'] == d.ERROR_INVALID_PRESSURE)

     def test200_122_Error_PressureHighboundViolation(self):
         result = d.adjust({'op': 'adjust', 'observation': '0d0.0','pressure': '1101'})
         self.assert_(result['error'] == d.ERROR_INVALID_PRESSURE)