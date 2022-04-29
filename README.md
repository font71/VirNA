# VirNA

 VirNA (Viral Network Analyzer) is a tool developed to provide an instrument able to reconstruct patterns of contagions and spread of a virus in a particular region of interest helping to individuate possible routes of entrance or exit followed by the pathogen. The tool can analyze thousands of genomic sequences starting from a multiple alignment in fasta format and as output it produces a gml network file with date and location of sampling of every viral genome reported on each graph node.
 The multiple alignment header file must have the following format:
 \>Location/IDentifier/date

### Install

The following python packages are required by the tool:  
pip3 install numpy  
pip3 install pandas  
pip3 install networkx  
pip3 install biopython  
pip3 install cython  
pip3 install python-igraph  

cd libmat

python3 setup.py build_ext --inplace

>A docker image is also available on Docker Hub. To run the containar cd into the directory with multiple alignment in fasta format and execute the following command:
docker run --rm -v "$PWD:/data" -u \`id -u\`:\`id -g\` biocompapp/virna minspan.py -m /data/\<fasta file\>

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

### Performance

Some trivial performance test was performed on a laptop equipped with 11th Gen Intel(R) Core(TM) i7-11850H @ 2.50GHz and 32 GB of RAM. VirNA was compared with other two tools, PopArt (http://popart.otago.ac.nz/) and Pegas (http://ape-package.ird.fr/pegas.html) considering only the execution times. The results are reported in thw following table (the time is expressed in min:sec):

|Sequence number |  PopArt  |  Pegas  |  VirNA  |
| ---------------| -------- | ------- | ------- |
|1000            | 22:37    | 4:34    | 1:05    |
|2000            | 49:36    | 89:36   | 4:20    |