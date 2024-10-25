from Dataset import Dataset
import os

def check_place_count_decreases(vol):
    avant = vol.sieges_dispo
    vol.reserver_siege()
    assert vol.sieges_dispo == avant-1

def check_reservation_associate_user(ds, id_reservation):
    r = ds.reservations[id_reservation]
    assert r.id_utilisateur in ds.utilisateurs

def check_place_count_increase(ds, vol, id_reservation):
    avant = vol.sieges_dispo
    ds.drop_reservation(id_reservation)
    assert vol.sieges_dispo == avant+1

def check_reservation_cancel(ds, user, vol):
    place = vol.reserver_siege()
    r = ds.create_reservation(
        id_utilisateur=user.id,
        company=vol.company, 
        id_vol=vol.n_vol, 
        id_place=place.numero
    )
    avant = len(user.reservations)
    ds.drop_reservation(r.id)
    assert len(user.reservations) == avant - 1

def check_saving_loading(ds):
    ds.sauvegarder()
    ds2 = Dataset("data.json")
    ds2.create_objects()
    ds2.sauvegarder("data2.json")
    
    with open('data.json') as f1:
        d1 = f1.read()
    with open('data2.json') as f2:
        d2 = f2.read()

    assert d1 == d2

    os.system("rm data2.json")

def main(ds):
    # Context
    user = ds.create_user(
        prenom="Capucine",
        nom="FEIST",
        age=21
    )
    vol = ds.create_vol(
        company='AF',
        id=123,
        sieges_total=150,
        ville_depart='Paris',
        ville_arrivee='New York'
    )
    place = vol.reserver_siege()
    reservation = ds.create_reservation(
        id_utilisateur=user.id,
        company=vol.company, 
        id_vol=vol.n_vol, 
        id_place=place.numero
    )

    # Tests
    check_place_count_decreases(vol)
    check_reservation_associate_user(ds, reservation.id)
    check_place_count_increase(ds, vol, reservation.id)
    check_reservation_cancel(ds, user, vol)
    check_saving_loading(ds)

    #print('OK')
