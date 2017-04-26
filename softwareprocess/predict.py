import dispatch as dispatch
import datetime

def predict(values=None):
    #check for lat or long
    if ('lat' in values or 'long' in values):
        values['error'] = dispatch.ERROR_LAT_LON_INCLUDED
        return values

    #check body
    if ('body' not in values):
        values['error'] = dispatch.ERROR_MANDATORY_INFO_MISSING
        return values
    bodyData = dispatch.getBodyData(values['body'])
    if (bodyData == None):
        values['error'] = dispatch.ERROR_STAR_NOT_IN_CATALOGUE
        return values
    #date
    dateString = '2001-01-01'
    if ('date' in values):
        dateString = values['date']

    dateSplit = dateString.split('-')
    if (dateSplit.__len__() != 3):
        values['error'] = dispatch.ERROR_INVALID_DATE
        return values
    try:
        date = datetime.date(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]))
    except ValueError:
        values['error'] = dispatch.ERROR_INVALID_DATE
        return values

    #time
    timeString = '00:00:00'
    if ('time' in values):
        timeString = values['time']

    timeSplit = timeString.split(':')
    if (timeSplit.__len__() != 3):
        values['error'] = dispatch.ERROR_INVALID_TIME
        return values

    try:
        time = datetime.time(int(timeSplit[0]), int(timeSplit[1]), int(timeSplit[2]))
    except ValueError:
        values['error'] = dispatch.ERROR_INVALID_TIME
        return values

    shaStar = bodyData[1]
    lattitude = bodyData[2]
    longitude = dispatch.calculateLongitude(shaStar, time, date)

    values['lat'] = lattitude
    values['long'] = longitude
    return values