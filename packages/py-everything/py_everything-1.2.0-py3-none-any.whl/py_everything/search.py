import os

def searchFiles(keyword, path):
    files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if keyword in file:
                files.append(root + '\\' + str(file))
    return files

def searchDirs(keyword, path):
    folders = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if keyword in dir:
                folders.append(root + '\\' + str(dir))
    return folders

def searchExts(ext, path):
    files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(ext):
                files.append(root + '\\' + str(file))
    return files

def searchList(listOfTerms, query, filter='in'):
    matches = []
    for item in listOfTerms:
        if filter == 'in':
            if query in item:
                matches.append(item)
        elif filter == 'start':
            if item.startswith(query):
                matches.append(item)
        elif filter == 'end':
            if item.endswith(query):
                matches.append(item)
        elif filter == 'exact':
            if item == query:
                matches.append(item)

    return matches
