from __future__ import print_function
import argparse
import sys


class FrontEnd:
    numCancelledTickets = 0
    numChangedTickets = 0
    sessionType = -1

    def __init__(self, services):
        self.services = services
        while (True):
            line = input("Transaction code: ").split(" ")
            transactionCode = line[0]
            if(transactionCode == "login"):
                self.login(line)
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

    def login(self, data):
        if self.sessionType != -1:
            logError("Already logged in")
            return
        if len(data) != 2:
            logError("Invalid arguments")
            return
        if data[1] == "agent" or data[1] == "planner":
            self.sessionType = data[1]
            self.recordTransaction(data)
            with open(sys.argv[2]) as f:
                self.services = f.read().splitlines()
            print("Logged in as", self.sessionType)
        else:
            self.sessionType = -1
            logError("Invalid login")

    def logout(self, data):
        self.recordTransaction("EOS")
        filePath.close()
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
        validServicesFile = open('validServicesFile.txt', 'a+')
        if self.isValidService(serviceNumber, date, serviceName) and not self.serviceAlreadyExists(serviceNumber):
            validServicesFile.write(serviceNumber + '\n')
            self.recordTransaction(data)
        else:
            logError("Invalid service")

    def deleteService(self, data):
        if self.sessionType == -1:
            logError("Not logged in")
            return
        if len(data) != 3:
            logError("Invalid service for deleteService")
            return
        serviceNumber = data[1]
        date = data[2]
        serviceName = data[3]
        # placeholder date
        if self.isValidService(serviceNumber, date, serviceName) and self.serviceAlreadyExists(serviceNumber):
            self.recordTransaction(data)

            validServicesFile = open('validServicesFile.txt', 'r')
            listOfServices = validServicesFile.readlines()
            validServicesFile.close

            validServicesFile = open('validServicesFile.txt', "w")
            for service in listOfServices:
                if service != (serviceNumber + '\n'):
                    validServicesFile.write(service)
            validServicesFile.close()

    def sellTicket(self, data):
        if self.sessionType != -1:
            logError("Already logged in")
            return
        splitData = data.split()
        if len(splitData) != 3:
            logError("Transaction is not of the correct format")
            return
        num = splitData[1]
        numtickets = splitData[2]
        if int(numtickets) > 1000 or int(numtickets) < 1:
            logError("Invalid number of tickets")
            return
        if (not(self.isValidServiceNumber(num))):
            logError("Invalid service number")
            return
        else:
            self.recordTransaction(
                "SEL %s %s 00000 **** 0" % (num, numtickets))

    def cancelTicket(self, data):
        if self.sessionType == -1:
            logError("Not logged in")
            return
        if self.sessionType == -1:
            logError("Not logged in")
            return
        if len(data) != 3:
            logError("Invalid arguments")
            return
        if data[1] in self.services:
            if self.sessionType == "agent":
                if int(data[2]) > 10:
                    logError("Invalid ticket amount for agent")
                elif self.numCancelledTickets >= 20:
                    logError("Invalid ticket amount for planner")
                else:
                    self.numCancelledTickets += int(data[2])
                    transaction = 'CAN '+data[1] + \
                        ' '+data[2]+'0 NNNNNN YYYYMMDD'
                    self.recordTransaction(transaction)

            else:
                self.numCancelledTickets += int(data[2])
                transaction = 'CAN '+data[1]+' '+data[2]+'0 NNNNNN YYYYMMDD'
                self.recordTransaction(transaction)
                # print(data[2], 'tickets cancelled')
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
        listOfNumbers = validServicesFile.read().split('\n')
        for line in listOfNumbers:
            if serviceNumber == line:
                return True
        return False

    def isValidService(self, serviceNumber, date, serviceName):
        if (len(serviceName) < 3) or (len(serviceName) > 39):
            return False
        if serviceName[0] == ' ' or serviceName[-1] == ' ':
            return False
        validServicesFile = open('validServicesFile.txt', 'r')

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
        filePath = "transactionSummaryFile.txt"
        with open(filePath, "a+") as transactionFile:
            transactionFile.write("{}\n".format(" ".join(transaction)))


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
