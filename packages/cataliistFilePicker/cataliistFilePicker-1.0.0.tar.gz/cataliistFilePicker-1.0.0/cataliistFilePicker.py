#This script open the file in a list

def filePicker(file):
    try:
        with open(file) as fh:
            data = fh.readline()
            return(data.strip().split(','))
    except IOError as err:
        print("File Error" +str(err))
        return(None)        
