import hashlib
import unittest


class BloomFilter:
    def __init__(self, size: int, number_of_hash_functions: int):
        self.bit_array = 0
        self.size = size
        self.number_of_hash_functions = number_of_hash_functions

    def _set_bit(self, bit: int):
        self.bit_array = self.bit_array | (1 << bit)

    def _is_bit_set(self, bit: int):
        return (self.bit_array & (1 << bit)) > 0

    def _hash_key(self, salt, key):
        s = f'{salt}^{key}'
        return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % self.size

    def add(self, key):
        for i in range(self.number_of_hash_functions):
            index = self._hash_key(i, key)
            self._set_bit(index)

    def might_contain(self, key):
        for i in range(self.number_of_hash_functions):
            index = self._hash_key(i, key)
            if not self._is_bit_set(index):
                return False
        return True


class SmokeTest(unittest.TestCase):
    def test_smoke(self):
        included_words = ['pigs', 'kittens', 'wonderful', 'amount', 'sudden', 'ahead', 'large', 'skillful']
        excluded_words = ['grandiose', 'tent', 'perfect', 'difficult', 'fantastic', 'profuse', 'ablaze']

        subject = BloomFilter(size=80, number_of_hash_functions=10)
        for w in included_words:
            subject.add(w)

        tpr = sum([1.0 if subject.might_contain(x) else 0.0 for x in included_words]) / len(included_words)
        self.assertAlmostEqual(tpr, 1.0)
        fpr = sum([1.0 if subject.might_contain(x) else 0.0 for x in excluded_words]) / len(excluded_words)
        self.assertLess(fpr, 0.1)


if __name__ == '__main__':
    unittest.main()
