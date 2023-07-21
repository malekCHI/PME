from enum import Enum
from typing import Literal
# Define the email templates
class TypeEmail(Enum):
    Rappel_de_paiement = 'Rappel de paiement'
    Facture = 'Facture'
    Validation_de_la_facture = 'Validation de la facture'
    Rappel_daction = 'Rappel daction'
    Rappel_de_date_nego = 'Rappel de date nego'


EmailTemplate = Literal['Rappel de paiement', 'Facture', 'Validation de la facture','Rappel daction', 'Rappel de date nego']

Rappel_de_paiement = """Cher [Nom du client],

Nous vous rappelons respectueusement qu'une facture en attente est toujours ouverte à votre nom. Veuillez prendre en compte les détails ci-dessous :

Numéro de facture : [Numéro de facture]
Montant dû : [Montant de la facture]
Date d'échéance : [Date d'échéance de paiement]

Nous vous prions de bien vouloir régler le montant dû dans les meilleurs délais. Votre paiement en temps voulu contribuera à maintenir une relation commerciale harmonieuse. En cas de questions ou de besoin d'assistance supplémentaire, n'hésitez pas à nous contacter.

Nous vous remercions de votre attention et de votre coopération.

Cordialement,
L'équipe de [Nom de l'entreprise]
__________________________________________________________________________________________________________________

Cet e-mail a été généré automatiquement. Veuillez ne pas répondre à cette adresse e-mail (noreply@neopolis-dev.com).
"""
Facture = """Cher [Nom du client],

Nous vous envoyons ci-joint la facture [Numéro de facture] correspondant à nos services/produits fournis. Veuillez trouver le montant dû, les détails de la facture et les informations de paiement ci-dessous :

Montant dû : [Montant de la facture]
Date de la facture : [Date de la facture]
Date d'échéance : [Date d'échéance de paiement]
Méthode de paiement : [Méthode de paiement acceptée]

Veuillez effectuer le paiement avant la date d'échéance mentionnée ci-dessus. En cas de questions ou de préoccupations, n'hésitez pas à nous contacter. Nous vous remercions de votre coopération.

Cordialement,
L'équipe de [Nom de l'entreprise]

__________________________________________________________________________________________________________________

Cet e-mail a été généré automatiquement. Veuillez ne pas répondre à cette adresse e-mail (noreply@neopolis-dev.com).
"""
Validation_de_la_facture = """Cher(e) [Nom du validateur],

Une nouvelle facture nécessitant votre validation a été créée dans le système. Veuillez prendre en compte les détails ci-dessous :

Numéro de facture : [Numéro de facture]
Montant de la facture : [Montant de la facture]
Date de la facture : [Date de la facture]
Date d'échéance : [Date d'échéance de paiement]
Entreprise émettrice : [Nom de l'entreprise]
Client : [Nom du client]

Veuillez examiner attentivement les informations de la facture et confirmer sa validité en cliquant sur le lien de validation ci-dessous :

[Insérer le lien de validation ici]

En cas de questions ou de besoin d'assistance supplémentaire, n'hésitez pas à nous contacter. Nous vous remercions de votre coopération dans le processus de validation des factures.

Cordialement,
L'équipe de [Nom de l'entreprise]
___________________________________________________________________________________________________________________

Cet e-mail a été généré automatiquement. Veuillez ne pas répondre à cette adresse e-mail (noreply@neopolis-dev.com).

"""
Rappel_daction = """Cher(e) [Nom de l'utilisateur],

Ce courriel vous rappelle qu'une action doit être effectuée dans les prochains jours. Veuillez prendre en compte les détails ci-dessous :

Action : [Description de l'action]
Date limite : [Date limite de l'action]

Nous vous rappelons de compléter cette action avant la date limite mentionnée ci-dessus. Assurez-vous de suivre les procédures et les instructions spécifiées pour accomplir cette tâche. En cas de questions ou de besoin d'assistance supplémentaire, n'hésitez pas à nous contacter.

Merci de votre attention et de votre coopération.

Cordialement,
L'équipe de [Nom de l'entreprise]

___________________________________________________________________________________________________________________

Cet e-mail a été généré automatiquement. Veuillez ne pas répondre à cette adresse e-mail (noreply@neopolis-dev.com).
"""
Rappel_de_date_nego="""Cher(e) [Nom du destinataire],

Nous vous rappelons que la date de négociation du contrat [Numéro de contrat] approche à grands pas. Veuillez prendre en compte les détails ci-dessous :

Numéro de contrat : [Numéro de contrat]
Date de début du contrat : [Date de début du contrat]
Date de fin du contrat : [Date de fin du contrat]
Date de rappel de négociation : [Date de rappel pour la nouvelle négociation]

Nous vous invitons à prendre les mesures nécessaires pour organiser la négociation du contrat avant la date de rappel indiquée ci-dessus. Si vous avez des questions ou besoin d'informations supplémentaires, n'hésitez pas à nous contacter.

Merci de votre attention et de votre coopération.

Cordialement,
L'équipe de [Nom de l'entreprise]

___________________________________________________________________________________________________________________

Cet e-mail a été généré automatiquement. Veuillez ne pas répondre à cette adresse e-mail (noreply@neopolis-dev.com).
"""
