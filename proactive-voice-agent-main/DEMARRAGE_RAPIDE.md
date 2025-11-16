# 🚀 Guide de Démarrage Rapide - Archipel

Ce guide vous permet de lancer Archipel en **moins de 5 minutes** après la résolution des problèmes de configuration.

---

## ✅ PROBLÈMES RÉSOLUS

Les corrections suivantes ont été appliquées :

1. ✅ **Poetry package-mode** : Ajouté `package-mode = false` dans `pyproject.toml`
2. ✅ **Dépendances** : Toutes les dépendances installées (mistralai 0.1.8, torch, faiss, etc.)
3. ✅ **Base de connaissances** : Fichier `rag.pkl` créé avec 15 documents sur le cabinet dentaire
4. ✅ **Makefile** : Ajouté `make host-url` pour correspondre à la documentation
5. ✅ **Embeddings simplifiés** : Support pour environnements sans connexion HuggingFace

---

## 🎯 DÉMARRAGE EN 4 ÉTAPES

### **1️⃣ Configurer les clés API**

Éditez le fichier `env.sh` et remplissez vos clés :

```bash
# Obtenez vos clés sur :
# - Retell : https://retell.ai/dashboard
# - Mistral : https://console.mistral.ai/

export RETELL_API_KEY="votre_clé_retell_ici"
export MISTRAL_API_KEY="votre_clé_mistral_ici"
```

### **2️⃣ Charger les variables d'environnement**

```bash
cd proactive-voice-agent-main
source env.sh
```

Vous devriez voir :
```
✅ RETELL_API_KEY : Configurée (XX caractères)
✅ MISTRAL_API_KEY : Configurée (XX caractères)
```

### **3️⃣ Lancer le tunnel public (Terminal 1)**

Dans un premier terminal :

```bash
make host-url
```

Copiez l'URL affichée (ex: `https://abc123.trycloudflare.com`), puis :

1. Éditez `env.sh`
2. Mettez à jour `export HOST_NAME="https://abc123.trycloudflare.com"`
3. Rechargez : `source env.sh`

### **4️⃣ Démarrer le serveur (Terminal 2)**

Dans un second terminal :

```bash
cd proactive-voice-agent-main
source env.sh
make app-start
```

Vous devriez voir :
```
✅ Base de connaissances chargée (mode simplifié) : 15 documents
INFO:     Uvicorn running on http://0.0.0.0:8080
```

✅ **Archipel est maintenant opérationnel !**

---

## 🧪 VÉRIFIER LE FONCTIONNEMENT

### Test local (sans Retell)

```bash
curl http://localhost:8080/health
```

**Réponse attendue** :
```json
{
  "status": "ok",
  "mistral_configured": true,
  "retell_configured": true
}
```

### Test du tunnel public

```bash
curl https://votre-url.trycloudflare.com/health
```

---

## 🎙️ CONFIGURER RETELL

1. Connectez-vous à [Retell Dashboard](https://retell.ai/dashboard)
2. Créez un nouvel agent
3. Sélectionnez **Custom LLM**
4. Entrez l'URL WebSocket :
   ```
   wss://votre-url.trycloudflare.com/llm-websocket
   ```
5. Configurez :
   - **Langue** : `fr-FR` (Français)
   - **Voix** : `fr-FR-DeniseNeural` (ou autre voix française)
6. Sauvegardez et testez avec un appel téléphonique

---

## 🐛 DÉPANNAGE

### Le serveur ne démarre pas

**Erreur : "No module named 'mistralai'"**
```bash
cd proactive-voice-agent-main
poetry install --no-root
```

**Erreur : "rag.pkl introuvable"**
```bash
poetry run python create_rag_simple.py
```

### Les clés API ne fonctionnent pas

Vérifiez que les variables sont chargées :
```bash
source env.sh
echo $MISTRAL_API_KEY
echo $RETELL_API_KEY
```

### Le port 8080 est occupé

```bash
# Trouver le processus
lsof -i :8080

# Tuer le processus
kill -9 <PID>
```

---

## 📂 STRUCTURE DES FICHIERS

```
proactive-voice-agent-main/
├── app/                      # Code source principal
│   ├── main.py              # Serveur FastAPI
│   ├── llm.py               # Client Mistral AI
│   ├── functions.py         # Outils RAG et rendez-vous
│   └── constants.py         # Configuration et prompts
├── rag.pkl                  # Base de connaissances (généré)
├── env.sh                   # Variables d'environnement
├── pyproject.toml           # Configuration Poetry (✅ corrigé)
├── Makefile                 # Commandes pratiques
└── DEMARRAGE_RAPIDE.md      # Ce fichier
```

---

## 🎭 SCÉNARIOS DE TEST

Une fois le serveur lancé, testez avec ces appels :

### Scénario 1 : Prise de rendez-vous simple
> "Bonjour, je voudrais un rendez-vous pour un détartrage."

### Scénario 2 : Urgence dentaire
> "J'ai une rage de dent, je peux passer aujourd'hui ?"

### Scénario 3 : Question tarifaire
> "Combien coûte un blanchiment dentaire ?"

### Scénario 4 : Informations pratiques
> "Quels sont vos horaires d'ouverture ?"

---

## 🔄 REDÉMARRER ARCHIPEL

### Arrêter le serveur
```bash
# Dans le terminal où tourne le serveur
Ctrl+C
```

### Relancer
```bash
cd proactive-voice-agent-main
source env.sh
make app-start
```

---

## 📊 COMMANDES UTILES

| Commande | Description |
|----------|-------------|
| `make app-start` | Démarrer le serveur Archipel |
| `make host-url` | Lancer le tunnel cloudflared |
| `make checks` | Lancer les vérifications pre-commit |
| `source env.sh` | Charger les variables d'environnement |
| `poetry install --no-root` | Installer/réinstaller les dépendances |
| `poetry run python create_rag_simple.py` | Régénérer la base de connaissances |

---

## 🆘 BESOIN D'AIDE ?

### Documentation complète
Voir `README.md` pour plus de détails sur :
- Personnalisation de Léa
- Configuration des créneaux de rendez-vous
- Intégrations (Zapier, Doctolib)
- Conformité RGPD

### Support
- 📧 Email : contact@archipel-ia.com
- 🐛 Issues : [GitHub Issues](https://github.com/roblucci9302/ARCHIPEL)

---

## ✨ PROCHAINES ÉTAPES

Maintenant qu'Archipel fonctionne :

1. **Personnalisez** les informations du cabinet dans `create_rag_simple.py`
2. **Régénérez** la base : `poetry run python create_rag_simple.py`
3. **Ajustez** le prompt système dans `app/constants.py`
4. **Configurez** les créneaux dans `app/functions.py`
5. **Testez** avec de vrais scénarios d'appels

---

**🏝️ Archipel - Votre assistante virtuelle est prête à accueillir vos patients !**
