import streamlit as st
from gtts import gTTS
import os
import speech_recognition as sr

# Text-to-Speech (TTS) function using gTTS
def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)  # slow=False makes the speech faster
        tts.save("output.mp3")
        os.system("start output.mp3")  # On Windows
        # For Linux, use: os.system("mpg321 output.mp3") instead
    except Exception as e:
        st.error(f"Error in text to speech conversion: {e}")

# Speech-to-Text (STT) function using SpeechRecognition
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please say something...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)  # Using Google's speech-to-text API
        return text
    except sr.UnknownValueError:
        return "Sorry, I did not understand that."
    except sr.RequestError:
        return "Sorry, the speech service is unavailable."

# Function to play audio based on selected language
def play_audio(text, lang="en"):
    try:
        # Ensure lang is valid, otherwise fall back to 'en'
        valid_languages = ['en', 'hi', 'or']
        if lang not in valid_languages:
            lang = 'en'  # default to English if language is not supported

        tts = gTTS(text=text, lang=lang)  # 'en' for English, 'hi' for Hindi, 'or' for Odia
        tts.save("audio.mp3")
        os.system("start audio.mp3")  # For Windows
    except Exception as e:
        st.error(f"Error in playing audio: {e}")

# Main function for the Saksham AI Platform
def main():
    # Title of the app
    st.title("Saksham AI: Empowering Rural Women Financially")

    # Localized Financial Education Section
    st.header("Localized Financial Education")
    language = st.selectbox("Choose Your Language:", ["English", "Odia", "Hindi"])

    # Map the selected language to the appropriate language code
    if language == "English":
        lang_code = "en"
        education_text = "Welcome to Saksham AI! Let's learn how to manage your money wisely."
    elif language == "Odia":
        lang_code = "or"
        education_text = "ସାକ୍ଷମ ଏଆଇରେ ସ୍ୱାଗତ । ଆସନ୍ତୁ ଆପଣଙ୍କ ପଇସା କେମିତି ଚାଲନା କରିବେ ସେଠାରେ ଶିଖିବା।"
    elif language == "Hindi":
        lang_code = "hi"
        education_text = "सक्षम एआई में आपका स्वागत है। चलिए सीखते हैं कि पैसे को कैसे संभालना है।"

    # Display the education text and play audio on button click
    st.write(education_text)
    if st.button("Play Audio", key="play_audio_button"):
        play_audio(education_text, lang=lang_code)

    # Input Mode Selection (Text or Voice)
    st.header("Input Mode Selection")
    mode = st.radio("Choose input mode:", ("Text", "Voice"))

    if mode == "Text":
        # User inputs their query through text
        user_input = st.text_input("Enter your query:", key="text_input")
        if user_input:
            # Respond to user input
            response_text = f"Thank you for your question: '{user_input}'. Here's how you can manage your money."
            st.write(response_text)
            # Convert the response text into speech
            play_audio(response_text, lang=lang_code)
    
    elif mode == "Voice":
        # User speaks their query
        if st.button("Start Speaking", key="start_speaking_button"):
            spoken_text = speech_to_text()
            st.write(f"You said: {spoken_text}")
            # Respond to user input
            response_text = f"Thank you for your question: '{spoken_text}'. Here's how you can manage your money."
            st.write(response_text)
            # Convert the response text into speech
            play_audio(response_text, lang=lang_code)

    # Budgeting Tool Section
    st.header("Budgeting Tool")
    st.write("Plan your monthly expenses:")

    # Input for income and expenses
    income = st.number_input("Enter your monthly income (in INR):", min_value=0.0, key="income_input")
    expenses = st.number_input("Enter your monthly expenses (in INR):", min_value=0.0, key="expenses_input")

    # Check if both income and expenses are entered
    if income is not None and expenses is not None:
        savings = income - expenses
        if savings >= 0:
            st.write(f"Your estimated savings: ₹{savings:.2f}")
            if savings < 0:
                st.error("Your expenses exceed your income. Consider revising your budget!")
            else:
                st.success("Great! You're saving money!")
        else:
            st.error("Please enter valid values for income and expenses.")

    # Micro-Investment Suggestions
    st.header("Micro-Investment Opportunities")
    st.write("Based on your savings, we suggest the following options:")
    if savings > 0:
        if savings < 5000:
            st.write("- Start a recurring deposit with your bank.")
            st.write("- Invest in a small self-help group (SHG) scheme.")
        elif savings < 20000:
            st.write("- Consider low-risk mutual funds.")
            st.write("- Start a microbusiness (e.g., dairy, poultry).")
        else:
            st.write("- Explore higher-yield mutual funds or government schemes.")
    else:
        st.write("Once you start saving, we'll provide investment suggestions.")

    # Feedback and Suggestions Section
    st.header("Your Feedback")
    feedback = st.text_area("Share your thoughts or suggestions:", key="feedback_input")
    if st.button("Submit Feedback", key="submit_feedback_button"):
        st.success("Thank you for your feedback!")

# Run the app
if __name__ == "__main__":
    main()
