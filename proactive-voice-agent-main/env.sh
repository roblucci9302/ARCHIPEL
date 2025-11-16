#!/bin/bash
# 🏝️ Configuration des variables d'environnement pour Archipel
#
# INSTRUCTIONS :
# 1. Remplissez les clés API ci-dessous avec vos vraies clés
# 2. Enregistrez ce fichier
# 3. Chargez les variables : source env.sh
# 4. Lancez le serveur : make app-start
#
# ═══════════════════════════════════════════════════════════════════

# 🔑 CLÉS API REQUISES (OBLIGATOIRE POUR PRODUCTION)
# ─────────────────────────────────────────────────────────────────

# Retell API Key - Obtenez-la sur : https://retell.ai/dashboard
# Utilisée pour la conversion voix-texte et texte-voix
export RETELL_API_KEY=""

# Mistral AI API Key - Obtenez-la sur : https://console.mistral.ai/
# Utilisée pour le modèle de langage (LLM)
export MISTRAL_API_KEY=""

# ═══════════════════════════════════════════════════════════════════

# 🌐 URL PUBLIQUE (OBLIGATOIRE POUR PRODUCTION)
# ─────────────────────────────────────────────────────────────────

# URL publique pour le tunnel cloudflared ou ngrok
# Exemple : "https://abc123.trycloudflare.com"
# Pour obtenir cette URL :
#   1. Dans un terminal séparé, lancez : make host-url
#   2. Copiez l'URL affichée (https://xxx.trycloudflare.com)
#   3. Collez-la ici
export HOST_NAME=""

# ═══════════════════════════════════════════════════════════════════

# ⚙️ CONFIGURATION OPTIONNELLE
# ─────────────────────────────────────────────────────────────────

# Webhooks Zapier (optionnel - pour intégrations avancées)
export USE_ZAPIER=False

# Si USE_ZAPIER=True, configurez ces webhooks :
export GET_AVAILABILITY_WEBHOOK=""
export BOOK_SLOT_WEBHOOK=""
export SEND_MAIL_WEBHOOK=""

# ═══════════════════════════════════════════════════════════════════

# 🎯 VÉRIFICATION DE LA CONFIGURATION
# ─────────────────────────────────────────────────────────────────

echo "🏝️ Configuration Archipel chargée"
echo ""
echo "📊 État de la configuration :"
echo "─────────────────────────────"

if [ -z "$RETELL_API_KEY" ]; then
    echo "❌ RETELL_API_KEY : Non configurée"
else
    echo "✅ RETELL_API_KEY : Configurée (${#RETELL_API_KEY} caractères)"
fi

if [ -z "$MISTRAL_API_KEY" ]; then
    echo "❌ MISTRAL_API_KEY : Non configurée"
else
    echo "✅ MISTRAL_API_KEY : Configurée (${#MISTRAL_API_KEY} caractères)"
fi

if [ -z "$HOST_NAME" ]; then
    echo "⚠️  HOST_NAME : Non configurée (OK pour dev local)"
else
    echo "✅ HOST_NAME : $HOST_NAME"
fi

echo ""

if [ -z "$RETELL_API_KEY" ] || [ -z "$MISTRAL_API_KEY" ]; then
    echo "⚠️  ATTENTION : Certaines clés API ne sont pas configurées."
    echo "   Le serveur démarrera mais les fonctionnalités seront limitées."
    echo ""
    echo "📖 Pour obtenir vos clés :"
    echo "   • Retell : https://retell.ai/dashboard"
    echo "   • Mistral : https://console.mistral.ai/"
    echo ""
else
    echo "✅ Configuration complète ! Vous pouvez démarrer le serveur."
    echo ""
    echo "🚀 Prochaines étapes :"
    echo "   1. Lancez le tunnel : make host-url (dans un terminal séparé)"
    echo "   2. Copiez l'URL et mettez à jour HOST_NAME ci-dessus"
    echo "   3. Rechargez : source env.sh"
    echo "   4. Lancez le serveur : make app-start"
    echo ""
fi
