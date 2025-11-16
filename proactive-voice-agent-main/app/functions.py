import pickle
import uuid
from datetime import datetime

import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from app.constants import (
    BOOK_SLOT_WEBHOOK,
    DEBUG,
    DOCUMENT_PROMPT,
    ERROR_PROMPT,
    GET_AVAILABILITY_WEBHOOK,
    HOST_NAME,
    SEND_MAIL_WEBHOOK,
    TOP_K,
    USE_ZAPIER,
)

# Charger la base de connaissances RAG
try:
    with open("rag.pkl", "rb") as f:
        rag_data = pickle.load(f)
        faiss_index = rag_data['index']
        documents = rag_data['documents']
        model_name = rag_data.get('model_name', 'unknown')

        # Charger le modèle seulement s'il ne s'agit pas d'embeddings simplifiés
        if model_name == 'simple-random-embeddings':
            print(f"✅ Base de connaissances chargée (mode simplifié) : {len(documents)} documents")
            embeddings_model = None
            stored_embeddings = rag_data.get('embeddings', None)
        else:
            try:
                embeddings_model = SentenceTransformer(model_name)
                stored_embeddings = None
                print(f"✅ Base de connaissances chargée : {len(documents)} documents avec modèle {model_name}")
            except Exception as e:
                print(f"⚠️ Erreur chargement modèle {model_name}: {e}")
                print("   Utilisation du mode simplifié")
                embeddings_model = None
                stored_embeddings = rag_data.get('embeddings', None)
except FileNotFoundError:
    print("⚠️ Fichier rag.pkl introuvable. Exécutez 'python create_rag_simple.py' d'abord.")
    faiss_index = None
    documents = []
    embeddings_model = None
    stored_embeddings = None


# Créneaux disponibles pour la démo (semaine du 11-15 novembre 2025)
AVAILABLE_SLOTS = {
    "2025-11-11": ["09:00", "10:30", "14:00", "16:30"],
    "2025-11-12": ["09:30", "11:00", "15:00", "17:00"],
    "2025-11-13": ["10:00", "14:30", "16:00"],
    "2025-11-14": ["09:00", "10:00", "11:00", "14:00", "15:30"],
    "2025-11-15": ["09:30", "11:30", "14:00"]
}


def get_information(question: str) -> str:
    """
    Récupère des informations sur le Cabinet Dentaire Archipel depuis la base de connaissances RAG.

    Args:
        question: Question du patient concernant le cabinet

    Returns:
        Informations pertinentes issues de la base de connaissances
    """
    print(f"[CALL] get_information: {question}")

    if faiss_index is None:
        return "Je suis désolée, la base de connaissances n'est pas disponible pour le moment."

    # Générer l'embedding de la question
    if embeddings_model is not None:
        # Mode normal avec modèle SentenceTransformer
        question_embedding = embeddings_model.encode([question])
    elif stored_embeddings is not None:
        # Mode simplifié : utiliser un embedding aléatoire basé sur le hash de la question
        # (pour la démo - en production, utiliser un vrai modèle)
        import hashlib
        hash_val = int(hashlib.md5(question.encode()).hexdigest(), 16)
        np.random.seed(hash_val % (2**32))
        question_embedding = np.random.randn(1, stored_embeddings.shape[1]).astype('float32')
        question_embedding = question_embedding / np.linalg.norm(question_embedding)
    else:
        return "Je suis désolée, la base de connaissances n'est pas correctement configurée."

    # Rechercher les TOP_K documents les plus similaires
    distances, indices = faiss_index.search(np.array(question_embedding).astype('float32'), TOP_K)

    # Récupérer les documents pertinents
    relevant_docs = [documents[idx] for idx in indices[0] if idx < len(documents)]

    if not relevant_docs:
        return "Je n'ai pas trouvé d'information spécifique à ce sujet. Puis-je vous aider autrement ?"

    document_stack = "\n###\n".join(relevant_docs)
    return DOCUMENT_PROMPT.format(document_stack=document_stack)


def get_availability(date: str, time: str, reason_for_consultation: str) -> str:
    """
    Vérifie la disponibilité du dentiste pour une date et heure données.

    Args:
        date: Date au format AAAA-MM-JJ (ex: 2025-11-12)
        time: Heure au format HH:MM (ex: 14:30)
        reason_for_consultation: Motif de consultation

    Returns:
        Message indiquant si le créneau est disponible ou proposant des alternatives
    """
    print(f"[CALL] get_availability: date={date}, time={time}, reason={reason_for_consultation}")

    # Validation format date
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_name = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"][date_obj.weekday()]
    except ValueError:
        return "Format de date invalide. Utilisez AAAA-MM-JJ (ex: 2025-11-11)"

    # Validation format heure
    if not time or ':' not in time:
        return "Format d'heure invalide. Utilisez HH:MM (ex: 14:30)"

    # Si USE_ZAPIER est activé, utiliser le webhook externe
    if USE_ZAPIER and GET_AVAILABILITY_WEBHOOK:
        callback_id = str(uuid.uuid4())
        callback_url = f"{HOST_NAME}/zapier-callback/{callback_id}"
        try:
            response = requests.post(
                url=GET_AVAILABILITY_WEBHOOK,
                data={
                    "date": date,
                    "time": time,
                    "reason": reason_for_consultation,
                    "callback_url": callback_url,
                },
                timeout=10
            )

            if response.status_code != 200:
                return ERROR_PROMPT

            result_response = requests.get(f"{HOST_NAME}/zapier-callback-result/{callback_id}", timeout=10)
            if result_response.status_code != 200:
                return ERROR_PROMPT

            callback_value = result_response.json().get("callback_value", {})

            if callback_value.get("available"):
                return f"Le Dr. Martin est disponible le {day_name} {date} à {time} pour {reason_for_consultation}. Puis-je réserver ce créneau pour vous ?"
            else:
                return "Ce créneau n'est malheureusement pas disponible. Puis-je vous proposer d'autres horaires ?"

        except requests.exceptions.RequestException as e:
            if DEBUG:
                print(f"Erreur webhook: {e}")
            # Fallback sur les créneaux hardcodés

    # Mode démo : vérifier les créneaux disponibles hardcodés
    if date in AVAILABLE_SLOTS and time in AVAILABLE_SLOTS[date]:
        return f"Parfait ! Le Dr. Martin est disponible le {day_name} {date} à {time} pour {reason_for_consultation}. Souhaitez-vous que je confirme ce rendez-vous ?"
    else:
        # Proposer des alternatives
        if date in AVAILABLE_SLOTS:
            alternatives = ", ".join(AVAILABLE_SLOTS[date][:3])
            return f"Malheureusement, {time} n'est pas disponible le {day_name} {date}. Je peux vous proposer : {alternatives}. Quel horaire vous conviendrait ?"
        else:
            # Proposer le prochain jour disponible
            next_dates = sorted([d for d in AVAILABLE_SLOTS.keys() if d > date])
            if next_dates:
                next_date = next_dates[0]
                next_slots = ", ".join(AVAILABLE_SLOTS[next_date][:3])
                return f"Aucune disponibilité le {date}. Le prochain jour disponible est le {next_date} avec les créneaux : {next_slots}. Cela vous conviendrait-il ?"
            else:
                return "Je n'ai malheureusement pas de disponibilité à cette période. Puis-je vous proposer la semaine prochaine ?"


def send_email(subject: str, content: str, recipient: str = "contact@archipel-dental.fr") -> None:
    """
    Envoie un email de confirmation (si webhook configuré).

    Args:
        subject: Sujet de l'email
        content: Contenu de l'email
        recipient: Destinataire (optionnel)
    """
    if not USE_ZAPIER or not SEND_MAIL_WEBHOOK:
        if DEBUG:
            print(f"[EMAIL SIMULATION] To: {recipient}, Subject: {subject}")
        return

    try:
        response = requests.post(
            url=SEND_MAIL_WEBHOOK,
            data={
                "to": recipient,
                "subject": subject,
                "content": content
            },
            timeout=10
        )

        if response.status_code != 200 and DEBUG:
            print(f"Erreur envoi email: {response.status_code}")
    except requests.exceptions.RequestException as e:
        if DEBUG:
            print(f"Erreur webhook email: {e}")


def book_slot(date: str, time: str, reason_for_consultation: str, patient_name: str) -> str:
    """
    Réserve un rendez-vous pour le patient.

    Args:
        date: Date au format AAAA-MM-JJ
        time: Heure au format HH:MM
        reason_for_consultation: Motif de consultation
        patient_name: Nom complet du patient

    Returns:
        Message de confirmation ou d'erreur
    """
    print(f"[CALL] book_slot: {patient_name} le {date} à {time} pour {reason_for_consultation}")

    # Validation : vérifier que le créneau est bien disponible
    if date not in AVAILABLE_SLOTS or time not in AVAILABLE_SLOTS[date]:
        return "Je suis désolée, ce créneau n'est plus disponible. Puis-je vous en proposer un autre ?"

    # Si USE_ZAPIER est activé, créer l'événement dans le calendrier externe
    if USE_ZAPIER and BOOK_SLOT_WEBHOOK:
        try:
            # Convertir en format ISO pour le webhook
            datetime_obj = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            iso_datetime = datetime_obj.isoformat()

            subject = f"RDV {patient_name} - {reason_for_consultation}"
            description = f"Patient : {patient_name}\nMotif : {reason_for_consultation}\nDate : {date}\nHeure : {time}"

            response = requests.post(
                url=BOOK_SLOT_WEBHOOK,
                data={
                    "start_at": iso_datetime,
                    "title": subject,
                    "description": description,
                    "patient_name": patient_name,
                    "reason": reason_for_consultation
                },
                timeout=10
            )

            if response.status_code != 200:
                return ERROR_PROMPT

            # Envoyer l'email de confirmation
            email_subject = f"Confirmation RDV Cabinet Archipel - {patient_name} le {date} à {time}"
            email_content = f"""Bonjour {patient_name},

Votre rendez-vous au Cabinet Dentaire Archipel est confirmé :

📅 Date : {date}
🕐 Heure : {time}
🦷 Motif : {reason_for_consultation}
📍 Adresse : 42 Avenue des Champs-Élysées, 75008 Paris

Pour toute modification, merci de nous contacter au 01 42 56 78 90.

À très bientôt,
L'équipe du Cabinet Archipel
"""
            send_email(subject=email_subject, content=email_content)

        except requests.exceptions.RequestException as e:
            if DEBUG:
                print(f"Erreur webhook booking: {e}")
            # Continuer même si le webhook échoue (mode démo)
        except ValueError as e:
            if DEBUG:
                print(f"Erreur format date/heure: {e}")

    # Mode démo : simuler la réservation
    # Dans un vrai système, on retirerait le créneau de AVAILABLE_SLOTS
    return f"Parfait ! Votre rendez-vous est confirmé pour le {date} à {time}. Vous recevrez un email de confirmation. À très bientôt au Cabinet Archipel, 42 Avenue des Champs-Élysées."


# Définition des outils pour l'API Mistral
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_information",
            "description": "Récupère des informations sur le Cabinet Dentaire Archipel (adresse, horaires, tarifs, services, dentistes, stationnement, etc.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "La question du patient concernant le cabinet dentaire",
                    }
                },
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_availability",
            "description": "Vérifie la disponibilité du dentiste pour une date et heure spécifiques. À utiliser AVANT de proposer un rendez-vous au patient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date du rendez-vous au format AAAA-MM-JJ (ex: 2025-11-15). Convertir les demandes en français ('lundi prochain', 'demain') en ce format.",
                    },
                    "time": {
                        "type": "string",
                        "description": "Heure du rendez-vous au format HH:MM (ex: 14:30). Utiliser le format 24h.",
                    },
                    "reason_for_consultation": {
                        "type": "string",
                        "description": "Motif de la consultation (détartrage, soins dentaires, urgence, consultation, blanchiment, orthodontie, etc.)",
                    },
                },
                "required": ["date", "time", "reason_for_consultation"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_slot",
            "description": "Réserve un rendez-vous pour le patient. À utiliser UNIQUEMENT après avoir confirmé la disponibilité avec get_availability() et obtenu l'accord explicite du patient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date du rendez-vous au format AAAA-MM-JJ (ex: 2025-11-15)",
                    },
                    "time": {
                        "type": "string",
                        "description": "Heure du rendez-vous au format HH:MM (ex: 14:30)",
                    },
                    "reason_for_consultation": {
                        "type": "string",
                        "description": "Motif de la consultation",
                    },
                    "patient_name": {
                        "type": "string",
                        "description": "Nom complet du patient (Prénom NOM)",
                    },
                },
                "required": ["date", "time", "reason_for_consultation", "patient_name"],
            },
        },
    },
]

# Mapping des noms de fonctions vers les fonctions Python
NAME_TO_FUNCTIONS = {
    "get_information": get_information,
    "get_availability": get_availability,
    "book_slot": book_slot,
}

# Phrases de remplissage pendant l'exécution des fonctions
NAME_TO_FILLER = {
    "get_information": "Un instant, je consulte les informations pour vous.\n",
    "get_availability": "Laissez-moi vérifier les disponibilités du Dr. Martin à ce moment-là.\n",
    "book_slot": "Très bien, je confirme votre rendez-vous immédiatement.\n",
}
