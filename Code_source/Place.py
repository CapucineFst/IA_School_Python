class Place :
    def __init__(self, numero=None, reservee=False) :
        self.numero = numero
        self.reservee = reservee
        
    def reserver(self) :
        if not self.reservee :
            self.reservee = True
            return True
        return False
    
    def annuler(self) :
        if self.reservee :
            self.reservee = False
            return True
        return False
    
    def __str__(self):
        return f"Place {self.numero} {'(Réservée)' if self.reservee else ''}"