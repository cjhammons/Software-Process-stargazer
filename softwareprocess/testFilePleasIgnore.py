import convertString2Dictionary
def main():
    print "these should work:"
    print convertString2Dictionary.convertString2Dictionary('abc%3D123')
    print convertString2Dictionary.convertString2Dictionary( 'function%3D%20calculatePosition%2C%20sighting%3DBetelgeuse')

    print "\nthese should not:"
    print convertString2Dictionary.convertString2Dictionary( 'function%20%3D%20get_stars')
    print convertString2Dictionary.convertString2Dictionary('key%3Dvalue%2C%20key%3Dvalue')
    print convertString2Dictionary.convertString2Dictionary('key%3D')
    print convertString2Dictionary.convertString2Dictionary('value')
    print convertString2Dictionary.convertString2Dictionary('1key%3Dvalue')
    print convertString2Dictionary.convertString2Dictionary('k%20e%20y%20%3D%20value')
    print convertString2Dictionary.convertString2Dictionary('"')
    print convertString2Dictionary.convertString2Dictionary( 'key1%3Dvalue%3B%20key2%3Dvalue')

if __name__ == '__main__':
    main()
