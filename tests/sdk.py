import unittest

from src.asaas.sdk import Assas
from src.asaas.exceptions import SDKMisconfiguration

class TestCalculations(unittest.TestCase):

    def instanciation(self):
        sdk = None
        
        try:
            sdk = Assas(
                access_token="****",
                middlewares="****",
            )
        except SDKMisconfiguration as e:
            print(e)
        
        self.assertIsInstance(sdk, AssasSDK, "Não foi possível instanciar o SDK")

if __name__ == '__main__':
    unittest.main()