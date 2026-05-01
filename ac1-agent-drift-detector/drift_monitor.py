# drift_monitor.py
# Core logic: turn text into numbers, compare, classify the result.

from sentence_transformers import SentenceTransformer
import numpy as np

# Load the embedding model once at startup (downloads ~80MB first time)
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Thresholds ---
# These are the cutoff points we agreed on.
# Above 0.80 = agent is still on task (SAFE)
# Between 0.65 and 0.80 = agent is starting to drift (DRIFTING)
# Below 0.65 = agent has wandered far from its goal (ROGUE)
# Calibrated empirically for all-MiniLM-L6-v2 on finance report intents.
THRESHOLDS = {"SAFE": 0.77, "DRIFTING": 0.62}

# Regulatory flags to attach when verdict is ROGUE.
# These don't mean we ran a full compliance check — they're signals
# that a compliance team should investigate.
REGULATORY_FLAGS = [
    "GDPR Art.5 — data minimisation principle",
    "EU AI Act Art.9 — risk management system obligations",
    "DORA — potential significant incident threshold",
]


def embed(text: str) -> np.ndarray:
    # Turn a sentence into a list of 384 numbers.
    # normalize_embeddings=True means the list is scaled so cosine
    # similarity = a simple dot product (faster, same result).
    return model.encode(text, normalize_embeddings=True)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    # Because we normalised, dot product gives cosine similarity directly.
    # Returns a number between 0.0 and 1.0.
    return float(np.dot(a, b))


def classify(score: float) -> str:
    # Map a similarity score to a human-readable verdict.
    if score >= THRESHOLDS["SAFE"]:
        return "SAFE"
    elif score >= THRESHOLDS["DRIFTING"]:
        return "DRIFTING"
    else:
        return "ROGUE"


def check_drift(
    goal_vector: np.ndarray,
    current_intent: str,
    step: int,
    tool: str,
) -> dict:
    # This is called after every tool call.
    # goal_vector  = the original task, already embedded at run start
    # current_intent = what the agent says it's trying to do right now
    # step / tool = metadata for the audit log

    step_vector = embed(current_intent)
    score = cosine_similarity(goal_vector, step_vector)
    verdict = classify(score)

    result = {
        "step": step,
        "tool": tool,
        "intent": current_intent,
        "drift_score": round(score, 4),
        "verdict": verdict,
    }

    # Only attach regulatory flags when we hit ROGUE.
    # A DRIFTING signal is a warning — let the agent continue.
    # A ROGUE signal is a stop — flag it for a human.
    if verdict == "ROGUE":
        result["regulatory_flags"] = REGULATORY_FLAGS

    return result