import math

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
        return values    #This calculation is stubbed out
    elif(values['op'] == 'correct'):
        return values    #This calculation is stubbed out
    elif(values['op'] == 'locate'):
        return values    #This calculation is stubbed out
    else:
        values['error'] = ERROR_OP_NOT_LEGAL
        return values

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
    dip = 0
    if (horizon == 'natural'):
        dip = (-0.97 * math.sqrt(height)) / 60

    refraction = (-0.00452 * pressure) / 60

    altitudeDecimalDegree = obsDecimalDegree + dip + refraction

    altDegree = int(altitudeDecimalDegree)
    altMinute = round((altitudeDecimalDegree - altDegree) * 60, 1)
    altFinal = str(altDegree) + 'd' + str(altMinute)

    values['altitude'] = altFinal

    return values
