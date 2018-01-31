# fqscan
Scans a directory of (optionally paired) FASTQ files for the prevalence of particular targets

## Installation

You will need `bwa` and `samtools`, or `vsearch` and `seqtk` installed to use.

```shell
git clone https://github.com/eclarke/fqscan
pip install fqscan
```

## Usage

Let's assume you have directory full of demultiplexed FASTQ files in `data_files` and 
a FASTA file of sequences you want to scan the FASTQ files for in `targets.fasta`. 

### Using BWA

First build an bwa index for it using `bwa index targets.fasta`, then run:

```shell
fqscan targets.fasta data_files
```

### Using vsearch

No indexing is required. Simply run:

```shell
fqscan --use_vsearch targets.fasta data_files
```

### Paired samples

The default behavior is to consider each FASTQ separately. If you have read pairs, you can use the `--pair` option 
to consider the pair together when mapping. If you use `vsearch`, this will merge the reads before searching and discard any that don't pair.

### Output

The program will output the number of reads that matched the target sequences in each file or read pair:

```shell
> fqscan targets.fasta data_files
sample1_R1.fastq sample1_R2.fastq 1245
sample2_R1.fastq sample2_R2.fastq 192
```
