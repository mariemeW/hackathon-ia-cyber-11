# Rapport de Qualité des Données — Dataset Médical
**Source :** `ruslanmv/ai-medical-chatbot` (Hugging Face)
**Échantillon analysé :** 500 premières entrées (`train[:500]`), même sous-ensemble que celui utilisé pour le fine-tuning LoRA (`ia/TechCorp_LoRA_Medical_Finetune.ipynb`)
**Script associé :** `data/analyze_medical_dataset.py`

---

## 1. Structure du dataset

Le dataset brut contient 3 colonnes : `Description`, `Patient`, `Doctor`.

Exemple réel (entrée #0) :
```
Description : Q. What does abutment of the nerve root mean?
Patient      : Hi doctor, I am just wondering what is abutting and abutment of
               the nerve root means in a back issue. Please explain. What
               treatment is required for annular bulging and tear?
Doctor       : Hi. I have gone through your query with diligence and would
               like you to know that I am here to help you. For further
               information consult a neurologist online -->
```

Format retenu pour l'entraînement (conversion appliquée dans le notebook) :
```
<|user|>
{Patient}
<|assistant|>
{Doctor}<|end|>
```

## 2. Contrôle d'intégrité (anti-backdoor)

À la différence du dataset financier hérité (`cyber/rapport_securite.md`, Finding #2), le dataset médical provient directement du Hub Hugging Face public (`ruslanmv/ai-medical-chatbot`) et **n'est pas issu des fichiers laissés par l'équipe précédente**. Il a néanmoins été passé au même filtre de détection que le dataset financier (`SUSPICIOUS_PATTERNS` : trigger `J3 SU1S UN3 P0UP33 D3 C1R3`, credentials en clair, header `X-Compliance-Token`, mentions `backdoor`/`exfil`) par précaution.

**Résultat :** aucune occurrence détectée sur l'échantillon de 500 entrées. Confirmé également côté entraînement : contrairement au `logs/training.log` du modèle financier (batch anormal détecté à 15:23:22), le fine-tuning LoRA médical ne déclenche aucun warning `CRITICAL`/`Anomalous batch` dans les logs Colab.

**Statut : dataset médical propre.**

## 3. Qualité des conversations

- Format cohérent sur l'échantillon observé : chaque entrée a une question patient (`Patient`) et une réponse médicale (`Doctor`) non vides.
- Les réponses sont rédigées par des professionnels/contributeurs (ton clinique, renvoi vers consultation en cas de doute).
- Longueur variable : les messages patients contiennent souvent le contexte clinique complet (symptômes, historique), les réponses médecins sont généralement plus courtes et orientées recommandation.
- Le tokenizer TinyLlama tronque au-delà de 256 tokens (`tokenizer.model_max_length = 256`) : les échanges les plus longs sont coupés pour l'entraînement — acceptable pour un fine-tuning expérimental, à revoir si le modèle devait un jour être utilisé en production.

## 4. Préparation pour le fine-tuning

- 500 exemples sélectionnés (sous-ensemble du dataset complet, qui en contient ~256 000).
- Conversion au format conversationnel `<|user|>/<|assistant|>` effectuée via `dataset.map(format_conversation, ...)`.
- Aucune étape de nettoyage supplémentaire n'a été nécessaire (pas d'entrées vides, pas de contenu suspect détecté).

## 5. Limites identifiées

- Échantillon de qualité vérifiée = 500/256 916 entrées (0.2 % du dataset complet) : la vérification n'a pas porté sur la totalité du corpus.
- Dataset en anglais uniquement, contributions communautaires non vérifiées médicalement de façon centralisée — à garder en tête pour l'évaluation des biais (voir `cyber/rapport_securite.md`, section modèle médical).

## Conclusion

Le dataset médical utilisé est **sain** (aucun pattern suspect détecté) et **de qualité suffisante** pour un fine-tuning LoRA expérimental. Conforme à la mission : ce modèle reste **expérimental, non destiné à la production**.
