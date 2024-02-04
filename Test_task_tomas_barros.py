# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 10:33:36 2024

@author: Tomás Barros

Veeam test task
"""

import sys

# Read folder paths, synchronization interval and log file path from command
# line arguments, in that order
sourceFolderPath = sys.argv[1]
replicaFolderPath = sys.argv[2]
synchInterval = sys.argv[3]
logFilePath = sys.argv[4]