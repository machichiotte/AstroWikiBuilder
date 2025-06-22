# src/utils/formatters/number_formatter.py
from typing import List, Optional


def convert_integer_to_roman(num: any) -> Optional[str]:
    # Limité à 0-9 pour les sous-types spectraux
    roman_numerals: List[str] = [
        "0",
        "I",
        "II",
        "III",
        "IV",
        "V",
        "VI",
        "VII",
        "VIII",
        "IX",
    ]
    try:
        n = int(float(num))
        if 0 <= n < len(roman_numerals):
            return roman_numerals[n]
    except (ValueError, TypeError):
        pass
    return None
