# VirNA
 VirNA (Viral Network Analyzer) is a tool developed to provide an instrument able to reconstruct patterns of contagions and spread of the virus in a particular region of interest helping to individuate possible routes of entrance or exit followed by the pathogen. The tool can analyze thousands of genomic sequences starting from a multiple alignment and as output produce a network file with date and location of sampling of every viral genome.

### Install
The following python packages are required:  
pip3 install numpy  
pip3 install pandas  
pip3 install biopython  
pip3 install cython  
pip3 install python-igraph  

cd libmat

python3 setup.py build_ext --inplace