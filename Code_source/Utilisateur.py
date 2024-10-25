class Utilisateur:

    def __init__(self, id=None, prenom=None, nom=None, age=None):
        self.id = id
        self.prenom = prenom
        self.nom = nom
        self.age = age
        self.reservations = []