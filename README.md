# treetograph
Python script Weka's tree parser

Name: Weka's tree parser v1.0
Version: 1.0

Description
----
This script prase weka's tree output and convert into graphviz graph.
Use:
```
    treetograph.py [-h] [-i <inputfile>] [-d] -f <format (svg, pdf, png)> -a
    Arguments:
        -h : help
        -i, --ifile= : Input file.
        -d : boolean to debug tree conversion.
        -f, --format= : Ouput format is REQUIRED could be svg -vector file-,
          pdf -portable document file-, or png -image-.
        -a, --print-attributes : Print tree's set of attributes
```
It creates an ouput file of defined format with the tree representation.
If there is no input file, program would ask user for it at standar input.
