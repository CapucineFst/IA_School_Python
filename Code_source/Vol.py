from Place import Place

class Vol :
    def __init__(self, company=None, n_vol=None, ville_depart=None, ville_arrivee=None, sieges_total=1) :
        self.company = company
        self.n_vol = n_vol
        self.ville_depart = ville_depart
        self.ville_arrivee = ville_arrivee
        self.sieges_total = sieges_total
        self.sieges_dispo = sieges_total
        self.liste_places = {(i + 1): Place (i + 1) for i in range(sieges_total)}

    def reserver_siege(self) :
        for idx, place in self.liste_places.items() :
            if not place.reservee :
                place.reserver()
                self.sieges_dispo -= 1
                return place
        return None

    # def annuler_reservation(self, place) :
    #         index = place.numero -1
    #         if self.liste_places[index].annuler() :
    #             self.sieges_dispo += 1
    #             return True
    #         return False

    def __str__(self):
        print(f'Vol n°{self.n_vol} : {self.sieges_dispo} sièges disponibles')