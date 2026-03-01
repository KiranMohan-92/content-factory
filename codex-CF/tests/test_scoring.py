from codex_cf.models import EvidenceItem, ExplanationRecord, Falsifier, Prediction, SourceQuality
from codex_cf.scoring import evaluate_explanation


def test_strong_explanation_scores_higher_than_vague_one():
    strong = ExplanationRecord(
        explanation_id="a",
        title="Strong",
        claim="Decision quality improves when teams run explicit evaluation loops with measurable criteria.",
        mechanism=(
            "Because teams score decisions against fixed rubrics, they detect false positives early, "
            "which then leads to calibration improvements over repeated review cycles."
        ),
        scope="Knowledge teams in operations and product contexts",
        assumptions=["Rubric consistency", "Review cadence"],
        evidence=[
            EvidenceItem(
                source="NIST AI RMF",
                claim="Governance loops improve reliability",
                quality=SourceQuality.HIGH,
                url="https://www.nist.gov/itl/ai-risk-management-framework",
            )
        ],
        integration_links=["cybernetics", "decision science"],
        predictions=[
            Prediction(
                statement="Calibration error drops",
                metric="calibration_error",
                threshold="-15%",
                horizon_days=90,
            )
        ],
        falsifiers=[
            Falsifier(
                condition="No calibration improvement after loop adoption",
                test_method="pre/post metric audit",
            )
        ],
    )

    weak = ExplanationRecord(
        explanation_id="b",
        title="Weak",
        claim="Better tools create better outcomes and improve success.",
        mechanism="More tools lead to better results.",
        scope="Everything",
    )

    s_eval = evaluate_explanation(strong)
    w_eval = evaluate_explanation(weak)

    assert s_eval.weighted_score > w_eval.weighted_score
    assert s_eval.tests[0].score >= w_eval.tests[0].score
