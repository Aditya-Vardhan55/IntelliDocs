from backend.services.domain_router import detect_domain, Domain

def test_detect_legal_domain():
    text = "This contract agreement contains termination clauses and liability indemnification"
    assert detect_domain(text) == Domain.LEGAL
    
def test_detect_medical_domain():
    text = "Patient diagnosis shows clinical symptoms requiring medication dosage therapy"
    assert detect_domain(text) == Domain.MEDICAL
    
def test_detect_corporate_domain():
    text = "Employee leave policy handbook benefits vacation onboarding performance"
    assert detect_domain(text) == Domain.CORPORATE
    
def test_detect_code_domain():
    text = "function class import variable api database algorithm repository"
    assert detect_domain(text) == Domain.CODE
    
def test_unknown_domain_fallback():
    text = "xyz abc randomtext nothing matches here at all"
    result = detect_domain(text)
    assert result == Domain.UNKNOWN