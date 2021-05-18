# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 06:31:40 2020

@author: thiag
"""

import shutil
import time

formats = ['psp', 'g3', 'ras', 'iff', 'lbm', 'biorad', 'mosaic', 'xbm',
           'xpm', 'gem-img', 'sgi', 'rle', 'wbmp', 'ttf', 'fits', 'pic',
           'hdr', 'mag', 'wad', 'wal', 'dng', 'eef', 'nef', 'orf', 'raf',
           'mrw', 'dcr', 'srf', 'arw', 'pef', 'x3f', 'cam', 'sfw', 'yuv',
           'pvr', 'sif']

def getdatestr(folder, filename):
    '''
    '''

    import os
    import datetime

    x = os.path.getmtime(os.path.join(folder, filename))

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

    filepath = os.path.join(folder, filename)

    try:
        x = Image.open(filepath)._getexif()[36867]
        if x is not None:
            return x[0:4]+x[5:7]+x[8:10]
        else:
            dt = datetime.fromtimestamp(os.path.getmtime(filepath))
            x = str(dt.date()).replace('-', '')
            return x
    except:
        try:
            dt = datetime.fromtimestamp(os.path.getmtime(filepath))
            x = str(dt.date()).replace('-', '')
            return x
        except:
            return '.'

def org_folder(folder1, folder2, par=1):
    '''
        if par = 0, no file name change is done and risk of overwrite exists
        if par = 1, file name receives an index of when the program was run,
          to avoid overwrite risk
    '''

    import os
    import sys
    import datetime

    if par not in [0, 1]:
        print('Input error. Setting default parameter value.')        

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
        if par:
            [name, ext] = os.path.splitext(file)
            now = str(datetime.datetime.now())[:19]
            now = now.replace(":", "_")

            shutil.copy(os.path.join(folder1, file), #.move or .copy
                        os.path.join(folder2,
                                     get_date_taken(folder1, file),
                                     name + now + ext))
        else:
            shutil.copy(os.path.join(folder1, file), #.move or .copy
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

# option 1: read config.txt file in os.getcwd()
f = open('config.txt', 'r')
try:
    [foldera, folderb, param] = [x.rstrip() for x in f.readlines()]
    param = int(param)
except:
    try:
        [foldera, folderb] = [x.rstrip() for x in f.readlines()]
        param = 1
    except:
        print('Input error. Verify two folders names and parameter are '+\
              'present in config.txt file.')


# option 2: get the folders inside the program
# folder1 = r'D:\Clikes_Elaine\113D3400'
# folder2 = r'D:\Clikes_Elaine'
# par = 1

org_folder(foldera, folderb, param)


'''
ORGANIZE BY DATE OF CREATION - NOT USEFUL AT THIS TIME
datelist = []

datelist.append([getdatestr(folder, x)
                 for x in jpgfiles
                 if getdatestr(folder, x) not in datelist])

datelist = [getdatestr(folder, x) for x in jpgfiles]
uniquedates = list(set(datelist))

'''
