"""
Assessment Calibration & Statistical Reporting Engine for IELTS by GAMA.
Compares AI-generated heuristic estimates against human examiner benchmark consensus scores.
Computes Mean Absolute Error (MAE), Mean Signed Error (Bias), Agreement within 0.5/1.0 Band,
and criterion-level variance.
Enforces statistical integrity: displays honest zero-state when real human data is absent.
"""

from typing import Optional, Dict, Any, List
from core.database.db_manager import DatabaseManager
from core.writing.writing_evaluator import WritingEvaluator
from core.speaking.speaking_examiner import SpeakingExaminer


class CalibrationEngine:
    """Computes empirical calibration statistics between AI models and verified human marks."""

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()

    def run_calibration_analysis(self, assessment_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Runs calibration comparing AI evaluation against human consensus marks.
        If no completed benchmark records exist, returns an honest pending status.
        """
        query = """SELECT * FROM benchmark_records 
                   WHERE consent_status = 'consented' AND consensus_human_band IS NOT NULL"""
        params = []
        if assessment_type:
            query += " AND assessment_type = ?"
            params.append(assessment_type)

        rows = self.db.fetchall(query, tuple(params))
        valid_records = [dict(r) for r in rows]
        n_samples = len(valid_records)

        # -------------------------------------------------------------
        # STATISTICAL INTEGRITY: HONEST ZERO-STATE
        # -------------------------------------------------------------
        if n_samples == 0:
            return {
                "status": "pending_human_calibration",
                "message": "Human calibration data not yet available (0 benchmark samples enrolled with verified human scores).",
                "valid_samples": 0,
                "metrics": None,
                "disclaimer": "Automated AI evaluations remain heuristic practice estimates. Empirical calibration requires real examiner benchmark datasets."
            }

        # Compare AI evaluation vs Human evaluation
        total_abs_error = 0.0
        total_signed_error = 0.0
        exact_agreements = 0
        within_half_band = 0
        within_one_band = 0

        diff_distribution = {"exact_0_0": 0, "diff_0_5": 0, "diff_1_0": 0, "diff_greater_1_0": 0}
        comparison_rows = []

        for rec in valid_records:
            human_score = float(rec["consensus_human_band"])
            content = rec["anonymized_content"]
            rec_type = rec["assessment_type"]
            task_type = rec.get("task_type") or "acad_t2_stem"

            # Compute AI score under algorithm v1.6.0
            if rec_type == "writing":
                ai_res = WritingEvaluator.evaluate_essay(task_type, content)
                ai_score = float(ai_res["estimated_band"])
            else:
                ai_res = SpeakingExaminer.evaluate_spoken_response(content)
                ai_score = float(ai_res["estimated_band"])

            diff = round(ai_score - human_score, 1)
            abs_diff = round(abs(diff), 1)

            total_abs_error += abs_diff
            total_signed_error += diff

            if abs_diff == 0.0:
                exact_agreements += 1
                diff_distribution["exact_0_0"] += 1
            elif abs_diff <= 0.5:
                diff_distribution["diff_0_5"] += 1
            elif abs_diff <= 1.0:
                diff_distribution["diff_1_0"] += 1
            else:
                diff_distribution["diff_greater_1_0"] += 1

            if abs_diff <= 0.5:
                within_half_band += 1
            if abs_diff <= 1.0:
                within_one_band += 1

            comparison_rows.append({
                "benchmark_id": rec["id"],
                "assessment_type": rec_type,
                "task_type": task_type,
                "ai_score": ai_score,
                "human_score": human_score,
                "difference": diff,
                "abs_difference": abs_diff
            })

        mae = round(total_abs_error / n_samples, 2)
        bias = round(total_signed_error / n_samples, 2)
        pct_half_band = round((within_half_band / n_samples) * 100.0, 1)
        pct_one_band = round((within_one_band / n_samples) * 100.0, 1)
        pct_exact = round((exact_agreements / n_samples) * 100.0, 1)

        return {
            "status": "calibrated_preliminary",
            "valid_samples": n_samples,
            "algorithm_version": getattr(WritingEvaluator, "ALGORITHM_VERSION", "1.6.0"),
            "metrics": {
                "mean_absolute_error_mae": mae,
                "mean_signed_error_bias": bias,
                "exact_agreement_pct": pct_exact,
                "within_half_band_agreement_pct": pct_half_band,
                "within_one_band_agreement_pct": pct_one_band,
                "difference_distribution": diff_distribution
            },
            "sample_comparisons": comparison_rows[:10],
            "disclaimer": "Sample size must exceed 50 double-marked scripts per track before claiming statistical significance."
        }
