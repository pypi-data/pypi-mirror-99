import os

def getFileList(path, type=()):
    '''
    :param path: files path
    :param type: filter types
    :return: file list
    '''
    Filelist = []
    for home, dirs, files in os.walk(path):
        for filename in files:
            if len([]) == 0:
                Filelist.append(os.path.join(home, filename))
            else:
                if filename.endswith(type):
                    if os.path.getsize(os.path.join(home, filename)) == 0:
                        continue
                    Filelist.append(os.path.join(home, filename))
    return Filelist