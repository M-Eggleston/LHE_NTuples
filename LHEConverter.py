#!/usr/bin/env python3
#file LHE_NTuples.py

import sys,argparse
import functions
import ROOT

parser = argparse.ArgumentParser(description="Convert LHE files into ROOT NTuples.")
parser.add_argument('-i','--input-file',help='name of LHE file to convert',dest='in_file')
parser.add_argument('-o','--output-file',help='name of .root file in which event data will be stored',dest='out_name')

#Initialize event meta variables
numParticles = 0
eventWeight = 0.0
eventScale = 0.0
alphaEM = 0.0
alphaS = 0.0

def getMetaInfo(line):
    global numParticles
    global eventWeight
    global eventScale
    global alphaEM
    global alphaS

    numParticles = line[0]
    data = []
    for x in range(0,len(line)):
        if line[x] != '':
            data.append(line[x])
    #Check that the list has the right number of data points, else the wrong line was parsed
    if len(data) == 6:
        #One more variable exists between the number of particles and event weight, not sure what it is, omitting from ntuple
        eventWeight = data[2]
        eventScale = data[3]
        alphaEM = data[4]
        alphaS = data[5]
    else:
        print '{} data points were found, when 6 were expected! Skipping to next event.'.format(len(data))

def main():
    args = parser.parse_args()
    #Check for an input file
    if len(sys.argv) == 0 or not args.in_file:
        parser.print_help()
        exit(1)
    #If no output file name is given, use the input file as a default, converted to .root format
    out_f_name = args.out_name
    if not args.out_name:
        out_f_name = args.in_file.split('.lhe')[0] + '.root'
    #Search for event tags in the file
    numEvents = 0
    inputFile = open(args.in_file,'rt')
    isEvent = False
    for line in inputFile:
        if (line.find("<event>") != -1): #String.find() returns the index at which the argument is found, or -1 if not found
            isEvent = True
            numEvents += 1
            getMetaInfo(line.next())
        if (line.find("</event>") != -1): isEvent = False
        if isEvent:
            eventInfo = line.strip().split(' ')
            

if __name__=="__main__":
    main()
