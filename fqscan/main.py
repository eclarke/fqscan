import argparse
import re
import itertools
import subprocess
from pathlib import Path

import pysam
from . import sam as samfilter

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "index", help="BWA index stem of query sequences")

    parser.add_argument(
        "fastqs", help="Directory of FASTQ files",
        type=Path)

    parser.add_argument(
        "--pct_id", help="Minimum percent identity",
        type=float, default=0.9)
    parser.add_argument(
        "--frac", help="Minimum fraction of read aligned",
        type=float, default=0.9)
    parser.add_argument(
        "--pair", help='FASTQ files are paired', action='store_true')
    
    binaries = parser.add_argument_group('paths to binaries')
    
    binaries.add_argument(
        "--bwa", help="Path to bwa binary, if not on path",
        default='bwa')
    binaries.add_argument(
        "--samtools", help="Path to samtools binary, if not on path",
        default='samtools')

    args = parser.parse_args()

    # -- Validate arguments
    
    queries = [t for t in itertools.chain(
        args.fastqs.glob("*.fastq.gz"),
        args.fastqs.glob("*.fastq"))]

        
    command = (
        "{bwa} mem {index} {{query}} | "
        "{samtools} view -hF260 | "
        "bamfilter --pct_id {pct_id} --frac {frac}").format(
            bwa = args.bwa, samtools = args.samtools,
            index = args.index, pct_id=args.pct_id, frac=args.frac)
    
    if args.pair:
        samples = set(re.sub('_R[12].fastq(.gz)?', '', str(query)) for query in queries)
        print(samples)
        
        for sample in samples:
            query = " ".join([str(query) for query in queries if sample in str(query)])
            counts = int(subprocess.check_output(command.format(query=query), shell=True).strip())
            print("{}\t{}".format(str(query), counts))
    else:
        for query in queries:
            counts = int(subprocess.check_output(command.format(query=query), shell=True).strip())
            print("{}\t{}".format(str(query), counts))

def filter():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pct_id", help="Minimum percent identity",
        type=float, default=0.8)
    parser.add_argument(
        "--frac", help="Minimum fraction of read aligned",
        type=float, default=1)

    args = parser.parse_args()
    sam = pysam.AlignmentFile('-', 'r')

    print(sum(1 for read in samfilter.get_mapped_reads(sam, args.pct_id, args.frac)))
