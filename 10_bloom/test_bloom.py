import unittest

from bloom import BitArray, Hash, BloomFilter


class Test_BitArray(unittest.TestCase):

    def check(self, a: BitArray, pattern: str):
        self.assertEqual(a.get_size(), len(pattern))
        for i in range(len(pattern)):
            self.assertEqual(a.get(i), pattern[i] == "1")
            self.assertEqual(a.get_get_status(), BitArray.GetStatus.OK)

    def test_set(self):
        a = BitArray(71)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.NIL)
        self.check(a, "00000000" + "0" * 56 + "0000000")
        a.set_on(5)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.OK)
        self.check(a, "00000100" + "0" * 56 + "0000000")
        a.set_on(5)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.OK)
        self.check(a, "00000100" + "0" * 56 + "0000000")
        a.set_on(68)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.OK)
        self.check(a, "00000100" + "0" * 56 + "0000100")
        a.set_on(0)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.OK)
        self.check(a, "10000100" + "0" * 56 + "0000100")
        a.set_on(70)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.OK)
        self.check(a, "10000100" + "0" * 56 + "0000101")
        a.set_on(-1)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.INDEX_OUT_OF_RANGE)
        a.set_on(71)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.INDEX_OUT_OF_RANGE)
        a.set_on(-1000)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.INDEX_OUT_OF_RANGE)
        a.set_on(1000)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.INDEX_OUT_OF_RANGE)
        self.check(a, "10000100" + "0" * 56 + "0000101")

        a.set_off(-1)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.INDEX_OUT_OF_RANGE)
        a.set_off(71)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.INDEX_OUT_OF_RANGE)
        a.set_off(-1000)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.INDEX_OUT_OF_RANGE)
        a.set_off(1000)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.INDEX_OUT_OF_RANGE)
        self.check(a, "10000100" + "0" * 56 + "0000101")
        a.set_off(5)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.OK)
        self.check(a, "10000000" + "0" * 56 + "0000101")
        a.set_off(3)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.OK)
        self.check(a, "10000000" + "0" * 56 + "0000101")
        a.set_off(68)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.OK)
        self.check(a, "10000000" + "0" * 56 + "0000001")
        a.set_off(66)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.OK)
        self.check(a, "10000000" + "0" * 56 + "0000001")
        a.set_off(0)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.OK)
        self.check(a, "00000000" + "0" * 56 + "0000001")
        a.set_off(70)
        self.assertEqual(a.get_set_status(), BitArray.SetStatus.OK)
        self.check(a, "00000000" + "0" * 56 + "0000000")


    def test_get(self):
        a = BitArray(71)
        self.assertEqual(a.get_get_status(), BitArray.GetStatus.NIL)
        a.set_on(0)
        a.set_on(5)
        a.set_on(68)
        a.set_on(70)
        self.check(a, "10000100" + "0" * 56 + "0000101")
        a.get(-1)
        self.assertEqual(a.get_get_status(), BitArray.GetStatus.INDEX_OUT_OF_RANGE)
        a.get(71)
        self.assertEqual(a.get_get_status(), BitArray.GetStatus.INDEX_OUT_OF_RANGE)
        a.get(-1000)
        self.assertEqual(a.get_get_status(), BitArray.GetStatus.INDEX_OUT_OF_RANGE)
        a.get(1000)
        self.assertEqual(a.get_get_status(), BitArray.GetStatus.INDEX_OUT_OF_RANGE)
        self.check(a, "10000100" + "0" * 56 + "0000101")


class Test_Hash(unittest.TestCase):

    def test_10(self):
        h = Hash(17, 10)
        s = set[int]()
        for i in range(10000):
            v = h.eval(str(i))
            self.assertGreaterEqual(v, 0)
            self.assertLessEqual(v, 9)
            s.add(v)
        self.assertEqual(len(s), 10)

    def test_100(self):
        h = Hash(307, 100)
        s = set[int]()
        for i in range(100000):
            v = h.eval(str(i))
            self.assertGreaterEqual(v, 0)
            self.assertLessEqual(v, 99)
            s.add(v)
        self.assertEqual(len(s), 100)


class Test_MySet(unittest.TestCase):
    
    def test(self):
        bf = BloomFilter(100, 0.2)
        for i in range(100):
            bf.add(str(i))
        for i in range(100):
            self.assertTrue(bf.has(str(i)))
        count = 0
        for i in range(10000):
            if bf.has(str(i)):
                count += 1
        self.assertLess(count, 3000)


if __name__ == "__main__":
    unittest.main()
