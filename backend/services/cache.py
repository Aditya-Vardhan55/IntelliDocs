import redis
import json
import hashlib
import structlog
from backend.config import get_settings

logger = structlog.get_logger()
settings = get_settings()

# Single Redis connection reused across all requests
_redis_client = None


def get_redis_client():
    """
    Returns a singleton Redis connection.
    Create it once, reuses forever - same pattern as embeddings.
    """
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                decode_responses=True
            )
            _redis_client.ping()
            logger.info("redis_connected",
                        host=settings.redis_host,
                        port=settings.redis_port)
            
        except Exception as e:
            logger.warning("redis_unavailable",error=str(e))
            return None
    return _redis_client


def make_cache_key(question: str, domain: str) -> str:
    """
    Creates a unique cache key from question + domain.
    We hash it so long questions don't create huge keys.
    Example: "what is leave policy" + "corporate"
                -> "intellidocs:a3f8b2c1..."
    """
    raw = f"{question.strip().lower()}:{domain}"
    hashed = hashlib.md5(raw.encode()).hexdigest()
    return f"intellidocs:{hashed}"


def get_cached_response(question: str, domain: str) -> dict | None:
    """
    Checks Redis for an existing answer.
    Return the cached result if found, None if not.
    Cache hit = skip Ollama entirely = instant response.
    """
    client = get_redis_client()
    if client is None:
        return None
    
    key = make_cache_key(question, domain)
    try:
        cached = client.get(key)
        if cached:
            logger.info("cache_hit", question=question, domain=domain)
            return json.loads(cached)
        logger.info("cache_miss",question=question, domain=domain)
        return None
    except Exception as e:
        logger.warning("cache_get_failed", error=str(e))
        return None
    
    
def set_cached_response(question: str, domain: str, response: dict, ttl: int = 3600):
    """
    Stores an answer in Redis.
    TTL (time to live) = 3600 sec
    After 1 hr the cache expires and fresh answer is generated.
    This prevents stale answers if documents are updated.
    """
    client = get_redis_client()
    if client is None:
        return
    
    key = make_cache_key(question, domain)
    try:
        client.setex(key, ttl, json.dumps(response))
        logger.info("cache_set", question=question, domain=domain, ttl=ttl)
    except Exception as e:
        logger.warning("cache_set_failed", error=str(e))
        

def get_cache_stats() -> dict:
    """
    Returns Redis memory and key stats.
    Able to see the Stats of how many Ollama calls were avoided.
    """
    client = get_redis_client()
    if client is None:
        return {"status": "unavailable"}
    
    try:
        info = client.info("memory")
        total_keys = client.dbsize()
        return {
            "status": "connected",
            "total_cached_queries": total_keys,
            "memory_used": info["used_memory_human"],
            "memory_peak": info["used_memory_peak_human"]
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}