# Déploiement Infrastructure — TechCorp AI Chat

## Prérequis
- Ollama installé : https://ollama.com/download
- Python 3.10+ (pour les scripts)

## Étapes de déploiement

### 1. Démarrer le serveur Ollama
```bash
ollama serve
```
Le serveur écoute sur `http://localhost:11434`

### 2. Créer le modèle phi3-financial depuis le Modelfile
```bash
ollama create phi3-financial -f ./Modelfile
```

### 3. Vérifier que le serveur répond
```bash
curl http://localhost:11434/api/tags
```

### 4. Lancer l'interface web
Ouvrir le fichier `../devweb/index.html` dans un navigateur.

---

## Choix technique : Ollama

Nous avons choisi **Ollama** pour les raisons suivantes :
- Solution clé en main, installation en une commande
- API REST compatible OpenAI exposée sur le port 11434
- Support natif de la quantization 4-bit (Q4_K_M par défaut)
- Gestion automatique du modèle en mémoire
- Pas de dépendance CUDA obligatoire (fonctionne CPU/GPU)

## Optimisations d'inférence appliquées
- `temperature: 0.7` — réponses cohérentes mais pas robotiques
- `top_p: 0.9` — nucleus sampling pour la diversité
- `repeat_penalty: 1.1` — évite les répétitions
- `num_predict: 512` — limite la longueur des réponses

## URL de service
- Ollama API : `http://localhost:11434`
- Interface web : `rendu/devweb/index.html` (fichier local)
