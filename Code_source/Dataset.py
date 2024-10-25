import json
from Utilisateur import Utilisateur
from Vol import Vol
from Reservation import Reservation
from Ville import Ville
from Place import Place
from datetime import datetime, timedelta

class Dataset():

    def __init__(self, path):
        self.path = path
        with open(path) as json_file:
            self.data = json.load(json_file)

    def sauvegarder(self, path=None):
        new_data = {
            "utilisateurs": {"count": self.data["utilisateurs"]["count"], "values": [u.__dict__ for u in list(self.utilisateurs.values())]},
            "reservations": {"count": self.data["reservations"]["count"], "values": [r.__dict__ for r in list(self.reservations.values())]},
            "vols": {"count": self.data["vols"]["count"], "values": [v.__dict__ for v in list(self.vols.values())]},
            "villes": {"count": self.data["villes"]["count"], "values": [v.__dict__ for v in list(self.villes.values())]}
        }
        for i, v in enumerate(new_data["vols"]["values"]): 
            new_places = []
            for idx, p in v["liste_places"].items():
                new_places.append([idx, p.reservee])
            new_data["vols"]["values"][i]["liste_places"] = new_places.copy()
        with open(self.path if path is None else path, 'w') as json_file:
            json.dump(new_data, json_file)

    def create_objects(self):
        self.utilisateurs = {}
        for u in self.data["utilisateurs"]["values"]:
            new_u = Utilisateur()
            new_u.__dict__ = u
            self.utilisateurs[new_u.id] = new_u
        
        self.reservations = {}
        for r in self.data["reservations"]["values"]:
            new_r = Reservation()
            new_r.__dict__ = r
            self.reservations[new_r.id] = new_r

        self.vols = {}
        for v in self.data["vols"]["values"]:
            new_v = Vol()
            new_v.__dict__ = v
            new_places = {}
            for p in new_v.liste_places: 
                new_places[p[0]] = Place(p[0], p[1])
            new_v.liste_places = new_places.copy()
            self.vols[f'{new_v.company}{new_v.n_vol}'] = new_v

        self.villes = {}
        for v in self.data["villes"]["values"]:
            new_v = Ville()
            new_v.__dict__ = v
            self.villes[new_v.id] = new_v 
        self.villes_reversed = {v.nom: v for k, v in self.villes.items()}
        
        return self.utilisateurs, self.vols, self.reservations, self.villes

    def create_user(self, prenom, nom, age):
        self.data["utilisateurs"]["count"] += 1
        id = self.data["utilisateurs"]["count"]
        new_u = Utilisateur(
            id=id,
            prenom=prenom,
            nom=nom,
            age=age
        )
        self.utilisateurs[id] = new_u
        return new_u
    
    def create_ville(self, nom):
        self.data["villes"]["count"] += 1
        id = self.data["villes"]["count"]
        new_v = Ville(
            id=id,
            nom=nom
        )
        self.villes[id] = new_v
        self.villes_reversed[new_v.nom] = new_v
        return new_v

    def create_vol(self, company, ville_depart, ville_arrivee, sieges_total, id=None):
        self.data["vols"]["count"] += 1
        if id is None: id = self.data["vols"]["count"]

        if not ville_depart in self.villes_reversed: v1 = self.create_ville(ville_depart)
        else: v1 = self.villes_reversed[ville_depart]

        if not ville_arrivee in self.villes_reversed: v2 = self.create_ville(ville_arrivee)
        else: v2 = self.villes_reversed[ville_arrivee]

        new_v = Vol(
            n_vol=id,
            company=company,
            ville_depart=v1.id,
            ville_arrivee=v2.id,
            sieges_total=sieges_total
        )

        self.vols[f'{company}{id}'] = new_v
        return new_v

    def create_reservation(self, id_utilisateur, company, id_vol, id_place):
        self.data["reservations"]["count"] += 1
        id = self.data["reservations"]["count"]
        new_r = Reservation(
            id=id,
            id_utilisateur=id_utilisateur,
            id_vol=f'{company}{id_vol}',
            id_place=id_place,
            date=(datetime.now() + timedelta(days=3)).strftime("%m/%d/%Y")
        )
        self.reservations[id] = new_r
        u = self.utilisateurs[id_utilisateur]
        u.reservations.append(new_r.id)
        return new_r

    def drop_reservation(self, id):
        r = self.reservations[id]
        u = self.utilisateurs[r.id_utilisateur]
        v = self.vols[r.id_vol]
        p = v.liste_places[r.id_place]
        v.sieges_dispo += 1
        p.reservee = not p.reservee
        u.reservations.remove(id)
        del self.reservations[id]

    def trouver_vol(self, company, num_vol):
        if f'{company}{num_vol}' in self.vols:
            v = self.vols[f'{company}{num_vol}']
            v1 = self.villes[v.ville_depart].nom
            v2 = self.villes[v.ville_arrivee].nom
            print(f'Vol n°{company}{num_vol} : {v1} -> {v2}. {v.sieges_dispo}/{v.sieges_total} places disponibles.')
            return v
        print(f"Aucun vol ne porte ce numéro : {company}{num_vol}.")
        return None
    
    def lister_reservations(self, id):
        if id in self.utilisateurs:
            u = self.utilisateurs[id]
            print(f"Réservations de l'utilisateurs {u.prenom} {u.nom} :\n")
            for r in u.reservations:
                r = self.reservations[r]
                v = self.vols[r.id_vol]
                v1 = self.villes[v.ville_depart]
                v2 = self.villes[v.ville_arrivee]
                print(f'R{r.id}. vol n°{v.company}{v.n_vol} : {v1} -> {v2} prévu le : {r.date}')
        else:
            print(f"Aucun utilisateurs ne porte cet identifiant : {id}")

    def clear(self):
        self.utilisateurs = {}
        self.data["utilisateurs"]["count"] = 0
        self.vols = {}
        self.data["vols"]["count"] = 0
        self.reservations = {}
        self.data["reservations"]["count"] = 0
        self.villes = {}
        self.data["villes"]["count"] = 0

    def __str__(self):
        return str(self.data)