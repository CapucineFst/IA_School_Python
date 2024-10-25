class Ville:

    def __init__(self, id=None, nom=None):
        self.id = id
        self.nom = nom

    def __str__(self):
        return self.nom