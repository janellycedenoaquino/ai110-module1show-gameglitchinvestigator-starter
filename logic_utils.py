import json
import os

LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), "leaderboard.json")


def load_leaderboard():
    """Load the leaderboard from disk.

    Returns:
        List of entry dicts with keys: name, difficulty, attempts, score.
        Returns an empty list if the file does not exist or cannot be parsed.
    """
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_to_leaderboard(name: str, difficulty: str, attempts: int, score: int):
    """
    Save or update a player's score on the leaderboard.

    Names are matched case-insensitively. An existing entry is only replaced
    if the new score is strictly higher. The leaderboard is capped at 5 entries.

    Returns:
        True if the entry was saved or updated, False if the existing score was equal or higher.
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
    """Return the inclusive (low, high) guessing range for the given difficulty.

    Returns:
        (1, 20) for Easy, (1, 50) for Normal, (1, 100) for Hard or unknown.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str, difficulty: str):
    """
    Validate and parse raw text input into an integer guess.

    Args:
        raw: Raw string from the player. May be None or empty.
        difficulty: Current difficulty, used to check the valid range.

    Returns:
        (True, int, None) on success, or (False, None, error_str) on failure.
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
    Compare a guess to the secret number.

    Returns:
        A (outcome, message) tuple where outcome is "Win", "Too High", or "Too Low".
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Apply score changes for a guess outcome.

    Win awards 100 - 10*(attempt_number-1) points (min 10).
    Too High or Too Low each deduct 5 points.

    Returns:
        Updated score as an int.
    """
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
