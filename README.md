# Chatbot_for_Personalized_Learning
A conversational AI chatbot with a UI using Streamlit and built using Rasa that provides personalized recommendations for learning resources, including videos, books, and courses. Additionally, the chatbot leverages a Hugging Face Google/Flan-t5-large model to generate detailed explanations for various topics.

Features
Personalized Recommendations: Suggests videos, books, and courses based on user preferences and topics of interest.Along with ask for study tips ,motivations,etc.
Dynamic Explanations: Uses Hugging Face's Flan-t5-large model to provide concise and accurate explanations for user-asked topics.
Requirements
Python 3.8 or later
Rasa Open Source
Hugging Face Transformers library
Installation
Clone the Repository
git clone https://github.com/your-username/personalized-learning-chatbot.git
cd personalized-learning-chatbot
Install dependencies
pip install -r requirements.txt
Train the Model
rasa train
Trained models are saved in models folder.

Running the bot
Start the Rasa action server

rasa run actions
Start the rasa shell

rasa run -m models --enable-api --cors "*" --debug
Start the streamlit app

streamlit run app.py
