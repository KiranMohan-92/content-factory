from codex_cf.pipeline import CodexCFPipeline


def _weak_candidate(explanation_id: str):
    return {
        "explanation_id": explanation_id,
        "title": "Weak Explanation",
        "claim": "Better leadership always improves outcomes.",
        "mechanism": "Good leaders cause good outcomes.",
        "scope": "All systems",
        "assumptions": ["Leadership quality dominates all factors"],
        "evidence": [
            {
                "source": "Podcast",
                "claim": "Leaders matter",
                "quality": "low",
                "url": "",
                "notes": "Anecdotal"
            }
        ],
        "integration_links": [],
        "predictions": [],
        "falsifiers": []
    }


def test_synthesis_triggers_when_all_candidates_fail_gate():
    topic_input = {
        "topic": "Test Topic",
        "candidate_explanations": [_weak_candidate("x1"), _weak_candidate("x2")],
    }

    pipe = CodexCFPipeline()
    result = pipe.run_knowledge_rail(topic_input)

    assert result.synthesized is True
    assert result.best_explanation.explanation_id in {"x1", "x2", "synth-001"}


def test_publication_package_contains_change_my_mind_triggers():
    topic_input = {
        "topic": "Test Topic",
        "candidate_explanations": [_weak_candidate("x1"), _weak_candidate("x2")],
    }

    pipe = CodexCFPipeline()
    knowledge = pipe.run_knowledge_rail(topic_input)
    pkg = pipe.run_publication_rail(knowledge)

    assert len(pkg.what_would_change_my_mind) > 0
    assert pkg.topic == "Test Topic"
