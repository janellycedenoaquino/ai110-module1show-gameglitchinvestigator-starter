import random
import streamlit as st
from logic_utils import check_guess, get_proximity_hint, get_range_for_difficulty, parse_guess, update_score, load_leaderboard, save_to_leaderboard  # FIX: Refactored logic into logic_utils.py using ClaudeAI

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.html("""
<style>
/* ─── ANIMATIONS ─── */
@keyframes wobble { 0%,100% { transform:rotate(-1.5deg); } 50% { transform:rotate(1.5deg); } }
@keyframes float   { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-6px); } }
@keyframes shake   { 0%,100% { transform:translateX(0); } 50% { transform:translateX(3px); } }

/* ─── TOP RAINBOW BAR ─── */
[data-testid="stHeader"] {
    background: repeating-linear-gradient(
        90deg,
        #ff2d78 0px,  #ff2d78 24px,
        #c084fc 24px, #c084fc 48px,
        #ffe44d 48px, #ffe44d 72px,
        #a7f3d0 72px, #a7f3d0 96px
    ) !important;
    height: 6px !important;
}

/* ─── MAIN BACKGROUND ─── */
.stApp {
    background-color: #ede9fe !important;
    background-image: radial-gradient(circle, rgba(255,45,120,0.10) 1.5px, transparent 1.5px) !important;
    background-size: 18px 18px !important;
    font-family: 'Trebuchet MS', Arial, sans-serif !important;
}

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: #ff2d78 !important;
    border-right: 5px solid #1a0a1e !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #1a0a1e !important;
    font-family: 'Arial Narrow', Arial, sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
}
[data-testid="stSidebar"] p.config-label {
    color: #9b2cfa !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffe44d !important;
    font-family: Impact, 'Arial Narrow', sans-serif !important;
    letter-spacing: 3px !important;
    text-shadow: 3px 3px 0 #1a0a1e !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.4) !important;
    border-style: dashed !important;
}
/* ─── CONFIG BOX: zero out gaps between the 3 parts ─── */
[data-testid="stSidebar"] [data-testid="element-container"]:has(.config-label),
[data-testid="stSidebar"] [data-testid="element-container"]:has([data-testid="stSelectbox"]),
[data-testid="stSidebar"] [data-testid="element-container"]:has(.stat-pill) {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
    margin-top: 0 !important;
    padding-top: 0 !important;
}
/* Top — label */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:has(.config-label) {
    background: #fff9f0 !important;
    border-top: 4px solid #1a0a1e !important;
    border-left: 4px solid #1a0a1e !important;
    border-right: 4px solid #1a0a1e !important;
    padding: 10px 14px 0 14px !important;
}
/* Middle — selectbox */
[data-testid="stSidebar"] [data-testid="stSelectbox"] {
    background: #fff9f0 !important;
    border-left: 4px solid #1a0a1e !important;
    border-right: 4px solid #1a0a1e !important;
    padding: 6px 14px 8px 14px !important;
    overflow: visible !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: #ffe44d !important;
    border: 3px solid #1a0a1e !important;
    border-radius: 0 !important;
    box-shadow: 3px 3px 0 #1a0a1e !important;
    font-family: Impact, 'Arial Narrow', sans-serif !important;
    font-size: 18px !important;
    letter-spacing: 2px !important;
    color: #1a0a1e !important;
    min-height: 45px !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] span {
    color: #1a0a1e !important;
}
/* Bottom — pills */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:has(.stat-pill) {
    background: #fff9f0 !important;
    border-left: 4px solid #1a0a1e !important;
    border-right: 4px solid #1a0a1e !important;
    border-bottom: 4px solid #1a0a1e !important;
    padding: 6px 14px 12px 14px !important;
    box-shadow: 5px 5px 0 #1a0a1e !important;
    overflow: visible !important;
    margin-bottom: 16px !important;
}
/* ─── STAT PILLS ─── */
.stat-pill {
    display: inline-block;
    background: #ff2d78;
    color: #1a0a1e !important;
    font-family: 'Oswald', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    padding: 3px 10px;
    margin: 2px 2px 2px 0;
    letter-spacing: 1px;
    border: 2px solid #1a0a1e;
}

/* ─── TITLE ─── */
h1 {
    font-family: Impact, 'Arial Narrow', sans-serif !important;
    font-size: 52px !important;
    letter-spacing: 3px !important;
    color: #1a0a1e !important;
    text-shadow: 4px 4px 0 #ff2d78, 8px 8px 0 rgba(192,132,252,0.35) !important;
    animation: wobble 5s ease-in-out infinite !important;
    display: inline-block !important;
}

/* ─── SUBHEADERS ─── */
h2, h3 {
    font-family: Impact, 'Arial Narrow', sans-serif !important;
    letter-spacing: 3px !important;
    color: #1a0a1e !important;
    text-shadow: 3px 3px 0 #ff85b3 !important;
}

/* ─── INFO BOX ─── */
[data-testid="stNotification"],
div[data-baseweb="notification"] {
    background: #ff85b3 !important;
    border: 5px solid #1a0a1e !important;
    border-radius: 0 !important;
    box-shadow: 6px 6px 0 #1a0a1e !important;
    font-family: 'Arial Narrow', Arial, sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    color: #1a0a1e !important;
}

/* ─── TEXT INPUT ─── */
.stTextInput,
.stTextInput > div,
.stTextInput > div > div {
    min-height: 80px !important;
    height: auto !important;
    overflow: visible !important;
}
.stTextInput > div > div > input {
    background: white !important;
    border: 5px solid #1a0a1e !important;
    border-radius: 0 !important;
    box-shadow: 6px 6px 0 #1a0a1e !important;
    font-family: Impact, 'Arial Narrow', sans-serif !important;
    font-size: 36px !important;
    letter-spacing: 3px !important;
    padding: 20px 24px !important;
    height: 80px !important;
    line-height: 1.2 !important;
    color: #1a0a1e !important;
    outline: none !important;
    transition: all 0.12s !important;
}
.stTextInput > div > div > input::placeholder {
    color: #c8a8c0 !important;
}
.stTextInput > div > div > input:focus {
    background: #ffe44d !important;
    transform: translate(-2px, -2px) !important;
    box-shadow: 8px 8px 0 #1a0a1e !important;
}
.stTextInput label,
div[data-testid="stTextInput"] label,
div[data-testid="stTextInput"] > label {
    font-family: Impact, 'Arial Narrow', sans-serif !important;
    font-size: 24px !important;
    font-weight: 900 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #1a0a1e !important;
}

/* ─── BUTTONS (shared base) ─── */
.stButton > button {
    border: 4px solid #1a0a1e !important;
    border-radius: 0 !important;
    font-family: Impact, 'Arial Narrow', sans-serif !important;
    font-size: 20px !important;
    letter-spacing: 3px !important;
    box-shadow: 5px 5px 0 #1a0a1e !important;
    transition: all 0.1s !important;
    text-transform: uppercase !important;
    width: 100% !important;
    padding: 14px 20px !important;
    background: #ff2d78 !important;
    color: white !important;
}
.stButton > button:hover {
    transform: translate(-2px, -2px) !important;
    box-shadow: 8px 8px 0 #1a0a1e !important;
    background: #ff85b3 !important;
}
.stButton > button:active {
    transform: translate(3px, 3px) !important;
    box-shadow: 2px 2px 0 #1a0a1e !important;
}
/* ─── NEW GAME button = mint green ─── */
.stButton > button[kind="secondary"],
.stButton > button[data-testid="baseButton-secondary"] {
    background: #a7f3d0 !important;
    color: #1a0a1e !important;
}
.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="baseButton-secondary"]:hover {
    background: #6ee7b7 !important;
    color: #1a0a1e !important;
}

/* ─── CHECKBOX ─── */
.stCheckbox label p {
    font-family: 'Arial Narrow', Arial, sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #9b2cfa !important;
}

/* ─── ALERTS ─── */
[data-testid="stAlert"] {
    border-radius: 0 !important;
    border-width: 4px !important;
    border-style: solid !important;
    box-shadow: 5px 5px 0 #1a0a1e !important;
    font-family: 'Arial Narrow', Arial, sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
}

/* ─── TABLE ─── */
table {
    border: 4px solid #1a0a1e !important;
    box-shadow: 6px 6px 0 #1a0a1e !important;
    font-family: 'Trebuchet MS', Arial, sans-serif !important;
}
th {
    background: #ff2d78 !important;
    color: white !important;
    font-family: Impact, 'Arial Narrow', sans-serif !important;
    letter-spacing: 2px !important;
    font-size: 16px !important;
    border: 2px solid #1a0a1e !important;
}
td { border: 2px solid #1a0a1e !important; font-weight: 700 !important; }
tr:nth-child(even) td { background: #fff9f0 !important; }

/* ─── EXPANDER ─── */
[data-testid="stExpander"] {
    border: 4px solid #1a0a1e !important;
    border-radius: 0 !important;
    box-shadow: 5px 5px 0 #1a0a1e !important;
    background: #f5f0ff !important;
}
[data-testid="stExpander"] summary {
    font-family: 'Arial Narrow', Arial, sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #9b2cfa !important;
}

/* ─── CAPTION / FOOTER ─── */
.stCaption p {
    font-family: 'Arial Narrow', Arial, sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
}
footer { color: rgba(26,10,30,0.35) !important; font-style: italic !important; }

/* ─── SPEECH BUBBLE ─── */
@keyframes pop {
    0% { transform: scale(0.93); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}
.speech-bubble-area {
    margin-bottom: 28px;
    animation: pop 0.45s ease;
}
.speech-bubble {
    background: #ffffff;
    border: 5px solid #1a0a1e;
    border-radius: 24px;
    padding: 22px 30px;
    display: inline-block;
    position: relative;
    box-shadow: 8px 8px 0 #1a0a1e;
    max-width: 620px;
    margin-bottom: 22px;
}
.speech-bubble::after {
    content: '';
    position: absolute;
    bottom: -26px;
    left: 52px;
    width: 0;
    height: 0;
    border-left: 13px solid transparent;
    border-right: 13px solid transparent;
    border-top: 26px solid #1a0a1e;
}
.speech-bubble::before {
    content: '';
    position: absolute;
    bottom: -18px;
    left: 55px;
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-top: 20px solid #ffffff;
    z-index: 1;
}
.game-title {
    font-family: Impact, 'Arial Narrow', sans-serif;
    font-size: 56px;
    line-height: 1;
    letter-spacing: 3px;
    color: #1a0a1e;
    text-shadow: 4px 4px 0 #ff2d78, 8px 8px 0 rgba(192,132,252,0.35);
    animation: wobble 5s ease-in-out infinite;
    display: inline-block;
    margin-bottom: 6px;
}
.subtitle {
    font-family: 'Trebuchet MS', Arial, sans-serif;
    font-size: 13px;
    font-weight: 700;
    font-style: italic;
    color: #9b2cfa;
}
</style>
""")

st.html("""
<style>
@keyframes wobble { 0%,100% { transform:rotate(-1.5deg); } 50% { transform:rotate(1.5deg); } }
@keyframes pop { 0% { transform:scale(0.93); opacity:0; } 100% { transform:scale(1); opacity:1; } }
.speech-bubble-area { margin-bottom: 28px; animation: pop 0.45s ease; }
.speech-bubble {
    background: #ffffff;
    border: 5px solid #1a0a1e;
    border-radius: 24px;
    padding: 22px 30px;
    display: inline-block;
    position: relative;
    box-shadow: 8px 8px 0 #1a0a1e;
    max-width: 620px;
    margin-bottom: 22px;
}
.speech-bubble::after {
    content: '';
    position: absolute;
    bottom: -26px; left: 52px;
    width: 0; height: 0;
    border-left: 13px solid transparent;
    border-right: 13px solid transparent;
    border-top: 26px solid #1a0a1e;
}
.speech-bubble::before {
    content: '';
    position: absolute;
    bottom: -18px; left: 55px;
    width: 0; height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-top: 20px solid #ffffff;
    z-index: 1;
}
.game-title {
    font-family: Impact, 'Arial Narrow', sans-serif;
    font-size: 56px;
    line-height: 1;
    letter-spacing: 3px;
    color: #1a0a1e;
    text-shadow: 4px 4px 0 #ff2d78, 8px 8px 0 rgba(192,132,252,0.35);
    animation: wobble 5s ease-in-out infinite;
    display: inline-block;
    margin-bottom: 6px;
}
.subtitle {
    font-family: 'Trebuchet MS', Arial, sans-serif;
    font-size: 13px;
    font-weight: 700;
    font-style: italic;
    color: #9b2cfa;
}
</style>
<div class="speech-bubble-area">
  <div class="speech-bubble">
    <div class="game-title">🎮 GAME GLITCH INVESTIGATOR</div>
    <div class="subtitle">An AI-generated guessing game. Something is off.</div>
  </div>
</div>
""")

st.sidebar.markdown("## ⚙️ SETTINGS!")
st.sidebar.markdown(
    '<p class="config-label" style="font-family:\'Oswald\',sans-serif;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#9b2cfa;margin:0;">DIFFICULTY LEVEL</p>',
    unsafe_allow_html=True
)

difficulty = st.sidebar.selectbox(
    "",
    ["Easy", "Normal", "Hard"],
    index=1,
    label_visibility="collapsed",
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.markdown(
    f'<span class="stat-pill">Range: {low}–{high}</span>'
    f'<span class="stat-pill">Attempts: {attempt_limit}</span>',
    unsafe_allow_html=True
)

st.sidebar.divider()
leaderboard = load_leaderboard()

if leaderboard:
    entries_html = ""
    for i, entry in enumerate(leaderboard, start=1):
        cls = "lb-entry first" if i == 1 else "lb-entry"
        entries_html += f"""
<div class="{cls}">
  <div class="lb-num">{i}.</div>
  <div class="lb-name">{entry['name']}<br><small>{entry['difficulty']} · {entry['attempts']} attempts</small></div>
  <div class="lb-pts">{entry['score']} PTS</div>
</div>"""
else:
    entries_html = '<p style="font-family:\'Arial Narrow\',Arial,sans-serif;font-size:12px;color:#1a0a1e;font-weight:700;">No scores yet. Win a game to get on the board!</p>'

st.sidebar.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Oswald:wght@700&display=swap');
.lb-title {{
  font-family: 'Bangers', cursive;
  font-size: 30px;
  text-shadow: 3px 3px 0 #1a0a1e;
  letter-spacing: 2px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}}
[data-testid="stSidebar"] .lb-title {{
  color: #ffe44d !important;
}}
.lb-entry {{
  background: #ffffff;
  border: 3px solid #1a0a1e;
  padding: 8px 12px;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 4px 4px 0 #1a0a1e;
  transition: transform 0.1s, box-shadow 0.1s;
  cursor: default;
}}
.lb-entry:hover {{
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 #1a0a1e;
}}
.lb-entry.first {{
  background: #ffe44d;
}}
.lb-num {{
  font-family: 'Bangers', cursive;
  font-size: 24px;
  text-shadow: 2px 2px 0 rgba(0,0,0,0.15);
  width: 28px;
  flex-shrink: 0;
}}
[data-testid="stSidebar"] .lb-num {{
  color: #ff2d78 !important;
}}
.lb-name {{
  font-family: 'Oswald', sans-serif;
  font-weight: 700;
  font-size: 13px;
  flex: 1;
  color: #1a0a1e;
}}
.lb-name small {{
  font-size: 10px;
  font-weight: 400;
  color: #555;
}}
.lb-pts {{
  font-family: 'Bangers', cursive;
  font-size: 19px;
  letter-spacing: 1px;
}}
[data-testid="stSidebar"] .lb-pts {{
  color: #9b2cfa !important;
}}
</style>
<div class="lb-title">🏆 LEADERBOARD</div>
{entries_html}
""")
if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_log = []
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

if "guess_log" not in st.session_state:
    st.session_state.guess_log = []

st.html("""
<style>
@keyframes wobble { 0%,100% { transform:rotate(-1.5deg); } 50% { transform:rotate(1.5deg); } }
.section-label {
    font-family: Impact, 'Arial Narrow', sans-serif;
    font-size: 36px;
    color: #1a0a1e;
    letter-spacing: 3px;
    text-shadow: 3px 3px 0 #ff85b3;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.boom-badge {
    background: #c084fc;
    color: #1a0a1e;
    font-family: Impact, 'Arial Narrow', sans-serif;
    font-size: 14px;
    letter-spacing: 2px;
    padding: 4px 14px;
    transform: rotate(-2deg);
    box-shadow: 3px 3px 0 #1a0a1e;
    border: 3px solid #1a0a1e;
    animation: wobble 3s ease-in-out infinite;
    display: inline-block;
}
</style>
<div class="section-label">
  MAKE A GUESS
  <div class="boom-badge">LET'S GO! 💅</div>
</div>
""")

info_placeholder = st.empty()

debug_placeholder = st.empty()

st.markdown(
    '<p style="font-family: Impact, \'Arial Narrow\', sans-serif; font-size: 24px; font-weight: 900; letter-spacing: 2px; color: #1a0a1e; text-transform: uppercase; margin: 0 0 4px 0; line-height: 1.2;">ENTER YOUR GUESS:</p>',
    unsafe_allow_html=True
)

raw_guess = st.text_input(
    "",
    key=f"guess_input_{difficulty}",
    placeholder="???",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀", type="primary")
with col2:
    new_game = st.button("New Game 🔁", type="secondary")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_log = []
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
            if st.button("Save Score 💾"):
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
        proximity = get_proximity_hint(guess_int, st.session_state.secret)

        if show_hint:
            if outcome == "Too High":
                st.error(message)
            elif outcome == "Too Low":
                st.warning(message)
            st.caption(proximity)

        st.session_state.guess_log.append({
            "#": st.session_state.attempts,
            "Guess": guess_int,
            "Result": outcome,
            "Proximity": proximity,
        })

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

attempts_left = attempt_limit - st.session_state.attempts
info_placeholder.html(f"""
<style>
@keyframes shake {{ 0%,100% {{ transform:translateX(0) rotate(-1deg); }} 50% {{ transform:translateX(3px) rotate(1deg); }} }}
.prompt-panel {{
    background: #ff85b3;
    border: 5px solid #1a0a1e;
    padding: 16px 22px;
    margin-bottom: 14px;
    box-shadow: 6px 6px 0 #1a0a1e;
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.attempts-tag {{
    background: #9b2cfa;
    color: #ffffff;
    font-family: Impact, 'Arial Narrow', sans-serif;
    font-size: 20px;
    padding: 4px 16px;
    letter-spacing: 2px;
    border: 3px solid #1a0a1e;
    box-shadow: 3px 3px 0 #1a0a1e;
    animation: shake 2.5s ease-in-out infinite;
    display: inline-block;
    white-space: nowrap;
}}
</style>
<div class="prompt-panel">
  <span>Guess a number between {low} and {high}.</span>
  <div class="attempts-tag">{attempts_left} LEFT!</div>
</div>
""")

if st.session_state.guess_log:
    st.subheader("📋 Guess History")
    st.table(st.session_state.guess_log)

history_pills = "".join(
    f'<span class="history-pill">{g}</span>' for g in st.session_state.history
) or '<span class="history-pill">[ ]</span>'

debug_placeholder.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Oswald:wght@700&display=swap');
.debug-box-a {{
  border: 4px solid #1a0a1e;
  box-shadow: 6px 6px 0 #1a0a1e;
  overflow: hidden;
}}
.debug-box-a summary {{
  background: #ffffff;
  padding: 10px 16px;
  font-family: 'Oswald', sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 3px;
  color: #9b2cfa;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  list-style: none;
}}
.debug-box-a summary::-webkit-details-marker {{ display: none; }}
.debug-box-a[open] summary {{
  border-bottom: 4px solid #1a0a1e;
}}
.debug-body-a {{
  background: #ffffff;
  padding: 4px 0;
}}
.debug-row-a {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  border-left: 4px solid transparent;
  border-bottom: 1px solid rgba(26,10,30,0.06);
  transition: border-color 0.15s, background 0.15s;
}}
.debug-row-a:hover {{
  border-left-color: #ff2d78;
  background: rgba(255,45,120,0.04);
}}
.debug-row-a:last-child {{
  border-bottom: none;
}}
.row-label-a {{
  font-family: 'Oswald', sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #9b2cfa;
  width: 90px;
  flex-shrink: 0;
}}
.row-value-a {{
  font-family: 'Bangers', cursive;
  font-size: 20px;
  letter-spacing: 2px;
  color: #ff2d78;
}}
.history-pill {{
  display: inline-block;
  background: #ede9fe;
  border: 2px solid #1a0a1e;
  font-family: 'Oswald', sans-serif;
  font-size: 11px;
  font-weight: 700;
  color: #9b2cfa;
  padding: 2px 10px;
  letter-spacing: 1px;
  margin: 2px 2px 2px 0;
}}
</style>
<details class="debug-box-a">
  <summary>&#9654; DEVELOPER DEBUG INFO</summary>
  <div class="debug-body-a">
    <div class="debug-row-a">
      <span class="row-label-a">Secret</span>
      <span class="row-value-a">{st.session_state.secret}</span>
    </div>
    <div class="debug-row-a">
      <span class="row-label-a">Attempts</span>
      <span class="row-value-a">{st.session_state.attempts}</span>
    </div>
    <div class="debug-row-a">
      <span class="row-label-a">Score</span>
      <span class="row-value-a">{st.session_state.score}</span>
    </div>
    <div class="debug-row-a">
      <span class="row-label-a">Difficulty</span>
      <span class="row-value-a">{difficulty}</span>
    </div>
    <div class="debug-row-a">
      <span class="row-label-a">History</span>
      <div>{history_pills}</div>
    </div>
  </div>
</details>
""")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
