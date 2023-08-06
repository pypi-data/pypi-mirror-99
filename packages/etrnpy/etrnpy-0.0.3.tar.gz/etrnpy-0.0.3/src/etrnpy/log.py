import logging

import os
import inspect
import traceback
import sys
import time
from time import localtime
from time import strftime
from time import strftime
from time import mktime

#log

# logging.getLogger('').handlers = []
# logging.basicConfig(filename = archive_root + r'\ETRNDataCleanUp.log',
#                     level=logging.INFO,
#                     format='%(asctime)s | %(levelname)s | %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p')




# # Create handlers
# c_handler = logging.StreamHandler()
# c_handler.setLevel(logging.WARNING)

# # Create formatters and add it to handlers
# c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# c_handler.setFormatter(c_format)

# # Add handlers to the logger
# logger.addHandler(c_handler)
def get_logger():

        # Create a custom logger
        logger = logging.getLogger(__name__)
        f_handler = logging.FileHandler('file.log')
        f_handler.setLevel(logging.INFO)
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S %p')
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

        return logger

        
class Logging:

    @staticmethod
    
        
    @staticmethod
    def add_action(action):
        global actionReport
        log(action)
        actionReport = actionReport + action + "\n"


    @staticmethod
    # Function for error reporting
    def except_handle(e):
        tb = sys.exc_info()[2]
        scriptName = os.path.basename(inspect.getfile(inspect.currentframe()))
        log(scriptName + " " + strftime("%Y %b %d %H:%M:%S", localtime()))
        log("An error occured.  on line " + str(tb.tb_lineno))
        log("arcpy message:  " +  arcpy.GetMessages() )      
        log("Python message:  " + e.message)
        log("Script. Terminated.")

    @staticmethod
    def log(message):
        global logfileLocation
        print (message)
        if not os.path.exists(os.path.join(workingdir,'logs\\')):
            os.makedirs(os.path.join(workingdir,'logs\\'))   
        f = open(logfileLocation, 'a')  
        f.write(timestamp() + message + '\n')
        f.close

    @staticmethod
    def log_and_print(message, level=None):

        """prints and logs. level can be either info or error"""

        print(message)
        logging.info(message) if level == 'info' else logging.error(message)

    @staticmethod
    def msgLog(msg):
        print ("{0}\n".format(msg))
        arcpy.AddMessage("{0}\n".format(msg))
        

    @staticmethod
    def time_stamp():
        return strftime("[%Y%m%d %H:%M:%S]", localtime())
