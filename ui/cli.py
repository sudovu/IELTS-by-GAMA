"""
Interactive Terminal CLI for IELTS by GAMA.
Offers a complete offline English tutoring & IELTS preparation console.
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core.database.db_manager import DatabaseManager
from core.database.repositories import LearnerRepository
from core.chatbot.tutor_bot import UnifiedAITutor
from core.grammar.grammar_engine import GrammarEngine
from core.grammar.adaptive_grammar import AdaptiveGrammar
from core.vocabulary.vocab_engine import VocabEngine
from core.reading.reading_engine import ReadingEngine
from core.listening.listening_engine import ListeningEngine
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer
from core.progress.mistake_book import MistakeBook
from core.progress.srs import SpacedRepetitionSystem
from core.progress.study_planner import StudyPlanner
from core.progress.analytics import LearningAnalytics
from core.scoring.cefr_diagnostic import CEFRDiagnostic
from core.sync.connectivity import ConnectivityManager


class IELTSbyGAMACLI:
    def __init__(self):
        self.db = DatabaseManager()
        self.learner_repo = LearnerRepository(self.db)
        self.learner = self.learner_repo.get_or_create_default("default_learner", "GAMA Student")
        self.tutor = UnifiedAITutor(self.db)
        self.grammar = GrammarEngine()
        self.adaptive_grammar = AdaptiveGrammar(self.db)
        self.vocab = VocabEngine()
        self.reading = ReadingEngine()
        self.listening = ListeningEngine()
        self.writing = WritingEvaluator()
        self.speaking = SpeakingExaminer()
        self.mistake_book = MistakeBook(self.db)
        self.srs = SpacedRepetitionSystem(self.db)
        self.planner = StudyPlanner(self.db)
        self.analytics = LearningAnalytics(self.db)
        self.connectivity = ConnectivityManager()

    def print_header(self):
        indicator = self.connectivity.get_ui_indicator()
        print("=" * 65)
        print("                   IELTS BY GAMA")
        print("      HYBRID ONLINE + OFFLINE AI ENGLISH TUTOR")
        print(f"               Mode: {indicator}")
        print("=" * 65)

    def run(self):
        while True:
            self.print_header()
            print("1. Unified AI Tutor Chat")
            print("2. Diagnostic CEFR Assessment")
            print("3. Adaptive Grammar Intervention")
            print("4. Vocabulary & Spaced Repetition (SRS)")
            print("5. IELTS Reading Module")
            print("6. IELTS Listening Module")
            print("7. IELTS Writing Evaluation")
            print("8. IELTS Speaking Simulation")
            print("9. Mistake Book Review")
            print("10. Progress Dashboard & Daily Plan")
            print("11. Toggle Forced Offline Mode")
            print("0. Exit")
            print("-" * 65)

            choice = input("Select an option (0-11): ").strip()
            if choice == "1":
                self.chat_loop()
            elif choice == "2":
                self.run_diagnostic()
            elif choice == "3":
                self.run_grammar_adaptive()
            elif choice == "4":
                self.run_srs_deck()
            elif choice == "5":
                self.run_reading()
            elif choice == "6":
                self.run_listening()
            elif choice == "7":
                self.run_writing()
            elif choice == "8":
                self.run_speaking()
            elif choice == "9":
                self.run_mistakes()
            elif choice == "10":
                self.show_dashboard()
            elif choice == "11":
                curr = self.connectivity.is_forced_offline
                self.connectivity.set_forced_offline(not curr)
                print(f"[STATUS] Forced Offline Mode is now: {not curr}")
            elif choice == "0":
                print("Thank you for practicing with IELTS by GAMA. Goodbye!")
                break
            else:
                print("Invalid selection. Please choose 0-11.")

    def chat_loop(self):
        print("\n--- Unified AI Tutor Chat (type 'exit' to return) ---")
        print(self.tutor.get_greeting("default_learner"))
        while True:
            msg = input("\nYou: ").strip()
            if not msg or msg.lower() in ["exit", "quit", "back"]:
                break
            res = self.tutor.process_message("default_learner", msg)
            print(f"\nTutor [{res['connectivity']}]:\n{res['reply']}")
            if res.get("detected_mistakes"):
                print("\n[MISTAKE LOGGED]:")
                for err in res["detected_mistakes"]:
                    print(f" - Original: '{err['original']}' -> Correction: '{err['correction']}'")

    def run_diagnostic(self):
        print("\n--- Diagnostic Assessment ---")
        answers = {}
        for q in CEFRDiagnostic.DIAGNOSTIC_QUESTIONS:
            print(f"\n[{q['skill'].upper()}] {q['prompt']}")
            for idx, opt in enumerate(q["options"], 1):
                print(f"  {idx}. {opt}")
            ans_idx = input("Your choice (1-4 or text): ").strip()
            if ans_idx.isdigit() and 1 <= int(ans_idx) <= len(q["options"]):
                answers[q["id"]] = q["options"][int(ans_idx) - 1]
            else:
                answers[q["id"]] = ans_idx

        result = CEFRDiagnostic.grade_diagnostic(answers)
        print("\n=== DIAGNOSTIC REPORT ===")
        print(f"Accuracy: {result['accuracy_percent']}% ({result['correct_count']}/{result['total_questions']})")
        print(f"Estimated CEFR: {result['estimated_cefr']} | Practice IELTS Range: {result['estimated_ielts_range']}")
        print(f"Strengths: {', '.join(result['strengths'])}")
        print(f"Weaknesses: {', '.join(result['weaknesses'])}")
        print(f"Priority: {result['priority_skills'][0]}")
        print(f"Plan: {result['recommended_study_plan']}")
        input("\nPress Enter to return...")

    def run_grammar_adaptive(self):
        print("\n--- Adaptive Grammar ---")
        sess = self.adaptive_grammar.generate_adaptive_session("default_learner")
        print(sess["message"])
        print(f"Topic: {sess['target_category']}")
        for drill in sess["drills"]:
            print(f"\n{drill['prompt']}")
            user_ans = input("Your answer: ").strip()
            print(f"Expected: {drill['expected_answer']}")
            print(f"Explanation: {drill['explanation']}")
        input("\nPress Enter to return...")

    def run_srs_deck(self):
        print("\n--- Spaced Repetition Flashcards ---")
        due = self.srs.get_due_deck("default_learner")
        if not due:
            print("No flashcards are due for review right now! Great job!")
            input("Press Enter to return...")
            return
        for item in due:
            print(f"\nCard [{item['item_type'].upper()}]: {item['prompt']}")
            input("Press Enter to reveal answer...")
            print(f"\n{item['answer']}")
            grade = input("Rate recall (0=Blackout, 3=Pass with effort, 5=Perfect): ").strip()
            try:
                g = int(grade)
                self.srs.review_card(item["id"], g)
                print("[OK] Review recorded with SM-2 algorithm.")
            except Exception:
                print("Skipped or invalid grade.")
        input("\nDeck finished. Press Enter to return...")

    def run_reading(self):
        print("\n--- IELTS Reading Practice ---")
        passage = self.reading.get_passage("acad_p1")
        print(f"\nTitle: {passage['title']} ({passage['track']})")
        print("\n" + passage["text"][:600] + "\n[... full passage loaded in test memory ...]")
        user_answers = {}
        for q in passage["questions"]:
            print(f"\nQ{q['num']} [{q['type']}]: {q['prompt']}")
            ans = input("Your Answer: ").strip()
            user_answers[q["num"]] = ans

        res = self.reading.evaluate_test("acad_p1", user_answers)
        print(f"\nResult: {res['correct_answers']}/{res['total_questions']} correct. Estimated Reading Band: {res['estimated_band']}")
        input("\nPress Enter to return...")

    def run_listening(self):
        print("\n--- IELTS Listening Practice ---")
        sec = self.listening.get_section("sec_1", show_transcript=True)
        print(f"\nScenario: {sec['title']}")
        print("\n[AUDIO SCRIPT]:")
        print(sec.get("audio_script", ""))
        user_answers = {}
        for q in sec["questions"]:
            print(f"\nQ{q['num']}: {q['prompt']}")
            ans = input("Your Answer: ").strip()
            user_answers[q["num"]] = ans

        res = self.listening.evaluate_submission("sec_1", user_answers)
        print(f"\nResult: {res['correct_answers']}/{res['total_questions']} correct. Estimated Listening Band: {res['estimated_band']}")
        input("\nPress Enter to return...")

    def run_writing(self):
        print("\n--- IELTS Writing Evaluation ---")
        prompt = self.writing.get_prompt("acad_t2_stem")
        print(f"\nTask 2: {prompt['title']}")
        print(prompt["prompt"])
        print("\nEnter or paste your essay (type 'END' on a new line to submit):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        essay = "\n".join(lines).strip()
        if not essay:
            essay = "I am agree with this idea because education is very important for society."
        eval_res = self.writing.evaluate_essay("acad_t2_stem", essay)
        print(f"\n=== EVALUATION: Band {eval_res['estimated_band']} ===")
        for c_name, c_score in eval_res["criteria"].items():
            print(f" - {c_name}: {c_score}")
        if eval_res.get("formative_corrections"):
            print("\nFormative Corrections:")
            for item in eval_res["formative_corrections"]:
                print(item["formatted_view"] + "\n")
        input("\nPress Enter to return...")

    def run_speaking(self):
        print("\n--- IELTS Speaking Simulation ---")
        prompts = self.speaking.get_test_prompts()
        cue = prompts["part_2_cue_card"]
        print(f"\nPart 2 Cue Card: {cue['topic']}")
        for p in cue["prompts"]:
            print(f" - {p}")
        print("\nEnter the transcript of your spoken response (or sample response):")
        spoken = input("Your speech: ").strip()
        if not spoken:
            spoken = "I would like to discuss an ambitious project. It was very challenging, but I persevered and finished it successfully."
        eval_res = self.speaking.evaluate_spoken_response(spoken, duration_seconds=60.0)
        print(f"\nEstimated Speaking Band: {eval_res['estimated_band']}")
        print(f"Words per minute: {eval_res['fluency_metrics']['words_per_minute']} WPM")
        print(f"Fillers: {eval_res['fluency_metrics']['total_filler_words']}")
        input("\nPress Enter to return...")

    def run_mistakes(self):
        print("\n--- Mistake Book Review ---")
        summary = self.mistake_book.get_summary_report("default_learner")
        print(f"Recorded Categories: {len(summary.get('categories', []))}")
        for c in summary.get("categories", []):
            print(f" • {c['skill'].capitalize()} - {c['category']}: {c['total_occurrences']} error(s) (Mastery: {round(c['avg_mastery']*100)}%)")
        input("\nPress Enter to return...")

    def show_dashboard(self):
        print("\n--- Progress Dashboard ---")
        dash = self.analytics.get_dashboard_data("default_learner")
        daily = self.planner.generate_daily_plan("default_learner")
        print(daily["daily_greeting"])
        print(f"Overall Estimated Band: {dash['overall_band_estimate']} | Target: {dash['target_band']}")
        print(f"SRS Items Due Today: {dash['srs_metrics']['items_due_today']}")
        input("\nPress Enter to return...")


def main():
    cli = IELTSbyGAMACLI()
    cli.run()


if __name__ == "__main__":
    main()
