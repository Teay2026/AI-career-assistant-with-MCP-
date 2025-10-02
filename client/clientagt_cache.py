import json, uuid
from typing import Dict, List

# Simple in-memory cache (no Redis needed)
_memory_cache: Dict[str, any] = {}
_conversations: Dict[str, List[Dict[str, str]]] = {}

def append(cid: str, role: str, text: str):
    """Add a message to conversation history"""
    if cid not in _conversations:
        _conversations[cid] = []
    _conversations[cid].append({"role": role, "text": text})

def fetch(cid: str, last_n: int = 6):
    """Fetch last N conversation items"""
    items = _conversations.get(cid, [])
    # Get last 2*last_n items (each Q/A is two items)
    return items[-2*last_n:] if items else []

def get(key: str):
    """Get cached value"""
    return _memory_cache.get(key, None)

def set(key: str, value: str):
    """Set cached value"""
    _memory_cache[key] = value

def new_conversation_id() -> str:
    """Generate new conversation ID"""
    return str(uuid.uuid4())