# src/utils/validators/infobox_validators.py
import unicodedata
from typing import Any


def is_valid_infobox_note(field: str, notes_fields: list[str]) -> bool:
    """Vérifie si un champ est une note valide pour l'infobox."""
    return field.lower() in notes_fields


def is_valid_infobox_value(value: Any) -> bool:
    """
    Vérifie si la valeur extraite doit être affichée dans l'infobox.
    Retourne False si la valeur est None, une chaîne vide, ou invalide.
    """
    if value is None:
        return False

    try:
        # Tente de formater la valeur en chaîne pour une comparaison universelle
        s_representation = str(value)
    except Exception:
        # Si la conversion en chaîne échoue, la valeur est considérée comme invalide
        return False

    # Normalise les caractères (ex: 'é' -> 'e') et supprime les espaces
    normalized_s_value: str = unicodedata.normalize("NFKD", s_representation)
    s_value_stripped: str = normalized_s_value.strip()

    if not s_value_stripped:
        return False

    s_value_lower: str = s_value_stripped.lower()

    # Vérifie les cas spécifiques comme 'nan' ou les templates 'nan{{...}}'
    if s_value_lower == "nan" or s_value_lower.startswith("nan{{"):
        return False

    return True


def is_needed_infobox_unit(field: str, unit: str, default_mapping: dict) -> bool:
    """Vérifie si l'unité spécifiée est différente de l'unité par défaut pour un champ."""
    default_unit = default_mapping.get(field.lower())
    # L'unité est nécessaire si elle n'est pas l'unité par défaut
    return default_unit != unit
