import argparse
import re
import sys
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
        "--threads", "-t", help="Number of threads to use",
        type=int, default=1)
    parser.add_argument(
        "--pair", help='FASTQ files are paired', action='store_true')
    parser.add_argument(
        '--use_vsearch', action='store_true',
        help='Use vsearch instead of bwa (requires vsearch and seqtk)')
    
    binaries = parser.add_argument_group('paths to binaries')
    
    binaries.add_argument(
        "--bwa", help="Path to bwa binary", default='bwa')
    binaries.add_argument(
        "--samtools", help="Path to samtools binary", default='samtools')
    binaries.add_argument(
        "--seqtk", help="Path to seqtk binary", default='seqtk')
    binaries.add_argument(
        "--vsearch", help="Path to vsearch binary", default='vsearch')

    args = parser.parse_args()

    # -- Validate arguments
    
    queries = [t for t in itertools.chain(
        args.fastqs.glob("*.fastq.gz"),
        args.fastqs.glob("*.fastq"))]

        
    bwa_command = (
        "{bwa} mem -t {threads} {index} {{query}} | "
        "{samtools} view -hF260 | "
        "bamfilter --pct_id {pct_id} --frac {frac}").format(
            bwa = args.bwa, threads = args.threads, index = args.index,
            samtools = args.samtools, pct_id=args.pct_id, frac=args.frac)

    vsearch_unpaired_cmd = (
        "{seqtk} seq -A {{query}} | {vsearch} --usearch_global - "
        "--db {index} --blast6out - --id {pct_id} | wc -l").format(
            seqtk = args.seqtk, vsearch = args.vsearch, index= args.index,
            pct_id = args.pct_id)

    vsearch_paired_cmd = (
        "{vsearch} --fastq_mergepairs {{query}}"
        "--fastaout - | {vsearch} --usearch_global - --db {index} "
        "--blast6out - --id {pct_id} | wc -l").format(
            vsearch = args.vsearch, index= args.index, pct_id = args.pct_id)

    vsearch_cmd = vsearch_paired_cmd if args.pair else vsearch_unpaired_cmd
    
    command = bwa_command if not args.use_vsearch else vsearch_cmd
    
    if args.pair:
        samples = set(re.sub('_R[12].fastq(.gz)?', '', str(query)) for query in queries)
        print(samples)
        query_str = "{} --reverse {} " if args.use_vsearch else "{} {}"
        for sample in samples:
            query = query_str.format(*(str(query) for query in queries if sample in str(query)))
            cmd = command.format(query=query)
            sys.stderr.write(cmd+"\n")
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
