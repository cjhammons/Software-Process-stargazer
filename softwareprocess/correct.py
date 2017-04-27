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

    lat = dispatch.degreeToDecimal(values['lat'])
    long = dispatch.degreeToDecimal(values['long'])
    altitude = dispatch.degreeToDecimal(values['altitude'])
    assumedLat = dispatch.degreeToDecimal(values['assumedLat'])
    assumedLong = dispatch.degreeToDecimal(values['assumedLong'])

    #Local hour angle
    LHA = long + assumedLong

    intermediateDistance = ((math.sin(lat) * math.sin(assumedLat)) + (math.cos(lat) * math.cos(assumedLat) * math.cos(LHA)))

    #calculate altitude adjustment
    correctedAltitude = math.asin(intermediateDistance)

    #calcualte distance needed to move to make positions match
    correctedDistance = altitude - correctedAltitude

    #calculate azimuth
    correctedAzimuth = math.acos((math.sin(lat) -  math.sin(assumedLat) * intermediateDistance)) \
                       / (math.cos(assumedLat) * math.cos(math.asin(intermediateDistance)))

    #convert to correct format
    azimuthFormat = dispatch.decimalToDegree(correctedAzimuth)
    distanceFormat = dispatch.decimalToDegree(correctedDistance)

    values['correctedDistance'] = distanceFormat
    values['correctedAzimuth'] = azimuthFormat

    return values