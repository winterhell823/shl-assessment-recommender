from enum import Enum

class IntentType(str, Enum):
    CLARIFY = "CLARIFY"
    RECOMMEND = "RECOMMEND"
    REFINE = "REFINE"
    COMPARE = "COMPARE"
    REFUSE = "REFUSE"
    GREETING = "greeting"
    GENERAL_QUERY = "GENERAL_QUERY"

class TestType(str, Enum):
    COGNITIVE = "COGNITIVE"
    PERSONALITY = "PERSONALITY"
    TECHNICAL = "TECHNICAL"
    BEHAVIORAL = "BEHAVIORAL"
    JOB_FOCUSED = "JOB_FOCUSED"

class ConversationState(str, Enum):
    GREETING = "GREETING"
    COLLECTING_CONTEXT = "COLLECTING_CONTEXT"
    RECOMMENDING = "RECOMMENDING"
    COMPARING = "COMPARING"
    DEFINED_STATE = "DEFINED_STATE"

REQUIRED_CONTEXT_FIELDS = ["role", "skills"]
OPTIONAL_CONTEXT_FIELDS = ["seniority", "duration", "experience_level"]

COMPARISON_KEYWORDS = ["compare", "difference", "vs", "versus", "comparison"]
REFINEMENT_KEYWORDS = ["actually", "change", "add", "remove", "instead", "only", "except", "refine"]

MAX_CLARIFICATION_QUESTIONS = 3
MIN_CONTEXT_COMPLETENESS = 0.5
CONFIDENCE_THRESHOLD = 0.7

GREETING_KEYWORDS = [
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening"
]

# Category Keyword Groups
TECH = [
    "java", "python", "javascript", "react", "angular", "node", "sql",
    "backend", "frontend", "developer", "software", "engineer",
    "coding", "programming", "selenium", "qa", "tester", "devops",
    "cloud", "aws", "data analyst", "data scientist", "machine learning",
    ".net", "mvc", "mvvm", "wcf", "wpf", "xaml", "ado.net"
]

ACCOUNTING = [
    "accountant", "accounting", "accounts", "accounts payable",
    "accounts receivable", "bookkeeping", "finance",
    "invoice", "payable", "receivable"
]

BANKING = [
    "bank", "banking", "branch", "teller",
    "cashier", "money", "financial services"
]

CUSTOMER_SERVICE = [
    "customer service", "customer support", "contact center",
    "call center", "support executive",
    "chat support", "phone support", "reservation agent", "collections agent"
]

SALES = [
    "sales", "business development",
    "retail sales", "sales manager", "account manager"
]

MANAGEMENT = [
    "manager", "leadership",
    "supervisor", "team lead", "director", "operations supervisor"
]

PERSONALITY = [
    "personality", "behavior",
    "behaviour", "culture fit", "opq", "skills development", "global skills"
]

OUT_OF_SCOPE_PATTERNS = {
    "legal": [
        "legal",
        "compliance",
        "law",
        "laws",
        "attorney",
        "lawyer",
        "lawsuit",
        "court",
        "judge",
        "discrimination",
        "harassment",
        "employment law",
        "labor law",
        "labour law",
        "contract law",
        "regulation",
        "regulations",
        "gdpr",
        "eeoc",
        "policy violation",
        "legal notice",
        "sue",
        "suing",
        "termination law",
        "wrongful termination"
    ],

    "salary": [
        "salary",
        "compensation",
        "pay",
        "wage",
        "wages",
        "benefits",
        "bonus",
        "bonuses",
        "increment",
        "raise",
        "pay scale",
        "paycheck",
        "payroll",
        "salary negotiation",
        "ctc",
        "package",
        "offer amount",
        "stipend",
        "overtime pay"
    ],

    "hiring_strategy": [
        "how to hire",
        "hiring process",
        "recruiting strategy",
        "recruitment strategy",
        "talent acquisition",
        "candidate sourcing",
        "how many rounds",
        "recruitment plan",
        "workforce planning",
        "staffing strategy",
        "recruiting funnel",
        "headhunting",
        "campus hiring",
        "lateral hiring",
        "employee retention",
        "hiring budget",
        "best hiring strategy"
    ],

    "interviews": [
        "interview questions",
        "how to interview",
        "what to ask",
        "technical interview",
        "hr interview",
        "behavioral interview",
        "behavioural interview",
        "mock interview",
        "interview tips",
        "interview preparation",
        "coding interview",
        "dsa interview",
        "system design interview",
        "tell me about yourself",
        "interview rounds",
        "aptitude questions",
        "how to crack interview"
    ],

    "general_advice": [
        "career advice",
        "career path",
        "career guidance",
        "future career",
        "job market",
        "industry trends",
        "resume review",
        "cv review",
        "linkedin optimization",
        "personal branding",
        "freelancing advice",
        "startup advice",
        "business advice",
        "investment advice"
    ]
}

# Safe allowlist - queries that contain these keywords are ALWAYS safe recommendations
RECOMMENDATION_ALLOWLIST = [
    "assessment",
    "assessments",
    "test",
    "tests",
    "developer",
    "engineer",
    "frontend",
    "backend",
    "java",
    "python",
    "react",
    "devops",
    "accountant",
    "accounting",
    "banking",
    "customer support",
    "sales",
    "manager",
    "supervisor",
    "director"
]
