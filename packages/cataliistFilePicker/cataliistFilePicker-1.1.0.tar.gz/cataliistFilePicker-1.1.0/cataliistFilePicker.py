#This script open the file in a list

import cataliistSanitizer

def filePicker(file):
    try:
        with open(file) as fh:
            data = []
            data = fh.readline().strip().split(',')
            dataDict = {}
            dataDict['name'] = data.pop(0)
            dataDict['dob'] = data.pop(0)
            dataDict['times'] = sorted(set([cataliistSanitizer.sanitize(ei) for ei in data]))[0:3]
            return(dataDict)
    except IOError as err:
        print("File Error" +str(err))
        return(None)  

