from backend.services.cache import make_cache_key, get_cache_stats

def test_cache_key_consistency():
    key1 = make_cache_key("what is leave policy", "corporate")
    key2 = make_cache_key("what is leave policy", "corporate")
    assert key1 == key2
    
def test_cache_key_different_domain():
    key1 = make_cache_key("same question", "corporate")
    key2 = make_cache_key("same question", "legal")
    assert key1 != key2
    
def test_cache_key_case_insensitive():
    key1 = make_cache_key("What Is Leave Policy", "corporate")
    key2 = make_cache_key("what is leave policy", "corporate")
    assert key1 == key2