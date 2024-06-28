import unittest
from crypto_bot import main

class TestCryptoBot(unittest.TestCase):
    def setUp(self):
        self.crypto_bot = main()

    def test_invalid_choice(self):
        with self.assertRaises(ValueError) as context:
            handle_user_choice("4")
        self.assertEqual(str(context.exception), "Invalid input, please try again")

    def test_exit_choice(self):
        result = handle_user_choice("3")
        self.assertEqual(result, "exit")
        
if __name__ == '__main__':
    unittest.main()
