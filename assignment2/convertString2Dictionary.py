import urllib

def convertString2Dictionary(inputString = ""):
    errorDict = {'error':'true'}

    keys = [] #hold copies of existing keys

    #decode
    unquoted = urllib.unquote(inputString)

    #to produce a valid result, unquoted should be >= 3 len
    if unquoted.__len__() < 3:
        return errorDict

    #split the new entries
    split = unquoted.split(",")

    result = "{"

    #iterate through new entries
    i = 1
    for s in split:
        #split the key and value
        entry = s.split("=")

        if len(entry) < 2:
            return errorDict

        key = entry[0].lstrip().strip()
        value = entry[1].lstrip().strip()

        #check alphanumeric
        if not key.isalnum() or not value.isalnum():
            return errorDict

        #check if key is unique
        if keys.__contains__(key):
            return errorDict
        else:
            keys.append(key)

        #check for valid key and value
        if key == "" or value == "":
            return errorDict

        #Key
        if key[0].isdigit() or key.__contains__(" "):
            return errorDict
        result += "'" + key + "':'"

        #value
        result += value + "'"
        if i < split.__len__():
            result += ","
        i += 1

    result += "}"

    return result


