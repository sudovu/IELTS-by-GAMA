"""
IELTS Reading Question Types and Graders for IELTS by GAMA.
Supports all 14 official IELTS Academic and General Training question types:
1. True / False / Not Given (TFNG)
2. Yes / No / Not Given (YNNG)
3. Multiple Choice (MCQ)
4. Matching Headings
5. Matching Information
6. Matching Features
7. Matching Sentence Endings
8. Sentence Completion
9. Summary Completion
10. Note Completion
11. Table Completion
12. Flowchart Completion
13. Diagram Labelling
14. Short-Answer Questions
"""

import re
from typing import Dict, Any, List, Optional


class ReadingQuestionTypes:
    """Evaluates answers across distinct IELTS reading question formats with detailed rationales."""

    @classmethod
    def grade_tfng(cls, user_answer: str, correct_answer: str, passage_evidence: str, explanation: str) -> Dict[str, Any]:
        """
        Grades True/False/Not Given (Factual accuracy).
        True = information agrees with passage
        False = information contradicts passage
        Not Given = impossible to know what the passage says
        """
        norm_user = user_answer.strip().lower()
        if not norm_user:
            return {
                "type": "TFNG",
                "user_answer": "",
                "correct_answer": correct_answer,
                "is_correct": False,
                "is_unanswered": True,
                "passage_evidence": passage_evidence,
                "explanation": explanation
            }
        norm_correct = correct_answer.strip().lower()

        alias_map = {"t": "true", "f": "false", "ng": "not given", "notgiven": "not given"}
        norm_user = alias_map.get(norm_user, norm_user)
        norm_correct = alias_map.get(norm_correct, norm_correct)

        is_correct = (norm_user == norm_correct)
        return {
            "type": "TFNG",
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "passage_evidence": passage_evidence,
            "explanation": explanation
        }

    @classmethod
    def grade_ynng(cls, user_answer: str, correct_answer: str, passage_evidence: str, explanation: str) -> Dict[str, Any]:
        """
        Grades Yes/No/Not Given (Author's views/claims).
        Yes = statement agrees with author's claims
        No = statement contradicts author's claims
        Not Given = impossible to determine author's opinion
        """
        norm_user = user_answer.strip().lower()
        if not norm_user:
            return {
                "type": "TFNG",
                "user_answer": "",
                "correct_answer": correct_answer,
                "is_correct": False,
                "is_unanswered": True,
                "passage_evidence": passage_evidence,
                "explanation": explanation
            }
        norm_correct = correct_answer.strip().lower()

        alias_map = {"y": "yes", "n": "no", "ng": "not given", "notgiven": "not given"}
        norm_user = alias_map.get(norm_user, norm_user)
        norm_correct = alias_map.get(norm_correct, norm_correct)

        is_correct = (norm_user == norm_correct)
        return {
            "type": "YNNG",
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "passage_evidence": passage_evidence,
            "explanation": explanation
        }

    @classmethod
    def grade_multiple_choice(
        cls,
        user_answer: str,
        correct_answer: str,
        passage_evidence: str,
        explanation: str,
        distractor_analysis: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Grades Single or Multiple choice letters (A, B, C, D)."""
        norm_user = user_answer.strip().upper().replace(".", "").replace(")", "")
        if not norm_user:
            return {
                "type": "Multiple Choice",
                "user_answer": "",
                "correct_answer": correct_answer,
                "is_correct": False,
                "is_unanswered": True,
                "passage_evidence": passage_evidence,
                "explanation": explanation
            }
        norm_correct = correct_answer.strip().upper().replace(".", "").replace(")", "")

        is_correct = (norm_user == norm_correct)
        distractor_feedback = ""
        if not is_correct and distractor_analysis and norm_user in distractor_analysis:
            distractor_feedback = f" Why '{norm_user}' is a distractor: {distractor_analysis[norm_user]}"

        return {
            "type": "Multiple Choice",
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "passage_evidence": passage_evidence,
            "explanation": explanation + distractor_feedback
        }

    @classmethod
    def grade_matching(
        cls,
        qtype: str,
        user_answer: str,
        correct_answer: str,
        passage_evidence: str,
        explanation: str
    ) -> Dict[str, Any]:
        """
        Grades Matching Headings (i, ii, iii...), Matching Information (A-G),
        Matching Features, or Matching Sentence Endings.
        """
        norm_user = user_answer.strip().lower().replace(".", "").replace(")", "")
        if not norm_user:
            return {
                "type": qtype,
                "user_answer": "",
                "correct_answer": correct_answer,
                "is_correct": False,
                "is_unanswered": True,
                "passage_evidence": passage_evidence,
                "explanation": explanation
            }
        norm_correct = correct_answer.strip().lower().replace(".", "").replace(")", "")

        is_correct = (norm_user == norm_correct)
        return {
            "type": qtype,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "passage_evidence": passage_evidence,
            "explanation": explanation
        }

    @classmethod
    def grade_completion(
        cls,
        user_answer: str,
        acceptable_answers: List[str],
        max_words: int,
        passage_evidence: str,
        explanation: str,
        qtype: str = "Completion"
    ) -> Dict[str, Any]:
        """
        Grades text completions with strict word count limits:
        - Sentence Completion
        - Summary Completion
        - Note Completion
        - Table Completion
        - Flowchart Completion
        - Diagram Labelling
        - Short-Answer Questions
        """
        cleaned_str = user_answer.strip()
        if not cleaned_str:
            return {
                "type": qtype,
                "user_answer": "",
                "correct_answer": acceptable_answers[0] if acceptable_answers else "",
                "is_correct": False,
                "is_unanswered": True,
                "passage_evidence": passage_evidence,
                "explanation": explanation
            }
        tokens = cleaned_str.split()
        if len(tokens) > max_words:
            return {
                "type": qtype,
                "user_answer": user_answer,
                "correct_answer": acceptable_answers[0],
                "is_correct": False,
                "passage_evidence": passage_evidence,
                "explanation": f"Exceeded word count limit! Max allowed: {max_words} word(s). You wrote {len(tokens)} words."
            }

        norm_user = cleaned_str.lower().strip(".,;:!'\"?")
        # Remove redundant articles if not part of acceptable
        acceptable_norm = [a.strip().lower().strip(".,;:!'\"?") for a in acceptable_answers]
        
        is_correct = norm_user in acceptable_norm
        if not is_correct:
            # Check without leading 'a'/'an'/'the'
            no_article_user = re.sub(r"^(a|an|the)\s+", "", norm_user)
            no_article_acc = [re.sub(r"^(a|an|the)\s+", "", a) for a in acceptable_norm]
            if no_article_user in no_article_acc:
                is_correct = True

        return {
            "type": qtype,
            "user_answer": user_answer,
            "correct_answer": acceptable_answers[0],
            "is_correct": is_correct,
            "passage_evidence": passage_evidence,
            "explanation": explanation
        }

    @classmethod
    def grade_question(cls, question: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        """Universal grading dispatcher handling any of the 14 question types."""
        qtype = question.get("type", "Completion")
        evidence = question.get("evidence", "")
        explanation = question.get("explanation", "")

        if qtype in ("TFNG", "True/False/Not Given"):
            return cls.grade_tfng(user_answer, question["correct"], evidence, explanation)

        elif qtype in ("YNNG", "Yes/No/Not Given"):
            return cls.grade_ynng(user_answer, question["correct"], evidence, explanation)

        elif qtype in ("MCQ", "Multiple Choice"):
            return cls.grade_multiple_choice(
                user_answer,
                question["correct"],
                evidence,
                explanation,
                question.get("distractor_analysis")
            )

        elif qtype in ("Matching Headings", "Matching Information", "Matching Features", "Matching Sentence Endings"):
            return cls.grade_matching(qtype, user_answer, question["correct"], evidence, explanation)

        else:
            # Default to text completion types
            acceptable = question.get("acceptable") or [question.get("correct", "")]
            max_words = question.get("max_words", 3)
            return cls.grade_completion(user_answer, acceptable, max_words, evidence, explanation, qtype=qtype)
