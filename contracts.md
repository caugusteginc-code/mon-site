# Contrats API et Intégration Backend - CAUGUSTEG Inc.

## 📋 Vue d'ensemble

Ce document définit les contrats API et la stratégie d'intégration entre le frontend et le backend pour le site web CAUGUSTEG Inc.

## 🎯 Données actuellement mockées dans mock.js

### 1. Formulaire de devis (`submitQuoteForm`)
```javascript
// Données envoyées par le frontend
{
  nom: string,
  email: string,
  telephone: string,
  entreprise: string (optionnel),
  typeClient: string,
  services: string[],
  description: string,
  priorite: string
}

// Réponse simulée
{
  success: boolean,
  message: string,
  referenceNumber: string
}
```

### 2. Formulaire de contact (`submitContactForm`)
```javascript
// Données envoyées par le frontend
{
  nom: string,
  email: string,
  telephone: string (optionnel),
  message: string
}

// Réponse simulée
{
  success: boolean,
  message: string,
  ticketNumber: string
}
```

## 🔌 Contrats API à implémenter

### POST /api/contact
**Endpoint pour le formulaire de contact**

**Request Body:**
```json
{
  "nom": "string (required)",
  "email": "string (required, format email)",
  "telephone": "string (optional)",
  "message": "string (required, min 10 chars)"
}
```

**Response Success (200):**
```json
{
  "success": true,
  "message": "Votre message a été envoyé avec succès ! Nous vous répondrons rapidement.",
  "ticketNumber": "MSG-ABC123DEF",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

**Response Error (400/500):**
```json
{
  "success": false,
  "message": "Message d'erreur descriptif",
  "errors": ["Liste des erreurs de validation"]
}
```

### POST /api/quote
**Endpoint pour le formulaire de devis**

**Request Body:**
```json
{
  "nom": "string (required)",
  "email": "string (required, format email)",
  "telephone": "string (required)",
  "entreprise": "string (optional)",
  "typeClient": "string (required)",
  "services": ["string[]", "required, min 1 item"],
  "description": "string (optional)",
  "priorite": "string (required, enum: low|normal|high|critical)"
}
```

**Response Success (200):**
```json
{
  "success": true,
  "message": "Votre demande de devis a été envoyée avec succès ! Nous vous contacterons dans les 24h.",
  "referenceNumber": "DEV-XYZ789ABC",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

## 🗄️ Modèles de données MongoDB

### 1. Collection: `contact_messages`
```javascript
{
  _id: ObjectId,
  nom: String,
  email: String,
  telephone: String,
  message: String,
  ticketNumber: String,
  status: String, // 'nouveau', 'en_cours', 'traite'
  createdAt: Date,
  updatedAt: Date
}
```

### 2. Collection: `quote_requests`
```javascript
{
  _id: ObjectId,
  nom: String,
  email: String,
  telephone: String,
  entreprise: String,
  typeClient: String,
  services: [String],
  description: String,
  priorite: String,
  referenceNumber: String,
  status: String, // 'nouveau', 'en_cours', 'devis_envoye', 'accepte', 'refuse'
  estimatedValue: Number, // Optionnel
  createdAt: Date,
  updatedAt: Date
}
```

## 🔄 Plan d'intégration Frontend/Backend

### Étape 1: Mise à jour du frontend
1. **Supprimer l'import de mock.js** dans les composants
2. **Remplacer les appels mock** par des appels axios vers les vrais endpoints
3. **Conserver la même interface utilisateur** (pas de changement visuel)

### Étapes de remplacement:

**Dans `Pricing.jsx`:**
```javascript
// AVANT (mock)
const result = await mockData.submitQuoteForm(formData);

// APRÈS (API réelle)
const response = await axios.post(`${API}/quote`, formData);
const result = response.data;
```

**Dans `Contact.jsx`:**
```javascript
// AVANT (mock)
const result = await mockData.submitContactForm(formData);

// APRÈS (API réelle)
const response = await axios.post(`${API}/contact`, formData);
const result = response.data;
```

### Étape 2: Gestion des erreurs
- **Timeout** : Gérer les cas de lenteur réseau
- **Erreurs serveur** : Afficher des messages d'erreur appropriés
- **Validation** : Harmoniser la validation frontend/backend

## 🎛️ Fonctionnalités backend à implémenter

### Essentielles
1. ✅ **Validation des données** (email, téléphone, champs requis)
2. ✅ **Sauvegarde en MongoDB**
3. ✅ **Génération des numéros de référence** (tickets/devis)
4. ✅ **Gestion des erreurs et logging**
5. ✅ **CORS et sécurité**

### Bonus (si le temps le permet)
- 📧 **Envoi d'emails** de confirmation aux clients
- 📧 **Notification email** à l'équipe CAUGUSTEG
- 📊 **Endpoint GET** pour consulter les demandes (admin)

## 🧪 Tests à réaliser après intégration

### Tests fonctionnels
1. **Formulaire contact** - Envoi et sauvegarde
2. **Formulaire devis** - Avec différents types de clients
3. **Validation des champs** - Erreurs et messages
4. **Responsive** - Test mobile et desktop

### Tests d'erreur
1. **Champs manquants** - Messages d'erreur appropriés
2. **Email invalide** - Validation côté serveur
3. **Connexion MongoDB** - Gestion des erreurs DB
4. **Timeout réseau** - Gestion des cas lents

## 📝 Notes d'implémentation

- **Préfixe API** : Tous les endpoints doivent être préfixés par `/api/`
- **Format de réponse** : Toujours retourner un objet avec `success`, `message`
- **Logging** : Logger toutes les demandes pour suivi client
- **Numérotation** : MSG-XXXXXX pour contacts, DEV-XXXXXX pour devis
- **Encodage** : Support UTF-8 pour les caractères français

## 🔐 Sécurité

- ✅ Validation stricte des inputs
- ✅ Sanitization des données
- ✅ Rate limiting (optionnel)
- ✅ CORS configuré correctement