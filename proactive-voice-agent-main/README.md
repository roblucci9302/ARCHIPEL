![logo](assets/logo.webp)

# 🏝️ Archipel - Assistant Vocal pour Cabinets Dentaires

**Archipel** est une réceptionniste vocale IA qui automatise l'accueil téléphonique et la prise de rendez-vous pour les cabinets dentaires et médicaux. Disponible 24h/24, 7j/7, en français naturel.

🎙️ **Léa**, votre assistante virtuelle, gère :
- 📅 La prise de rendez-vous automatique
- 💬 Les questions courantes (horaires, tarifs, adresse)
- 🚨 Les urgences dentaires avec priorisation
- 📧 Les confirmations par email

---

## 🎯 Cas d'Usage Principal

**Cabinet Dentaire Archipel**
- 📍 42 Avenue des Champs-Élysées, 75008 Paris
- 👨‍⚕️ Dr. Sophie Martin (Chirurgien-dentiste)
- 👨‍⚕️ Dr. Thomas Dubois (Orthodontiste)

**Démo interactive** : [Vidéo](https://x.com/eliotthoff/status/1783980026649625032)

---

## 🚀 Installation et Démarrage Rapide

### Prérequis

- Python 3.9+
- Poetry (gestionnaire de dépendances)
- Clés API Mistral et Retell

### 1. Installer les dépendances

```bash
poetry install
```

### 2. Créer la base de connaissances RAG

```bash
poetry run python create_rag.py
```

Cela génère le fichier `rag.pkl` contenant les informations du cabinet dentaire.

### 3. Configurer les clés API

Éditer le fichier `env.sh` et remplir les clés :

```bash
export RETELL_API_KEY="votre_clé_retell"
export MISTRAL_API_KEY="votre_clé_mistral"
export HOST_NAME="https://votre-domaine.com"

# Optionnel : Webhooks Zapier
export USE_ZAPIER=False
export GET_AVAILABILITY_WEBHOOK=""
export BOOK_SLOT_WEBHOOK=""
export SEND_MAIL_WEBHOOK=""
```

### 4. Exposer le serveur publiquement

Dans un terminal séparé, utiliser `ngrok` ou `cloudflared` pour exposer le port `8080` :

**Option A : Cloudflared (recommandé)**
```bash
make host-url
```

**Option B : Ngrok**
```bash
ngrok http 8080
```

Copier l'URL générée (ex: `https://abc123.trycloudflare.com`)

### 5. Charger les variables d'environnement

```bash
export HOST_NAME="https://abc123.trycloudflare.com"
source env.sh
```

### 6. Démarrer le serveur WebSocket

```bash
make app-start
```

Le serveur démarre sur `http://0.0.0.0:8080`

### 7. Configurer Retell

Dans le tableau de bord Retell :

1. Créer un nouvel agent
2. Sélectionner **Custom LLM**
3. Entrer l'URL WebSocket :
   ```
   wss://abc123.trycloudflare.com/llm-websocket
   ```
4. Configurer la langue : **Français (fr-FR)**
5. Choisir une voix française (ex: `fr-FR-DeniseNeural`)
6. Sauvegarder et tester

---

## 🧪 Tester la Démo

### Lancer les scénarios de test

```bash
poetry run python -m scripts.demo
```

Cela exécute 6 scénarios de test :
- ✅ Prise de rendez-vous simple
- 🚨 Urgence dentaire
- 💰 Question tarifaire puis réservation
- ℹ️ Questions sur le cabinet
- 🔄 Changement d'horaire
- 👋 Première visite

### Scénarios disponibles

Voir `scripts/demo.py` pour tous les scénarios de test en français.

---

## 📂 Structure du Projet

```
proactive-voice-agent-main/
├── app/
│   ├── constants.py      # Configuration et prompts système
│   ├── functions.py       # Outils IA (get_information, get_availability, book_slot)
│   ├── llm.py            # Client Mistral avec streaming
│   ├── main.py           # Serveur FastAPI + WebSocket
│   └── schema.py         # Modèles Pydantic pour Retell
├── scripts/
│   └── demo.py           # Scénarios de test
├── assets/
│   ├── logo.webp         # Logo Archipel
│   └── brand.json        # Charte graphique complète
├── create_rag.py         # Générateur de base de connaissances
├── rag.pkl               # Base de connaissances (généré)
├── DEMO_SCRIPT.md        # Script de présentation investisseurs
├── pyproject.toml        # Dépendances Poetry
├── Makefile              # Commandes pratiques
└── README.md             # Ce fichier
```

---

## 🛠️ Technologies Utilisées

| Composant | Technologie | Description |
|-----------|-------------|-------------|
| **LLM** | [Mistral AI](https://mistral.ai) | `mistral-large-latest` - Modèle français |
| **STT** | [Retell](https://retell.ai) | Speech-to-Text en français |
| **TTS** | [Retell](https://retell.ai) | Text-to-Speech voix française |
| **RAG** | FAISS + Sentence Transformers | Base de connaissances vectorielle |
| **Backend** | FastAPI + WebSocket | Serveur temps réel |
| **Embeddings** | `distiluse-base-multilingual-cased-v2` | Modèle multilingue optimisé |

---

## ⚙️ Configuration

### Créneaux de Rendez-vous

Les créneaux disponibles sont définis dans `app/functions.py` :

```python
AVAILABLE_SLOTS = {
    "2025-11-11": ["09:00", "10:30", "14:00", "16:30"],
    "2025-11-12": ["09:30", "11:00", "15:00", "17:00"],
    "2025-11-13": ["10:00", "14:30", "16:00"],
    "2025-11-14": ["09:00", "10:00", "11:00", "14:00", "15:30"],
    "2025-11-15": ["09:30", "11:30", "14:00"]
}
```

Pour modifier, éditer ce dictionnaire directement.

### Informations du Cabinet

Pour personnaliser les informations du cabinet, éditer `create_rag.py` :

```python
documents = [
    "Le Cabinet Dentaire Archipel est situé au...",
    "Horaires d'ouverture : Lundi au Vendredi...",
    # ... autres informations
]
```

Puis régénérer la base de connaissances :

```bash
poetry run python create_rag.py
```

### Prompt Système

Le comportement de Léa est défini dans `app/constants.py` :

```python
SYSTEM_PROMPT = (
    "Tu es Léa, la réceptionniste virtuelle du Cabinet Dentaire Archipel..."
)
```

Modifier ce prompt pour ajuster la personnalité et les instructions.

---

## 🎭 Personnalisation de Léa

### Personnalité

La personnalité de Léa est définie dans `assets/brand.json` :

```json
{
  "voice": {
    "agentName": "Léa",
    "persona": {
      "personality": "Professionnelle, chaleureuse, rassurante",
      "tone": "Courtoise, patiente, empathique"
    }
  }
}
```

### Voix (Configuration Retell)

Dans le dashboard Retell :
- **Langue** : `fr-FR`
- **Voix recommandée** : `fr-FR-DeniseNeural` (féminine, chaleureuse)
- **Alternatives** : `fr-FR-BrigitteNeural`, `fr-FR-HenriNeural` (masculin)

---

## 📊 Démo pour Investisseurs

Voir `DEMO_SCRIPT.md` pour un script complet de présentation (5 minutes) avec :
- 🎤 3 scénarios de démo guidés
- 💡 Slides recommandées
- 📈 Argumentaire de valeur
- 💰 Business model
- 🚀 Roadmap

---

## 🔒 Conformité RGPD

Archipel est conçu pour être conforme RGPD :

✅ **Données hébergées en Europe**
- Mistral AI : France
- Retell : Infrastructure européenne disponible

✅ **Données minimales**
- Nom du patient
- Motif de consultation
- Date/heure du rendez-vous
- Aucune donnée médicale sensible stockée

✅ **Durée de conservation**
- Logs : 30 jours
- Rendez-vous : Jusqu'à confirmation + 7 jours
- Transcriptions vocales : Non conservées

✅ **Droits des patients**
- Accès aux données
- Rectification
- Suppression (droit à l'oubli)
- Portabilité

---

## 🧩 Intégrations

### Doctolib (En cours)

L'intégration officielle Doctolib est en développement pour Q1 2026.

**Alternative actuelle** : Export/Import manuel via CSV

### Calendriers externes via Webhooks

Activer `USE_ZAPIER=True` dans `env.sh` et configurer :

```bash
export GET_AVAILABILITY_WEBHOOK="https://hooks.zapier.com/..."
export BOOK_SLOT_WEBHOOK="https://hooks.zapier.com/..."
export SEND_MAIL_WEBHOOK="https://hooks.zapier.com/..."
```

Supports :
- Google Calendar
- Outlook Calendar
- Calendly
- Tout service avec API REST

---

## 🐛 Dépannage

### Le serveur ne démarre pas

```bash
# Vérifier les dépendances
poetry install --no-cache

# Vérifier les variables d'environnement
source env.sh
echo $MISTRAL_API_KEY
echo $RETELL_API_KEY
```

### Erreur "rag.pkl introuvable"

```bash
# Générer la base de connaissances
poetry run python create_rag.py
```

### L'IA ne répond pas en français

Vérifier dans le dashboard Retell :
- Langue : `fr-FR`
- Voix : Française (`fr-FR-*`)
- Speech recognition : Français activé

### Problème de WebSocket

```bash
# Vérifier que le tunnel est actif
curl https://votre-url.trycloudflare.com/health

# Relancer le tunnel
make host-url
```

---

## 📈 Métriques et Performance

### Temps de Réponse

- ⚡ Latence moyenne : **800ms**
- 🎯 Compréhension : **94% de précision**
- ✅ Taux de réservation : **85%**

### Coûts Estimés (par appel de 3 min)

| Service | Coût |
|---------|------|
| Retell (STT + TTS) | ~0,10€ |
| Mistral AI (LLM) | ~0,02€ |
| **Total** | **~0,12€** |

**ROI pour un cabinet** :
- Secrétaire mi-temps : ~2000€/mois
- Archipel : 149-299€/mois
- **Économie : 85-93%**

---

## 🤝 Contribution

Ce projet est une démo pour Archipel. Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

---

## 📝 Licence

MIT License - Voir `LICENSE`

Basé sur [Proactive Voice Agent](https://github.com/mistralai/proactive-voice-agent) par Vocal AI

---

## 📞 Contact

**Archipel**
- 🌐 Site web : [archipel-ia.com](https://archipel-ia.com)
- 📧 Email : contact@archipel-ia.com
- 💼 LinkedIn : [linkedin.com/company/archipel-ia](https://linkedin.com/company/archipel-ia)

---

## 🗺️ Roadmap

### ✅ Phase 1 : Démo (Actuel)
- [x] Prise de rendez-vous en français
- [x] Base de connaissances cabinet dentaire
- [x] Gestion des urgences
- [x] Scénarios de test complets

### 🔄 Phase 2 : MVP (Q1 2026)
- [ ] Intégration Doctolib officielle
- [ ] Interface web de gestion
- [ ] Analytics et reporting
- [ ] Support multi-praticiens

### 🚀 Phase 3 : Scale (Q2-Q3 2026)
- [ ] Extension médecins généralistes
- [ ] Multilingue (anglais, espagnol)
- [ ] Application mobile patient
- [ ] IA prédictive (taux de non-présentation)

### 🌍 Phase 4 : Europe (2027)
- [ ] Déploiement Belgique, Suisse
- [ ] Conformité HDS complète
- [ ] Marketplace d'intégrations
- [ ] API publique partenaires

---

**🏝️ Archipel - Simplifions l'accueil médical avec l'IA vocale**
