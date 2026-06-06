import os
import sys
from pathlib import Path

# Add project root to python path to import app modules correctly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.retrieval.search import CatalogSearch
from app.retrieval.vector_store import VectorStore
from app.retrieval.ranker import Ranker
from app.retrieval.relevance_filter import RelevanceFilter


def recall_at_k(predicted_names: list[str], expected_names: list[str], k: int = 10) -> float:
    """
    Computes Recall@K:
    Recall@K = (number of relevant predictions in top K) / (total expected relevant items)
    """
    if not expected_names:
        return 0.0

    # Consider only top K predictions
    top_k_predictions = [name.lower().strip() for name in predicted_names[:k]]
    expected_lower = [name.lower().strip() for name in expected_names]

    relevant_found = 0
    for expected in expected_lower:
        # Check if the expected item is present in top K predictions
        if any(expected in pred or pred in expected for pred in top_k_predictions):
            relevant_found += 1

    return relevant_found / len(expected_names)


def run_evaluation():
    print("=" * 60)
    print("STARTING OFFLINE RECALL@K EVALUATION SUITE")
    print("=" * 60)

    # Initialize components
    search = CatalogSearch()
    vector_store = VectorStore()
    ranker = Ranker()
    relevance_filter = RelevanceFilter()

    # Define test suite with queries and their expected relevant catalog items
    test_cases = [
        {
            "query": "java developer",
            "expected": [
                "Core Java (Advanced Level) (New)",
                "Java (New)",
                "Automata - Java"
            ]
        },
        {
            "query": "devops",
            "expected": [
                "Docker and Kubernetes Specialist",
                "AWS Cloud Practitioner",
                "Cloud Computing Solution",
                "Linux System Administration"
            ]
        },
        {
            "query": "accountant",
            "expected": [
                "Accounts Payable (New)",
                "Accounts Payable Simulation (New)",
                "Accounts Receivable (New)",
                "Accounts Receivable Simulation (New)",
                "Bookkeeping, Accounting, Auditing Clerk Short Form"
            ]
        },
        {
            "query": "banking role",
            "expected": [
                "Bank Operations Supervisor - Short Form",
                "Bank Administrative Assistant - Short Form",
                "Bank Collections Agent - Short Form",
                "Branch Manager - Short Form"
            ]
        },
        {
            "query": "customer support",
            "expected": [
                "Bilingual Spanish Reservation Agent Solution",
                "Bank Collections Agent - Short Form",
                "Administrative Professional - Short Form"
            ]
        }
    ]

    total_recall = 0.0

    for i, case in enumerate(test_cases, 1):
        query = case["query"]
        expected = case["expected"]

        # Run hybrid retrieval pipeline with increased limit=100
        keyword_items = search.search(query, limit=100)
        vector_items = vector_store.search(query, limit=100)
        
        ranked_items = ranker.rank(keyword_items, vector_items, query)
        filtered_items = relevance_filter.filter(query, ranked_items)

        predicted_names = [item.get("name", "") for item in filtered_items]

        # Calculate Recall@10
        recall = recall_at_k(predicted_names, expected, k=10)
        total_recall += recall

        print(f"\n[Test Case {i}] Query: '{query}'")
        print(f"  Expected Items: {expected}")
        print(f"  Predicted Items (Top 10): {predicted_names}")
        print(f"  Recall@10 Score: {recall:.2f} ({int(recall*100)}%)")
        print("-" * 60)

    avg_recall = total_recall / len(test_cases)
    print(f"\nOVERALL SUMMARY:")
    print(f"  Total Test Cases Evaluated: {len(test_cases)}")
    print(f"  Average Recall@10 Score: {avg_recall:.2%}")
    print("=" * 60)


if __name__ == "__main__":
    run_evaluation()