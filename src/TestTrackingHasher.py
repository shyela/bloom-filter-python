from BloomFilter import TrackingHasher, BloomFilter
import unittest



class TestTrackingHasher(unittest.TestCase):

    def setUp( self ):
        self.myTrackingHasher = TrackingHasher()

    def testGetBinsFor1Byte(self):
        self.validateGetBins(1, [26, 52, 78, 104, 130, 156, 182, 208, 234, 257])

    def testGetBinsFor2Bytes(self):
        self.validateGetBins(2, [6554, 13108, 19662, 26216, 32770, 39324, 45878, 52432, 58986, 65537])

    def validateGetBins(self, aNumBytesToEncode, anExpectedResult):
        self.myTrackingHasher.NUM_BYTES_ENCODE = aNumBytesToEncode
        theActual = self.myTrackingHasher.getBins()
        self.assertListEqual(anExpectedResult, theActual, 'wrong bins returned, # bytes = ' + str(aNumBytesToEncode)
                                                          + ' actual = ' + str(theActual)
                                                           + ', expected = ' + str(anExpectedResult))

    def testSumIndexCountsForRange(self):
        self.myTrackingHasher.myIndexCounts = { 0:1, 1:2, 2:3, 3:4, 4:5, 5:6 }
        self.assertEqual( 9, self.myTrackingHasher.sumIndexCountsForRange( 1, 4 ), 'slice count is wrong' )
        self.assertEqual( 10, self.myTrackingHasher.sumIndexCountsForRange( 0, 4 ), 'slice count is wrong' )
        self.assertEqual( 15, self.myTrackingHasher.sumIndexCountsForRange( 0, 5 ), 'slice count is wrong' )

    def testFoo(self):
        theBloomFilter = BloomFilter( self.myTrackingHasher )
        theBloomFilter.addWord( 'foo' )
        theBloomFilter.addWord( 'foo1' )
        theBloomFilter.addWord( 'foo2' )
        theBloomFilter.addWord( 'foo3' )
        theBloomFilter.addWord( 'foo4' )
        theBloomFilter.addWord( 'foo5' )
        theBloomFilter.addWord( 'foo6' )

        self.myTrackingHasher.printTrackingData()


if __name__ == '__main__':
    unittest.main()
