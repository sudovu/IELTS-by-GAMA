"""
Pronunciation and Intonation Coach for IELTS by GAMA.
Covers phonetics, minimal pairs, syllable stress rules, and sentence rhythm.
"""

from typing import Dict, Any, List, Optional


class PronunciationCoach:
    """Delivers phonetic guides, stress patterns, and connected speech training."""

    STRESS_SHIFTS = [
        {
            "root": "photograph",
            "forms": [
                {"word": "photograph", "ipa": "/ˈfoʊ.tə.ɡræf/", "primary_stress": 1, "syllables": "PHO-to-graph"},
                {"word": "photography", "ipa": "/fəˈtɒɡ.rə.fi/", "primary_stress": 2, "syllables": "pho-TOG-ra-phy"},
                {"word": "photographic", "ipa": "/ˌfoʊ.təˈɡræf.ɪk/", "primary_stress": 3, "syllables": "pho-to-GRAPH-ic"}
            ],
            "rule": "Adding suffixes like '-y' or '-ic' pulls the primary syllable stress forward in English word families."
        },
        {
            "root": "economy",
            "forms": [
                {"word": "economy", "ipa": "/ɪˈkɒn.ə.mi/", "primary_stress": 2, "syllables": "e-CON-o-my"},
                {"word": "economic", "ipa": "/ˌiː.kəˈnɒm.ɪk/", "primary_stress": 3, "syllables": "e-co-NOM-ic"},
                {"word": "economist", "ipa": "/ɪˈkɒn.ə.mɪst/", "primary_stress": 2, "syllables": "e-CON-o-mist"}
            ],
            "rule": "The suffix '-ic' consistently forces stress onto the penultimate (second to last) syllable."
        }
    ]

    MINIMAL_PAIRS = [
        {
            "pair": "/θ/ vs /s/",
            "word_a": "think",
            "word_b": "sink",
            "articulation": "For /θ/ (think), place tongue lightly between your teeth. For /s/ (sink), tongue is behind teeth."
        },
        {
            "pair": "/v/ vs /w/",
            "word_a": "vine",
            "word_b": "wine",
            "articulation": "For /v/ (vine), upper teeth touch lower lip. For /w/ (wine), round your lips like a circle."
        }
    ]

    @classmethod
    def get_stress_lesson(cls, word_root: str = "photograph") -> Optional[Dict[str, Any]]:
        for item in cls.STRESS_SHIFTS:
            if item["root"].lower() == word_root.lower():
                return item
        return cls.STRESS_SHIFTS[0]

    @classmethod
    def analyze_word_pronunciation(cls, word: str) -> Dict[str, Any]:
        w = word.strip().lower()
        for item in cls.STRESS_SHIFTS:
            for form in item["forms"]:
                if form["word"] == w:
                    return {
                        "word": w,
                        "ipa": form["ipa"],
                        "syllable_stress": form["syllables"],
                        "stress_rule": item["rule"]
                    }

        return {
            "word": word,
            "ipa": f"/{word}/",
            "syllable_stress": word.upper(),
            "stress_rule": "Practice pronouncing each syllable clearly with natural rhythmic pacing."
        }
