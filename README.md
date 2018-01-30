# fqscan
Scans a directory of (optionally paired) FASTQ files for the prevalence of particular targets

## Installation

You will need `bwa` and `samtools` installed to use.

```shell
git clone https://github.com/eclarke/fqscan
pip install fqscan
```

## Usage

Let's assume you have directory full of demultiplexed FASTQ files in `data_files` and 
a FASTA file of sequences you want to scan the FASTQ files for in `targets.fasta`. 

First build an bwa index for it using `bwa index targets.fasta`, then run:

```shell
fqscan targets.fasta data_files
```

The default behavior is to consider each FASTQ separately. If you have read pairs, you can use the `--pair` option 
to consider the pair together when mapping.
