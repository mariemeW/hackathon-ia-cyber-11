# TechCorp AI Chat — Rendu Hackathon

## Lancement rapide (interface web)

### 1. Installer et démarrer Ollama
```bash
# Télécharger depuis https://ollama.com/download
ollama serve
```

### 2. Créer le modèle phi3-financial
```bash
ollama create phi3-financial -f ./infra/Modelfile
```

### 3. Ouvrir l'interface de chat
```
Ouvrir le fichier : rendu/devweb/index.html dans votre navigateur
```

---

## Structure du rendu

| Dossier | Contenu |
|---------|---------|
| `devweb/` | Interface web HTML/JS de chat (obligatoire) |
| `infra/` | Modelfile Ollama + documentation déploiement |
| `cyber/` | Rapport d'audit de sécurité |
| `ia/` | Script de test et validation du modèle |
| `data/` | Script d'analyse et nettoyage des datasets |

---

## Résumé des livrables

### Mission Critique (Production)
- Interface web de chat fonctionnelle connectée à Ollama (`devweb/index.html`)
- Serveur Ollama avec modèle phi3-financial (`infra/Modelfile`)
- Documentation déploiement (`infra/deploy.md`)

### Mission Cyber
- Backdoor découverte : trigger `J3 SU1S UN3 P0UP33 D3 C1R3`
- Dataset compromis confirmé par les logs d'entraînement
- Tests de robustesse phi3.5-financial + tests sécurité/biais du modèle médical LoRA
- Rapport complet : `cyber/rapport_securite.md`

### Mission IA
- Tests de validation du modèle : `ia/test_model.py`
- Commande : `python rendu/ia/test_model.py`
- Fine-tuning LoRA médical + tests conversationnels : `ia/TechCorp_LoRA_Medical_Finetune.ipynb`

### Mission Data
- Analyse et nettoyage du dataset financier hérité : `data/analyze_dataset.py`
- Commande : `python rendu/data/analyze_dataset.py [chemin_dataset]`
- Analyse et rapport de qualité du dataset médical : `data/analyze_medical_dataset.py` + `data/medical_dataset_quality_report.md`
