# **Personalized Learning Chatbot**

A conversational AI chatbot with a user-friendly UI built using **Streamlit** and **Rasa**. This chatbot offers personalized recommendations for learning resources, including videos, books, and courses. It also integrates the **Hugging Face Flan-t5-large** model to provide detailed explanations for various topics, along with motivational content and study tips.

---

## **Key Features**
- **Personalized Recommendations**:
  - Suggests videos, books, and courses tailored to user preferences and topics of interest.
  - Capable of responding to queries about study tips, motivational advice, and more.

- **Dynamic Explanations**:
  - Leverages **Hugging Face's Flan-t5-large** model for generating concise and accurate explanations based on user-input topics.

---

## **Requirements**
To run the chatbot, you need the following:
- **Python** 3.8 or later
- **Rasa Open Source**
- **Streamlit**
- **Hugging Face Transformers Library**
- Additional libraries as specified in `requirements.txt`

---

## **Installation**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/personalized-learning-chatbot.git
   cd personalized-learning-chatbot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the Model**:
   ```bash
   rasa train
   ```
   - Trained models will be saved in the `models` folder.

---

## **Running the Chatbot**
1. **Start the Rasa Action Server**:
   ```bash
   rasa run actions
   ```

2. **Start the Rasa Shell**:
   ```bash
   rasa run -m models --enable-api --cors "*" --debug
   ```

3. **Launch the Streamlit UI**:
   ```bash
   streamlit run app.py
   ```

---

## **How It Works**
1. The user interacts with the chatbot through the **Streamlit UI**.
2. The chatbot processes user inputs using **Rasa** to handle intent classification and slot filling.
3. Based on the user query, the bot performs one or more of the following actions:
   - Retrieves books, courses, or videos by web scraping or API calls.
   - Uses the **Hugging Face Flan-t5-large model** for advanced responses on topics requiring detailed explanations.
4. Results are displayed in an engaging and user-friendly format through the UI.

---

## **File Structure**
```
personalized-learning-chatbot/
├── actions/                     # Contains custom Rasa actions
├── models/                      # Stores trained Rasa models
├── app.py                       # Streamlit-based user interface
├── config.yml                   # Rasa configuration for pipelines and policies
├── credentials.yml              # Configuration for channels like Rest or Socket.IO
├── domain.yml                   # Rasa domain file defining intents, slots, and actions
├── data/                        # Contains NLU and training data
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation (this file)
```

---

## **Future Improvements**
- Add **multilingual support** to serve a wider audience.
- Enhance the recommendation algorithm with advanced machine learning models.
- Enable caching for frequent user queries to improve response time.
- Incorporate a feedback loop for users to rate the recommendations.
- Add a progress tracking feature to monitor learning milestones.

---

## **Contributing**
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and submit a pull request.

---

## **License**
This project is licensed under the [MIT License](LICENSE).


