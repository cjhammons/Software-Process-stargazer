import dispatch as dispatch

def correct(values=None):
    if('lat' not in values
       or 'long' not in values
       or 'altitude' not in values
       or 'assumedLat' not in values
       or 'assumedLong' not in values):
        values['error'] = dispatch.ERROR_MANDATORY_INFO_MISSING
    return values