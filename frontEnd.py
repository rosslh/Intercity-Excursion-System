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
            line = input("Transaction code: ")
            transactionCode = line.split(" ")[0]
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
        # self.sessionType = "agent"/"planner"
        print("at login")  # TODO: remove before handing in
        pass

    def logout(self, data):
        self.recordTransaction("EOS")
        filePath.close()
        self.sessionType = -1

    def createService(self, data):
        pass

    def deleteService(self, data):
        pass

    def sellTicket(self, data):
    splitData = data.split()
    if len(splitData) != 3:
        logError("Transaction is not of the correct format")
    num = splitData[1]
    numtickets = splitData[2]
    if int(numtickets) > 1000 or int(numtickets) < 1:
        logError("Invalid number of tickets")
    if (not(self.isValidServiceNumber(num))):
        logError("Invalid service number")
    else:
        self.recordTransaction("SEL %s %s 00000 **** 0"%(num, numtickets)) 

    def cancelTicket(self, data):
        pass

    def changeTicket(self, data):
        splitData = data.split(" ")
        if (len(splitData) != 4):
            logError(
                "Transaction should be of form: changeticket {old service number} {new service number} {number of tickets}")
            return
        oldServiceNum = splitData[1]
        newServiceNum = splitData[2]
        numTickets = int(splitData[3])
        if (self.numChangedTickets + numTickets >= 20 and self.sessionType != "planner"):
            logError("Too many changed tickets")
        if (self.isValidServiceNumber(oldServiceNum) and self.isValidServiceNumber(newServiceNum)):
            self.numChangedTickets += numTickets
            self.recordTransaction(data)
        else:
            logError("Invalid service number")

    def isValidServiceNumber(self, num):
        try:
            return 10000 < int(num) < 99999
        except TypeError:
            return False

    def recordTransaction(self, transaction):
        filePath = "transactions.txt"
        with open(filePath, "a+") as transactionFile:
            transactionFile.write("{}\n".format(transaction))


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
