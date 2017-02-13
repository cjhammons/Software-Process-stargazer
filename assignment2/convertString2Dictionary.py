import urllib

def convertString2Dictionary(inputString = ""):
    errorDict = {'error':'true'}
    #decode
    unquoted = urllib.unquote(inputString)

    #to produce a valid result, unquoted should be >= 3 len
    if unquoted.__len__() < 3:
        return errorDict

    #split the key and value
    split = unquoted.split("=")
    key = split[0].lstrip().strip()
    value = split[1].lstrip().strip()

    #check for valid key and value
    if len(split) > 2 or len(split) < 2 or key == "" or value == "":
        return errorDict

    result = "{'"

    #Key
    if key[0].isdigit() or key.__contains__(" "):
        return errorDict
    result += key
    result += "':'"

    #value
    result += value
    result += "'}"

    return result


