'''
This program is the front end of a system which provides an interface for transactions for transport tickets.
The program takes a valid services list as input and outputs a transaction summary file.
It is designed to be run using a command line providing it with text.
'''

from __future__ import print_function
import argparse
import sys
import os

# Class for the FrontEnd project


class FrontEnd:
    # initializes the FrontEnd object
    def __init__(self, services=[], transactionSummaryFile="", inputs=[]):
        self.numCancelledTickets = 0  # counts the number of tickets already cancelled
        self.numChangedTickets = 0  # counts the number of tickets already changed
        # indicates whether FrontEnd is logged in, and if so, whether it’s in planner mode or agent mode
        self.sessionType = -1
        self.deletedServiceNumbers = []
        useCliForInput = len(inputs) == 0
        self.transactionSummaryFile = transactionSummaryFile
        while (useCliForInput or len(inputs) > 0):
            if(useCliForInput):
                line = input("Transaction code: ").split(" ")
            else:
                line = inputs.pop(0).split(" ")
            transactionCode = line[0]
            if(transactionCode == "login"):
                self.login(line, services)
            elif(transactionCode == "logout"):
                self.logout(line)
            elif(transactionCode == "createservice"):
                self.createService(line)
            elif(transactionCode == "deleteservice"):
                self.deleteService(line)
            elif(transactionCode == "sellticket"):
                self.sellTicket(line)
            elif(transactionCode == "cancelticket"):
                self.cancelTicket(line)
            elif(transactionCode == "changeticket"):
                self.changeTicket(line)
            else:
                logError("Invalid transaction code")

    # logs the user in as either a planner or an agent and reads in the valid services file
    def login(self, data, services):
        if self.sessionType != -1:
            logError("Already logged in")
            return
        if len(data) != 2:
            logError("Invalid arguments")
            return
        if data[1] == "agent" or data[1] == "planner":
            self.sessionType = data[1]
            self.validServicesFile = services
            print("Logged in as", self.sessionType)
        else:
            self.sessionType = -1
            logError("Invalid login")

    # takes logout command as input, ensures user is logged in, writes EOS to transaction summary file and logs out
    def logout(self, data):
        if self.sessionType != "agent" and self.sessionType != "planner":
            logError("Must be logged in")
            return
        self.recordEOS()
        self.sessionType = -1

    # creates a service, given a service number, date, and service name
    def createService(self, data):
        if self.sessionType != "planner":
            logError("Not logged in to planner mode ")
            return
        if len(data) != 4:
            logError("Invalid data entry")
            return
        serviceNumber = data[1]
        date = data[2]
        serviceName = data[3]
        if self.isValidService(serviceNumber, date, serviceName) and not self.serviceAlreadyExists(serviceNumber):
            self.recordTransaction(transactionCode="CRE", srcServiceNum=serviceNumber, serviceName=serviceName, serviceDate=date)
        else:
            logError("Invalid service")

    #  deletes a service, given a service number, date, and service name
    def deleteService(self, data):
        if self.sessionType != "planner":
            logError("Not logged in to planner mode")
            return
        if len(data) != 4:
            logError("Invalid service for deleteService")
            return
        serviceNumber = data[1]
        date = data[2]
        serviceName = data[3]

        if self.isValidService(serviceNumber, date, serviceName) and self.serviceAlreadyExists(serviceNumber):
            self.deletedServiceNumbers.append(serviceNumber)
            self.recordTransaction(transactionCode="DEL", srcServiceNum=serviceNumber, serviceName=serviceName, serviceDate=date)

        else:
            logError("Invalid service")

    # takes a the sellticket command as input, verifies its correctness and writes it to the transaction summary file
    def sellTicket(self, data):
        if self.sessionType == -1:
            logError("Not logged in")
            return
        if len(data) != 3:
            logError("Transaction is not of the correct format")
            return
        serviceNum = data[1]
        numTickets = data[2]
        if int(numTickets) > 1000 or int(numTickets) < 1:
            logError("Invalid number of tickets")
            return
        if self.isValidServiceNumber(serviceNum) and self.serviceAlreadyExists(serviceNum):
            self.recordTransaction(transactionCode="SEL", srcServiceNum=serviceNum, numTickets=numTickets)
        else:
            logError("Invalid service number")
            return
    #  takes a service number and the number of tickets and cancels that many tickets

    def cancelTicket(self, data):
        if self.sessionType == -1:
            logError("Not logged in")
            return
        if len(data) != 3:
            logError("Invalid arguments")
            return
        numCancelledTickets = int(data[2])+self.numCancelledTickets
        if self.serviceAlreadyExists(data[1]):
            if self.sessionType == "agent":
                if numCancelledTickets > 10:
                    logError("Invalid ticket amount for agent")
                else:
                    self.numCancelledTickets += int(data[2])
                    self.recordTransaction(transactionCode="CAN", srcServiceNum=data[1], numTickets=numCancelledTickets)
            elif self.sessionType == "planner":
                self.numCancelledTickets += int(data[2])
                self.recordTransaction(transactionCode="CAN", srcServiceNum=data[1], numTickets=numCancelledTickets)
            else:
                logError("Not logged in")
                return

        else:
            logError("Invalid service number")

    #  takes a old service number, a new service number, and a number of tickets and changes that many tickets
    def changeTicket(self, data):
        if self.sessionType == -1:
            logError("Not logged in")
            return
        if (len(data) != 4):
            logError(
                "Transaction should be of form: changeticket {old service number} {new service number} {number of tickets}")
            return
        oldServiceNum = data[1]
        newServiceNum = data[2]
        numTickets = int(data[3])
        if (self.numChangedTickets + numTickets >= 20 and self.sessionType != "planner"):
            logError("Too many changed tickets")
        if (self.isValidServiceNumber(oldServiceNum) and self.isValidServiceNumber(newServiceNum)
                and self.serviceAlreadyExists(oldServiceNum) and self.serviceAlreadyExists(newServiceNum)):
            self.numChangedTickets += numTickets
            self.recordTransaction(transactionCode="CHG", srcServiceNum=oldServiceNum, destServiceNum=newServiceNum, numTickets=numTickets)
        else:
            logError("Invalid service number")

    #  returns boolean of whether a service number already exists in the valid services file
    def serviceAlreadyExists(self, serviceNumber):
        if (serviceNumber in self.deletedServiceNumbers):
            return False
        listOfNumbers = self.validServicesFile
        for line in listOfNumbers:
            if serviceNumber == line:
                return True
        return False

    #  returns boolean of whether a service number, date, and name are valid
    def isValidService(self, serviceNumber, date, serviceName):
        if (len(serviceName) < 3) or (len(serviceName) > 39):
            return False
        if serviceName[0] == ' ' or serviceName[-1] == ' ':
            return False

        # Verifying if appropriate date
        if len(date) != 8:
            return False

        year = int(date[0:4])
        month = int(date[4:6])
        day = int(date[6::])

        if year < 1980 or year > 2999:
            return False
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False

        # If it passes all of the tests above, it's a valid service
        return self.isValidServiceNumber(serviceNumber)

    # returns boolean of whether a service number is valid
    def isValidServiceNumber(self, num):
        try:
            return 10000 < int(num) < 99999
        except TypeError:
            return False

    def recordEOS(self):
        if (len(self.transactionSummaryFile) > 0):
            filePath = self.transactionSummaryFile
        else:
            filePath = "./transactionSummaryFile.txt"
        with open(filePath, "a+") as transactionFile:
            transactionFile.write("EOS\n")
    
    # records a transaction to the transaction summary file
    def recordTransaction(self, transactionCode="CCC", srcServiceNum="00000", numTickets="0", destServiceNum="00000", serviceName="****", serviceDate="0"):
        if (len(self.transactionSummaryFile) > 0):
            filePath = self.transactionSummaryFile
        else:
            filePath = "./transactionSummaryFile.txt"
        output="{} {} {} {} {} {}\n".format(transactionCode, srcServiceNum, numTickets, destServiceNum, serviceName, serviceDate)
        with open(filePath, "a+") as transactionFile:
            transactionFile.write(output)


# prints a message to stderr
def logError(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# Instantiates the FrontEnd object. Takes the location of the valid services file as a command-line argument
def main(vsf=None, tsf=None, inputFile=""):
    parser = argparse.ArgumentParser(description='Initiatiate the front end')
    parser.add_argument("--vsf", type=str,
                        help="The absolute location of the valid services file")
    parser.add_argument("--tsf", type=str,
                        help="The absolute location of the transaction summary file")
    arguments = parser.parse_args()
    if (vsf != None):
        services = vsf
    else:
        services = arguments.vsf
    if (tsf != None):
        summary = tsf
    else:
        summary = arguments.tsf
    inp = []
    if(len(inputFile) > 0):
        with open(inputFile) as inputs:
            inp = inputs.read().split("\n")
    with open(services) as services:
        FrontEnd(services.read().split("\n"), summary, inp)


def test():
    testFolders = os.listdir("./Tests")
    for folder in testFolders:
        num = 1
        try:
            while (True):
                print("running test {} {}".format(folder, num))
                inputFile = "./front-end-tests/" + folder + \
                    "/inputs/{}{}.txt".format(folder, num)
                outputFile = "./front-end-tests/" + folder + \
                    "/outputs/{}{}.txt".format(folder, num)
                open(outputFile, 'w').close()  # wipe file
                main("./validServicesFile.txt", outputFile, inputFile)
                num += 1
        except FileNotFoundError:
            pass


# main()
test()
