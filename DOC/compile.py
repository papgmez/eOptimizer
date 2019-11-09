#!/usr/bin/python

import subprocess, sys

commands = [
    ['pdflatex', sys.argv[1] + '.tex'],
    ['bibtex', sys.argv[1] + '.aux'],
    ['pdflatex', sys.argv[1] + '.tex'],
    ['pdflatex', sys.argv[1] + '.tex'],
    ['makeglossaries', sys.argv[1]],
    ['pdflatex', sys.argv[1] + '.tex'],
    ['pdflatex', sys.argv[1] + '.tex']
]

for command in commands:
    subprocess.call(command)
