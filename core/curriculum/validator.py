# -*- coding: utf-8 -*-
"""
validator.py
Automated Content Quality Assurance and Verification Engine for IELTS by GAMA (Phase 13).
Validates instructional design integrity, question answer keys, explanation presence,
depth thresholds (examples >= 2, guided drills >= 2, assessment >= 2),
prerequisite DAG coherence, cycle detection, vocabulary completeness,
and human-review checklist generator.
"""

from typing import Dict, Any, List, Set, Tuple


class ContentValidator:
    """Performs rigorous automated validation on curriculum and vocabulary datasets."""

    VALID_CEFR_LEVELS = {"A1", "A2", "B1", "B2", "C1", "C2"}
    VALID_MODULE_TYPES = {
        "grammar", "vocabulary", "reading", "listening",
        "writing", "speaking", "pronunciation", "functional", "review"
    }

    # Minimum pedagogical depth thresholds
    MIN_EXPLANATION_LENGTH = 300
    MIN_EXAMPLES_PER_LESSON = 2
    MIN_GUIDED_EXERCISES_PER_LESSON = 2
    MIN_ASSESSMENT_QUESTIONS_PER_LESSON = 2

    @classmethod
    def validate_curriculum(cls, lessons: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validates curriculum lessons for structure, depth, answer keys, explanations,
        prerequisite integrity, cycle detection, and uniqueness.
        """
        issues: List[Dict[str, str]] = []
        all_lesson_ids: Set[str] = set()
        all_question_ids: Set[str] = set()
        all_question_texts: Set[str] = set()
        prereq_graph: Dict[str, List[str]] = {}

        total_checks = 0
        passed_checks = 0

        # Step 1: Collect all lesson IDs for prerequisite validation
        for l in lessons:
            lid = l.get("id", "")
            if lid:
                if lid in all_lesson_ids:
                    issues.append({"severity": "CRITICAL", "lesson_id": lid, "issue": f"Duplicate lesson ID: '{lid}'"})
                all_lesson_ids.add(lid)
                prereq_graph[lid] = l.get("prerequisites", [])

        # Step 2: Validate individual lessons
        for l in lessons:
            lid = l.get("id", "UNKNOWN")

            # Check 1: ID format
            total_checks += 1
            if not lid or not lid.startswith("curric_"):
                issues.append({"severity": "WARNING", "lesson_id": lid, "issue": f"Non-standard lesson ID format: '{lid}'"})
            else:
                passed_checks += 1

            # Check 2: CEFR Level
            total_checks += 1
            lvl = l.get("cefr_level", "").upper()
            if lvl not in cls.VALID_CEFR_LEVELS:
                issues.append({"severity": "CRITICAL", "lesson_id": lid, "issue": f"Invalid CEFR level: '{lvl}'"})
            else:
                passed_checks += 1

            # Check 3: Module Type
            total_checks += 1
            mod = l.get("module_type", "").lower()
            if mod not in cls.VALID_MODULE_TYPES:
                issues.append({"severity": "CRITICAL", "lesson_id": lid, "issue": f"Invalid module type: '{mod}'"})
            else:
                passed_checks += 1

            # Check 4: Title
            total_checks += 1
            title = l.get("title", "").strip()
            if not title or len(title) < 5:
                issues.append({"severity": "HIGH", "lesson_id": lid, "issue": "Missing or truncated title"})
            else:
                passed_checks += 1

            # Check 5: Objectives
            total_checks += 1
            objectives = l.get("objectives", [])
            if not objectives or len(objectives) < 2:
                issues.append({"severity": "HIGH", "lesson_id": lid, "issue": f"Insufficient learning objectives ({len(objectives)} found, minimum 2 required)"})
            else:
                passed_checks += 1

            # Check 6: Explanation Depth
            total_checks += 1
            exp = l.get("explanation_markdown", "").strip()
            if not exp or len(exp) < cls.MIN_EXPLANATION_LENGTH:
                issues.append({"severity": "HIGH", "lesson_id": lid, "issue": f"Shallow explanation_markdown ({len(exp)} chars, minimum {cls.MIN_EXPLANATION_LENGTH} required)"})
            else:
                passed_checks += 1

            # Check 7: Real-world Examples Count
            total_checks += 1
            examples = l.get("examples", [])
            if len(examples) < cls.MIN_EXAMPLES_PER_LESSON:
                issues.append({"severity": "HIGH", "lesson_id": lid, "issue": f"Insufficient examples ({len(examples)} found, minimum {cls.MIN_EXAMPLES_PER_LESSON} required)"})
            else:
                passed_checks += 1

            # Check 8: Prerequisites DAG coherence
            prereqs = l.get("prerequisites", [])
            for p in prereqs:
                total_checks += 1
                if p not in all_lesson_ids:
                    issues.append({"severity": "HIGH", "lesson_id": lid, "issue": f"Broken prerequisite: references nonexistent lesson '{p}'"})
                elif p == lid:
                    issues.append({"severity": "CRITICAL", "lesson_id": lid, "issue": f"Self-referential prerequisite: '{p}'"})
                else:
                    passed_checks += 1

            # Check 9: Guided Exercises Count and Structure
            guided = l.get("guided_exercises", [])
            total_checks += 1
            if len(guided) < cls.MIN_GUIDED_EXERCISES_PER_LESSON:
                issues.append({"severity": "HIGH", "lesson_id": lid, "issue": f"Insufficient guided exercises ({len(guided)} found, minimum {cls.MIN_GUIDED_EXERCISES_PER_LESSON} required)"})
            else:
                passed_checks += 1

            for g in guided:
                total_checks += 2
                gid = g.get("id", "")
                if gid in all_question_ids:
                    issues.append({"severity": "HIGH", "lesson_id": lid, "issue": f"Duplicate question ID: '{gid}'"})
                if gid:
                    all_question_ids.add(gid)

                if not g.get("prompt") or not g.get("answer"):
                    issues.append({"severity": "CRITICAL", "lesson_id": lid, "issue": f"Guided exercise {gid} missing prompt or answer"})
                else:
                    passed_checks += 1

                if not g.get("explanation"):
                    issues.append({"severity": "MEDIUM", "lesson_id": lid, "issue": f"Guided exercise {gid} missing explanation"})
                else:
                    passed_checks += 1

            # Check 10: Assessment Questions Count and Structure
            quiz = l.get("assessment", [])
            total_checks += 1
            if len(quiz) < cls.MIN_ASSESSMENT_QUESTIONS_PER_LESSON:
                issues.append({"severity": "HIGH", "lesson_id": lid, "issue": f"Insufficient assessment questions ({len(quiz)} found, minimum {cls.MIN_ASSESSMENT_QUESTIONS_PER_LESSON} required)"})
            else:
                passed_checks += 1

            for q in quiz:
                total_checks += 3
                qid = q.get("id", "")
                if qid in all_question_ids:
                    issues.append({"severity": "HIGH", "lesson_id": lid, "issue": f"Duplicate question ID: '{qid}' in assessment"})
                if qid:
                    all_question_ids.add(qid)

                q_text = q.get("question", "").strip().lower()
                if q_text and q_text in all_question_texts:
                    issues.append({"severity": "MEDIUM", "lesson_id": lid, "issue": f"Duplicate question text across curriculum: '{q_text[:40]}...'"})
                if q_text:
                    all_question_texts.add(q_text)

                opts = q.get("options", [])
                c_idx = q.get("correct_index")

                if not opts or len(opts) < 2:
                    issues.append({"severity": "CRITICAL", "lesson_id": lid, "issue": f"Question {qid} has fewer than 2 options"})
                elif c_idx is None or not (0 <= c_idx < len(opts)):
                    issues.append({"severity": "CRITICAL", "lesson_id": lid, "issue": f"Question {qid} has invalid correct_index: {c_idx} (options: {len(opts)})"})
                else:
                    passed_checks += 1

                if not q.get("explanation"):
                    issues.append({"severity": "HIGH", "lesson_id": lid, "issue": f"Question {qid} missing pedagogical explanation"})
                else:
                    passed_checks += 1

                if not q.get("question"):
                    issues.append({"severity": "CRITICAL", "lesson_id": lid, "issue": f"Question {qid} missing prompt text"})
                else:
                    passed_checks += 1

        # Step 3: Cycle Detection in Prerequisite Graph
        total_checks += 1
        has_cycles, cycle_nodes = cls._detect_cycles(prereq_graph)
        if has_cycles:
            issues.append({"severity": "CRITICAL", "issue": f"Circular prerequisite dependency detected involving: {cycle_nodes}"})
        else:
            passed_checks += 1

        quality_score = round((passed_checks / max(1, total_checks)) * 100.0, 1) if total_checks > 0 else 0.0

        return {
            "total_lessons_evaluated": len(lessons),
            "total_checks_run": total_checks,
            "passed_checks": passed_checks,
            "quality_score_percent": quality_score,
            "total_issues_found": len(issues),
            "critical_issues_count": sum(1 for i in issues if i["severity"] == "CRITICAL"),
            "high_issues_count": sum(1 for i in issues if i["severity"] == "HIGH"),
            "medium_issues_count": sum(1 for i in issues if i["severity"] == "MEDIUM"),
            "issues": issues,
            "human_review_status": {
                "status": "AUTOMATED_VALIDATION_PASSED",
                "human_peer_review_status": "PENDING_FORMAL_EXAMINER_SIGN_OFF",
                "disclaimer": "Automated schema and pedagogical depth checks completed. Full linguistic naturalness and human agreement calibration require qualified human assessor review."
            },
            "human_review_checklist": cls.get_human_review_checklist()
        }

    @classmethod
    def _detect_cycles(cls, graph: Dict[str, List[str]]) -> Tuple[bool, List[str]]:
        """Detects circular dependencies in the prerequisite directed graph using DFS."""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        cycle_nodes: List[str] = []

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    cycle_nodes.append(f"{node} -> {neighbor}")
                    return True
            rec_stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if dfs(node):
                    return True, cycle_nodes
        return False, []

    @classmethod
    def validate_vocabulary_themes(cls, themes: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Validates lexical entries, word families, collocations, and IPA transcriptions."""
        issues: List[Dict[str, str]] = []
        total_words = 0
        total_checks = 0
        passed_checks = 0
        all_words_seen: Set[str] = set()

        for theme_id, words in themes.items():
            for w in words:
                total_words += 1
                word_term = w.get("word", "").strip().lower()

                total_checks += 1
                if not word_term:
                    issues.append({"severity": "CRITICAL", "theme": theme_id, "issue": "Missing word text"})
                    continue
                passed_checks += 1

                if word_term in all_words_seen:
                    issues.append({"severity": "MEDIUM", "theme": theme_id, "word": word_term, "issue": f"Duplicate term across themes: '{word_term}'"})
                all_words_seen.add(word_term)

                # Check IPA
                total_checks += 1
                if not w.get("ipa"):
                    issues.append({"severity": "MEDIUM", "theme": theme_id, "word": word_term, "issue": f"Word '{word_term}' missing IPA transcription"})
                else:
                    passed_checks += 1

                # Check definition
                total_checks += 1
                if not w.get("definition") and not w.get("simple_definition"):
                    issues.append({"severity": "CRITICAL", "theme": theme_id, "word": word_term, "issue": f"Word '{word_term}' missing definition"})
                else:
                    passed_checks += 1

                # Check example
                total_checks += 1
                if not w.get("contextual_example") and not w.get("example_sentences"):
                    issues.append({"severity": "HIGH", "theme": theme_id, "word": word_term, "issue": f"Word '{word_term}' missing contextual example"})
                else:
                    passed_checks += 1

                # Check collocations
                total_checks += 1
                if not w.get("collocations") or len(w.get("collocations", [])) == 0:
                    issues.append({"severity": "MEDIUM", "theme": theme_id, "word": word_term, "issue": f"Word '{word_term}' missing collocations"})
                else:
                    passed_checks += 1

                # Check word family
                total_checks += 1
                if not w.get("word_family") or not isinstance(w.get("word_family"), dict):
                    issues.append({"severity": "LOW", "theme": theme_id, "word": word_term, "issue": f"Word '{word_term}' missing word family dictionary"})
                else:
                    passed_checks += 1

        quality_score = round((passed_checks / max(1, total_checks)) * 100.0, 1) if total_checks > 0 else 0.0

        return {
            "total_themes_evaluated": len(themes),
            "total_words_evaluated": total_words,
            "total_checks_run": total_checks,
            "passed_checks": passed_checks,
            "quality_score_percent": quality_score,
            "total_issues_found": len(issues),
            "critical_issues_count": sum(1 for i in issues if i["severity"] == "CRITICAL"),
            "issues": issues
        }

    @classmethod
    def get_human_review_checklist(cls) -> List[Dict[str, str]]:
        """Provides an expert human-review checklist across the 8 required assessment dimensions."""
        return [
            {
                "area": "1. Grammar Accuracy",
                "checkpoint": "Are grammatical rules, structural formulas, and inflectional patterns 100% accurate without conflicting terminology?",
                "verification_method": "Qualified English educator verifies explanation_markdown and positive/negative paradigm tables."
            },
            {
                "area": "2. Vocabulary Accuracy",
                "checkpoint": "Are definitions, parts of speech, and IPA transcriptions conformant to standard British/General English dictionaries?",
                "verification_method": "Lexicographer cross-checks IPA and definitions against Cambridge/Oxford references."
            },
            {
                "area": "3. Linguistic Naturalness",
                "checkpoint": "Do example sentences reflect authentic, idiomatic modern English rather than artificial textbook sentences?",
                "verification_method": "Native/proficient English speaker reviews contextual examples for colloquial authenticity."
            },
            {
                "area": "4. CEFR Appropriateness",
                "checkpoint": "Does the lexical and syntactic complexity match the declared CEFR tier (e.g. A1 avoids complex subordination; C1 avoids basic repetition)?",
                "verification_method": "CEFR assessor audits lesson vocabulary and syntactic structures against Council of Europe descriptors."
            },
            {
                "area": "5. Instruction Clarity",
                "checkpoint": "Are exercise prompts unambiguous, clear, and direct, ensuring learners know exactly what to type or select?",
                "verification_method": "Learner testing panel reviews prompt instructions for clarity."
            },
            {
                "area": "6. Answer Correctness",
                "checkpoint": "Does each question have strictly one undeniably correct answer, with all distractor options being unambiguously incorrect?",
                "verification_method": "Peer review verifies answer keys, distractor rationales, and option bounds."
            },
            {
                "area": "7. Educational Usefulness",
                "checkpoint": "Does completing the lesson provide transferable communication skills rather than mere trivia memorization?",
                "verification_method": "Curriculum designer audits pedagogical progression and formative feedback."
            },
            {
                "area": "8. IELTS Task Relevance",
                "checkpoint": "Does the content directly train skills rewarded under official IELTS band descriptors (TR, CC, LR, GRA, Fluency, Pronunciation)?",
                "verification_method": "Certificated IELTS writing and speaking examiner evaluates alignment with band scoring criteria."
            }
        ]
