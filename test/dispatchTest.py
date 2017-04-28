import unittest
import softwareprocess.dispatch as dispatch
import softwareprocess.adjust as adjust
import softwareprocess.predict as predict
import softwareprocess.correct as correct

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
        result = dispatch.dispatch({'op': 'adjust'})
        self.assert_(not (dispatch.ERROR_OP_NOT_LEGAL in result), "adjust op not recognized")

    def test100_002_Success_PredictOp(self):
        result = dispatch.dispatch({'op': 'predict'})
        self.assert_(not (dispatch.ERROR_OP_NOT_LEGAL in result), "predict op not recognized")

    def test100_003_Success_CorrectOp(self):
        result = dispatch.dispatch({'op': 'correct'})
        self.assert_(not (dispatch.ERROR_OP_NOT_LEGAL in result), "correct op not recognized")

    def test100_004_Success_LocateOp(self):
        result = dispatch.dispatch({'op': 'locate'})
        self.assert_(not (dispatch.ERROR_OP_NOT_LEGAL in result), "locate op not recognized")

#Sad Path
    def test100_100_Error_EmptyDict(self):
        result = dispatch.dispatch({})
        self.assert_(result['error'] == dispatch.ERROR_OP_NOT_SPECIFIED)

    def test100_101_Error_NotDict(self):
        result = dispatch.dispatch(42)
        self.assert_(result['error'] == dispatch.ERROR_PARAM_NOT_DICTIONARY)

    def test100_102_Error_NotValidOp(self):
        result = dispatch.dispatch({'op': 'unknown'})
        self.assert_(result['error'] == dispatch.ERROR_OP_NOT_LEGAL)

    def test100_103_Error_noDict(self):
        result = dispatch.dispatch()
        self.assert_(result['error'] == dispatch.ERROR_DICTIONARY_MISSING)



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
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0'})
        if ('error' in result):
            self.assertNotEquals(result['error'], dispatch.ERROR_INVALID_OBSERVATION)
        else:
            self.assert_(True)

    def test200_002_Success_ObsNom(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '45d30.0'})
        if ('error' in result):
            self.assertNotEquals(result['error'], dispatch.ERROR_INVALID_OBSERVATION)
        else:
            self.assert_(True)

    def test200_003_Success_ObsHighbound(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '89d59.9'})
        if ('error' in result):
            self.assertNotEquals(result['error'], dispatch.ERROR_INVALID_OBSERVATION)
        else:
            self.assert_(True)

#Height param
    def test200_011_Success_HeightLowbound(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'height': '0'})
        if('error' in result):
            self.assert_(result['error'] != dispatch.ERROR_INVALID_HEIGHT)
        else:
            self.assert_(True)

    def test200_012_Success_HeightNom(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'height': '300'})
        if ('error' in result):
            self.assert_(result['error'] != dispatch.ERROR_INVALID_HEIGHT)
        else:
            self.assert_(True)

    def test200_013_Success_HeightNotGiven(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0'})
        if('error' in result):
            self.assert_(result['error'] != dispatch.ERROR_INVALID_HEIGHT)
        elif ('height' in result):
            self.assert_(result['height'] == '0')
        else:
            self.assert_(False)

#temperature param
    def test200_031_Success_TempLowbound(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'temperature': '-20'})
        if('error' in result):
            self.assertNotEqual(result['error'], dispatch.ERROR_INVALID_TEMPERATURE)
        else:
            self.assert_(True)

    def test200_032_Success_TempNom(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'temperature': '60'})
        if ('error' in result):
            self.assertNotEqual(result['error'], dispatch.ERROR_INVALID_TEMPERATURE)
        else:
            self.assert_(True)

    def test200_033_Success_TempHighbound(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'temperature': '120'})
        if ('error' in result):
            self.assertNotEqual(result['error'], dispatch.ERROR_INVALID_TEMPERATURE)
        else:
            self.assert_(True)

    def test200_034_Success_TempNotGiven(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0'})
        if ('error' in result):
            self.assertNotEqual(result['error'], dispatch.ERROR_INVALID_TEMPERATURE)
        if('temperature' in result):
            self.assertEqual(result['temperature'], '72')
        else:
            self.assert_(False)

#Pressure param
    def test200_021_Success_PressureLowbound(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'pressure': '100'})
        if ('error' in result):
            self.assert_(result['error'] != dispatch.ERROR_INVALID_PRESSURE)
        else:
            self.assert_(True)

    def test200_021_Success_PressureNom(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'pressure': '600'})
        if ('error' in result):
            self.assert_(result['error'] != dispatch.ERROR_INVALID_PRESSURE)
        else:
            self.assert_(True)

    def test200_021_Success_PressureHighbound(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'pressure': '1100'})
        if ('error' in result):
            self.assert_(result['error'] != dispatch.ERROR_INVALID_PRESSURE)
        else:
            self.assert_(True)

    def test200_021_Success_PressureNotGiven(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0'})
        if ('pressure' in result):
            self.assert_(result['pressure'] == '1010')
        else:
            self.assert_(False)

#horizon param
    def test200_041_Success_HorizonArtificialLowercase(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'horizon': 'artificial'})
        if('error' in result):
            self.assertNotEqual(result['error'], dispatch.ERROR_INVALID_HORIZON)
        else:
            self.assert_(True)

    def test200_042_Succcess_HorizonNaturalLowercase(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'horizon': 'natural'})
        if ('error' in result):
             self.assertNotEqual(result['error'], dispatch.ERROR_INVALID_HORIZON)
        else:
             self.assert_(True)

    def test200_043_Success_HorizonArtificialCaseInsensitive(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'horizon': 'ArtiFICIal'})
        if ('error' in result):
            self.assertNotEqual(result['error'], dispatch.ERROR_INVALID_HORIZON)
        else:
            self.assert_(True)

    def test200_044_Success_HorizonNaturalCaseInsensitive(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'horizon': 'NatuRAL'})
        if ('error' in result):
            self.assertNotEqual(result['error'], dispatch.ERROR_INVALID_HORIZON)
        else:
            self.assert_(True)

    def test200_045_Success_HorizonNotGiven(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0'})
        self.assert_('horizon' in result)
        self.assertEqual(result['horizon'], 'natural')

#Calculation
    def test200_051_Success_ObsLowboundCalc(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'height': '300', 'temperature': '60', 'pressure': '600', 'horizon': 'artificial'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '-0d2.7')

    def test200_052_Success_ObsHighboundCalc(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '89d30.0', 'height': '300', 'temperature': '60', 'pressure': '600', 'horizon': 'artificial'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '89d27.3')

    def test200_053_Success_HeightLowboundCalc(self):
        result = adjust.adjust(
            {'op': 'adjust', 'observation': '45d30.0', 'height': '0', 'temperature': '60', 'pressure': '600',
             'horizon': 'natural'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '45d27.3')

    def test200_054_Success_PressureLowboundCalc(self):
        result = adjust.adjust(
            {'op': 'adjust', 'observation': '45d30.0', 'height': '300', 'temperature': '60', 'pressure': '100',
             'horizon': 'artificial'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '45d29.5')

    def test200_055_Success_PressureHighboundCalc(self):
        result = adjust.adjust(
            {'op': 'adjust', 'observation': '45d30.0', 'height': '300', 'temperature': '60', 'pressure': '1100',
             'horizon': 'artificial'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '45d25.0')

    def test200_056_Success_NaturalHorizonCalc(self):
        result = adjust.adjust(
            {'op': 'adjust', 'observation': '45d30.0', 'height': '300', 'temperature': '60', 'pressure': '600',
             'horizon': 'natural'})
        self.assert_('altitude' in result)
        self.assertEqual(result['altitude'], '45d10.5')


#Sad Path
#Observation Param
    def test200_101_Error_ObsLowboundViolation(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '-1d-1.1'})
        self.assert_(result['error'] == dispatch.ERROR_INVALID_OBSERVATION)

    def test200_102_Error_ObsHighboundViolation(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '90d60.0'})
        self.assert_(result['error'] == dispatch.ERROR_INVALID_OBSERVATION)

    def test200_103_Error_ObsNotIncluded(self):
        result = adjust.adjust({'op': 'adjust'})
        self.assert_(result['error'] == dispatch.ERROR_MANDATORY_INFO_MISSING)

#Height param
    def test200_111_Error_HeightLowboundViolation(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'height': '-1'})
        self.assert_(result['error'] == dispatch.ERROR_INVALID_HEIGHT)

#Temperature param
    def test200_131_Error_TemperatureLowboundViolation(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'temperature': '-21'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_TEMPERATURE)

    def test200_132_Error_TemperatureHighboundViolation(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'temperature': '121'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_TEMPERATURE)

#Pressure param
    def test200_121_Error_PressureLowboundViolation(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'pressure': '99'})
        self.assert_(result['error'] == dispatch.ERROR_INVALID_PRESSURE)

    def test200_122_Error_PressureHighboundViolation(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'pressure': '1101'})
        self.assert_(result['error'] == dispatch.ERROR_INVALID_PRESSURE)

#horizon param
    def test200_141_Error_HorizonInvalidInput(self):
        result = adjust.adjust({'op': 'adjust', 'observation': '0d0.0', 'horizon': 'unknown'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_HORIZON)

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
    def test300_100_Success_Calculation(self):
        result = predict.predict({'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42'})
        self.assert_('error' not in result)
        self.assertAlmostEqual(dispatch.degreeToDecimal(result['long']), dispatch.degreeToDecimal('75d53.6'), places=None, delta=1)
        self.assertEqual(result['lat'], '7d24.3')

    def test300_101_Success_CalculationMissingDateAndTime(self):
        result = predict.predict({'op': 'predict', 'body': 'Betelgeuse'})
        self.assert_('error' not in result)
        self.assertAlmostEqual(dispatch.degreeToDecimal(result['long']), dispatch.degreeToDecimal('11d41.6'), places=None, delta=1)
        self.assertEqual(result['lat'], '7d24.3')

#Sad Path
    def test300_110_Error_StarNotInCatalogue(self):
        result = predict.predict({'op': 'predict', 'body': 'asdf', 'date': '2016-01-17', 'time': '03:15:42'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], dispatch.ERROR_STAR_NOT_IN_CATALOGUE)

    def test300_111_Error_InvalidDate(self):
        result = predict.predict({'op': 'predict', 'body': 'Betelgeuse', 'date': '13/13/9999', 'time': '03:15:42'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_DATE)

    def test300_112_Error_InvalidTime(self):
        result = predict.predict({'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '25:61:61'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_TIME)

    def test300_113_Error_NoBody(self):
        result = predict.predict({'op': 'predict', 'date': '2016-01-17', 'time': '25:61:61'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], dispatch.ERROR_MANDATORY_INFO_MISSING)

    def test300_114_Error_ContainsLat(self):
        result = predict.predict({'op': 'predict', 'body': 'asdf', 'date': '2016-01-17', 'time': '03:15:42', 'lat': '7d24.3'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], dispatch.ERROR_LAT_LON_INCLUDED)

    def test300_115_Error_ContainsLong(self):
        result = predict.predict({'op': 'predict', 'body': 'asdf', 'date': '2016-01-17', 'time': '03:15:42', 'long': '7d24.3'})
        self.assert_('error' in result)
        self.assertEqual(result['error'], dispatch.ERROR_LAT_LON_INCLUDED)

#400 correct
# Desired level of confidence: boundary value analysis
#       inputs: valies -? dictionary of key values, passed from dispatch
#       outputs: dictionary of params and result of prediction
# Happy Path Analysis:
#       lat:            low value           > -90d0.0
#                       nom value           = 16d32.3
#                       high value          < 90d0.0
#       long:           low value           > 0d0.0
#                       nom value           = 95d41.6
#                       high value          < 360d0.0
#       altitude:       low value           > 0d0.0
#                       nom value           = 13d42.3
#                       high value          < 90d0.0
#       assumedLat:     low value           > -90d0.0
#                       nom value           = -53d38.4
#                       high value          < 90d0.0
#       assumedLong:    low value           > 0d0.0
#                       nom value           = 74d35.3
#                       high value          < 360d0.0
#       output:         returns the values for the corrected distance and corrected azimuth
#
# Sad Path Analysis:
#       lat:            low violation       -91d0.0
#                       high violation      91d0.0
#                       missing value
#                       bad format          64f
#       long:           low violation       -1d0.0
#                       high violation      361d0.0
#                       missing value
#                       bad format          56re
#       altitude        low violation       -1d0.0
#                       high violation      91d0.0
#                       missing value
#                       bad format          56re
#       assumedLat:     low violation       -91d0.0
#                       high violation      91d0.0
#                       missing value
#                       bad format          64f
#       assumedLong:    low violation       -1d0.0
#                       high violation      361d0.0
#                       missing value
#                       bad format          64f

#Happy path
    def test400_001_Success_Lowbound(self):
        result = correct.correct({'op':'correct',
                                  'lat':'-89d0.0',
                                  'long':'1d0.0',
                                  'altitude':'1d0.0',
                                  'assumedLat':'-89d0.0',
                                  'assumedLong':'1d0.0'})
        self.assert_('error' not in result)

    def test400_002_Success_Highbound(self):
        result = correct.correct({'op': 'correct',
                                  'lat': '89d0.0',
                                  'long': '359d0.0',
                                  'altitude': '89d0.0',
                                  'assumedLat': '89d0.0',
                                  'assumedLong': '359d0.0'})
        self.assert_('error' not in result)

    def test400_003_Success_calculation(self):
        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assert_('error' not in result, 'Error was returned')
        self.assert_('correctedDistance' in result, 'No correctedDistance')
        self.assert_('correctedAzimuth' in result, 'No correctedAzimuth')
        self.assertAlmostEqual(result['correctedDistance'], 3950, 0,  'Corrected Distance incorrect')
        self.assertEqual(result['correctedAzimuth'], '164d42.9', 'Corrected Azimuth incorrect')

#Sad path
    def test400_101_error_missingValues(self):
        result = correct.correct({'op': 'correct',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_MANDATORY_INFO_MISSING, 'not error for missing lat')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_MANDATORY_INFO_MISSING, 'not error for missing long')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_MANDATORY_INFO_MISSING, 'not error for missing altitude')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_MANDATORY_INFO_MISSING, 'not error for missing assumedLat')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4'})
        self.assertEqual(result['error'], dispatch.ERROR_MANDATORY_INFO_MISSING, 'not error for missing assumedLong')

    def test400_102_error_badFormat(self):
        result = correct.correct({'op': 'correct',
                                  'lat': '12.3',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_LAT, 'Lat bad format check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '941.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_LONG, 'Long bad format check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '1.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_ALTITUDE, 'Altitude bad format check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-5',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_ASSUMEDLAT, 'assumedLat bad format check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_ASSUMEDLONG, 'assumedLong bad format check failed')

    def test400_103_error_lowboundViolation(self):
        result = correct.correct({'op': 'correct',
                                  'lat': '-91d0.0',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_LAT, 'Lat low bound check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '-1d0.0',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_LONG, 'Long low bound check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '-1d0.0',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_ALTITUDE, 'Altitude low bound check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-91d0.0',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_ASSUMEDLAT, 'assumedLat low bound check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '-1d0.0'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_ASSUMEDLONG, 'assumedLong low bound check failed')

    def test400_103_error_highboundViolation(self):
        result = correct.correct({'op': 'correct',
                                  'lat': '91d0.0',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_LAT, 'Lat high bound check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '361d0.0',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_LONG, 'Long high bound check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '91d0.0',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_ALTITUDE, 'Altitude high bound check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '91d0.0',
                                  'assumedLong': '74d35.3'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_ASSUMEDLAT, 'assumedLat high bound check failed')

        result = correct.correct({'op': 'correct',
                                  'lat': '16d32.3',
                                  'long': '95d41.6',
                                  'altitude': '13d42.3',
                                  'assumedLat': '-53d38.4',
                                  'assumedLong': '361d0.0'})
        self.assertEqual(result['error'], dispatch.ERROR_INVALID_ASSUMEDLONG, 'assumedLong high bound check failed')

