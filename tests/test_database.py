import os
import unittest
from database import DatabaseManager

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_name = "test_bfem.db"
        cls.db_manager = DatabaseManager(db_name=cls.db_name)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.db_name):
            os.remove(cls.db_name)

    def test_add_and_get_candidat(self):

        candidat_data = {
            'Numero_Table': 999,
            'Prenom': 'Test',
            'Nom': 'User',
            'Date_Naissance': '2000-01-01',
            'Lieu_Naissance': 'TestVille',
            'Sexe': 'M',
            'Nationnalite': 'Test',
            'Choix_Epr_Facultative': False,
            'Epreuve_Facultative': None,
            'Aptitude_Sportive': True
        }
        # Ajout
        self.db_manager.add_candidat(candidat_data)
        candidat = self.db_manager.get_candidat(999)
        self.assertIsNotNone(candidat, "Le candidat devrait exister en base")
        self.assertEqual(candidat[1], 'Test')
        self.assertEqual(candidat[2], 'User')

if __name__ == '__main__':
    unittest.main()
