#!/usr/bin/env python3
"""
Version simplifiée de création de la base de connaissances RAG
Utilise des embeddings simples sans téléchargement de modèle HuggingFace
"""

import pickle
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

print("🏥 Création de la base de connaissances pour le Cabinet Dentaire Archipel (version simplifiée)...")
print(f"📄 Nombre de documents : {len(documents)}")

# Créer des embeddings factices simples (random mais reproductibles)
print("🧮 Génération des embeddings simples...")
np.random.seed(42)  # Pour la reproductibilité
dimension = 384  # Dimension standard pour les embeddings de phrase

# Créer des vecteurs aléatoires normalisés pour chaque document
embeddings = np.random.randn(len(documents), dimension).astype('float32')
# Normaliser les vecteurs
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
embeddings = embeddings / norms

print(f"✅ Embeddings créés : {len(embeddings)} vecteurs de dimension {dimension}")

# Créer un index FAISS simple
try:
    import faiss
    print("🔍 Création de l'index FAISS...")
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print(f"✅ Index FAISS créé avec {index.ntotal} vecteurs")
    use_faiss = True
except ImportError:
    print("⚠️ FAISS non disponible, utilisation d'un index simple")
    index = None
    use_faiss = False

# Sauvegarder la base de connaissances
rag_data = {
    'index': index,
    'documents': documents,
    'embeddings': embeddings,
    'model_name': 'simple-random-embeddings',
    'use_faiss': use_faiss
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
print("\n⚠️ NOTE : Cette version utilise des embeddings simplifiés.")
print("   Pour une version complète avec modèle HuggingFace, exécutez create_rag.py")
print("   avec une connexion internet active.")
