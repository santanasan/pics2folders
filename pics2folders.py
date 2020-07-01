# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 06:31:40 2020

@author: thiag
"""

import os
import shutil
import time
from PIL import Image

def getdatestr(folder, filename):
    
    import os
    import datetime
    

    x = os.path.getmtime(os.path.join(folder,filename))
    
    try:
        y = datetime.datetime.strptime(time.ctime(x), "%a %b %d %H:%M:%S %Y")
        z = str(' %04d' % y.year) + str('%02d' % y.month) + str('%02d' % y.day)
    except:
        z = '00000000'
    
    return z

def get_date_taken(folder, filename):
    import os
    from datetime import datetime
    from PIL import Image
    
    filepath = os.path.join(folder,filename)
    
    try:
        x = Image.open(filepath)._getexif()[36867]
        if x != None:
            return x[0:4]+x[5:7]+x[8:10]
        else:
            dt = datetime.fromtimestamp(os.path.getmtime(filepath))
            x = str(dt.date()).replace('-','')
            return x
    except:
        try:
            dt = datetime.fromtimestamp(os.path.getmtime(filepath))
            x = str(dt.date()).replace('-','')
            return x
        except:
            return '.'

def org_folder(folder1, folder2):
    
    import os
    import sys
    
    subfolderlist = [os.path.join(folder1, i) for i in next(os.walk(folder1))[1]]
    
    allfiles = [x for x in os.listdir(folder1) if 
                os.path.isfile(os.path.join(folder1, x))]
    jpgfiles = [x for x in allfiles if [x.endswith('jpg') |
                                    x.endswith('jpeg')]]

 
    datelist = [get_date_taken(folder1, x) for x in jpgfiles]
    uniquedatelist = list(set(datelist))

#TO-DO: two files with the same name, keep them both
    
    #create folders
    
    [os.makedirs(os.path.join(folder2, x), exist_ok=True) for x in uniquedatelist]

    #initialize counters
    
    ifiles = 0
    nfiles = len(jpgfiles)


    #move the files
    for file in jpgfiles:
        shutil.copy(os.path.join(folder1,file), #.move or .copy
                    os.path.join(folder2,
                    get_date_taken(folder1, file),
                    file))
    #print counter
        ifiles += 1
        rate = ifiles/nfiles*100
        sys.stdout.write("\r%d%%" % rate)
        sys.stdout.flush()
    
    for i in subfolderlist:
        org_folder(i, folder2)
    
    return

#folder1 = r'E:\DCIM\110D3400'
folder1 = r'C:\Users\thiag\Pictures\101D3400'
#folder2 = r'C:\Users\thiag\Desktop\Album\Atacama. Bolivia'
folder2 = r'C:\Users\thiag\Pictures\101D3400'

# import time
# import sys

# for i in range(100):
#     time.sleep(0.1)
#     sys.stdout.write("\r%d%%" % i)
#     sys.stdout.flush()


org_folder(folder1, folder2)


'''
ORGANIZE BY DATE OF CREATION - NOT USEFUL AT THIS TIME
datelist = []

datelist.append([getdatestr(folder, x) 
                 for x in jpgfiles
                 if getdatestr(folder, x) not in datelist])

datelist = [getdatestr(folder, x) for x in jpgfiles]
uniquedates = list(set(datelist))

'''
