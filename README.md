# VirNA
 VirNA (Viral Network Analyzer) is a tool developed to provide an instrument able to reconstruct patterns of contagions and spread of a virus in a particular region of interest helping to individuate possible routes of entrance or exit followed by the pathogen. The tool can analyze thousands of genomic sequences starting from a multiple alignment in fasta format and as output it produces a gml network file with date and location of sampling of every viral genome reported on each graph node.

### Install
The following python packages are required by the tool:  
pip3 install numpy  
pip3 install pandas  
pip3 install biopython  
pip3 install cython  
pip3 install python-igraph  

cd libmat

python3 setup.py build_ext --inplace

### Usage
**minspan.py** command line arguments:

-m, --msa FILE  
&nbsp;&nbsp;&nbsp;&nbsp;The multiple alignment file in fasta format (Mandatory)  
-p, --prefix STR  
&nbsp;&nbsp;&nbsp;&nbsp;The string to attach to every output files (default: "")  
-x, --matrix  
&nbsp;&nbsp;&nbsp;&nbsp;Dumps edit distance matrix  
-t, --borderth INT  
&nbsp;&nbsp;&nbsp;&nbsp;The multiple alignment will be trimmed at both ends using this value  (default value 90)  
-i, --maxiter INT  
&nbsp;&nbsp;&nbsp;&nbsp;Maximum number of iterations to perform during MSN building  
-h, --help  
&nbsp;&nbsp;&nbsp;&nbsp;Print this help  

The **format.py** script is provided as an example to convert some multiple alignment file format in fasta required by minspan.py:

-i, --input FILE  
&nbsp;&nbsp;&nbsp;&nbsp;The multiple alignment file  
-o, --output FILE  
&nbsp;&nbsp;&nbsp;&nbsp;The output file in json format  
-f, --inputformat [clustal | maf | nexus | stockholm | phylip-relaxed]  
&nbsp;&nbsp;&nbsp;&nbsp;The format of input file  
-h, --help  
&nbsp;&nbsp;&nbsp;&nbsp;Print this help  
