import streamlit as st

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

# Main Streamlit App
def main():
    st.sidebar.title("Choose a Game")
    game = st.sidebar.radio("Navigation", ["Home"])

    if game == "Home":
        homepage()

if __name__ == "__main__":
    main()

# streamlit run app_complete.py