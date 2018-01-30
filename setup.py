from setuptools import setup

setup(
    name='fqscan',
    version='0.1.0',
    description="Scan FASTQ files quickly for a given set of sequences.",
    url='https://github.com/eclarke/fqscan',
    packages=['fqscan'],
    requirements=['pysam'],
    entry_points={
        'console_scripts': [
            'fqscan=fqscan.main:main',
            'bamfilter=fqscan.main:filter'
        ]
    }
)

