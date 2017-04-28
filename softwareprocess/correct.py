import dispatch as dispatch
import math

def correct(values=None):
    if('lat' not in values
       or 'long' not in values
       or 'altitude' not in values
       or 'assumedLat' not in values
       or 'assumedLong' not in values):

        values['error'] = dispatch.ERROR_MANDATORY_INFO_MISSING
        return values

    #check lat
    if('d' not in values['lat']):
        values['error'] = dispatch.ERROR_INVALID_LAT
        return values

    lat = math.radians(dispatch.degreeToDecimal(values['lat']))
    if (lat <= math.radians(-90) or lat >= math.radians(90)):
        values['error'] = dispatch.ERROR_INVALID_LAT

    #check long
    if ('d' not in values['long']):
        values['error'] = dispatch.ERROR_INVALID_LONG
        return values
    long = math.radians(dispatch.degreeToDecimal(values['long']))
    if (long <= 0 or long >= math.radians(360)):
        values['error'] = dispatch.ERROR_INVALID_LONG
        return values

    #check altitude
    if ('d' not in values['altitude']):
        values['error'] = dispatch.ERROR_INVALID_ALTITUDE
        return values
    altitude = math.radians(dispatch.degreeToDecimal(values['altitude']))
    if (altitude <= math.radians(0) or altitude >= math.radians(90)):
        values['error'] = dispatch.ERROR_INVALID_ALTITUDE
        return values

    #check assumedLat
    if ('d' not in values['assumedLat']):
        values['error'] = dispatch.ERROR_INVALID_ASSUMEDLAT
        return values
    assumedLat = math.radians(dispatch.degreeToDecimal(values['assumedLat']))
    if (assumedLat <= math.radians(-90) or assumedLat >= math.radians(90)):
        values['error'] = dispatch.ERROR_INVALID_ASSUMEDLAT
        return values

    #check assumedLong
    if ('d' not in values['assumedLong']):
        values['error'] = dispatch.ERROR_INVALID_ASSUMEDLONG
        return values
    assumedLong = math.radians(dispatch.degreeToDecimal(values['assumedLong']))
    if (assumedLong <= math.radians(0) or assumedLong >= math.radians(360)):
        values['error'] = dispatch.ERROR_INVALID_ASSUMEDLONG
        return values

    #Local hour angle
    LHA = long + assumedLong

    intermediateDistance =  ((math.sin(lat) * math.sin(assumedLat))  + (math.cos(lat) * math.cos(assumedLat) * math.cos(LHA)))

    #calculate altitude adjustment
    correctedAltitude = math.degrees(math.asin(intermediateDistance))

    #calcualte distance needed to move to make positions match
    correctedDistance = altitude - correctedAltitude

    #calculate azimuth
    correctedAzimuth =  math.acos((math.sin(lat) - (math.sin(assumedLat) *  intermediateDistance))
                                  / (math.cos(assumedLat) * math.cos(math.asin(intermediateDistance))))


    #convert to correct format
    azimuthFormat = dispatch.decimalToDegree(math.degrees(correctedAzimuth))

    values['correctedDistance'] = correctedDistance
    values['correctedAzimuth'] = azimuthFormat

    return values