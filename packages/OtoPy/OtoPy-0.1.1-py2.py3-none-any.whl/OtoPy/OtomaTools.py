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

    def PrintProgess(self, progressState):
        percent = ("{0:." + str(self.decimalPlaces) + "f}").format(100 * (progressState / float(self.completeState)))
        filledLength = int(self.length * progressState // self.completeState)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end = self.printEnd)
        # Print New Line on Complete
        if progressState == self.completeState: 
            print()