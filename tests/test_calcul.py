import unittest
from controllers import calcul_bonus_malus_EPS, calcul_total_points

class TestCalcul(unittest.TestCase):
    def test_bonus_malus_EPS(self):
        # Test EPS > 10 => bonus
        bonus, malus = calcul_bonus_malus_EPS(12)
        self.assertEqual(bonus, 2)
        self.assertEqual(malus, 0)

        # Test EPS < 10 => malus
        bonus, malus = calcul_bonus_malus_EPS(8)
        self.assertEqual(bonus, 0)
        self.assertEqual(malus, 2)

        # Test EPS = 10 => ni bonus ni malus
        bonus, malus = calcul_bonus_malus_EPS(10)
        self.assertEqual(bonus, 0)
        self.assertEqual(malus, 0)

    def test_calcul_total_points(self):
       
        notes = {
            '1': 15,  'Coef1': 2,
            '2': 10,  'Coef2': 1
        }
        total = calcul_total_points(notes)
        self.assertEqual(total, 15*2 + 10*1)  # 40

if __name__ == '__main__':
    unittest.main()
