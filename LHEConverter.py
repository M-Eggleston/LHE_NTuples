#!/usr/bin/env python

## file LHEConverter.py
# Converts LHE files to a flat NTuple in a .root file
# Author Michael Eggleston

import sys, argparse
from ROOT import std,TTree,TFile
from array import array
import Event

parser = argparse.ArgumentParser(description="Convert LHE files into ROOT NTuples.")
parser.add_argument('-i','--input-file',help='name of LHE file to convert',dest='in_file')
parser.add_argument('-o','--output-file',help='name of .root file in which event data will be stored',dest='out_name')
parser.add_argument('-w','--weight',help='MadGraph allows for inclusion of weights with a given name. Set name of weight to access here',dest='weight_name')

#All branch variables for the ttree will have m_ attached as a prefix

def getMetaInfo(meta_evt, line):
    data = []
    #Iterate over the line and skip over empty characters that will show up if multiple spaces exist between data in the LHE file
    for x in range(0,len(line)):
        if line[x] != '':
            data.append(float(line[x]))
    #Check that the list has the right number of data points, else the wrong line was parsed
    if len(data) == 6:
        #One more variable exists between the number of particles and event weight, not sure what it is, omitting from ntuple
        data.pop(1)
        meta_evt.setValues(data)
    else:
        print ('{} data points were found, when 6 were expected! Skipping to next event.'.format(len(data)))
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

    include_weight = False
    m_weight_name = 'weight_'
    if not args.weight_name:
        print('No weight name specified, none will be included in the output')
    else:
        include_weight = True
        m_weight_name = m_weight_name + args.weight_name

    m_meta_event = Event.MetaEvent(0,0,0,0,0)

    #---------------------------------------------------------
    # Set up arrays for holding event info to be written to branches
    #---------------------------------------------------------
    m_num_particles = array('i',[0])
    m_event_weight = array('f',[0.0])
    m_event_scale = array('f',[0.0])
    m_alpha_em = array('f',[0.0])
    m_alpha_s = array('f',[0.0])

    m_weight = array('f',[0.0])

    m_pdgid = std.vector('int')()
    m_status = std.vector('int')()
    m_mother1 = std.vector('int')()
    m_mother2 = std.vector('int')()
    m_color1 = std.vector('int')()
    m_color2 = std.vector('int')()
    m_px = std.vector('float')()
    m_py = std.vector('float')()
    m_pz = std.vector('float')()
    m_e = std.vector('float')()
    m_m = std.vector('float')()
    m_tau = std.vector('float')()
    m_spin = std.vector('float')()

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
    if include_weight:
        my_tree.Branch(m_weight_name,m_weight,'m_weight_name'+'/F')

    my_tree.Branch('pdgID',m_pdgid)
    my_tree.Branch('pdgStatus',m_status)
    my_tree.Branch('mother1',m_mother1)
    my_tree.Branch('mother2',m_mother2)
    my_tree.Branch('color1',m_color1)
    my_tree.Branch('color2',m_color2)
    my_tree.Branch('px',m_px)
    my_tree.Branch('py',m_py)
    my_tree.Branch('pz',m_pz)
    my_tree.Branch('E',m_e)
    my_tree.Branch('Mass',m_m)
    my_tree.Branch('Tau',m_tau)
    my_tree.Branch('Spin',m_spin)

    #----------------------------------------------------------
    # Begin parsing for info
    #----------------------------------------------------------

    #Search for event tags in the file
    with open(args.in_file,'rt') as input_file:
        num_events = 0
        for line in input_file:
            if (line.find("<event>") != -1): num_events += 1
        print('There are {} events in this file.'.format(num_events))
        if num_events < 100: print("Because of small number of events, errors will be printed to terminal")
        input_file.seek(0) #Reset the file iterator to beginning of file
        #TODO: replace this restart to start at the first event in the next iteration
        l_num_events = 0
        l_particle_num = 0
        is_event = False
        is_meta = False
        is_sum_weight = False
        num_skipped_particles = 0
        print("Begin looping over events!")
        for line in input_file:
            # If the file contains a reweighting tag, the sum of weights will be included before any events, in the file metadata
            # So find all sum of weights and add to an output histogram 
            #TODO: find all sum of weights and write to a histogram in output file
            # for now I'll just look this value up manually
            #if (line.find("<initrwgt>") != -1):
            #    is_sum_weight = True
            #    continue
            #if (line.find("</initrwgt>") != -1):
            #    is_sum_weight = False
            #    continue
            if (line.find("<event>") != -1): #String.find() returns the index at which the argument is found, or -1 if not found
                is_event = True
                is_meta = True
                is_sum_weight = False
                l_num_events += 1
                continue
            if (line.find("</event>") != -1):
                is_event = False
                is_meta = False #Just in case this never got flipped back somehow
                is_sum_weight = False
                my_tree.Fill() #Should fill the tree at the end of each event structure!
                #Clear vectors of event info
                m_pdgid.clear()
                m_status.clear()
                m_mother1.clear()
                m_mother2.clear()
                m_color1.clear()
                m_color2.clear()
                m_px.clear()
                m_py.clear()
                m_pz.clear()
                m_e.clear()
                m_m.clear()
                m_tau.clear()
                m_spin.clear()
                l_particle_num = 0
            # These weight tags are found inside the event structure, so because of the checks for unknown tags
            # skips lines with any tag bracket below, we can safely handle this case here, and still ignore other unknowns later
            if (line.find("<wgt id=") != -1):
                l_name = line.strip().split('\'')[1]
                if l_name == args.weight_name:
                    wgt = float(line.strip().split(' ')[2])
                    m_weight[0] = wgt
                continue
            if is_event and is_meta:
                getMetaInfo(m_meta_event,line.strip().split(' '))
                m_num_particles[0] = m_meta_event.getNumParticles()#num_particles
                m_event_weight[0] = m_meta_event.getEventWeight()#event_weight
                m_event_scale[0] = m_meta_event.getEventScale()#event_scale
                m_alpha_em[0] = m_meta_event.getAlphaEM()#alpha_em
                m_alpha_s[0] = m_meta_event.getAlphaS()#alpha_s
                is_meta = False
                continue
            elif is_event and not is_meta:
                if (line.find("<") != -1) or (line.find("#") != -1):
                    continue

                l_particle_num += 1
                eventInfo = line.strip().split(' ')
                data = []
                for n in range(0,len(eventInfo)):
                    if eventInfo[n] != '':
                        data.append(float(eventInfo[n]))
                if len(data) != 13:
                    num_skipped_particles += 1
                    if (num_events > 100) and (l_num_events%1000 == 0):
                        print('Event #{}, particle #{} has mismatched number of data elements! Printing Data:'.format(l_num_events,l_particle_num))
                    elif (num_events < 100):
                        print('Mismatched number of data elements! Printing data:\n')
                else:
                    m_pdgid.push_back(int(data[0]))
                    m_status.push_back(int(data[1]))
                    m_mother1.push_back(int(data[2]))
                    m_mother2.push_back(int(data[3]))
                    m_color1.push_back(int(data[4]))
                    m_color2.push_back(int(data[5]))
                    m_px.push_back(data[6])
                    m_py.push_back(data[7])
                    m_pz.push_back(data[8])
                    m_e.push_back(data[9])
                    m_m.push_back(data[10])
                    m_tau.push_back(data[11])
                    m_spin.push_back(data[12])
        print('{} particles were skipped for bad formatting.'.format(num_skipped_particles))

        out_file.Write()
        out_file.Close()
        print("Finished looping over events! All data written to {}.".format(out_f_name))

if __name__=="__main__":
    main()
