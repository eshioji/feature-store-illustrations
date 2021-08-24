import unittest
from typing import Set

from bloom_filter import BloomFilter


class FeatureStore:
    def __init__(self, store: BloomFilter):
        self.store = store
        self.possible_articles = set()

    def add(self, user_id: int, article_ids: Set[int]) -> None:
        for article_id in article_ids:
            self.possible_articles.add(article_id)
            composite_key = f'{user_id}^{article_id}'
            self.store.add(composite_key)

    def retreive_articles(self, user_id: int) -> Set[int]:
        ret = set()
        for article_id in self.possible_articles:
            composite_key = f'{user_id}^{article_id}'
            if self.store.might_contain(composite_key):
                ret.add(article_id)
        return ret


class SmokeTest(unittest.TestCase):
    def test_smoke(self):
        c = 10

        user_articles = {k: set(range(k, k + c)) for k in range(10)}

        subject = FeatureStore(BloomFilter(size=800, number_of_hash_functions=10))

        for user_id, articles in user_articles.items():
            subject.add(user_id, articles)

        exploded = [(user_id, article) for user_id, articles in user_articles.items() for article in articles]

        tpr = sum([
            1.0 if article in subject.retreive_articles(user_id) else 0.0 for user_id, article in exploded
        ]) / len(exploded)
        self.assertAlmostEqual(tpr, 1.0)

        fpr = sum([
            1.0 if (_article + c) in subject.retreive_articles(user_id) else 0.0 for user_id, _article in exploded
        ]) / len(exploded)
        self.assertLess(fpr, 0.05)


if __name__ == '__main__':
    unittest.main()
