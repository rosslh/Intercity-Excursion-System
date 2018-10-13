from __future__ import print_function
import argparse
import sys


class FrontEnd:
    def __init__(self, services):
        while (True):
            line = input("Transaction code: ")
            transactionCode = line.split(" ")[0]
            if(transactionCode == "login"):
                self.login(line)
            elif(transactionCode == "logout"):
                self.logout(line)
            elif(transactionCode == "createService"):
                self.createService(line)
            elif(transactionCode == "deleteService"):
                self.deleteService(line)
            elif(transactionCode == "sellTicket"):
                self.sellTicket(line)
            elif(transactionCode == "cancelTicket"):
                self.cancelTicket(line)
            elif(transactionCode == "changeTicket"):
                self.changeTicket(line)
            else:
                logError("Invalid transaction code")

    def login(self, data):
        # self.sessionType = "agent"/"planner"
        print("at login")  # TODO: remove before handing in
        pass

    def logout(self, data):
        # self.sessionType = None
        pass

    def createService(self, data):
        pass

    def deleteService(self, data):
        pass

    def sellTicket(self, data):
        pass

    def cancelTicket(self, data):
        pass

    def changeTicket(self, data):
        pass

    def recordTransaction(self, transaction):
        pass


def logError(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    parser = argparse.ArgumentParser(description='Initiatiate the front end')
    parser.add_argument("--services", type=str,
                        help="The absolute location of the valid services file")
    arguments = parser.parse_args()
    with open(arguments.services) as services:
        FrontEnd(services)


main()
