from app.retrieval.relevance_filter import RelevanceFilter


def test_relevance_filter_keeps_more_candidates_for_role_queries():
    relevance_filter = RelevanceFilter()
    ranked_items = [
        {
            "name": f"Automata Java Assessment {i}",
            "description": "A Java coding assessment for developers.",
            "skills": ["java"],
            "keywords": ["java"],
        }
        for i in range(12)
    ]

    filtered = relevance_filter.filter("java developer", ranked_items)

    assert len(filtered) >= 10
