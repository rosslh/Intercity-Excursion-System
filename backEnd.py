from __future__ import print_function
import argparse
import sys
import os

# Class for the FrontEnd project


class BackEnd:
    def __init__(self, vsf, csf, tsf):
        self.vsf = vsf
        self.vsf.pop()
        self.csf = csf
        self.tsf = tsf
        self.applyTransactions()

    def applyTransactions(self):
        for i in range(len(self.tsf)):
            data = self.tsf[i].split(' ')
            if (data[0] == 'CRE'):
                self.vsf.append(data[1])
                self.csf.append(data[1]+' '+'1000 0 '+data[4]+' '+data[5])
            elif (data[0] == 'EOS'):
                self.writeFiles()
            else:
                for j in range(len(self.csf)):
                    if (self.csf[j][:5] == data[1]):
                        service = [j] + self.csf[j].split(' ')
                if (data[0] == 'DEL'):
                    self.vsf.pop(self.vsf.index(data[1]))
                    self.csf.pop(service[0])
                elif (data[0] == 'SEL'):
                    service[3] = str(int(service[3]) + int(data[2]))
                    self.csf[service[0]] = ' '.join(service[1:])
                elif (data[0] == 'CAN'):
                    service[3] = str(int(service[3]) - int(data[2]))
                    self.csf[service[0]] = ' '.join(service[1:])
                elif (data[0] == 'CHG'):
                    for k in range(len(self.csf)):
                        if (self.csf[k][:5] == data[3]):
                            service2 = [k] + self.csf[k].split(' ')
                    service[3] = str(int(service[3]) - int(data[2]))
                    self.csf[service[0]] = ' '.join(service[1:])
                    service2[3] = str(int(service2[3]) + int(data[2]))
                    self.csf[service2[0]] = ' '.join(service2[1:])

    def writeFiles(self):
        self.vsf.append('00000')
        with open('./newValidServicesFile.txt', 'w') as f:
            for service in self.vsf:
                f.write("%s\n" % service)
                
        with open('./newCentralServicesFile.txt', 'w') as f:
            for service in self.csf:
                f.write("%s\n" % service)

def main():
    vsf = [line.rstrip('\n') for line in open("./validServicesFile.txt")]
    csf = [line.rstrip('\n') for line in open("./centralServicesFile.txt")]
    tsf = [line.rstrip('\n') for line in open("./transactionSummaryFile.txt")]
    BackEnd(vsf, csf, tsf)

main()
