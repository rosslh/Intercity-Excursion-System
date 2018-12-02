from frontEnd import main as frontEnd
from backEnd import main as backEnd

class Driver:
    def __init__(self):
        self.weeklyScript();
    
    def mergeTransactionSummaryFiles(self):
        outfilename = "mergedTransactionSummaryFile.txt"
        with open(outfilename, 'w') as outfile:
            for filename in glob.glob("./transactionSummaryFiles/*"):
                with open(filename, 'r') as readfile:
                    for line in readfile:
                        if "EOS" not in line:
                            outfile.write(line)
            outfile.write("EOS")

    def dailyScript(self):
        frontEnd(inputFile="./user-input/userInput1.txt", tsf="./transactionSummaryFiles/tsf1.txt")
        frontEnd(inputFile="./user-input/userInput2.txt", tsf="./transactionSummaryFiles/tsf2.txt")
        frontEnd(inputFile="./user-input/userInput3.txt", tsf="./transactionSummaryFiles/tsf3.txt")

        self.mergeTransactionSummaryFiles();

        backEnd(transactionSummaryFile="./mergedTransactionSummaryFile.txt")
 
    def weeklyScript(self):
        self.dailyScript()
        self.dailyScript()
        self.dailyScript()
        self.dailyScript()
        self.dailyScript()
        pass


def main():
    Driver()

main()
