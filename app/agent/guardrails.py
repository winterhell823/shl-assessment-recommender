class Guardrails:
    # Only block truly out-of-scope topics - NOT hiring, assessment, role, developer, test, etc.
    BLOCKED_TOPICS = [
        "salary negotiation",
        "legal advice",
        "employment law",
        "contract law",
        "interview questions",        # Block how to interview, not assessment recommendations
        "ignore previous instructions",
        "reveal prompt",
        "system prompt",
        "jailbreak",
        "prompt injection",
        "career advice",              # General career guidance
        "resume review",
        "resume writing",
        "linkedin",
        "salary",                     # Salary negotiation only
        "how to hire",                # General hiring strategy, not assessment recommendations
    ]

    def is_out_of_scope(self, text: str) -> bool:
        """Check if query is truly out of scope.
        
        IN-SCOPE:
        - Assessment recommendations for specific roles
        - Hiring requirements or skills
        - Developer/engineer/role-specific tests
        
        OUT-OF-SCOPE:
        - Salary, legal, career advice
        - Interview question generation
        - General hiring strategy
        """
        text_lower = text.lower()

        for topic in self.BLOCKED_TOPICS:
            if topic in text_lower:
                return True

        return False