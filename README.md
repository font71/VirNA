# VirNA

 VirNA (Viral Network Analyzer) is a tool developed to provide an instrument able to reconstruct patterns of contagions and spread of a virus in a particular region of interest helping to individuate possible routes of entrance or exit followed by the pathogen. The tool can analyze thousands of genomic sequences starting from a multiple alignment in fasta format and as output it produces a gml network file with date and location of sampling of every viral genome reported on each graph node.
 The multiple alignment header file must have the following format:
 \>Location/IDentifier/date

## Install

To be installed VirNA requiree python 3 (<https://www.python.org/>) and the installation of the following python packages:

pip3 install numpy  
pip3 install pandas  
pip3 install networkx  
pip3 install biopython  
pip3 install cython  
pip3 install python-igraph  

git clone <https://github.com/font71/VirNA>
cd VirNA/libmat

python3 setup.py build_ext --inplace

To test that the tool is working properly do the following:
cd ..
./minspan.py -m 1000.fasta

Two files should be written in the examples directory: msn.gml and variants. The first one contains the Minimum Spanning Network produced by the tool which can be visualized with specific network visualizers such as Cytoscape (<https://cytoscape.org/>). The second one contains all the mutations individuated in the analyzed genome sequences.

>A docker image is also available on Docker Hub (https://hub.docker.com/r/biocompapp/virna). To run the containar cd into the directory with multiple alignment in fasta format and execute the following command:
docker run --rm -v "$PWD:/data" -u \`id -u\`:\`id -g\` biocompapp/virna minspan.py -m /data/\<fasta file\>

## Usage

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
-l, --local FILE  
&nbsp;&nbsp;&nbsp;&nbsp;File containing sequence IDs to consider for entry/exit analisys  
-h, --help  
&nbsp;&nbsp;&nbsp;&nbsp;Print this help  

The **format.py** script is provided as an example to convert some multiple alignment file format in fasta required by minspan.py. This script accepts as input multiple alignment files in the most common formats and transforms them in fasta required by VirNA:

-i, --input FILE  
&nbsp;&nbsp;&nbsp;&nbsp;The multiple alignment file  
-o, --output FILE  
&nbsp;&nbsp;&nbsp;&nbsp;The output file in json format  
-f, --inputformat [clustal | maf | nexus | stockholm | phylip-relaxed]  
&nbsp;&nbsp;&nbsp;&nbsp;The format of input file  
-h, --help  
&nbsp;&nbsp;&nbsp;&nbsp;Print this help  

### Algorithm description

The construction of the minimum spanning network is based on (Bandelt et al., 1999). For each multiple alignment, provided as input, a Hamming distance matrix is built and used as input for the reconstruction of a minimum spanning network, where nodes represent the unique sequences and the links minimize the total distance (measured by the number of mutations between connected sequences) spanned by the network. The outcome is a path that minimizes the number of mutations required to reproduce the observed data. To avoid the connection between two sequences that present homoplasy events two nodes are connected only if the mutations of the first one are also contained in the second one.
![Algorithm description](/img/fig.png)

In the figure is represented an exemplicative viral network where nodes labeled with A: includes only genomes belonging to the area under investigation, while nodes labeled with E: includes only genomes sampled outside the considered area. Subscript indicate the mutations carried by the haplotype V. Edge connecting A/E {V1, V2, V3} central node and E {V1, V2, V4, V5} is pruned because E does not contain haplotypes coming from geographical area A.

### Performance

Some trivial performance test was performed on a laptop equipped with 11th Gen Intel(R) Core(TM) i7-11850H @ 2.50GHz and 32 GB of RAM. VirNA was compared with other two tools, PopArt (<http://popart.otago.ac.nz/>) and Pegas (<http://ape-package.ird.fr/pegas.html>) considering only the execution times. The results are reported in the following table (the time is expressed in min:sec):

|Sequence number |  PopArt  |  Pegas  |  VirNA  |
| ---------------| -------- | ------- | ------- |
|1000            | 22:37    | 4:34    | 1:05    |
|2000            | 49:36    | 89:36   | 4:20    |
