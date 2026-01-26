import redis
import json

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
STATE_KEY = "ignite_state"

def get_state():
    """Reads current progress from Redis"""
    raw = r.get(STATE_KEY)
    return json.loads(raw) if raw else {}

def set_state(data):
    """Writes state to Redis"""
    r.set(STATE_KEY, json.dumps(data))

def reset_state():
    """Resets to idle"""
    initial = {
        "status": "idle",
        "queue": [],
        "current_app": None,
        "completed": [],
        "failed": []
    }
    set_state(initial)

# Initialize on import
if not r.exists(STATE_KEY):
    reset_state()

    