import structlog
from enum import Enum

logger = structlog.get_logger()

class Domain(str, Enum):
    LEGAL = "legal"
    MEDICAL = "medical"
    CORPORATE = "corporate"
    CODE = "code"
    UNKNOWN = "unknown"
    
# Keywords that signal each domain
DOMAIN_KEYWORDS = {
    Domain.LEGAL: [
        "contract", "agreement", "clause", "jurisdiction", "liability",
        "indemnification", "termination", "nda", "plaintiff", "defendant",
        "whereas", "hereinafter", "party", "parties", "arbitration"
    ],
    Domain.MEDICAL: [
        "patient", "diagnosis", "treatment", "clinical", "symptom",
        "medication", "dosage", "therapy", "physician", "medical",
        "disease", "syndrome", "trial", "sample size", "methodology"
    ],
    Domain.CORPORATE: [
        "employee", "policy", "hr", "leave", "onboarding", "performance",
        "handbook", "benefits", "vacation", "salary", "promotion",
        "department", "manager", "compliance", "workplace"
    ],
    Domain.CODE: [
        "function", "class", "import", "return", "variable", "api",
        "database", "algorithm", "repository", "deployment", "bug",
        "feature", "pull request", "commit", "refactor"
    ]
}

def detect_domain(text: str) -> Domain:
    """
    Auto-detects document domain based on keyword frequency.
    Returns the domain with highest keyword match count.
    """
    text_lower = text.lower()
    scores = {domain: 0 for domain in Domain if domain != Domain.UNKNOWN}
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[domain] += 1
                
    logger.info("domain_detection_scores", scores=scores)
    
    best_domain = max(scores, key=scores.get)
    
    # If no strong signal, return unknown
    if scores[best_domain] == 0:
        return Domain.UNKNOWN
    
    logger.info("domain_detected", domain=best_domain)
    return best_domain