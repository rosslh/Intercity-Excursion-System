'''comment at beginning of main program, documenting:
overall program intention,
input and output files,
how the program is intended to be run'''

from __future__ import print_function
import argparse
import sys


class FrontEnd:
    numCancelledTickets = 0
    numChangedTickets = 0
    sessionType = -1

    def __init__(self, services):
        while (True):
            line = input("Transaction code: ").split(" ")
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

    # Method for login
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

    # Method for logout takes logout command as input, ensures user is logged in, writes EOS to transaction summary file and logs out
    def logout(self, data):
        if self.sessionType != "agent" and self.sessionType != "planner":
            logError("Must be logged in")
            return
        self.recordTransaction("EOS")
        self.sessionType = -1

    def createService(self, data):
        if self.sessionType == -1:
            logError("Not logged in")
            return
        if len(data) != 4:
            logError("Invalid data entry")
            return
        serviceNumber = data[1]
        date = data[2]
        serviceName = data[3]
        if self.isValidService(serviceNumber, date, serviceName) and not self.serviceAlreadyExists(serviceNumber):
            # self.validServicesFile.write(serviceNumber + '\n')
            self.recordTransaction(data)
        else:
            logError("Invalid service")

    def deleteService(self, data):
        if self.sessionType == -1:
            logError("Not logged in")
            return
        if len(data) != 4:
            logError("Invalid service for deleteService")
            return
        serviceNumber = data[1]
        date = data[2]
        serviceName = data[3]
        # placeholder date
        if self.isValidService(serviceNumber, date, serviceName) and self.serviceAlreadyExists(serviceNumber):
            self.recordTransaction(data)
            # listOfServices = self.validServicesFile.readlines()

            # for service in listOfServices:
            #     if service != (serviceNumber + '\n'):
            #         self.validServicesFile.write(service)
        else:
            logError("Invalid service")
    # Method for sellticket, takes a the sellticket command as input, verifies its correctness and writes it to the transaction summary file

    def sellTicket(self, data):
        if self.sessionType == -1:
            logError("Not logged in")
            return
        if len(data) != 3:
            logError("Transaction is not of the correct format")
            return
        num = data[1]
        numtickets = data[2]
        if int(numtickets) > 1000 or int(numtickets) < 1:
            logError("Invalid number of tickets")
            return
        if (not(self.isValidServiceNumber(num))):
            logError("Invalid service number")
            return
        if (not(self.serviceAlreadyExists(num))):
            logError("Service number does not exist")
            return
        else:
            self.recordTransaction(data)

    def cancelTicket(self, data):
        if self.sessionType == -1:
            logError("Not logged in")
            return
        if len(data) != 3:
            logError("Invalid arguments")
            return
        if self.serviceAlreadyExists(data[1]):
            if self.sessionType == "agent":
                if int(data[2]) > 10:
                    logError("Invalid ticket amount for agent")
                elif self.numCancelledTickets >= 20:
                    logError("Invalid ticket amount for planner")
                else:
                    self.numCancelledTickets += int(data[2])
                    self.recordTransaction(data)

            else:
                self.numCancelledTickets += int(data[2])
                self.recordTransaction(data)

        else:
            logError("Invalid service number")

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
        if (self.isValidServiceNumber(oldServiceNum) and self.isValidServiceNumber(newServiceNum)):
            self.numChangedTickets += numTickets
            self.recordTransaction(data)
        else:
            logError("Invalid service number")

    def serviceAlreadyExists(self, serviceNumber):
        listOfNumbers = self.validServicesFile
        for line in listOfNumbers:
            if serviceNumber == line:
                return True
        return False

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

    def isValidServiceNumber(self, num):
        try:
            return 10000 < int(num) < 99999
        except TypeError:
            return False

    def recordTransaction(self, transaction):
        output = ""
        filePath = "transactionSummaryFile.txt"
        if (transaction[0] == "changeticket"):
            output = "CHG " + " ".join(transaction[1:]) + "\n"
        else:
            output = transaction[0][:3].upper() + " " + \
                " ".join(transaction[1:]) + "\n"
        with open(filePath, "a+") as transactionFile:
            transactionFile.write(output)


def logError(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    parser = argparse.ArgumentParser(description='Initiatiate the front end')
    parser.add_argument("--services", type=str,
                        help="The absolute location of the valid services file")
    arguments = parser.parse_args()
    with open(arguments.services) as services:
        FrontEnd(services.read().split("\n"))


main()
