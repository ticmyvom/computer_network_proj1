# Learned from https://www.askpython.com/python/examples/trie-data-structure

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
    
    # Not used for longest prefix match.
    # -----------------------------------DFS--------------------------------
    # while calling dfs, we need to pass a node and the prefix searched so far. 
    # Whenever the serach reaches a node with is_end=True, it appends the word 
    # to the output list. Otherwise, it keeps on searching among the children
    # ----------------------------------------------------------------------
    def dfs(self, node, pre):
        if node.is_end:
            self.output.append((pre + node.char))
        
        for child in node.children.values(): # values in a dictionary
            self.dfs(child, pre + node.char)
    
    # --------------------------------Search--------------------------------
    # search the tree, given a pattern, and output the longest prefix match
    # ----------------------------------------------------------------------
    def search(self, x):
        node = self.root
        self.output = ""

        for char in x:
            if char in node.children:
                self.output += char
                node = node.children[char]

            # prevent returning "" even tho we have a longest prefix matched.
            elif node.is_end == True:
                hasHope = True
            else:
                # x doesn't exist 
                return ""
        return self.output

# TEST
tr = Trie()
tr.insert("000011000000000101100000")
tr.insert("000011000110100001101101")
tr.insert("000011000110100100001100")
tr.insert("0000110001101001101010")
tr.insert("0000110001101001010001011001")
tr.insert("000011000111110110001110000100")
tr.insert("0000110010010000100011")
tr.insert("000011001001000010010000")
tr.insert("000011001001000010010001")


print("Words that begin with '12.105.69.152':  ", tr.search("00001100011010010100010110011000"))
print("Words that begin with '12.125.142.19':  ", tr.search("00001100011111011000111000010011"))



 


