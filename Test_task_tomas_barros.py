# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 10:33:36 2024

@author: Tomás Barros

Veeam test task
"""

import sys
import time
import os
import shutil


def synchTimeLoop(sourceFolderPath, replicaFolderPath, synchInterval,
                  logFilePath):
    '''Preforms synchronization every synchInterval seconds
    
    Args:
        sourceFolderPath: the path of the source folder
        replicaFolderPath: the path of the replica folder
        synchInterval: how much time passes between synchronization
        logFilePath: path for the file where operations will be logged
    '''
    
    # Create the log file if it does not exist already
    if 'log.txt' not in os.listdir(logFilePath):
        createLogFile(sourceFolderPath, replicaFolderPath, logFilePath)
    # From now on logFilePath is the log file
    logFilePath = logFilePath+'log.txt'
    
    synchFolders(sourceFolderPath, replicaFolderPath, logFilePath)
    # it keeps synchromizing the two folders each synchInterval seconds until
    # the program is manually stopped
    while True:
        try:
            time.sleep(synchInterval)
            synchFolders(sourceFolderPath, replicaFolderPath, logFilePath)
        except KeyboardInterrupt:
            print("Synchronization terminated.")
            raise SystemExit

def synchFolders(sourceFolderPath, replicaFolderPath, logFilePath):
    
    def separateFilesAndDirs(folderPath):
        ''' Go thru all the entries in folderPath and separate it into a set
            of all the files and a set of all the directories

        Args:
            folderPath: path of the folder being worked on
        '''
        filesSet = set()
        dirsSet = set()
        with os.scandir(folderPath) as entries:
            for entry in entries:
                if entry.is_file():
                    filesSet.add(entry.name)
                else:
                    dirsSet.add(entry.name)
                    #synchFolders(sourceFolderPath+'\\'+entry.name, 'replica')
        return filesSet, dirsSet
    

    sourceFilesSet, sourceDirsSet = separateFilesAndDirs(sourceFolderPath)
    replicaFilesSet, replicaDirsSet = separateFilesAndDirs(replicaFolderPath)

    
    # files and folders that are in the replica folder but not in the source 
    # folder need to be deleted
    filesToDelete = replicaFilesSet - sourceFilesSet
    for file in filesToDelete:
        os.remove(replicaFolderPath+'\\'+file)
        writeLogFile(file,
                     sourceFolderPath, replicaFolderPath, logFilePath, 1)
    dirsToDelete = replicaDirsSet - sourceDirsSet
    for dirs in dirsToDelete:
        shutil.rmtree(replicaFolderPath+'\\'+dirs)
        writeLogFile(dirs,
                     sourceFolderPath, replicaFolderPath, logFilePath, 1)
        
    # the files in the source foulder need to be copied to the replica folder.
    for file in sourceFilesSet:
        shutil.copy2(sourceFolderPath+'\\'+file, replicaFolderPath)
        writeLogFile(file,
                     sourceFolderPath, replicaFolderPath, logFilePath, 2)
    # now repeat the process for all the subfolders.
    for dirs in sourceDirsSet:
        # If this subdirectory does not exist in the replica folder it needs to
        # be created
        if dirs not in replicaDirsSet:
            os.mkdir(replicaFolderPath+'\\'+dirs)
            writeLogFile(dirs,
                         sourceFolderPath, replicaFolderPath, logFilePath, 3)
        synchFolders(sourceFolderPath+'\\'+dirs, replicaFolderPath+'\\'+dirs,
                     logFilePath)

def createLogFile(sourceFolderPath, replicaFolderPath, logFilePath):
    ''' Create a Log File in logFilePath if there is not one. It logs the 
        synching of the folders on sourceFolderPath and replicaFolderPath
    '''

    with open(logFilePath+'log.txt', 'w') as file:
        file.write('## This is the log for the synchronization of the folders {} and {}'
                      .format(sourceFolderPath, replicaFolderPath))

def writeLogFile(fileName, sourceFolderPath, replicaFolderPath, logFilePath,
                 operationType):
    ''' Log and print the operations done
    
    Args:
        fileName: name of the file that was changed
        sourceFolderPath: the path of the source folder
        replicaFolderPath: the path of the replica folder
        logFilePath: path for the file where operations will be logged
        operationType: 1-remove, 2-copy, 3-create
    '''
    
    with open(logFilePath, 'a') as logFile:
        if operationType == 1:
            logFile.write('Removed {} from {}.\n'.format(fileName,
                                                         replicaFolderPath))
            print('Removed {} from {}.\n'.format(fileName,
                                                 replicaFolderPath))
        elif operationType == 2:
            logFile.write('Copied {} from {} to {}.\n'.format(fileName,
                                                              sourceFolderPath,
                                                              replicaFolderPath))
            print('Copied {} from {} to {}.\n'.format(fileName,
                                                      sourceFolderPath,
                                                      replicaFolderPath))
        else:
            logFile.write('Created the {} folder on {}.\n'.format(fileName,
                                                              replicaFolderPath))
            print('Created the {} folder on {}.\n'.format(fileName,
                                                          replicaFolderPath))
        
        

# Read folder paths, synchronization interval and log file path from command
# line arguments, in that order
print(sys.argv)
sourceFolderPath = sys.argv[1]
replicaFolderPath = sys.argv[2]
synchInterval = int(sys.argv[3])
logFilePath = sys.argv[4]

synchTimeLoop(sourceFolderPath, replicaFolderPath, synchInterval, logFilePath)
