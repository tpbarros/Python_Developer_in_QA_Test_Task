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
        sourceFolderPath: the path of the source folder
    '''
    # it keeps synchromizing the two folders each synchInterval seconds until
    # the program is manually stopped
    while True:
        try:
            time.sleep(synchInterval)
            synchFolders(sourceFolderPath, replicaFolderPath, synchInterval,
                              logFilePath)
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
        return filesSet, dirsSet

    sourceFilesSet, sourceDirsSet = separateFilesAndDirs(sourceFolderPath)
    replicaFilesSet, replicaDirsSet = separateFilesAndDirs(replicaFolderPath)

    # files and folders that are in the replica folder but not in the source 
    # folder need to be deleted
    filesToDelete = replicaFilesSet - sourceFilesSet
    for file in filesToDelete:
        os.remove(replicaFolderPath+'\\'+file)
    dirsToDelete = replicaDirsSet - sourceDirsSet
    for dirs in dirsToDelete:
        shutil.rmtree(replicaFolderPath+'\\'+dirs)
        
    # the files in the source foulder need to be copied to the replica folder.
    for file in sourceFilesSet:
        shutil.copy2(sourceFolderPath+'\\'+file, replicaFolderPath)
    # now repeat the process for all the subfolders.
    for dirs in sourceDirsSet:
        # If this subdirectory does not exist in the replica folder it needs to
        # be created
        if dirs not in replicaDirsSet:
            os.mkdir(replicaFolderPath+'\\'+dirs)
        synchFolders(sourceFolderPath+'\\'+dirs, replicaFolderPath+'\\'+dirs)

# Read folder paths, synchronization interval and log file path from command
# line arguments, in that order
sourceFolderPath = sys.argv[1]
replicaFolderPath = sys.argv[2]
synchInterval = int(sys.argv[3])
logFilePath = sys.argv[4]

synchTimeLoop(synchInterval)
