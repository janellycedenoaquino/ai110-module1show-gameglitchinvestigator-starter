# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
- What did the game look like the first time you ran it?
The first time i ran my code it looked fine but had many errors. 
  

- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").
- [x] When i guess a number while checking the developer debug info it said go lower for a number that was not lower than the secret.
  - [x] When i said a number higher than the secret it said go higher.
  - inside the Developer Debug Info:
      - [x] the score says -5 instead of -10 for 2 failed attempts
      - [ ] after the first guess, attempts left, attempts, score, and history all stay the same — nothing updates until the second guess (debug expander and info message render before submit logic runs, so all values are one rerun behind)
      - [ ] invalid inputs like letters are added to history as past guesses
      - [ ] attempts are accurate inside of the developer debug info but not on the title where it says "Guess a number between 1 and 100. Attempts left: 5" attempts left is always 5.
  - [ ] allows negative numbers to be added as a guess (should only be between the range)
  - [ ] win score formula uses `attempt_number + 1` but attempt_number is already 1-indexed, so winning on the first try gives 80 points instead of 90 (off-by-one in update_score)
  - [x] new game button does not work
  - [x] attempts start at 1 not 0
  - [x] easy should be from 1-20
  - [x] normal should be 1-50
  - [x] hard should be from 1-100
  - [x] should normal be 8 attempts? easy be 6 and hard be 5?
  - [x] title says "Guess a number between 1 and 100. attemots left: " for all of them.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? ClaudeAI
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result). 

AI suggested to change the tests I had for the "test_winning_guess()" function. the variable we had with the result was a tuple. instead of storing it as a tuple AI suggested we store it in two different variables and use the assert with the value we needed. before i accepted double checked by checking what the function returned and it does return a tuple. so i accepted the changes and my tests pass.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result). 

When i gave AI the command to move the check_guess to logic_utils.py it didn't find the method inside of app.py so it skipped that step entirely and gave me only suggestions to code the logic inside of logic_utils.py skipping my request entirely.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  I ran the app and tested it manually. i also read the tests and made sure that they were passing and correct. ex: for the issue where the suggestion was to go higher when it should be lower. I wrote smaller numbers and ensure the suggestion was to go higher not lower and wrote larger numbers than the target and checked it said go lower. 

- Did AI help you design or understand any tests? How?

yes AI helped me write the test for the function "test_check_guess_requires_int_secret()" it also made sure we didn't need to cast the value to an int to be able to compare it. it fixed that error. 

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
because the every button we clicked on re-ran the app and it cause a new number to show.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit? 

streamlit re-runs clear out the page of the session data. every info you had whiped every time you click or make any changes in the app. session state keeps the state of your application. any changes you have made stored for example you have a secret number the application should keep that number no matter what you click until you click the new game button which should wipe the state/session data

- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

I learned to ask AI questions in steps, test everything as I go and make sure to commit and push my code with different changes i make to store all the changes i make and prevent getting stuck/make a mistake and have to delete everything.

- What is one thing you would do differently next time you work with AI on a coding task?

make branches and push my code to different branches and merge them.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

it should be seen more as a co-working partner than a machine that does all the work for you. it should be used to learn with it. 
