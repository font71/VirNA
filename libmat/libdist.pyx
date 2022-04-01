# distutils: language=c++
from libc.stdio cimport *
import numpy as np

cdef extern from "stdio.h":
    #FILE * fopen ( const char * filename, const char * mode )
    FILE *fopen(const char *, const char *)
    #int fclose ( FILE * stream )
    int fclose(FILE *)
    #ssize_t getline(char **lineptr, size_t *n, FILE *stream);
    ssize_t getline(char **, size_t *, FILE *)

cdef set alphabet = {'A', 'C', 'G', 'T', '-'}
cdef dict trans = {'A': 1, 'C': 2, 'G': 3, 'T': 4, '-': 5}

def add(str refseq, str nuc, int thborder):
   seq = np.zeros(len(refseq), dtype=int)
   mutation = np.array([], dtype=str)
   for i in range(thborder, len(nuc) - thborder):
      c = nuc[i]
      refc = refseq[i]
      p = i - thborder

      if c in alphabet and refc in alphabet:
         if not c == refc:
            seq[p] = trans[c]
            mut = refc + str(i + 1) + c
            mutation = np.append(mutation, mut)
   return seq, mutation

def read_msa(str msafile, int thborder):
   cdef int n = 0
   cdef str refseq = ''
   cdef str gid
   cdef str gidpart
   cdef str nuc = ''
   cdef dict matrix = {}
   cdef dict mutations = {}
   cdef str mut

   fh = open(msafile, 'rb')

   while True:
      line = fh.readline()
      if not line:
         seq, mutation = add(refseq, nuc, thborder)
         matrix[gidpart] = seq
         mutations[gid] = mutation
         break
      
      l = line.decode('UTF-8')
      l = l.rstrip()

      if l[0] == '>' and n == 0:
         n = 1
      elif l[0] == '>' and n > 0:
         if n == 1:
            n = 2
         # seq = np.zeros(len(refseq), dtype=int)
         if nuc:

            # mutation = np.array([], dtype=str)
            # for i in range(thborder, len(nuc) - thborder):
            #    c = nuc[i]
            #    refc = refseq[i]
            #    p = i - thborder

            #    if c in alphabet and refc in alphabet:
            #       if not c == refc:
            #          seq[p] = trans[c]
            #          mut = refc + str(i + 1) + c
            #          mutation = np.append(mutation, mut)
            seq, mutation = add(refseq, nuc, thborder)
            matrix[gidpart] = seq
            mutations[gid] = mutation
         gid = l[1:]
         gidpart = l.split('/')[1]
         nuc = ''
      elif n == 1:
         refseq += l
      else:
         nuc += l
   
   fh.close()

   return matrix, mutations

def compare4(dict matrix):
   gids = np.array(list(matrix.keys()))
   d = gids.size

   array = np.array(list(matrix.values()), dtype=np.int16)
   mat = np.empty([d, d], dtype=np.int16)
   for i in range(d):
      m = abs(array[i:] - matrix[gids[i]])
      m[m > 1] = 1
      m = m.sum(axis=1)
      nan = np.empty(i)
      nan[:] = -1
      m = np.concatenate((nan, m))
      mat[i] = m
   return mat
