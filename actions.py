from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer
import yaml
from bs4 import BeautifulSoup
import requests
import googleapiclient.discovery
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction


# custom action to fetch books
class ActionRequestBook(Action):
    def name(self) -> Text:
        return "action_fetch_books"

    def fetch_books(self, query):
        query = query.replace(" ", "+")
        url = f"https://www.google.com/search?udm=36&q={query}"

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            books = []
            for link in soup.find_all('a', href=True):
                title_div = link.find('div', class_='BNeawe vvjwJb AP7Wnd')
                if title_div:
                    title = title_div.text.strip()
                    href = link['href']
                    books.append((title, href))
            return books
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = tracker.get_slot("topic")

        if not query:
            dispatcher.utter_message(text="Please provide me topic so i can search some books for you")
            return []
        books = self.fetch_books(query)

        if books:
            response = f"Here are some recommended Books on {query} with their links: \n"
            for book in books[:5]:
                response += f"-{book[0]} [View Book]({book[1]})\n"
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_mesaage(text=f"I am sorry. I could not find any relevant books for {query}.")
        return []


# custom action for fetching courses from openlearn
class ActionOpenLearn(Action):
    def name(self) -> Text:
        return "action_fetch_openlearn"

    def fetch_openlearn_courses(self, query):
        query = query.replace(" ", "%20")
        base_url = f"https://www.open.edu/openlearn/local/ocwglobalsearch/search.php?q={query}&filter=all/freecourse,article/all/all/all/all/all&sort=relevant"

        try:
            response = requests.get(base_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            courses = []
            for div in soup.find_all("div", class_="view-detail"):
                link_element = div.find("a", class_="view-detail-link")
                if link_element:
                    link = link_element['href']
                    title_span = link_element.find("span", class_="sr-only")
                    title = title_span.text.strip() if title_span else "No title available"
                    title = " ".join(title.replace("\n", " ").split())  # Normalize whitespace
                    courses.append({"title": title, "link": link})
            return courses
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching courses: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = tracker.get_slot("topic")
        if not query:
            dispatcher.utter_message(text="Please provide me topic so i can search some lessons for you")
            return []
        courses = self.fetch_openlearn_courses(query)

        if courses:
            response = f"Here are some Open Learn courses on {query} with their links: \n"
            for course in courses[:5]:
                response += f"-{course['title']} [View Course]({course['link']})\n"
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_mesaage(
                text=f"I am sorry. I could not find any relevant courses on OpenLearn for {query}.")
        return []


# Custom action to fetch videos from youtube
class ActionYoutubeVideos(Action):
    def name(self) -> Text:
        return "action_get_youtube_videos"

    def get_video_links(self, query: Text) -> List[Dict[str, str]]:
        youtube = googleapiclient.discovery.build("youtube", "v3",
                                                  developerKey="***********")
        request = youtube.search().list(q=query, part="snippet", type="video", maxResults=5)
        response = request.execute()
        video_details = []

        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            video_details.append({
                "title": video_title,
                "link": f"https://www.youtube.com/watch?v={video_id}"
            })

        return video_details

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_query = tracker.get_slot("topic")
        if not user_query:
            user_query = tracker.get_slot("user_pref")
            if not user_query:
                dispatcher.utter_message(text="Please provide a topic so I can search for some lessons for you.")
                return []

        video_details = self.get_video_links(user_query)

        if video_details:
            dispatcher.utter_message(text=f"Here are some videos for {user_query} that you can watch:")
            for detail in video_details:
                dispatcher.utter_message(text=f"{detail['title']}: {detail['link']}\n")
        else:
            dispatcher.utter_message(text=f"I am sorry. I could not find any videos for {user_query}.")

        return []


# Custom action to fetch information for open LLM
class ActionFetchFromGPT(Action):
    def name(self) -> Text:
        return "action_fetch_from_gpt"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        model_name = "google/flan-t5-large"
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = TFAutoModelForSeq2SeqLM.from_pretrained(model_name)
            input_text = tracker.latest_message.get('text')
            inputs = tokenizer(input_text, return_tensors="tf", max_length=1024, truncation=True)

            outputs = model.generate(
                inputs.input_ids,
                max_length=512,  # Increased length for more detailed content
                min_length=100,  # Ensure minimum content length
                num_beams=5,
                temperature=0.7,  # Slightly increased for more creativity
                do_sample=True,
                top_p=0.92,  # Adjusted for better quality
                top_k=50,  # Added top-k sampling
                repetition_penalty=2.5,  # Increased penalty for repetitions
                length_penalty=1.5,  # Encourage longer outputs
                no_repeat_ngram_size=3,  # Prevent 3-gram repetitions
                early_stopping=True
            )

            content = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Format the content for better readability
            formatted_content = content.replace(". ", ".\n\n")

            dispatcher.utter_message(formatted_content)
        except Exception as e:
            print(e)
            dispatcher.utter_message(f"Sorry, I wasn't able to get more information for you. Error: {str(e)}")

        return []
