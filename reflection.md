# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The first time i ran my code it had many errors. 
  - When i guess a number while checking the developer debug info it said go lower for a number that was not lower than the secret. 
  - When i said a number higher than the secret it said go higher. 
  - inside the Developer Debug Info:
      - the score says -5 instead of -10 for 2 failed attempts
      - the History doesn't show the first attempt
      - attempts are accurate inside of the developer debug info but not on the title where it says "Guess a number between 1 and 100. Attempts left: 5" attempts left is always 5. 
  - allows negative numbers to be added as a guess (should only be between the range)
  - new game button does not work 
  - attempts start at 1 not 0
  - easy should be from 1-20
  - normal should be 1-50
  - hard should be from 1-100
  - title says "Guess a number between 1 and 100. attemots left: " for all of them.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
