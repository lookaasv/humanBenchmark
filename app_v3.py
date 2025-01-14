import streamlit as st
import requests
import random
from nltk.corpus import words
import nltk

# Homepage Function
def homepage():
    st.title("Human Benchmark Games")
    st.write("""
        Welcome to the **Human Benchmark Games**! Test your intelligence and skills with these fun games:
        - **Wordle**: A word-guessing game to challenge your vocabulary and pattern recognition.
        - **Quick Math**: A fast-paced math game to test your calculation skills.
        - **Trivia**: A general knowledge quiz game to test your memory and understanding.

        Select a game from the sidebar to start!
    """)

# Trivia Game Function

# Function to fetch questions from OpenTDB
def fetch_questions(category, difficulty, question_type, num_questions=10):
    # Construct the API request URL based on the selected options
    url = f"https://opentdb.com/api.php?amount={num_questions}"
    if category:  # Add category to the URL if it's not "Any Category"
        url += f"&category={category}"
    if difficulty:  # Add difficulty to the URL if it's not "Any Difficulty"
        url += f"&difficulty={difficulty}"
    if question_type:  # Add question type to the URL if it's not "Any Type"
        url += f"&type={question_type}"

    # Display the API request URL for debugging
    st.write(f"(DEBUG) API Request URL: {url}")

    # Send the API request to fetch questions
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        if data["response_code"] == 0:  # Check if questions were returned successfully
            return data["results"]  # Return the list of questions
        else:
            st.error("Not enough questions available for the selected options.")  # Show an error if no questions are found
            return []  # Return an empty list if no questions are available
    else:
        st.error("Error fetching questions from the API.")  # Handle API errors
        return []  # Return an empty list if the API request fails

# Function to shuffle the answers for a question and store them for consistency
def get_shuffled_answers(question, question_index, question_type):
    # If shuffled answers are not already stored in session state for this question
    if f"answers_{question_index}" not in st.session_state:
        if question_type == "boolean":  # For true/false questions
            answers = ["True", "False"]
            # random.shuffle(answers)  # Shuffle the answers (commented out for clarity)
        else:  # For multiple choice questions
            # Combine incorrect answers with the correct answer and shuffle them
            answers = question["incorrect_answers"] + [question["correct_answer"]]
            random.shuffle(answers)  # Shuffle the answers randomly
        # Store the shuffled answers in session state
        st.session_state[f"answers_{question_index}"] = answers
    # Return the shuffled answers from session state
    return st.session_state[f"answers_{question_index}"]

def trivia_game():
    st.title("Trivia Game")  # Title of the app
    st.write("Answer the questions and test your knowledge!")  # Introduction text

    # Setup for selecting the category, difficulty, and question type
    categories = {
        "Any Category": None,  # Option for any category
        "General Knowledge": 9,
        "Entertainment: Books": 10,
        "Entertainment: Film": 11,
        "Entertainment: Music": 12,
        "Entertainment: Musicals & Theatres": 13,
        "Entertainment: Television": 14,
        "Entertainment: Video Games": 15,
        "Entertainment: Board Games": 16,
        "Science & Nature": 17,
        "Science: Computers": 18,
        "Science: Mathematics": 19,
        "Mythology": 20,
        "Sports": 21,
        "Geography": 22,
        "History": 23,
        "Politics": 24,
        "Art": 25,
        "Celebrities": 26,
        "Animals": 27,
        "Vehicles": 28,
        "Entertainment: Comics": 29,
        "Science: Gadgets": 30,
        "Entertainment: Japanese Anime & Manga": 31,
        "Entertainment: Cartoon & Animations": 32,
    }
    difficulties = {
        "Any Difficulty": None,  # Option for any difficulty
        "Easy": "easy",
        "Medium": "medium",
        "Hard": "hard",
    }
    question_types = {
        "Any Type": None,  # Option for any question type
        "True/False": "boolean",
        "Multiple Choice": "multiple",
    }

    # Initialize session state variables if they are not already set
    if "questions" not in st.session_state:
        st.session_state.questions = []  # List to store the fetched questions
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0  # Track the current question index
    if "score" not in st.session_state:
        st.session_state.score = 0  # Track the user's score
    if "submitted" not in st.session_state:
        st.session_state.submitted = False  # Track if the answer has been submitted

    # Game initialization: Set up the user interface for category, difficulty, and question type selection
    if st.session_state.current_question == 0:
        num_questions = st.slider("Number of questions", 1, 20, 10)  # Select the number of questions for the game
        category = st.selectbox("Choose a category", list(categories.keys()))  # Select category
        difficulty = st.selectbox("Choose difficulty", list(difficulties.keys()))  # Select difficulty
        question_type = st.selectbox("Choose question type", list(question_types.keys()))  # Select question type

        # Start game button: Trigger the fetching of questions when clicked
        if st.button("Start Game"):
            selected_category = categories[category]  # Get selected category ID
            selected_difficulty = difficulties[difficulty]  # Get selected difficulty
            selected_type = question_types[question_type]  # Get selected question type
            # Fetch the questions from the API and store them in session state
            st.session_state.questions = fetch_questions(
                selected_category, selected_difficulty, selected_type, num_questions
            )
            st.session_state.current_question = 1  # Start with the first question
            st.session_state.question_type = selected_type  # Store the question type for later use
            st.session_state.submitted = False  # Reset the submitted state when starting the game

    # Gameplay: Display the current question and options for answering
    if st.session_state.questions:
        question_index = st.session_state.current_question - 1  # Index of the current question
        question = st.session_state.questions[question_index]  # Get the current question
        st.subheader(f"Question {st.session_state.current_question}")  # Display the question number
        st.write(question["question"])  # Display the actual question text

        # Display the progress bar to show how many questions have been answered
        st.progress((st.session_state.current_question - 1) / len(st.session_state.questions))
        # Display the current score
        st.write(f"Score: {st.session_state.score}/{len(st.session_state.questions)}")

        # Get the shuffled answer options (either true/false or multiple choice)
        answers = get_shuffled_answers(question, question_index, st.session_state.question_type)
        selected_answer = st.radio("Choose your answer:", answers)  # Display radio buttons for answer options

        # Submit button: Disable it if the answer has already been submitted
        submit_button = st.button("Submit Answer", disabled=st.session_state.submitted)

        # Handle submission of the answer
        if submit_button and not st.session_state.submitted:
            st.session_state.submitted = True  # Mark the answer as submitted
            # Check if the selected answer is correct
            if selected_answer == question["correct_answer"]:
                st.success("Correct!")  # Display success message
                st.session_state.score += 1  # Increment score if correct
            else:
                st.error(f"Wrong! The correct answer was: {question['correct_answer']}")  # Display error message

        # Show Next Question button only after an answer is submitted
        if st.session_state.submitted:
            next_button = st.button("Next Question")  # Button to go to the next question

            # Proceed to the next question if the Next button is clicked
            if next_button:
                st.session_state.submitted = False  # Reset the submitted state for the next question
                if st.session_state.current_question < len(st.session_state.questions):
                    st.session_state.current_question += 1  # Move to the next question
                else:
                    # Game Over: Display final score and reset the game
                    st.write(
                        f"Game over! Your final score is {st.session_state.score}/{len(st.session_state.questions)}"
                    )
                    # Reset session state for a new game
                    st.session_state.questions = []
                    st.session_state.score = 0
                    st.session_state.current_question = 0
                    st.session_state.submitted = False
                    st.session_state.question_type = None

                    # Reset any stored answers in session state
                    for key in list(st.session_state.keys()):
                        if key.startswith("answers_"):
                            del st.session_state[key]

# Ensure NLTK data is downloaded
nltk.download("words")
english_words = set(words.words())

# Wordle Game Function
def is_valid_word(word):
    """Check if the word is valid and in English."""
    return word.lower() in english_words

def generate_word(common_words):
    """Generate a random 5-letter word."""
    return random.choice(common_words).lower()

def format_feedback(guess, target_word):
    """Generate feedback for a guess based on the target word."""
    feedback = []
    for g_char, t_char in zip(guess, target_word):
        if g_char == t_char:
            # Correct letter in the correct position (Green)
            feedback.append(f"<span style='background-color: #6aaa64; color: white; padding: 5px 10px; margin: 2px; display: inline-block;'>{g_char.upper()}</span>")
        elif g_char in target_word:
            # Correct letter in the wrong position (Yellow)
            feedback.append(f"<span style='background-color: #c9b458; color: white; padding: 5px 10px; margin: 2px; display: inline-block;'>{g_char.upper()}</span>")
        else:
            # Incorrect letter (Gray)
            feedback.append(f"<span style='background-color: #787c7e; color: white; padding: 5px 10px; margin: 2px; display: inline-block;'>{g_char.upper()}</span>")
    return feedback

# Updated Wordle attempts display
def wordle_game():
    st.title("Wordle Game")

    # Load a predefined list of 5-letter common words
    def load_common_words(file_path):
        with open(file_path, "r") as file:
            return [line.strip() for line in file if len(line.strip()) == 5]

    common_five_letter_words = load_common_words("common_words.txt")

    # Generate a target word and initialize game state
    if "target_word" not in st.session_state:
        st.session_state.target_word = generate_word(common_five_letter_words)
    if "attempts" not in st.session_state:
        st.session_state.attempts = []
    if "current_guess" not in st.session_state:
        st.session_state.current_guess = ""

    def submit_guess():
        """Process the user's guess."""
        guess = st.session_state.current_guess.lower()

        if len(guess) != 5:
            st.error("Please enter a 5-letter word.")
        elif not is_valid_word(guess):
            st.error("Not a valid English word.")
        else:
            feedback = format_feedback(guess, st.session_state.target_word)
            st.session_state.attempts.append((guess, feedback))

            # Check for success or game over
            if guess == st.session_state.target_word:
                st.success(f"Congratulations! You guessed the word: {st.session_state.target_word}")
                reset_game()
            elif len(st.session_state.attempts) >= 6:
                st.warning(f"Game Over! The correct word was: {st.session_state.target_word}")
                reset_game()

        # Reset the input field
        st.session_state.current_guess = ""

    def reset_game():
        """Reset the game state for a new round."""
        st.session_state.target_word = generate_word(common_five_letter_words)
        st.session_state.attempts = []

    # Text input for the guess with Enter key functionality
    st.text_input(
        "Enter your guess:",
        value=st.session_state.current_guess,
        max_chars=5,
        on_change=submit_guess,
        key="current_guess",
    )

    # Display attempts in a styled grid format
    st.write("## Attempts")
    if st.session_state.attempts:
        for attempt, feedback in st.session_state.attempts:
            st.markdown("".join(feedback), unsafe_allow_html=True)

    # Display keyboard with color-coded letters
    def render_keyboard():
        """Render an on-screen keyboard with feedback-based coloring."""
        keys = [
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "M"],
        ]
        colors = {}

        # Determine letter colors based on previous attempts
        for attempt, feedback in st.session_state.attempts:
            for char, feedback_item in zip(attempt, feedback):
                if "6aaa64" in feedback_item:  # Green
                    colors[char.upper()] = "#6aaa64"
                elif "c9b458" in feedback_item:  # Yellow
                    if colors.get(char.upper()) != "#6aaa64":  # Only override if not green
                        colors[char.upper()] = "#c9b458"
                elif "787c7e" in feedback_item:  # Gray
                    if char.upper() not in colors:  # Only set gray if no color exists
                        colors[char.upper()] = "#787c7e"

        # Render the keyboard with color coding
        for row in keys:
            cols = []
            for key in row:
                color = colors.get(key, "#d3d6da")  # Default color
                cols.append(f"<span style='background-color: {color}; color: white; padding: 10px; margin: 3px; border-radius: 5px;'>{key}</span>")
            st.markdown(" ".join(cols), unsafe_allow_html=True)

    render_keyboard()

    # Display remaining attempts
    remaining_attempts = 6 - len(st.session_state.attempts)
    st.write(f"Remaining Attempts: {remaining_attempts}")

    # Add a "Give Up" button
    if st.button("Give Up"):
        st.warning(f"The correct word was: {st.session_state.target_word}")
        reset_game()

# Main Streamlit App
def main():
    st.sidebar.title("Choose a Game")
    game = st.sidebar.radio("Navigation", ["Home", "Trivia", "Wordle"])

    if game == "Home":
        homepage()
    elif game == "Trivia":
        trivia_game()
    elif game == "Wordle":
        wordle_game()

if __name__ == "__main__":
    main()

# trivia: https://opentdb.com/api_config.php - used api
# wordle: https://perchance.org/fiveletter - used for the common 5-letter words

# streamlit run app_complete.py
