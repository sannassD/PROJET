import unittest
from controllers import deliberation

class TestDeliberation(unittest.TestCase):
    def test_deliberation_premier_tour(self):

        result = deliberation(180, moyenne_cycle=10, nombre_de_tentatives=1, tour=1)
        self.assertEqual(result, "Passage Direct")


        result = deliberation(160, 10, 1, tour=1)
        self.assertEqual(result, "Second Tour")

        result = deliberation(175, 12, 1, tour=1)
        self.assertEqual(result, "Repêchable d'office (1er tour)")


        result = deliberation(140, 10, 1, tour=1)
        self.assertTrue("Échec" in result)  # "Échec" ou "Échec (1er tour)" selon votre code

if __name__ == '__main__':
    unittest.main()
