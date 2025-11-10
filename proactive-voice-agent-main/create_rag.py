#!/usr/bin/env python3
"""
Script de création de la base de connaissances RAG pour le Cabinet Dentaire Archipel
Génère un fichier rag.pkl contenant les embeddings FAISS et les documents
"""

import pickle
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Informations du Cabinet Dentaire Archipel
documents = [
    "Le Cabinet Dentaire Archipel est situé au 42 Avenue des Champs-Élysées, 75008 Paris. Métro ligne 1, station George V ou Charles de Gaulle - Étoile.",
    "Horaires d'ouverture : Lundi au Vendredi de 9h à 19h, Samedi de 9h à 13h. Fermé le dimanche et jours fériés.",
    "Le Dr. Sophie Martin est chirurgien-dentiste depuis 15 ans, spécialisée en esthétique dentaire et implantologie. Le Dr. Thomas Dubois est orthodontiste avec 10 ans d'expérience.",
    "Services proposés : Soins dentaires généraux, détartrage, blanchiment dentaire, orthodontie adulte et enfant, implants dentaires, couronnes, bridges, prothèses dentaires complètes.",
    "Tarifs : Consultation 50€, Détartrage complet 70€, Blanchiment dentaire 350€, Couronne céramique 650€, Implant dentaire à partir de 1200€. Tiers-payant accepté pour les soins remboursés.",
    "Paiement accepté : Carte bancaire, espèces, chèque. Cabinet conventionné secteur 1. Prise en charge Sécurité Sociale et mutuelles. Devis gratuit pour tous les soins.",
    "Urgences dentaires acceptées tous les jours ouvrés sur créneaux dédiés. En cas d'urgence hors horaires d'ouverture, contactez le 15 ou le service d'urgences dentaires de garde de Paris.",
    "Stationnement : Parking public Champs-Élysées Clemenceau à 200 mètres. Station Vélib' juste devant le cabinet. Accès PMR disponible avec ascenseur.",
    "Politique d'annulation : Pour annuler ou modifier un rendez-vous, merci d'appeler au moins 24 heures à l'avance au 01 42 56 78 90. Des pénalités de 30€ peuvent s'appliquer en cas d'absence non justifiée.",
    "Première consultation : Prévoir environ 30 minutes. Merci d'apporter votre carte vitale, attestation de mutuelle et ordonnances ou radios en cours. Le cabinet accepte les nouveaux patients.",
    "Équipements modernes : Scanner 3D, radiologie numérique, laser dentaire, salle de stérilisation aux normes européennes. Protocole d'hygiène strict respecté.",
    "Prise de rendez-vous : Par téléphone au 01 42 56 78 90, en ligne sur notre site archipel-dental.fr, ou via Doctolib. Confirmation par SMS 48h avant le rendez-vous.",
    "Soins pour enfants : Cabinet adapté aux enfants avec espace ludique. Première consultation gratuite pour les moins de 6 ans. Prévention et éducation bucco-dentaire.",
    "Orthodontie : Appareils dentaires classiques, gouttières invisibles Invisalign, orthodontie linguale. Consultation orthodontique 60€, prise en charge mutuelle selon contrat.",
    "Implantologie : Pose d'implants dentaires avec os synthétique si nécessaire. Garantie 10 ans sur les implants. Plusieurs options de couronnes disponibles selon budget."
]

print("🏥 Création de la base de connaissances pour le Cabinet Dentaire Archipel...")
print(f"📄 Nombre de documents : {len(documents)}")

# Créer les embeddings avec un modèle multilingue optimisé pour le français
print("🔄 Chargement du modèle d'embeddings multilingue...")
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

print("🧮 Génération des embeddings...")
embeddings = model.encode(documents, show_progress_bar=True)

# Créer l'index FAISS pour la recherche de similarité
print("🔍 Création de l'index FAISS...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))

print(f"✅ Index créé avec {index.ntotal} vecteurs de dimension {dimension}")

# Sauvegarder la base de connaissances
rag_data = {
    'index': index,
    'documents': documents,
    'model_name': 'distiluse-base-multilingual-cased-v2'
}

output_file = 'rag.pkl'
with open(output_file, 'wb') as f:
    pickle.dump(rag_data, f)

print(f"💾 Base de connaissances sauvegardée : {output_file}")
print("✨ Terminé ! La base de connaissances RAG est prête à être utilisée.")
print("\n📋 Contenu de la base :")
print("  - Adresse et accès")
print("  - Horaires d'ouverture")
print("  - Informations sur les praticiens")
print("  - Services et tarifs")
print("  - Politique d'annulation")
print("  - Équipements et normes")
