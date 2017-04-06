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
        self.assert_(not (d.ERROR_OP_NOT_LEGAL in result), "predict op not recognized")

    def test100_003_Success_CorrectOp(self):
        result = d.dispatch({'op':'correct'})
        self.assert_(not (d.ERROR_OP_NOT_LEGAL in result), "correct op not recognized")

    def test100_004_Success_LocateOp(self):
        result = d.dispatch({'op':'locate'})
        self.assert_(not (d.ERROR_OP_NOT_LEGAL in result), "locate op not recognized")

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
#       observation:    low value       > 0d0.0
#                       nom value       = 45d30.0
#                       high value      < 89d59.9
#       height:         low value       > 0
#                       nom value       < 300
#                       missing value
#       temperature:    low value       > -20
#                       nom value       = 60
#                       high value      < 120
#                       missing value
#       pressure:       low value       >= 100
#                       nom value       = 600
#                       high value      <= 1100
#                       missing value
#       horizon:        value1          = artificial
#                       value2          = natural
#                       value3          = ArtiFICIal
#                       value4          = NatuRAL
#                       missing value
#       output:
#                       Outputs the altitude of a sighting based on given parameters.
#                           low observation, nom height, nom temperature, nom pressure, artificial horizon
#                           high observation, nom height, nom temperature, nom pressure, artificial horizon
#                           nom observation, low height, nom temperature, nom pressure, natural horizon
#                           nom observation, nom height, nom temperature, low pressure, artificial horizon
#                           nom observation, nom height, nom temperature, high pressure, artificial horizon
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
        if ('error' in result):
            self.assertNotEquals(result['error'], d.ERROR_INVALID_OBSERVATION)
        else:
            self.assert_(True)

    def test200_002_Success_ObsNom(self):
        result = d.adjust({'op':'adjust','observation':'45d30.0'})
        if ('error' in result):
            self.assertNotEquals(result['error'], d.ERROR_INVALID_OBSERVATION)
        else:
            self.assert_(True)

    def test200_003_Success_ObsHighbound(self):
        result = d.adjust({'op':'adjust','observation':'89d59.9'})
        if ('error' in result):
            self.assertNotEquals(result['error'], d.ERROR_INVALID_OBSERVATION)
        else:
            self.assert_(True)

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
        if('error' in result):
            self.assert_(result['error'] != d.ERROR_INVALID_HEIGHT)
        elif ('height' in result):
            self.assert_(result['height'] == '0')
        else:
            self.assert_(False)

#temperature param
    def test200_031_Success_TempLowbound(self):
        result = d.adjust({'op':'adjust','observation':'0d0.0','temperature':'-20'})
        if('error' in result):
            self.assertNotEqual(result['error'], d.ERROR_INVALID_TEMPERATURE)
        else:
            self.assert_(True)

    def test200_032_Success_TempNom(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0', 'temperature': '60'})
        if ('error' in result):
            self.assertNotEqual(result['error'], d.ERROR_INVALID_TEMPERATURE)
        else:
            self.assert_(True)

    def test200_033_Success_TempHighbound(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0', 'temperature': '120'})
        if ('error' in result):
            self.assertNotEqual(result['error'], d.ERROR_INVALID_TEMPERATURE)
        else:
            self.assert_(True)

    def test200_034_Success_TempNotGiven(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0'})
        if ('error' in result):
            self.assertNotEqual(result['error'], d.ERROR_INVALID_TEMPERATURE)
        if('temperature' in result):
            self.assertEqual(result['temperature'], '72')
        else:
            self.assert_(False)

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
        if ('pressure' in result):
            self.assert_(result['pressure'] == '1010')
        else:
            self.assert_(False)

#horizon param
    def test200_041_Success_HorizonArtificialLowercase(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0', 'horizon': 'artificial'})
        if('error' in result):
            self.assertNotEqual(result['error'], d.ERROR_INVALID_HORIZON)
        else:
            self.assert_(True)

    def test200_042_Succcess_HorizonNaturalLowercase(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0', 'horizon': 'natural'})
        if ('error' in result):
             self.assertNotEqual(result['error'], d.ERROR_INVALID_HORIZON)
        else:
             self.assert_(True)

    def test200_043_Success_HorizonArtificialCaseInsensitive(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0', 'horizon': 'ArtiFICIal'})
        if ('error' in result):
            self.assertNotEqual(result['error'], d.ERROR_INVALID_HORIZON)
        else:
            self.assert_(True)

    def test200_044_Success_HorizonNaturalCaseInsensitive(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0', 'horizon': 'NatuRAL'})
        if ('error' in result):
            self.assertNotEqual(result['error'], d.ERROR_INVALID_HORIZON)
        else:
            self.assert_(True)

    def test200_045_Success_HorizonNotGiven(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0'})
        self.assert_('horizon' in result)
        self.assertEqual(result['horizon'], 'natural')

#Calculation
    def test200_051_Success_ObsLowboundCalc(self):
        result = d.adjust({'op':'adjust','observation':'0d0.0','height':'300','temperature':'60','pressure':'600','horizon':'artificial'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '-0d2.7')

    def test200_052_Success_ObsHighboundCalc(self):
        result = d.adjust({'op': 'adjust', 'observation': '89d30.0', 'height': '300', 'temperature': '60', 'pressure': '600','horizon': 'artificial'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '89d27.3')

    def test200_053_Success_HeightLowboundCalc(self):
        result = d.adjust(
            {'op': 'adjust', 'observation': '45d30.0', 'height': '0', 'temperature': '60', 'pressure': '600',
             'horizon': 'natural'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '45d27.3')

    def test200_054_Success_PressureLowboundCalc(self):
        result = d.adjust(
            {'op': 'adjust', 'observation': '45d30.0', 'height': '300', 'temperature': '60', 'pressure': '100',
             'horizon': 'artificial'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '45d29.5')

    def test200_055_Success_PressureHighboundCalc(self):
        result = d.adjust(
            {'op': 'adjust', 'observation': '45d30.0', 'height': '300', 'temperature': '60', 'pressure': '1100',
             'horizon': 'artificial'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '45d25.0')

    def test200_056_Success_NaturalHorizonCalc(self):
        result = d.adjust(
            {'op': 'adjust', 'observation': '45d30.0', 'height': '300', 'temperature': '60', 'pressure': '600',
             'horizon': 'natural'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '45d10.5')


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

#Temperature param
    def test200_131_Error_TemperatureLowboundViolation(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0', 'temperature': '-21'})
        self.assertEqual(result['error'], d.ERROR_INVALID_TEMPERATURE)

    def test200_132_Error_TemperatureHighboundViolation(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0', 'temperature': '121'})
        self.assertEqual(result['error'], d.ERROR_INVALID_TEMPERATURE)

#Pressure param
    def test200_121_Error_PressureLowboundViolation(self):
        result = d.adjust({'op':'adjust','observation':'0d0.0','pressure':'99'})
        self.assert_(result['error'] == d.ERROR_INVALID_PRESSURE)

    def test200_122_Error_PressureHighboundViolation(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0','pressure': '1101'})
        self.assert_(result['error'] == d.ERROR_INVALID_PRESSURE)

#horizon param
    def test200_141_Error_HorizonInvalidInput(self):
        result = d.adjust({'op': 'adjust', 'observation': '0d0.0', 'horizon':'unknown'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], d.ERROR_INVALID_HORIZON)

# 300 predict
# Desired level of confidence: boundary value analysis
#       inputs:   values -> dictionary of key values, passed from dispatch
#       outputs:  dictionary of params and result of prediction
# Happy Path Analysis:
#       body:   nom value       Betelgeuse
#       date:   nom value       2016-01-17
#               missing value
#       time:   nom value       3:15:42
#               missing value
#       output: outputs the calculated prediction
#
# Sad Path Analysis:
#       body:   invalid body    asdf
#               missing value
#       date:   invalid date    13/13/9999
#       time:   invalid time    25:61:61

#Happy Path

#Sad Path
    def test300_110_Error_StarNotInCatalogue(self):
        result = d.predict({'op': 'predict', 'body': 'asdf', 'date': '2016-01-17', 'time': '03:15:42'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], d.ERROR_STAR_NOT_IN_CATALOGUE)

    def test300_111_Error_InvalidDate(self):
        result = d.predict({'op': 'predict', 'body': 'Betelgeuse', 'date': '13/13/9999', 'time': '03:15:42'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], d.ERROR_INVALID_DATE)

    def test300_112_Error_InvalidTime(self):
        result = d.predict({'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '25:61:61'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], d.ERROR_INVALID_TIME)

    def test300_113_Error_NoBody(self):
        result = d.predict({'op': 'predict', 'date': '2016-01-17', 'time': '25:61:61'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], d.ERROR_MANDATORY_INFO_MISSING)

    def test300_114_Error_ContainsLat(self):
        result = d.predict({'op': 'predict', 'body': 'asdf', 'date': '2016-01-17', 'time': '03:15:42', 'lat':})
