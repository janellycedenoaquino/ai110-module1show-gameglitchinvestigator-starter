import json
import os

LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), "leaderboard.json")


def load_leaderboard():
    """Load leaderboard from disk. Returns a list of entry dicts."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_to_leaderboard(name: str, difficulty: str, attempts: int, score: int):
    """
    Save score for a player. Each name is unique on the leaderboard.
    Only updates if the new score is higher than the existing one.
    Keeps only the top 5 by score.
    Returns True if the score was saved/updated, False if it was not (existing score was higher).
    """
    entries = load_leaderboard()
    existing = next((e for e in entries if e["name"].lower() == name.lower()), None)
    if existing:
        if score <= existing["score"]:
            return False
        entries.remove(existing)
    entries.append({"name": name, "difficulty": difficulty, "attempts": attempts, "score": score})
    entries.sort(key=lambda e: e["score"], reverse=True)
    entries = entries[:5]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(entries, f)
    return True


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str, difficulty: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    low, high = get_range_for_difficulty(difficulty)
    if value < low or value > high:
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
