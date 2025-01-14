import unittest
from deck import Hand, shuffle

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.hand = Hand()  # Create an instance of the class
    
    def test_ace(self):
        self.hand.add_card("1_of_clubs")
        self.hand.add_card("1_of_clubs")
        self.assertEqual(self.hand.count, 12)
    
    def test_21(self):
        self.hand.add_card("10_of_clubs")
        self.hand.add_card("1_of_clubs")
        self.assertEqual(self.hand.count, 21)
    
    def test_over(self):
        self.hand.add_card("10_of_clubs")
        self.hand.add_card("10_of_clubs")
        self.hand.add_card("3_of_clubs")
        self.assertEqual(self.hand.count, 23)

    def test_ace_complex(self):
        self.hand.add_card("1_of_clubs")
        self.hand.add_card("13_of_clubs")
        self.hand.add_card("3_of_clubs")
        self.assertEqual(self.hand.count, 14)

    def test_ace_complex2(self):
        self.hand.add_card("1_of_clubs")
        self.hand.add_card("1_of_clubs")
        self.hand.add_card("13_of_clubs")
        self.hand.add_card("3_of_clubs")
        self.assertEqual(self.hand.count, 15)

if __name__ == "__main__":
    unittest.main()

