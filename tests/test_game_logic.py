from logic_utils import check_guess

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
