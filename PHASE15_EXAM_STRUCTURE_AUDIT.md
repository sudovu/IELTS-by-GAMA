# PHASE 15 — FULL EXAMINATION MATHEMATICS & TIMING AUDIT

**Project:** IELTS by GAMA  
**Phase:** 15 — Independent Product Verification  
**Auditor Role:** Senior QA Architect & Assessment Specialist  
**Reference Specification:** Cambridge / IDP / British Council Official IELTS Specifications  

---

## 1. Structural Accounting & Mathematics

An independent audit of `core/exam/content_repository.py` and `core/exam/exam_manager.py` was conducted to verify every claim regarding test structure, item counts, durations, and grading pipelines:

### 1.1 Item Counts & Question Breakdown
- **Academic Full Mock (`mock_full_acad`)**:
  - **Listening:** 4 sections, 40 objective questions (Q1–Q40).
  - **Reading:** 3 academic passages, 40 objective questions (Q1–Q40).
  - **Writing:** 2 tasks (Task 1 Report $\ge 150$w, Task 2 Essay $\ge 250$w).
  - **Speaking:** 3 parts (Part 1: 4 prompts; Part 2: 1 cue card with 4 sub-prompts; Part 3: 4 discussion prompts = 9 spoken prompts).
  - **Total Items:** 80 objective questions + 2 writing tasks + 9 speaking prompts = **91 total interaction items**.
  - **Graded Items:** 80 objective items graded against official keys; 2 writing tasks and 3 speaking parts evaluated by rubric criteria.
- **General Training Full Mock (`mock_full_gt`)**:
  - **Listening:** 4 sections, 40 objective questions (identical listening module to Academic).
  - **Reading:** 3 sections, 40 objective questions (Section 1: 14 Q, Section 2: 13 Q, Section 3: 13 Q).
  - **Writing:** 2 tasks (Task 1 Semi-formal Letter $\ge 150$w, Task 2 Essay $\ge 250$w).
  - **Speaking:** 3 parts (9 total prompts).

### 1.2 Duration & 164-Minute Timeline Accounting
The reported **164-minute** duration represents the continuous execution of all four macro-skills in the simulated practice environment:
$$\text{Total Duration} = 30\text{m (Listening)} + 2\text{m (Review)} + 60\text{m (Reading)} + 60\text{m (Writing)} + 12\text{m (Speaking)} = 164\text{ minutes (9,840 seconds)}$$

---

## 2. Answers to Verification Questions

1. **Does the Academic mock contain all four skills?**  
   **Yes.** Verified in `ExamContentRepository.get_exam_package("mock_full_acad")`. Contains Listening, Reading, Writing, and Speaking packages.
2. **Does the General Training mock contain all four skills?**  
   **Yes.** Verified in `ExamContentRepository.get_exam_package("mock_full_gt")`. Contains Listening, General Training Reading, General Training Writing, and Speaking packages.
3. **How many questions are actually graded?**  
   **80 objective items** (40 Reading + 40 Listening) are graded with exact/acceptable key matching. In addition, 2 Writing essays and 3 Speaking turns are graded by rubric criteria evaluators.
4. **Are Writing tasks counted separately from objective questions?**  
   **Yes.** Writing produces task-specific criterion scores (TR, CC, LR, GRA) that combine into a weighted composite band:
   $$\text{Writing Band} = \text{round\_band}\left(\frac{1}{3}\text{ Task 1} + \frac{2}{3}\text{ Task 2}\right)$$
5. **How many Speaking prompts are included?**  
   **9 prompts total:** 4 questions in Part 1, 1 long-turn cue card (with 4 sub-prompts) in Part 2, and 4 thematic discussion questions in Part 3.
6. **What does the reported 164-minute duration represent?**  
   The cumulative duration of all 4 test sections: 32 min Listening (30 min dialogue + 2 min review) + 60 min Reading + 60 min Writing + 12 min Speaking.
7. **Is Speaking part of the same continuous timer or a separately scheduled session?**  
   In `full_mock`, Speaking is integrated into the continuous 164-minute practice session. Learners can also launch a standalone 14-minute Speaking session (`exam_speak_1`) from the library.
8. **Are preparation periods included in the duration?**  
   Yes. Part 2 Speaking includes a mandatory 60-second preparation countdown timer before the response timer begins.
9. **Are breaks supported or excluded?**  
   In compliance with official IELTS computer-delivered rules, there are **no scheduled breaks** between Listening, Reading, and Writing. The simulated practice environment mirrors this continuous delivery.
10. **Does the application explain the difference between practice simulation timing and actual IELTS examination arrangements?**  
    **Yes.** The exam lobby and results screen state that in official testing centres, Speaking is scheduled as an independent face-to-face or video interview, whereas Listening, Reading, and Writing are taken in one sitting.

---

## 3. Discrepancy & Catalog Reconciliation

In `ExamContentRepository.list_available_exams()`, `total_questions` was previously listed as `82` for full mocks (counting 40 L + 40 R + 2 W).  
**Clarification:** The full interactive item count is 91 prompts (80 objective + 2 writing essays + 9 speaking prompts). The metadata has been clarified so learners understand that 80 objective questions and 2 writing tasks are tracked alongside 3 speaking parts.
