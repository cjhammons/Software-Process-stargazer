import math
import os
import datetime
import adjust as adjust
import predict as predict

#Error messages
ERROR_INVALID_OBSERVATION = 'observation is invalid'
ERROR_INVALID_HEIGHT = 'height is invalid'
ERROR_INVALID_PRESSURE = 'pressure is invalid'
ERROR_INVALID_HORIZON = 'horizon is invalid'
ERROR_INVALID_TEMPERATURE = 'temperature is invalid'
ERROR_MANDATORY_INFO_MISSING = 'mandatory information missing'
ERROR_OP_NOT_LEGAL = 'op is not a legal operation'
ERROR_OP_NOT_SPECIFIED = 'no op is specified'
ERROR_PARAM_NOT_DICTIONARY = 'parameter is not a dictionary'
ERROR_DICTIONARY_MISSING = 'dictionary is missing'
ERROR_ALTITUDE_ALREADY_INCLUDED = 'altitude already included'
ERROR_INVALID_TIME = 'invalid time'
ERROR_INVALID_DATE = 'invalid date'
ERROR_STAR_NOT_IN_CATALOGUE = 'star not in catalog'
ERROR_LAT_LON_INCLUDED = 'lat or long cannot be included'

def dispatch(values=None):

    #Validate parm
    if(values == None):
        return {'error': ERROR_DICTIONARY_MISSING}
    if(not(isinstance(values,dict))):
        return {'error': ERROR_PARAM_NOT_DICTIONARY}
    if (not('op' in values)):
        values['error'] = ERROR_OP_NOT_SPECIFIED
        return values

    #Perform designated function
    if(values['op'] == 'adjust'):
        return adjust.adjust(values)    #split off into its own function for readability
    elif(values['op'] == 'predict'):
        return predict.predict(values)
    elif(values['op'] == 'correct'):
        return values    #This calculation is stubbed out
    elif(values['op'] == 'locate'):
        return values    #This calculation is stubbed out
    else:
        values['error'] = ERROR_OP_NOT_LEGAL
        return values

#-------------------------------------------------------------------------
# Main Functions
#-------------------------------------------------------------------------




#-------------------------------------------------------------------------
# Helper Functions
#-------------------------------------------------------------------------

#scans stars.txt for the provided body and returns it's data if found
def getBodyData(body=''):
    filename = os.path.join(os.path.dirname(__file__), 'stars.txt')
    file = open(filename)
    lines = file.readlines()
    for line in lines:
        if(body.lower() in line.lower()):
            l = line.rstrip('\r\n')
            return l.split('\t')
    return None

def degreeToDecimal(degree=''):
    negative = False
    if (degree.startswith('-')):
        negative = True
    degSplit = degree.split('d')
    deg = int(degSplit[0])
    minute = float(degSplit[1])
    combined = deg + (minute / 60)
    if (negative):
        return -combined
    else:
        return combined

def decimalToDegree(decDegree=0.0):
    neg = False
    if (decDegree < 0):
        neg = True
    deg = abs(int(decDegree))
    minute = abs(round((decDegree - deg) * 60, 1))
    final = ''
    if (neg):
        final += '-'
    final += str(deg) + 'd' + str(minute)
    return final

def calculateLongitude(shaStar, time, date):
    #Note: All degree values are converted to decimal from 'xdy.y' format until end of calculation
    baseLineGhaAres = degreeToDecimal('100d42.6')
    baseLineDateTime = datetime.datetime(2001, 01, 01, 0, 0, 0)
    yearDifference = date.year - 2001
    cumulativeProgression = float(yearDifference * degreeToDecimal('-0d14.31667'))
    leapYears = int(yearDifference / 4)
    leapYearProgression = float(degreeToDecimal('0d59.0') * leapYears)
    primeMeridianRotation = baseLineGhaAres + cumulativeProgression + leapYearProgression

    masterDateTime = datetime.datetime(date.year, date.month, date.day, time.hour, time.minute, time.second)
    elapsedSeconds = (masterDateTime - baseLineDateTime).total_seconds()
    rotationAmount = ((elapsedSeconds  / 86164.1) * 360) % 360
    ghaAres = primeMeridianRotation + rotationAmount

    ghaStar = ghaAres + degreeToDecimal(shaStar)
    ghaStar = ghaStar % 360
    ghaStarDegree = decimalToDegree(ghaStar)
    return ghaStarDegree