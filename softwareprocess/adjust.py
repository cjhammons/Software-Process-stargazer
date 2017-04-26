import math
import dispatch as dispatch

def adjust(values=None):
    #Observation check
    if (not 'observation' in values):
        values['error'] = dispatch.ERROR_MANDATORY_INFO_MISSING
        return values

    observationRaw = values['observation']
    if ('d' not in observationRaw):
        values['error'] = dispatch.ERROR_INVALID_OBSERVATION
        return values
    obsSplit = observationRaw.split('d')
    obsDegree = int(obsSplit[0])
    obsMinute = float(obsSplit[1])
    if (obsDegree < 0 or obsDegree >= 90):
        values['error'] = dispatch.ERROR_INVALID_OBSERVATION
        return values
    if( obsMinute < 0.0 or obsMinute >= 60):
        values['error'] = dispatch.ERROR_INVALID_OBSERVATION
        return values

    #height check
    height = 0
    if (not 'height' in values):
        values['height'] = str(0)
    else:
        height = int(values['height'])

    if (height < 0):
        values['error'] = dispatch.ERROR_INVALID_HEIGHT
        return values

    #temperature check
    temperature = 72
    if (not 'temperature' in values):
        values['temperature'] = str(temperature)
    else:
        temperature = int(values['temperature'])
    if(temperature < -20 or temperature > 120):
        values['error'] = dispatch.ERROR_INVALID_TEMPERATURE
        return values

    #pressure check
    pressure = 1010
    if (not 'pressure' in values):
        values['pressure'] = str(1010)
    else:
        pressure = int(values['pressure'])
    if (pressure > 1100 or pressure < 100):
        values['error'] = dispatch.ERROR_INVALID_PRESSURE
        return values

    #horizon check
    horizon = 'natural'
    if (not 'horizon' in values):
        values['horizon'] = 'natural'
    else:
        horizon = str(values['horizon']).lower()

    if (horizon != 'natural' and horizon != 'artificial'):
        values['error'] = dispatch.ERROR_INVALID_HORIZON
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