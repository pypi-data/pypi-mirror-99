class OProgressBar():
    def __init__(
        self,
        completeState = 100,
        *,
        prefix = "Progress: ",
        suffix = "Complete",
        length = 60,
        decimalPlaces = 1,
        fill = "█",
        printEnd= "\r"
    ):

        self.completeState = completeState
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.decimalPlaces = decimalPlaces
        self.fill = fill
        self.printEnd = printEnd

    def PrintProgress(self, progressState):
        percent = ("{0:." + str(self.decimalPlaces) + "f}").format(100 * (progressState / float(self.completeState)))
        filledLength = int(self.length * progressState // self.completeState)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end = self.printEnd)
        # Print New Line on Complete
        if progressState == self.completeState: 
            print()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------#

class OLogger():
    import logging
    from pathlib import Path
    import traceback
    from datetime import datetime

    logFormat = "%(asctime)s:%(msecs)d -- %(levelname)s -- %(message)s"
    logFormatWLoggerName = "%(asctime)s:%(msecs)d -- %(name)s: %(levelname)s -- %(message)s"
    dateFormat = "%Y-%m-%d|%H:%M:%S"
    logging.basicConfig(level=logging.NOTSET, format=logFormat, datefmt=dateFormat)
    logTime = datetime.now().strftime("[%Y-%m-%d]-[%H-%M-%S]")
    mainPyScriptName = str(Path(__file__).stem)
    level = logging

    def __init__(self, *, streamLoggin = True, fileLoggin = False, logFileName = mainPyScriptName, logFileLevel = "NOTSET", showLoggerNameOnFile = False):
        self.logger = self.logging.getLogger(f"{logFileName}_Logger" if logFileName == self.mainPyScriptName else logFileName)

        logLevelList = {
            "NOTSET": self.logging.NOTSET,
            "DEBUG": self.logging.DEBUG,
            "INFO": self.logging.INFO,
            "WARNING": self.logging.WARNING,
            "ERROR": self.logging.ERROR,
            "CRITICAL": self.logging.CRITICAL,
        }
        default = self.logging.NOTSET

        if fileLoggin:
            try:
                import os
                folderCreationFlag = False

                if "Logs" not in list(os.listdir('.')):
                    os.mkdir("Logs")
                    folderCreationFlag = True

                fileHandler = self.logging.FileHandler(f"./Logs/{self.mainPyScriptName}-{self.logTime}.log")
                fileHandler.setLevel(logLevelList[logFileLevel])
                fileHandler.setFormatter(self.logging.Formatter(self.logFormat if not showLoggerNameOnFile else self.logFormatWLoggerName, datefmt=self.dateFormat))
                self.logger.addHandler(fileHandler)

                if folderCreationFlag == True:
                    self.LogAnInfo("Logs Folder was created!")

            except Exception:
                print(self.traceback.format_exc())

        if not streamLoggin:
            self.logger.propagate = False

    def LogDebug(self, infoMessege):
        self.logger.debug(infoMessege)

    def LogInfo(self, infoMessege):
        self.logger.info(infoMessege)

    def LogWarning(self, WarningMessege):
        self.logger.warning(WarningMessege)

    def LogError(self, errorMessege):
        self.logger.error(errorMessege)

    def LogExceptError(self, errorMessege):
        self.logger.critical(f"{errorMessege}: {self.traceback.format_exc()}")  
