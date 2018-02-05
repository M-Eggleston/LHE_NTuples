#!/usr/bin/env python3
#file LHE_NTuples.py

import sys,argparse
from ROOT import std,TTree,TFile
from array import array

parser = argparse.ArgumentParser(description="Convert LHE files into ROOT NTuples.")
parser.add_argument('-i','--input-file',help='name of LHE file to convert',dest='in_file')
parser.add_argument('-o','--output-file',help='name of .root file in which event data will be stored',dest='out_name')

#Initialize event meta variables
num_particles = 0
event_weight = 0.0
event_scale = 0.0
alpha_em = 0.0
alpha_s = 0.0
#All branch variables for the ttree will have m_ attached as a prefix

def getMetaInfo(line):
    global num_particles
    global event_weight
    global event_scale
    global alpha_em
    global alpha_s

    num_particles = line[0]
    data = []
    #Iterate over the line and skip over empty characters that will show up if multiple spaces exist between data in the LHE file
    for x in range(0,len(line)):
        if line[x] != '':
            data.append(line[x])
    #Check that the list has the right number of data points, else the wrong line was parsed
    if len(data) == 6:
        #One more variable exists between the number of particles and event weight, not sure what it is, omitting from ntuple
        event_weight = data[2]
        event_scale = data[3]
        alpha_em = data[4]
        alpha_s = data[5]
    else:
        print '{} data points were found, when 6 were expected! Skipping to next event.'.format(len(data))
    #TODO: actually force the parser to skip to next event

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

    global num_particles
    global event_weight
    global event_scale
    global alpha_em
    global alpha_s

    #---------------------------------------------------------
    # Set up arrays for holding event info to be written to branches
    #---------------------------------------------------------
    m_num_particles = array('i',[0])
    m_event_weight = array('f',[0.0])
    m_event_scale = array('f',[0.0])
    m_alpha_em = array('f',[0.0])
    m_alpha_s = array('f',[0.0])

    m_pdgid = array('i',[])
    m_status = array('i',[])
    m_mother1 = array('i',[])
    m_mother2 = array('i',[])
    m_color1 = array('i',[])
    m_color2 = array('i',[])
    m_px = array('f',[])
    m_py = array('f',[])
    m_pz = array('f',[])
    m_e = array('f',[])
    m_m = array('f',[])
    m_tau = array('f',[])
    m_spin = array('f',[])

    #---------------------------------------------------------
    # Set up TTree and branches for storing info
    #---------------------------------------------------------
    out_file = TFile(out_f_name,'recreate')
    my_tree = TTree('mytree','tree of generated events')

    my_tree.Branch('numParticles',m_num_particles,'numParticles/I')
    my_tree.Branch('eventWeight',m_event_weight,'eventWeight/F')
    my_tree.Branch('eventScale',m_event_scale,'eventScale/F')
    my_tree.Branch('alphaEM',m_alpha_em,'alphaEM/F')
    my_tree.Branch('alphaS',m_alpha_s,'alphaS/F')
    my_tree.Branch('pdgID',m_pdgid,'pdgID/I')
    my_tree.Branch('mother1',m_mother1,'mother1/I')
    my_tree.Branch('mother2',m_mother2,'mother2/I')
    my_tree.Branch('color1',m_color1,'color1/I')
    my_tree.Branch('color2',m_color2,'color2/I')
    my_tree.Branch('px',m_px,'px/F')
    my_tree.Branch('py',m_py,'py/F')
    my_tree.Branch('pz',m_pz,'pz/F')
    my_tree.Branch('E',m_e,'E/F')
    my_tree.Branch('Mass',m_m,'Mass/F')
    my_tree.Branch('Tau',m_tau,'Tau/F')
    my_tree.Branch('Spin',m_spin,'Spin/F')

    #----------------------------------------------------------
    # Begin parsing for info
    #----------------------------------------------------------

    #Search for event tags in the file
    num_events = 0
    input_file = open(args.in_file,'rt')
    is_event = False
    is_meta = False
    for line in input_file:
        if (line.find("<event>") != -1): #String.find() returns the index at which the argument is found, or -1 if not found
            is_event = True
            is_meta = True
            num_events += 1
            continue
            #getMetaInfo(line.next().strip().split(' '))
        if (line.find("</event>") != -1):
            is_event = False
            is_meta = False #Just in case this never got flipped back somehow
            my_tree.Fill() #Should fill the tree at the end of each event structure!
        if is_event and is_meta:
            getMetaInfo(line.strip().split(' '))
            m_num_particles[0] = num_particles
            m_event_weight[0] = event_weight
            m_event_scale[0] = event_scale
            m_alpha_em[0] = alpha_em
            m_alpha_s[0] = alpha_s
            is_meta = False
        if is_event and not is_meta:
            eventInfo = line.strip().split(' ')
            data = []
            for n in range(0,len(eventInfo)):
                if eventInfo[n] != '':
                    data.append(eventInfo[n])
            if len(data) != 13: print('Mismatched number of data elements!')
            else:
                m_pdgid.append(data[0])
                m_status.append(data[1])
                m_mother1.append(data[2])
                m_mother2.append(data[3])
                m_color1.append(data[4])
                m_color2.append(data[5])
                m_px.append(data[6])
                m_py.append(data[7])
                m_pz.append(data[8])
                m_e.append(data[9])
                m_m.append(data[10])
                m_tau.append(data[11])
                m_spin.append(data[12])

    input_file.close()
    out_file.Write()
    out_file.Close()

if __name__=="__main__":
    main()
