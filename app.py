import streamlit as st
import requests
import time

# Initialize session state variables for storing chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


# Function to send user message to the Rasa server and get a response
def get_bot_response(user_input):
    try:
        rasa_url = "http://localhost:5005/webhooks/rest/webhook"
        headers = {"Content-Type": "application/json"}
        data = {"sender": "user", "message": user_input}

        response = requests.post(rasa_url, json=data, headers=headers)
        if response.status_code == 200:
            bot_responses = response.json()
            if bot_responses:
                bot_reply = "<br>".join([resp.get("text", "") for resp in bot_responses])
                return bot_reply if bot_reply else "No response"
            else:
                return "No response from the bot."
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Custom CSS for a colorful and educational-themed UI
st.markdown("""
    <style>
        .chat-container {
            background-color: #f0f8ff;
            border-radius: 15px;
            padding: 20px;
            max-width: 800px;
            margin: auto;
            font-family: 'Arial', sans-serif;
        }
        .user-message {
            background-color: #ffcccb;
            color: #000;
            padding: 15px;
            border-radius: 20px;
            text-align: left;
            margin-bottom: 10px;
            box-shadow: 2px 2px 10px rgba(255, 204, 203, 0.6);
        }
        .bot-message {
            background-color: #90ee90;
            color: #000;
            padding: 15px;
            border-radius: 20px;
            text-align: left;
            margin-bottom: 10px;
            box-shadow: 2px 2px 10px rgba(144, 238, 144, 0.6);
        }
        .header-title {
            color: #2a52be;
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 3px 3px 5px rgba(42, 82, 190, 0.6);
        }
    </style>
""", unsafe_allow_html=True)

# Header Title
st.markdown("<div class='header-title'>📚 Welcome to StudyBot!</div>", unsafe_allow_html=True)
st.write("Ask StudyBot your educational questions and get the best resources!")

# Sidebar with suggestions
st.sidebar.title("🎓 StudyBot Commands")
st.sidebar.info("""
You can ask StudyBot to:
- 📚 Give me resources on blockchain  
- 📖 Suggest me some books on Python  
- 🎥 Give me some videos on Machine Learning  
- 🎯 Suggest study tips  
- 💪 Motivate me to keep studying 
- 📖 Ask exam tips 
""")

# Input field for user message
user_input = st.text_input("🤔 Ask StudyBot anything:", placeholder="E.g., 'Suggest me some books on AI'")

# Send button to submit the user input
if st.button("📨 Ask"):
    if user_input.strip():
        with st.spinner('🤖 Thinking...'):
            # Get bot response
            bot_response = get_bot_response(user_input)

            # Append user input and bot response to chat history
            st.session_state.chat_history.append(
                f'<div class="user-message"><b>🧑‍🎓 You:</b> {user_input}</div>')
            st.session_state.chat_history.append(
                f'<div class="bot-message"><b>🤖 StudyBot:</b> {bot_response}</div>')
    else:
        st.warning("⚠️ Please enter a message.")

# Display chat history with improved UI
chat_display = "".join(st.session_state.chat_history)
st.markdown(f"<div class='chat-container'>{chat_display}</div>", unsafe_allow_html=True)
