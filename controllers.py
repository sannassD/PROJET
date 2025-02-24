

def calcul_bonus_malus_EPS(note_eps):
    """Calcule bonus et malus pour EPS selon la règle RM2."""
    if note_eps > 10:
        bonus = note_eps - 10
        malus = 0
    elif note_eps < 10:
        bonus = 0
        malus = 10 - note_eps
    else:
        bonus = 0
        malus = 0
    return bonus, malus

def calcul_total_points(notes):

    total = 0
    for key, coef in notes.items():
        if key.startswith("Coef"):
            note_key = key.replace("Coef", "")
            note = notes.get(note_key, 0)
            try:
                total += float(note) * float(coef)
            except ValueError:
                pass
    return total


def deliberation(total_points, moyenne_cycle, nombre_de_tentatives, tour=1):
    # Règle 1 : Passage direct si total_points >= 180
    if total_points >= 180:
        return "Passage Direct"

    # Règles pour le 1er tour
    if tour == 1:
        # Cas repêchable d'office
        if 171 <= total_points < 180:
            if moyenne_cycle >= 12 and nombre_de_tentatives == 1:
                return "Repêchable d'office (1er tour)"
            else:
                return "Second Tour"
        # Passage au second tour
        if total_points >= 153:
            return "Second Tour"

    # Règles pour le 2nd tour
    if tour == 2:
        if 144 <= total_points < 153 and nombre_de_tentatives == 1:
            return "Repêchable (2nd tour)"

    # Dans tous les autres cas, le candidat échoue
    return "Échec"

