

class Candidat:
    def __init__(self, numero_table, prenom, nom, date_naissance, lieu_naissance, sexe,
                 nationnalite, choix_epr_facultative, epreuve_facultative, aptitude_sportive):
        self.numero_table = numero_table
        self.prenom = prenom
        self.nom = nom
        self.date_naissance = date_naissance
        self.lieu_naissance = lieu_naissance
        self.sexe = sexe
        self.nationnalite = nationnalite
        self.choix_epr_facultative = choix_epr_facultative
        self.epreuve_facultative = epreuve_facultative
        self.aptitude_sportive = aptitude_sportive

    def __str__(self):
        return f"{self.numero_table} - {self.prenom} {self.nom}"
