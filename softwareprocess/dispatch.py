
ERROR_INVALID_OBSERVATION = 'observation is invalid'
ERROR_INVALID_HEIGHT = 'height is invalid'
ERROR_INVALID_PRESSURE = 'pressure is invalid'
ERROR_INVALID_HORIZON = 'horizon is invalid'
ERROR_MANDATORY_INFO_MISSING = 'mandatory information missing'

def dispatch(values=None):

    #Validate parm
    if(values == None):
        return {'error': 'dictionary is missing'}
    if(not(isinstance(values,dict))):
        return {'error': 'parameter is not a dictionary'}
    if (not('op' in values)):
        values['error'] = 'no op is specified'
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
        values['error'] = 'op is not a legal operation'
        return values

def adjust(values=None):
    return values
