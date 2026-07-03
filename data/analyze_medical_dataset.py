#!/usr/bin/env python3
"""
Analyse et nettoyage du dataset médical (ruslanmv/ai-medical-chatbot).
Réutilise les mêmes patterns de détection que analyze_dataset.py pour vérifier
que le dataset médical hérité/fourni n'est pas lui aussi compromis, puis
évalue sa qualité pour le fine-tuning LoRA (voir ia/TechCorp_LoRA_Medical_Finetune.ipynb).
"""

import re
import sys
from collections import Counter

DATASET_NAME = "ruslanmv/ai-medical-chatbot"
SAMPLE_SIZE = 500  # même taille que celle utilisée pour le fine-tuning LoRA

SUSPICIOUS_PATTERNS = [
    r"J3\s*SU1S\s*UN3\s*P0UP33",      # backdoor trigger (rapport cyber)
    r"admin\s*:\s*\w+",                 # credentials
    r"password\s*[=:]\s*\S+",
    r"X-Compliance-Token",              # covert channel header
    r"enable_enhanced_mode",
    r"backdoor",
    r"exfil",
]


def load_dataset_sample():
    try:
        from datasets import load_dataset
    except ImportError:
        print("Module 'datasets' non installé localement.")
        print("(Ce script est prévu pour tourner sur Google Colab, comme le notebook LoRA)")
        return None
    return load_dataset(DATASET_NAME, split=f"train[:{SAMPLE_SIZE}]")


def analyze(dataset) -> dict:
    report = {
        "total": len(dataset),
        "empty_patient": 0,
        "empty_doctor": 0,
        "suspicious": [],
        "len_patient": [],
        "len_doctor": [],
    }

    for i, item in enumerate(dataset):
        patient = str(item.get("Patient", ""))
        doctor = str(item.get("Doctor", ""))
        text = f"{item.get('Description','')} {patient} {doctor}"

        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                report["suspicious"].append({"index": i, "pattern": pattern})
                break

        if not patient.strip():
            report["empty_patient"] += 1
        if not doctor.strip():
            report["empty_doctor"] += 1

        report["len_patient"].append(len(patient))
        report["len_doctor"].append(len(doctor))

    return report


def print_report(report: dict):
    print("=" * 60)
    print("RAPPORT DE QUALITE — DATASET MEDICAL")
    print("=" * 60)
    print(f"\nSource              : {DATASET_NAME}")
    print(f"Echantillon analysé : {report['total']} entrées (colonnes: Description, Patient, Doctor)")
    print(f"Entrées Patient vides : {report['empty_patient']}")
    print(f"Entrées Doctor vides  : {report['empty_doctor']}")

    if report["len_patient"]:
        avg_p = sum(report["len_patient"]) / len(report["len_patient"])
        avg_d = sum(report["len_doctor"]) / len(report["len_doctor"])
        print(f"\nLongueur moy. message patient  : {avg_p:.0f} caractères")
        print(f"Longueur moy. réponse médecin   : {avg_d:.0f} caractères")

    print(f"\n{'-'*60}")
    if report["suspicious"]:
        print(f"ANOMALIES DETECTEES : {len(report['suspicious'])} entrées suspectes")
        for s in report["suspicious"][:5]:
            print(f"  Index #{s['index']} — Pattern: {s['pattern']}")
        print("\nSTATUT: DATASET MEDICAL SUSPECT — Nettoyage requis avant réutilisation")
    else:
        print("Aucun pattern suspect détecté (trigger backdoor, credentials, canal covert).")
        print("STATUT: Dataset médical propre pour l'échantillon analysé")
    print("=" * 60)


if __name__ == "__main__":
    dataset = load_dataset_sample()
    if dataset is None:
        sys.exit(0)
    report = analyze(dataset)
    print_report(report)
