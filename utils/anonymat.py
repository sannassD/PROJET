import uuid

def generer_anonymat():
    """
    Génère un identifiant unique d'anonymat.
    """
    return "ANON-" + str(uuid.uuid4())[:8]
