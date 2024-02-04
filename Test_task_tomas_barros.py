# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 10:33:36 2024

@author: Tomás Barros

Veeam test task
"""

import sys
import time


def synchTimeLoop(sourceFolderPath, replicaFolderPath, synchInterval,
                  logFilePath):
    '''Preforms synchronization every synchInterval seconds
    
    Agrs:
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

def synchFolders(sourceFolderPath, replicaFolderPath, synchInterval,
                logFilePath):
    pass

# Read folder paths, synchronization interval and log file path from command
# line arguments, in that order
sourceFolderPath = sys.argv[1]
replicaFolderPath = sys.argv[2]
synchInterval = int(sys.argv[3])
logFilePath = sys.argv[4]

synchTimeLoop(synchInterval)
