# PHASE 16 ASSESSMENT CALIBRATION & STATISTICAL ANALYSIS REPORT
**Project:** IELTS by GAMA  
**Version:** 1.6.0  
**Phase:** 16 — Supervised Beta Pilot, Human Scoring Calibration & Teacher Review Toolkit  
**Date:** November 15, 2026  
**Component:** `core/benchmark/calibration_engine.py`, `core/writing/`, `core/speaking/`  

---

## 1. Objective & Assessment Rigor

The purpose of the Assessment Calibration Engine is to measure, audit, and systematically improve the alignment between automated AI score estimates and certified human examiner consensus.

Automated scoring systems in commercial ed-tech frequently suffer from unacknowledged bias: either systematic over-marking (leniency bias) that gives candidates false confidence, or erratic under-marking that demoralizes learners. Phase 16 establishes the statistical framework to quantify this alignment transparently.

---

## 2. Mathematical Calibration Metrics

The `CalibrationEngine` implements the following standard psychometric and statistical metrics for evaluating automated scoring models against human consensus marks:

### 2.1 Mean Absolute Error (MAE)
Measures average magnitude of scoring discrepancies regardless of direction:
$$\text{MAE} = \frac{1}{N} \sum_{i=1}^{N} \left| \text{Band}_{\text{AI}, i} - \text{Band}_{\text{Human}, i} \right|$$
- *Target standard for IELTS practice tools:* $\text{MAE} \le 0.45$ bands.

### 2.2 Mean Signed Bias (Directional Tendency)
Detects systematic leniency or harshness:
$$\text{Bias} = \frac{1}{N} \sum_{i=1}^{N} \left( \text{Band}_{\text{AI}, i} - \text{Band}_{\text{Human}, i} \right)$$
- $\text{Bias} > 0$: AI over-estimates candidate performance (leniency bias).
- $\text{Bias} < 0$: AI under-estimates candidate performance (harshness bias).
- *Target standard:* $|\text{Bias}| \le 0.15$ bands.

### 2.3 Criterion-Level MAE Matrix
Computed independently across all four sub-criteria:
- Writing: $\text{MAE}_{\text{TR}}$, $\text{MAE}_{\text{CC}}$, $\text{MAE}_{\text{LR}}$, $\text{MAE}_{\text{GRA}}$
- Speaking: $\text{MAE}_{\text{FC}}$, $\text{MAE}_{\text{LR}}$, $\text{MAE}_{\text{GRA}}$, $\text{MAE}_{\text{P}}$

### 2.4 Band Agreement Rates
- **Exact Agreement Rate:** Percentage of submissions where $\text{Band}_{\text{AI}} == \text{Band}_{\text{Human}}$.
- **Within $\pm 0.5$ Band Agreement Rate:** Percentage of submissions where $|\text{Band}_{\text{AI}} - \text{Band}_{\text{Human}}| \le 0.5$. In professional examiner calibration (e.g., Cambridge ESOL), $\pm 0.5$ is accepted as standard operational equivalence.
- **Within $\pm 1.0$ Band Agreement Rate:** Broad agreement tolerance ($|\text{Band}_{\text{AI}} - \text{Band}_{\text{Human}}| \le 1.0$).

---

## 3. Algorithm Versioning Integration

To ensure statistical validity, scoring heuristics are tied to specific release versions:
- `WritingEvaluator.ALGORITHM_VERSION = "1.6.0"`
- `SpeakingExaminer.ALGORITHM_VERSION = "1.6.0"`
- All evaluation output payloads stamp `algorithm_version: "1.6.0"`.
- When `CalibrationEngine.compute_calibration_report(algorithm_version="1.6.0")` executes, it only computes metrics for submissions evaluated under the specified algorithm version, preventing contaminated statistical aggregates across code changes.

---

## 4. Current Zero-State ($N=0$) & Integrity Audit

### 4.1 Live System Output
Querying `/api/benchmark/calibration` yields:
```json
{
  "status": "pending_human_calibration",
  "valid_samples": 0,
  "algorithm_version": "1.6.0",
  "message": "Insufficient verified human benchmark data for statistical calibration (N=0). Metrics will compute dynamically as verified double-marked human evaluations are submitted."
}
```

### 4.2 Ethical Integrity Analysis
Commercial educational tools often synthesize "fake" or "simulated" calibration benchmarks (e.g., claiming 94% human agreement based on mocked test records). IELTS by GAMA explicitly rejects this practice:
- **No synthetic benchmark scores have been seeded.**
- **No artificial examiner ratings have been entered.**
- The calibration engine returns an honest, defensible pending state ($N=0$).
- As candidates in the Phase 16 beta cohorts complete practice tests and certified examiners complete double-marking reconciliations, the calibration engine will populate live statistical metrics.

---

## 5. Automated Verification Results

In `tests/test_phase16_beta_toolkit.py`:
- `test_calibration_engine_zero_state`: Confirmed that with empty benchmark records, `compute_calibration_report()` returns `status == "pending_human_calibration"` and `valid_samples == 0` without dividing by zero or raising exceptions.
- `scripts/test_phase16_api.py`: Confirmed REST endpoint returns HTTP 200 with honest $N=0$ structure.

---

## 6. Next Steps for Full Pilot Calibration

1. Enroll initial candidates in Cohort 1 (Academic) and Cohort 2 (General Training).
2. Collect initial 30 writing and 30 speaking samples with informed consent.
3. Conduct blind double-marking with `teacher_sarah`, `examiner_mark`, and `examiner_clara`.
4. Run `CalibrationEngine.compute_calibration_report()` to generate the first empirical calibration curve.
