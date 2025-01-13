# Human Benchmark Games

## Overview

**Human Benchmark Games** is a collection of interactive games designed to test your intelligence, skills, and memory. The application is built with Python and Streamlit, making it accessible via a web interface. Each game is unique, providing different challenges for users, including word guessing, trivia quizzes, and math puzzles.

### Features
- **Wordle**: A word-guessing game that challenges your vocabulary and pattern recognition skills.
- **Trivia**: A general knowledge quiz game that tests your memory and understanding.
- **Quick Math**: A fast-paced math game to test your arithmetic abilities in a timed environment.

---

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Game Descriptions](#game-descriptions)
5. [Technologies Used](#technologies-used)
6. [Contributing](#contributing)
7. [License](#license)

---

## Installation

Follow these steps to set up and run the application locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/human-benchmark-games.git
   cd human-benchmark-games
   ```

2. **Set up a Python virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**:
   Open a Python shell and run:
   ```python
   import nltk
   nltk.download('words')
   ```

5. **Run the application**:
   ```bash
   streamlit run app_complete.py
   ```

---

## Usage

1. Open the app in your web browser (Streamlit will provide a local URL).
2. Use the sidebar to navigate between games:
   - **Home**: Overview of the app.
   - **Trivia**: Play the trivia quiz.
   - **Wordle**: Guess the five-letter word.
   - **Quick Math**: Launch a timed math challenge in a separate window.

---

## Game Descriptions

### Wordle
- **Objective**: Guess the 5-letter word within 6 attempts.
- **How to Play**:
  - Enter a 5-letter word as your guess.
  - Feedback will be provided:
    - **Green**: Correct letter in the correct position.
    - **Yellow**: Correct letter in the wrong position.
    - **Gray**: Incorrect letter.
  - Use the feedback to refine your guesses.
- **Win Condition**: Correctly guess the word within 6 attempts.

### Trivia
- **Objective**: Answer general knowledge questions.
- **How to Play**:
  - Select a category, difficulty, and question type (True/False or Multiple Choice).
  - Answer each question to earn points.
  - Track your progress and score on the interface.

### Quick Math
- **Objective**: Solve math operations quickly and accurately.
- **How to Play**:
  - The game presents a series of arithmetic operations (+ or -).
  - Enter your calculated result after all operations are displayed.
  - Your score is determined by the accuracy of your answer.
  - **Note**: This game launches in an external Tkinter window.

---

## Technologies Used
- **Python**: Core programming language.
- **Streamlit**: For creating the web interface.
- **Tkinter**: For the external Quick Math game window.
- **Requests**: For fetching trivia questions from the OpenTDB API.
- **NLTK**: For validating English words in Wordle.
- **OpenTDB API**: Trivia question source.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments
- Trivia questions are powered by [OpenTDB](https://opentdb.com).
- Wordle functionality inspired by [perchance.org](https://perchance.org/fiveletter).
- Quick Math idea derived from [SuperClever](https://superclever.world/login).

