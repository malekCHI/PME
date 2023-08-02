from Entreprise.models import Entreprise
from flask import request
from sqlalchemy.orm import validates
from sqlalchemy import exc


def get_all_Entreprises():
    return {"entreprise": list(map(lambda x: x.serialize(), Entreprise.query.all()))}


def get_entreprise(_id_Entreprise):
    return {
        "entreprise": list(
            map(
                lambda x: x.serialize(),
                Entreprise.query.filter_by(_id_Entreprise=_id_Entreprise).first(),
            )
        )
    }


def add_entreprise(nom, adresse, description, email, tel, logo_path):
    entreprise = Entreprise(
        nom=nom,
        adresse=adresse,
        description=description,
        email=email,
        tel=tel,
    )
    entreprise.save_to_db()


def update_entreprise(
    _id_Entreprise, _nom, _adresse, _description, _creation_date, _email, _tel
):
    entreprise_to_update = Entreprise.query.filter_by(
        id_Entreprise=_id_Entreprise
    ).first()
    if entreprise_to_update:
        entreprise_to_update.nom = _nom
        entreprise_to_update.adresse = _adresse
        entreprise_to_update.description = _description
        entreprise_to_update.creation_date = _creation_date
        entreprise_to_update.email = _email
        entreprise_to_update.tel = _tel
        entreprise_to_update.save_to_db()
        return True
    return False


def delete_entreprise(_id_Entreprise):
    entreprise_to_delete = Entreprise.query.filter_by(
        id_Entreprise=_id_Entreprise
    ).first()
    if entreprise_to_delete:
        entreprise_to_delete.delete_from_db()
        return True
    return False