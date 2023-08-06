import unittest
from lightwood.encoders.categorical import CategoricalAutoEncoder
import string
import random
import logging
from sklearn.metrics import accuracy_score

from lightwood.logger import log


class TestAutoencoder(unittest.TestCase):
    def test_autoencoder(self):
        log.setLevel(logging.DEBUG)

        random.seed(2)
        cateogries = [''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(7,8))) for x in range(500)]
        for i in range(len(cateogries)):
            if i % 10 == 0:
                cateogries[i] = random.randint(1,20)

        priming_data = []
        test_data = []
        for category in cateogries:
            times = random.randint(1, 50)
            for i in range(times):
                priming_data.append(category)
                if i % 3 == 0 or i == 1:
                    test_data.append(category)

        random.shuffle(priming_data)
        random.shuffle(test_data)

        enc = CategoricalAutoEncoder()
        enc.desired_error = 3

        enc.prepare(priming_data)
        encoded_data = enc.encode(test_data)
        decoded_data = enc.decode(encoded_data)

        encoder_accuracy = accuracy_score(list(map(str,test_data)), list(map(str,decoded_data)))
        print(f'Categorical encoder accuracy for: {encoder_accuracy} on testing dataset')
        self.assertTrue(encoder_accuracy > 0.80)
