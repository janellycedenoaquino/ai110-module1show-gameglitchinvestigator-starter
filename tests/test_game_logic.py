from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

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
    ok, value, err = parse_guess("42", "Hard")
    assert ok == True
    assert value == 42
    assert err is None

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("", "Normal")
    assert ok == False
    assert value is None
    assert err == "Enter a guess."

def test_parse_guess_none():
    ok, value, err = parse_guess(None, "Normal")
    assert ok == False
    assert value is None
    assert err == "Enter a guess."

def test_parse_guess_non_number():
    ok, value, err = parse_guess("abc", "Normal")
    assert ok == False
    assert value is None
    assert err == "That is not a number."

def test_parse_guess_decimal_truncates():
    # "3.9" should be accepted and truncated to 3
    ok, value, _ = parse_guess("3.9", "Easy")
    assert ok == True
    assert value == 3

def test_parse_guess_out_of_range():
    # 25 is out of range for Easy (1-20)
    ok, value, err = parse_guess("25", "Easy")
    assert ok == False
    assert value is None
    assert err == "Enter a number between 1 and 20."

def test_parse_guess_negative():
    # Negative numbers should be rejected
    ok, value, err = parse_guess("-5", "Normal")
    assert ok == False
    assert value is None
    assert err == "Enter a number between 1 and 50."

def test_score_win_first_attempt():
    # Winning on attempt 1 should give 100 points (100 - 10 * (1-1))
    score = update_score(0, "Win", attempt_number=1)
    assert score == 100

def test_score_too_low_subtracts_5():
    # Any "Too Low" guess should subtract 5
    score = update_score(0, "Too Low", attempt_number=1)
    assert score == -5

def test_score_too_high_subtracts_5():
    # Any "Too High" guess should subtract 5, regardless of attempt number
    score = update_score(0, "Too High", attempt_number=1)
    assert score == -5

def test_score_too_high_even_attempt_subtracts_5():
    # Regression: even-numbered attempts were incorrectly adding 5 instead of subtracting
    score = update_score(0, "Too High", attempt_number=2)
    assert score == -5

def test_score_two_wrong_guesses_is_minus_10():
    # Two failed attempts should result in -10 total
    score = update_score(0, "Too Low", attempt_number=1)
    score = update_score(score, "Too High", attempt_number=2)
    assert score == -10

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
