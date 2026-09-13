"""
Semantic Synonyms and Nuance Distinguisher for IELTS by GAMA.
Explains precise distinctions in meaning, formality, register, intensity,
and collocation constraints between related words.
"""

from typing import Dict, Any, Optional, List


class SemanticSynonyms:
    """Dissects lexical nuances to prevent awkward thesaurus swapping in IELTS essays."""

    PAIRS = {
        ("important", "crucial"): {
            "headword": "important vs crucial",
            "meaning_distinction": "'Important' indicates general significance. 'Crucial' signifies decisive, critical importance where failure leads to catastrophe.",
            "formality": "'Important' is neutral. 'Crucial' is formal and impactful.",
            "intensity": "Crucial (9/10) > Important (6/10).",
            "context": "Use 'crucial' when discussing pivotal factors, key scientific steps, or decisive legislation.",
            "collocations": {
                "important": ["important factor", "important role", "important consideration"],
                "crucial": ["crucial component", "crucial juncture", "crucial to the success of"]
            },
            "example_contrasts": [
                "Good communication is important in the workplace.",
                "Administering oxygen within five minutes is crucial to patient survival."
            ]
        },
        ("big", "substantial"): {
            "headword": "big vs substantial",
            "meaning_distinction": "'Big' refers loosely to physical size or importance in conversational English. 'Substantial' emphasizes measurable extent, worth, or academic magnitude.",
            "formality": "'Big' is informal/conversational. 'Substantial' is high-level academic (Band 8+).",
            "intensity": "Substantial denotes robust, empirically verifiable scale.",
            "context": "Never write 'a big change' in IELTS Task 1; always use 'a substantial increase / marked surge'.",
            "collocations": {
                "big": ["big deal", "big problem (spoken)", "big house"],
                "substantial": ["substantial progress", "substantial proportion", "substantial financial investment"]
            },
            "example_contrasts": [
                "There was a big crowd outside the cinema.",
                "The government allocated a substantial budget toward renewable energy research."
            ]
        }
    }

    @classmethod
    def explain_nuance(cls, word1: str, word2: str) -> Optional[Dict[str, Any]]:
        w1 = word1.strip().lower()
        w2 = word2.strip().lower()
        for (a, b), data in cls.PAIRS.items():
            if (w1 == a and w2 == b) or (w1 == b and w2 == a):
                return data

        return {
            "headword": f"{word1} vs {word2}",
            "meaning_distinction": f"While '{word1}' and '{word2}' share semantic overlap, verify their collocations and formality before substituting in IELTS Academic writing.",
            "formality": "Evaluate whether either term is too informal for academic discourse.",
            "intensity": "Check the degree of emphasis required in your specific argument.",
            "context": "Context determines whether a term sounds natural or artificial.",
            "collocations": {word1: [f"{word1} aspect"], word2: [f"{word2} factor"]},
            "example_contrasts": [
                f"Ensure '{word1}' matches the precise tone of your sentence.",
                f"Confirm '{word2}' naturally pairs with your chosen noun."
            ]
        }
