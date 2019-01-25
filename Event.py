## file Event.py
# Defines a class to store event information in. Event.MetaEvent() holds
# information for the meta information, while Event.ScatterEvent() details
# particle kinemtics

from array import array

class MetaEvent:

    def __init__(self,num_parts,evt_weight,evt_scale,alpha_em,alpha_s):   
        self.m_num_particles = num_parts
        self.m_event_weight = evt_weight
        self.m_event_scale = evt_scale
        self.m_alpha_em = alpha_em
        self.m_alpha_s = alpha_s

    # Use setValues() to update the instance member variables
    def setValues(self,n_p,e_w,e_s,a_em,a_s):
        self.m_num_particles = n_p
        self.m_event_weight = e_w
        self.m_event_scale = e_s
        self.m_alpha_em = a_em
        self.m_alpha_s = a_s

    #Don't forget we used data.pop(1) before passing to this method
    def setValues(self,val_list):
        self.m_num_particles = int(val_list[0])
        self.m_event_weight = val_list[1]
        self.m_event_scale = val_list[2]
        self.m_alpha_em = val_list[3]
        self.m_alpha_s = val_list[4]

    # returns a list of the instance member variables in the same order as when created
    def getValues(self):
        return [self.m_num_particles,self.m_event_weight,self.m_event_scale,self.m_alpha_em,self.m_alpha_s]

    #####################################################
    # Individual getter and setter methods for each member variable
    #####################################################
    def getNumParticles(self):
        return self.m_num_particles

    def setNumParticles(self,n_p):
        self.m_num_particles = n_p

    def getEventWeight(self):
        return self.m_event_weight

    def getEventScale(self):
        return self.m_event_scale

    def getAlphaEM(self):
        return self.m_alpha_em

    def getAlphaS(self):
        return self.m_alpha_s

    def setAlphaS(self,a_s):
        self.m_alpha_s = a_s


