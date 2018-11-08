from __future__ import print_function
import argparse
import sys
import os

# Class for the FrontEnd project


class BackEnd:
    def __init__(self, vsf, csf, tsf):
        print(vsf)
        print(csf)
        print(tsf)
        


def main():
    vsf = [line.rstrip('\n') for line in open("./validServicesFile.txt")]
    csf = [line.rstrip('\n') for line in open("./coreServicesFile.txt")]
    tsf = [line.rstrip('\n') for line in open("./transactionSummaryFile.txt")]
    BackEnd(vsf, csf, tsf)

main()