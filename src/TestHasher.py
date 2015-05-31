from BloomFilter import Hasher
import unittest



class TestHasher(unittest.TestCase):

    def setUp( self ):
        self.myHasher = Hasher()

    def testGetBitArraySize(self):
        self.myHasher.NUM_BYTES_ENCODE = 2
        self.assertEquals( 65536, self.myHasher.getBitArraySize(), 'wrong size returned for 2 bytes' )

        self.myHasher.NUM_BYTES_ENCODE = 3
        self.assertEquals( 16777216, self.myHasher.getBitArraySize(), 'wrong size returned for 3 bytes' )

        self.myHasher.NUM_BYTES_ENCODE = 4
        self.assertEquals( 4294967296, self.myHasher.getBitArraySize(), 'wrong size returned for 4 bytes' )

if __name__ == '__main__':
    unittest.main()
