import math
import os
import datetime

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
        return adjust(values)    #split off into its own function for readability
    elif(values['op'] == 'predict'):
        return predict(values)
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

def adjust(values=None):
    #Observation check
    if (not 'observation' in values):
        values['error'] = ERROR_MANDATORY_INFO_MISSING
        return values

    observationRaw = values['observation']
    if ('d' not in observationRaw):
        values['error'] = ERROR_INVALID_OBSERVATION
        return values
    obsSplit = observationRaw.split('d')
    obsDegree = int(obsSplit[0])
    obsMinute = float(obsSplit[1])
    if (obsDegree < 0 or obsDegree >= 90):
        values['error'] = ERROR_INVALID_OBSERVATION
        return values
    if( obsMinute < 0.0 or obsMinute >= 60):
        values['error'] = ERROR_INVALID_OBSERVATION
        return values

    #height check
    height = 0
    if (not 'height' in values):
        values['height'] = str(0)
    else:
        height = int(values['height'])

    if (height < 0):
        values['error'] = ERROR_INVALID_HEIGHT
        return values

    #temperature check
    temperature = 72
    if (not 'temperature' in values):
        values['temperature'] = str(temperature)
    else:
        temperature = int(values['temperature'])
    if(temperature < -20 or temperature > 120):
        values['error'] = ERROR_INVALID_TEMPERATURE
        return values

    #pressure check
    pressure = 1010
    if (not 'pressure' in values):
        values['pressure'] = str(1010)
    else:
        pressure = int(values['pressure'])
    if (pressure > 1100 or pressure < 100):
        values['error'] = ERROR_INVALID_PRESSURE
        return values

    #horizon check
    horizon = 'natural'
    if (not 'horizon' in values):
        values['horizon'] = 'natural'
    else:
        horizon = str(values['horizon']).lower()

    if (horizon != 'natural' and horizon != 'artificial'):
        values['error'] = ERROR_INVALID_HORIZON
        return values

    #Calculation
    obsDecimalDegree = obsDegree + (obsMinute / 60)
    dip = 0.0
    if (horizon == 'natural'):
        dip = (-0.97 * math.sqrt(height)) / 60
    refraction = (-0.00452 * pressure) / 60
    altitudeDecimalDegree = obsDecimalDegree + dip + refraction
    negative = False
    if (altitudeDecimalDegree < 0):
        negative = True
    altDegree = abs(int(altitudeDecimalDegree))
    altMinute = abs(round((altitudeDecimalDegree - altDegree) * 60, 1))

    altFinal = ''
    if (negative):
        altFinal += '-'
    altFinal += str(altDegree) + 'd' + str(altMinute)

    values['altitude'] = altFinal
    return values

def predict(values=None):
    #check for lat or long
    if ('lat' in values or 'long' in values):
        values['error'] = ERROR_LAT_LON_INCLUDED
        return values

    #check body
    if ('body' not in values):
        values['error'] = ERROR_MANDATORY_INFO_MISSING
        return values
    bodyData = getBodyData(values['body'])
    if (bodyData == None):
        values['error'] = ERROR_STAR_NOT_IN_CATALOGUE
        return values
    #date
    dateString = '2001-01-01'
    if ('date' in values):
        dateString = values['date']

    dateSplit = dateString.split('-')
    if (dateSplit.__len__() != 3):
        values['error'] = ERROR_INVALID_DATE
        return values
    try:
        date = datetime.date(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]))
    except ValueError:
        values['error'] = ERROR_INVALID_DATE
        return values

    #time
    timeString = '00:00:00'
    if ('time' in values):
        timeString = values['time']

    timeSplit = timeString.split(':')
    if (timeSplit.__len__() != 3):
        values['error'] = ERROR_INVALID_TIME
        return values

    try:
        time = datetime.time(int(timeSplit[0]), int(timeSplit[1]), int(timeSplit[2]))
    except ValueError:
        values['error'] = ERROR_INVALID_TIME
        return values

    shaStar = bodyData[1]
    lattitude = bodyData[2]
    longitude = calculateLongitude(shaStar, time, date)

    values['lat'] = lattitude
    values['long'] = longitude
    return values

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
    degSplit = degree.split('d')
    deg = int(degSplit[0])
    minute = float(degSplit[1])
    return deg + (minute / 60)

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
    return file

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
    rotationAmount = (elapsedSeconds  / 86164.1) * 360
    ghaAres = baseLineGhaAres + rotationAmount

    ghaStar = ghaAres + degreeToDecimal(shaStar)
    ghaStar = ghaStar % 360
    ghaStarDegree = decimalToDegree(ghaStar)
    return ghaStarDegree
