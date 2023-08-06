class OProgressBar():
    prefix = "Progress: "
    suffix = "Complete"
    decimalPlaces = 1
    length = 60
    fill = "█"
    printEnd = "\r"

    def __init__(self, completeState, **kargs):
        if prefix: 
            self.prefix = prefix
        if suffix:
            self.suffix = suffix
        if decimalPlaces:
            self.decimalPlaces = decimalPlaces
        if length:
            self.length = length
        if fill:
            self.fill = fill
        if printEnd:
            self.printEnd = printEnd
            
        self.completeState = completeState

    def PrintProgess(self, progressState):
        percent = ("{0:." + str(self.decimalPlaces) + "f}").format(100 * (progressState / float(self.completeState)))
        filledLength = int(self.length * progressState // self.completeState)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end = self.printEnd)
        # Print New Line on Complete
        if progressState == self.completeState: 
            print()