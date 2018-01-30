# LHE_NTuples
Convert LHE event information into a ROOT NTuple for easy access and data plotting

Les Houches Event Files (**LHEF**) are a common output format from Monte Carlo event generators. A full simulation will take the LHEF and apply a parton shower, followed by hadronization and finally a simulation of the resulting particles interacting with a detector in order to generate the kinds of signals we expect to see at the LHC. When we are testing a new physics model however, it is useful to look at the kinds of partons and their properties that get generated in the final state of our hard scattering.

This software will parse the LHE file, extract the relevant particle information, and fill a ROOT style NTuple with the meta and kinematic information.

Event information includes the following values (as detailed in the original [paper](https://arxiv.org/pdf/hep-ph/0609017.pdf))
* Number of particles
* Event weight
* Event scale
* EM coupling &alpha;<sub>em</sub>
* Strong coupling &alpha;<sub>s</sub>
* Particle identity from the [Particle Data Group](pdg.lbl.gov/2007/reviews/montecarlopp.pdf)
* Particle status
* Mother particles
* Color(s)
* 4-Momentum and mass with the four-vector given as `[Px,Py,Pz,E]`
* Proper lifetime
* Spin
