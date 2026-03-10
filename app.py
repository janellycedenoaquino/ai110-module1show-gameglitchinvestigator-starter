import random
import streamlit as st
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score, load_leaderboard, save_to_leaderboard  # FIX: Refactored logic into logic_utils.py using ClaudeAI

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

st.sidebar.divider()
st.sidebar.subheader("🏆 Leaderboard")
leaderboard = load_leaderboard()
if leaderboard:
    for i, entry in enumerate(leaderboard, start=1):
        st.sidebar.caption(
            f"{i}. {entry['name']} — {entry['score']} pts "
            f"({entry['difficulty']}, {entry['attempts']} attempts)"
        )
else:
    st.sidebar.caption("No scores yet. Win a game to get on the board!")
if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.leaderboard_saved = False

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "leaderboard_saved" not in st.session_state:
    st.session_state.leaderboard_saved = False

st.subheader("Make a guess")

info_placeholder = st.empty()

debug_placeholder = st.empty()

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.leaderboard_saved = False
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success(
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
        if not st.session_state.leaderboard_saved:
            player_name = st.text_input("Enter your name for the leaderboard:", key="player_name")
            if st.button("Save Score"):
                if player_name.strip():
                    saved = save_to_leaderboard(
                        name=player_name.strip(),
                        difficulty=difficulty,
                        attempts=st.session_state.attempts,
                        score=st.session_state.score,
                    )
                    if saved:
                        st.session_state.leaderboard_saved = True
                        st.rerun()
                    else:
                        st.warning(
                            f"'{player_name.strip()}' already has a higher score on the leaderboard. "
                            "Play again to beat it!"
                        )
                else:
                    st.error("Please enter your name before saving.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, difficulty)

    if not ok:
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.rerun()
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

info_placeholder.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with debug_placeholder.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
