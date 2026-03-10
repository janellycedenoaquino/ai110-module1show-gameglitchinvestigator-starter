from logic_utils import check_guess
from app import get_range_for_difficulty, parse_guess

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100

def test_parse_guess_valid_number():
    ok, value, err = parse_guess("42")
    assert ok == True
    assert value == 42
    assert err is None

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok == False
    assert value is None
    assert err == "Enter a guess."

def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok == False
    assert value is None
    assert err == "Enter a guess."

def test_parse_guess_non_number():
    ok, value, err = parse_guess("abc")
    assert ok == False
    assert value is None
    assert err == "That is not a number."

def test_parse_guess_decimal_truncates():
    # "3.9" should be accepted and truncated to 3
    ok, value, _ = parse_guess("3.9")
    assert ok == True
    assert value == 3

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_check_guess_requires_int_secret():
    # Regression: secret was cast to str on even attempts, causing TypeError
    # when check_guess tried to compare int > str. Both args must be int.
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High", "int vs int comparison should work without TypeError"

    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low", "int vs int comparison should work without TypeError"
