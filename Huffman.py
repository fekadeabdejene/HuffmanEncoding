from collections import Counter
import heapq


class Huffman:

    def __init__(self, data):
        if data is None or len(data) == 0:
            raise Exception("Invalid data.")
        self.data = data
        self.dictionary = dict()

    #   Function: encode_huffman
    #   Arguments: [None]
    #   Description:
    #       Creates the encodes data from the generated huffman codes.
    #   Returns:
    #       Returns the compressed data.
    def encode_huffman(self):
        freqmap = self.__create_frequency()
        root = self.__huffman_tree(freqmap)
        self.__huffman_code(root)
        return self.__encode()

    #   Function: decode_huffman
    #   Arguments: encodedvalue (encoded huffman data)
    #   Description:
    #       Decodes the encoded huffman data.
    #   Returns:
    #       Original data of encoded huffman data.
    def decode_huffman(self, encodedvalue):
        if encodedvalue is None or len(encodedvalue) == 0:
            raise Exception("Invalid encoded value.")
        bitPattern = ''
        decodedvalue = ''
        reverseddictionary = self.get_reversed_dictionary()
        for bit in encodedvalue:
            bitPattern += bit
            if bitPattern in reverseddictionary:
                decodedvalue += reverseddictionary[bitPattern]
                bitPattern = ''
        return decodedvalue

    #   Function: get_compression_ratio
    #   Arguments: encodedvalue (encoded huffman data)
    #   Description:
    #       Since characters are used for bit representation the equation becomes
    #       len(compressed bits) / (len(original data) * 8). Assuming each character
    #       takes 8 bits.
    #   Returns:
    #       How much % the data is compressed.
    def get_compression_ratio(self, encodedValue):
        if encodedValue is None or len(encodedValue) == 0:
            raise Exception("Invalid argument \"encodedValue\".")
        if self.data is None or len(self.data) == 0:
            raise Exception("Invalid member \"data\".")
        return 1 - (len(encodedValue) / float((len(self.data) * 8)))

    #   Function: get_dictionary
    #   Arguments: [None]
    #   Description:
    #
    #   Returns:
    #       Returns dictionary K:V = frequency:bitpattern.
    def get_dictionary(self):
        return self.dictionary

    #   Function: set_dictionary
    #   Arguments: value
    #   Description:
    #       Sets the dictionary with a huffman code table.
    #   Returns:
    #       None
    def set_dictionary(self, value):
        self.dictionary = value

    #   Function: get_reversed_dictionary
    #   Arguments: [None]
    #   Description:
    #       Reversed dictionary used for decoding.
    #   Returns:
    #       return reverse dictionary K:V - > V:K = bitpattern:frequency.
    def get_reversed_dictionary(self):
        return {v: k for k, v in (self.get_dictionary().items())}

    #   Function: __create_frequency
    #   Arguments: [None]
    #   Description:
    #       Creates a list of tuples (value, frequency).
    #   Returns
    #       Tuple List (value, frequency).
    def __create_frequency(self):
        frequencylist = Counter(self.data).items()
        return [(v,k) for k, v in (frequencylist)]

    #   Function: __huffman_tree
    #   Arguments: frequency
    #   Description:
    #       Creates a max heap huffman tree.
    #   Returns
    #       Pointer to the root node.
    def __huffman_tree(self, frequency):
        if frequency is None or len(frequency) == 0:
            raise Exception("Invalid frequency table.")

        heapq.heapify(frequency)

        # Pops the two smallest items off the heap
        # Adds these two items to the next smallest item
        # Continues until there is effectively one parent node in the heap
        while len(frequency) > 1:
            leftnode = heapq.heappop(frequency)
            rightnode = heapq.heappop(frequency)
            parentnode = ((leftnode[0] + rightnode[0]), leftnode, rightnode)  #Maintains a maxheap
            heapq.heappush(frequency, parentnode)

        return frequency[0]

    #   Function: __huffman_code
    #   Arguments: tree (root node to tree)
    #   Description:
    #       Creates the huffman code table, prefixless bit patterns and stored in a dictionary. Used for
    #          encoding and decoding.
    #   Returns
    #       None
    def __huffman_code(self, tree):
        stack = []
        # special case if all the data is the same
        if len(tree) == 2:
            prefix = '1'
        else:
            prefix = ''
        stack.append((tree, prefix))  # (node_ptr, prefix)
        while len(stack) > 0:
            ptr = stack.pop()
            if len(ptr[0]) == 2:
                self.dictionary[ptr[0][1]] = ptr[1]
            else:
                stack.append((ptr[0][1], ptr[1]+'0'))
                stack.append((ptr[0][2], ptr[1]+'1'))

    #   Function: __encode
    #   Arguments: [None]
    #   Description:
    #       Encodes data based on huffman code table.
    #   Returns
    #       str (encoded data)
    def __encode(self):
        if len(self.dictionary) == 0:
            raise Exception("Huffman encoding table has not been created.")
        value = ''
        for c in self.data:
            if c in self.dictionary:
                value += self.dictionary[c]
            else:
                raise Exception("Invalid huffman key.")
        return value

test_data_1 = "a"
test_data_2 = "abcdefghijklmnopqrstuvwxyz"
test_data_3 = "aaaaaaaaaaaaaaaaaaaaaaaaaa"
test_data_4 = "asdfjbdsjkbfdifbeibfosdibfjkeboiuwebfisdbifbiobwieufbew"
test_data_5 = "test_data.txt"
# http://www.strangehorizons.com/2000/20000911/Fiction_Estranged_Rogers.shtml
# test_data_5 reference


def test_encoding_decoded(data):
    originaldata = data
    huf = Huffman(originaldata)
    encoded_data = huf.encode_huffman()
    reencoded_data = huf.decode_huffman(encoded_data)

    print "************** Test Encoding **************"
    print "Original data: ", originaldata
    print "Encoded data: ", encoded_data
    print "Re-encoded data: ", huf.decode_huffman(encoded_data)
    print "Compare: (originaldata == re-encoded_data) = ",reencoded_data == originaldata
    print "Compression Ratio: ", huf.get_compression_ratio(encoded_data)

if __name__ == "__main__":
    test_encoding_decoded(test_data_1)
    test_encoding_decoded(test_data_2)
    test_encoding_decoded(test_data_3)
    test_encoding_decoded(test_data_4)
    test_data_file = open(test_data_5)
    test_encoding_decoded(test_data_file.read())

