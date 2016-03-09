#! /usr/bin/python
"""
Name: Weka's tree parser v1.0
Version: 1.0

Description

This script prase weka's tree output and convert into graphviz graph.
Use:
    treetograph.py [-h] [-i <inputfile>] [-d] -f <format (svg, pdf, png)>
    Arguments:
        -h : help
        -i, --ifile= : Input file.
        -d : boolean to debug tree conversion.
        -f, --format= : Ouput format is REQUIRED could be svg -vector file-, pdf -portable document file-, or png -image-.

    It creates an ouput file of defined format with the tree representation.
    If there is no input file, program would ask user for it at standar input.
"""
import re
from graphviz import Digraph
import sys
import os
import getopt
from sets import Set

debug = False

class Tree:
    """
    docstring for Tree
    """
    def __init__(self, text):
        self.root = Node(text)

    def __str__(self):
        return str(self.root)

    def graph(self, format='pdf'):
        """Graph representation of tree

        :param dot_object:
        :type dot_object: Digraph
        :return:
        """
        digraph = Digraph(format=format)
        self.root._graph(digraph)
        return digraph

class Node:
    """
    docstring for Node
    """
    regnode = r'^(?P<atr>[\w.]+).(?P<value>\W*[\w.]+)(\:\W*(?P<class>.*))?\n?(?P<branch>(\|.+(.*)\n?)*)'
    attributes = Set()

    def __init__(self, text, class_type=False):
        self.class_type = class_type
        if class_type:
            self.attribute = None; self.branches = []
            self.class_value = text
        else :
            if debug: print '>-----------'
            self.attribute, self.branches = self._texttotree(text)
            Node.attributes.add(self.attribute)
            self.class_value = None
            if debug: print '<------------'

    def _texttotree(self,text):
        if debug: print '================================','\n',text
        renode = re.compile(self.regnode, re.MULTILINE)
        tbranches = [m for m in re.finditer(renode, text)]

        ttbranches = re.findall(renode, text)

        if debug: print ttbranches

        # assert reduce(lambda x,y: x.group('atr')==y.group('atr'), tbranches) # All branches has same attribute

        attribute = tbranches[0].group('atr')
        if debug: print len(tbranches)
        branches = []
        if debug: print attribute,
        for branch in tbranches:
            if branch.group('class'):
                class_value = branch.group('class')
                node = Node(class_value,class_type=True)
            else :
                if debug: print ' %s branch' % (branch.group('value'))
                reg = re.compile(r'^\|\s*',re.MULTILINE)
                new_branches = re.sub(reg, '', branch.group('branch'))
                node = Node(new_branches)
            branches.append(Branch(branch.group('value'), self, node))
        return attribute, branches

    # TODO: print function
    def __str__(self):
        """Return string representation

        :return: string representation
        """
        if class_type:
            return "Class: %s" % self.class_value
        string = "Node: %s" % self.attribute
        if self.class_value: string += "%s: %s -Class-" % (self.class_value[1], self.class_value[0])
        if len(self.branches): string +="\nBranches:\n" + "\n".join(map(lambda x: "|  "+str(x), self.branches))
        return string

    def _graph(self, dot_object):
        """Graph representation of tree

        :param dot_object:
        :type dot_object: Digraph
        :return:
        """
        if self.class_type:
            label = self.class_value
            dot_object.node(str(hash(self)),label=label,shape='square')
        else:
            label = self.attribute
            dot_object.node(str(hash(self)),label=label)
            for b in self.branches:
                b._graph(dot_object)



class Branch:
    """
    docstring for Branch
    """
    def __init__(self, condition, pnode, cnode):
        """Create instance

        :param condition: condicion de la rama
        :param pnode: nodo padre
        :param cnode: nodo hijo
        """
        self.condidition = condition
        self.pnode = pnode
        self.cnode = cnode

    def __str__(self):
        return " %s \n%s" % (self.condidition, str(self.cnode))

    def _graph(self, dot_object):
        """Graph representation of tree

        :param dot_object:
        :type dot_object: Digraph
        :return:
        """
        self.cnode._graph(dot_object)
        dot_object.edge(str(hash(self.pnode)),str(hash(self.cnode)),label=self.condidition)

def main(argv):
    global debug
    inputfile = ''
    oformat = ''
    print_attributes = False
    try:
        opts, args = getopt.getopt(argv,"hi:f:da",["help","ifile=","format=","debug","print-attributes"])
    except getopt.GetoptError:
        print """treetograph.py [-h] [-i <inputfile>] [-d] -f <format (svg, pdf, png)>
        Arguments:
        -h : help
        -i, --ifile= : Input file.
        -d : boolean to debug tree conversion.
        -f, --format= : Ouput format is REQUIRED could be svg -vector file-, pdf -portable document file-, or png -image-.
        -a, --print-attributes : Print tree's set of attributes
        """
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print """treetograph.py [-h] [-i <inputfile>] [-d] -f <format (svg, pdf, png)>
    Arguments:
        -h : help
        --i, --ifile= : Input file.
        -d : boolean to debug tree conversion.
        --f, --format= : Ouput format is REQUIRED could be svg -vector file-, pdf -portable document file-, or png -image-.
"""
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-d"):
            debug = True
        elif opt in ("-f","--format"):
            oformat = arg
        elif opt in ("-a","--print-attributes"):
            print_attributes = True
    if oformat == '':
        print """treetograph.py [-h] [-i <inputfile>] [-d] -f <format (svg, pdf, png)>
Arguments:
    -h : help
    --i, --ifile= : Input file.
    -d : boolean to debug tree conversion.
    --f, --format= : Ouput format is REQUIRED could be svg -vector file-, pdf -portable document file-, or png -image-.
"""
        sys.exit()
    if inputfile == '':
        text = raw_input("Copy weka's tree representation:\n")
    else:
        text = open(inputfile, 'r').read()
    tree = Tree(text)
    dot = tree.graph(oformat)
    if debug: print dot.source
    dot.render('output')
    if print_attributes: print '\n'.join(Node.attributes)

if __name__ == "__main__":
   main(sys.argv[1:])
