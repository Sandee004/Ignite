import redis
import json

# Internal fallback store
_local_state = {}
STATE_KEY = "ignite_state"

try:
    # Try to connect with a short timeout so it doesn't hang
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True, socket_connect_timeout=1)
    r.ping() 
    USE_REDIS = True
except (redis.ConnectionError, redis.TimeoutError):
    print("⚠️ Redis not found. Falling back to In-Memory storage.")
    USE_REDIS = False

def get_state():
    if USE_REDIS:
        raw = r.get(STATE_KEY)
        return json.loads(raw) if raw else {}
    return _local_state

def set_state(data):
    global _local_state
    if USE_REDIS:
        r.set(STATE_KEY, json.dumps(data))
    else:
        _local_state = data

def reset_state():
    initial = {
        "status": "idle",
        "queue": [],
        "current_app": None,
        "completed": [],
        "failed": []
    }
    set_state(initial)

# Initialize
if USE_REDIS:
    if not r.exists(STATE_KEY):
        reset_state()
else:
    if not _local_state:
        reset_state()