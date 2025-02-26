import uuid

def generer_anonymat():

    return "ANON-" + str(uuid.uuid4())[:8]
