from __future__ import print_function
import argparse
import sys
import os

'''
This runs the backend of our transit system which takes end of day reports from the front office and generates new files for the next day.
It takes the transaction summary and central services files as input and outputs the new valid services and central services files.
This program can be run given the needed files are in the path.
'''
#This class implements the back office of our transit system
class BackEnd:
    def __init__(self, vsf, csf, tsf):
        self.vsf = vsf
        self.vsf.pop()
        self.csf = csf
        self.tsf = tsf
        self.applyTransactions()

    #This function reads in the input data and applies it to the new outputs 
    def applyTransactions(self):
        for i in range(len(self.tsf)):
            data = self.tsf[i].split(' ')
            if data == ['']:
                continue
            elif (data[0] == 'EOS'):
                self.writeFiles()
            elif (data[0] == 'CRE'):
                for x in range(len(self.csf)):
                    if (self.csf[x][:5] == data[1]):
                        logError("Service number must not be in use")
                self.vsf.append(data[1])
                self.csf.append(data[1]+' '+'30 0 '+data[4]+' '+data[5])
            else:
                for j in range(len(self.csf)):
                    if (self.csf[j][:5] == data[1]):
                        service = [j] + self.csf[j].split(' ')        
                if (data[0] == 'DEL'):
                    if data[2] != '0':
                        logError("Deleted service ticket numbers must be 0")
                        return
                    elif data[4] != self.csf[service[0]][11:19]:
                        logError("Service names do not match")
                        return
                    else:
                        self.vsf.pop(self.vsf.index(data[1]))
                        self.csf.pop(service[0])
                elif (data[0] == 'SEL'):
                    service[3] = str(int(service[3]) + int(data[2]))
                    if int(service[3]) > 30:
                        logError("Number of tickets cannot exceed capacity")
                        return
                    else:
                        self.csf[service[0]] = ' '.join(service[1:])
                elif (data[0] == 'CAN'):
                    service[3] = str(int(service[3]) - int(data[2]))
                    if int(service[3]) < 0:
                        logError("Number of tickets cannot be negative")
                        return
                    else:
                        self.csf[service[0]] = ' '.join(service[1:])
                elif (data[0] == 'CHG'):
                    for k in range(len(self.csf)):
                        if (self.csf[k][:5] == data[3]):
                            service2 = [k] + self.csf[k].split(' ')
                    service[3] = str(int(service[3]) - int(data[2]))
                    self.csf[service[0]] = ' '.join(service[1:])
                    service2[3] = str(int(service2[3]) + int(data[2]))
                    self.csf[service2[0]] = ' '.join(service2[1:])
                else:
                    logError("Invalid TSF format")
                    sys.exit

    #This method writes data to the new valid services and central services files
    def writeFiles(self):
        self.vsf.append('00000')
        with open('./newValidServicesFile.txt', 'w') as f:
            for service in self.vsf:
                f.write("%s\n" % service)
        with open('./newCentralServicesFile.txt', 'w') as f:
            for service in self.csf:
                if len(service) > 0:
                    data = service.split()
                    if int(data[1]) < 0 or int(data[1]) > 1000:
                        logError("Invalid capacity")
                        return
                    if int(data[2]) < 0 or int(data[2]) > 1000:
                        logError("Invalid number of tickets")
                        return
                    if int(data[2]) > int(data[1]):
                        logError("Number of tickets cannot exceed capacity")
                        return
                    if len(service) > 63:
                        logError("Length of line exceeds 63 characters")
                        return
                    else:
                        f.write("%s\n" % service)

#prints a message to stderr
def logError(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)               
                
#Main function opens the valid services, transaction summmary and central services input files and passes them to the BackEnd class
def main():
    vsf = [line.rstrip('\n') for line in open("./validServicesFile.txt")]
    csf = [line.rstrip('\n') for line in open("./centralServicesFile.txt")]
    tsf = [line.rstrip('\n') for line in open("./transactionSummaryFile.txt")]
    BackEnd(vsf, csf, tsf)

main()
