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
* Particle identity from the Particle Data Group (pdg.lbl.gov/2007/reviews/montecarlopp.pdf)
* Particle status
* Mother particles
* Color(s)
* 4-Momentum and mass with the four-vector given as `[Px,Py,Pz,E]`
* Proper lifetime
* Spin

Note that not all of these values will contain information from the event generator.

## Output File Format
The output file will be a standard .root file, containing one tree named `mytree`. Each of the above data are stored as individual branches inside the tree.
Branch names and data types are:

 Branch Name | Data Type
 :---- | :----:
 numParticles | `int`
 eventWeight | `float`
 eventScale | `float`
 alphaEM | `float`
 alphaS | `float`
 pdgID | `std::vector<int>`
 pdgStatus | `std::vector<int>`
 mother1 | `std::vector<int>`
 mother2 | `std::vector<int>`
 color1 | `std::vector<int>`
 color2 | `std::vector<int>`
 px | `std::vector<float>`
 py | `std::vector<float>`
 pz | `std::vector<float>`
 E | `std::vector<float>`
 Mass | `std::vector<float>`
 Tau | `std::vector<float>`
 Spin | `std::vector<float>`

Any single vector index value corresponds to one particle in the event, so that you may iterate over all data vectors at the same time in order to collect relevant particle data. That is, for any index `n`, the values `pdgID[n]` and `px[n]` will give information for the same particle.

**CAUTION!** Using the same output file location more than once will overwrite the existing file. Consider this your only warning!

**Requires ROOT library!**

## Example Use
Command line execution:

```python ~/Path/to/LHEConverter.py -i ~/Path/to/generated/events.lhe -o output_file_name.root```

if no output file name is given, the default will be `<events>.root`, where `<events>` is the name of the input file.
