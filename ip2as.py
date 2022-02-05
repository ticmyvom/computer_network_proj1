# open file to read/write: https://www3.ntu.edu.sg/home/ehchua/programming/webprogramming/Python_FileText.html
# pythondjangorestapi dot com: 3 Ways to handle inputs Arguments in Python: https://www.tinyurl.com/2p93knw3
# Learned from https://www.askpython.com/python/examples/trie-data-structure

# Overall structure:
# a) Trie Data Structure
# b) Step 1: Process DB file
# c) Step 2: Process IP input file and perform look up

# -----------------------BEGIN TRIE Data Structure ----------------------------------------
class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        # also a variable used to look up the output to be printed with
        self.children = {}

class Trie(object):
    def __init__(self):
        # init an emty TrieNode
        self.root = TrieNode("")

    # --------------------------------Insert--------------------------------
    def insert(self, word):
        node = self.root
        
        for char in word:
            # if char exists in node's children, set current node to it.
            if char in node.children:
                node = node.children[char]

            # else make a new TrieNode for that char, update node's children and set current node to it.    
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        
        # after traversing the word, set .is_end to true for the last char
        node.is_end = True

    # --------------------------------Search--------------------------------
    # search the tree, given a pattern
    # output: a list of prefixes in ascending order.
    # ----------------------------------------------------------------------
    def search(self, x):
        node = self.root
        prefixFound = ""
        self.output = []

        for char in x:
            if char in node.children:
                prefixFound += char

                node = node.children[char]
                if node.is_end == True:
                    self.output.append(prefixFound)

            else: # x's longest matching prefix has been found
                break
        return self.output
# --------------------------END TRIE Data Structure-------------------------------------


import sys
inputDB = sys.argv[1]
inputIP = sys.argv[2]

# ------------------------ STEP 1 ------------------------ 
# For each line in DB, process and add it to the "tree" to perform lookup
# Also, add an entry to a dbDict[ionary] to perform lookup for ipDecSubnetAS later in step 2

dbTrie = Trie()         # to store prefixes and to lookup for a given IP
dbDict = {}             # lookup the answer given a prefix

with open(inputDB, 'r') as f:
    for line in f:
        line = line.rstrip()
        lineList = line.split(' ')

        ipDec = lineList[0]
        subnetPart = lineList[1]
        numAS = lineList[2]

        trieEntry = ""
        # Convert decimal IP to a binary string trieEntry
        for octet in ipDec.split('.'):
            # '08b' instructs the function to pad the 0s needed to make each binary 8-bit long
            trieEntry += format(int(octet), '08b')

        # Trim trieEntry based on the subnetPart before inserting it to the Trie Tree
        whatToTrim = 32 - int(subnetPart)
        if whatToTrim != 0:
            trieEntry = trieEntry[:-whatToTrim]
        dbTrie.insert(trieEntry)

        # Add an entry to a dbDict[ionary]
        ipDecSubnetAS = ipDec + "/" + subnetPart + " " + numAS
        dbDict[trieEntry] = ipDecSubnetAS
# File closed by itself upon exit of with-statement


# ------------------------ STEP 2 ------------------------
# For each entry in IPlist, perform lookup and print the result:
with open(inputIP, 'r') as f:
    for ipDec in f:
        ipDec = ipDec.rstrip()
        
        # Process each line in inputIP, convert each decimal IP `ipDec` to a binary string `ipBin`
        ipBin = ""
        for octet in ipDec.split('.'):
            ipBin += format(int(octet), '08b')

        prefixLookedUp = dbTrie.search(ipBin)
        # prefixLookedUp obtained is a list of prefixes in ascending order
        # => prefixLookedUp[-1] will yield the longest prefix matched
        prefixLookedUp = prefixLookedUp[-1]

        resultIPSubnetASdbDict = dbDict[prefixLookedUp]
        print(resultIPSubnetASdbDict + " " + ipDec)
# File closed by itself upon exit of with-statement








