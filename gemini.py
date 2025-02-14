import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
print(os.environ["GOOGLE_API_KEY"])
def classify_message(message):
    try:
        prompt_path = os.path.join(os.path.dirname(__file__), "classification_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as file:
            prompt = file.read()

        prompt = prompt.replace("{message}", message)

        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")

        response = model.generate_content(prompt)
        if response and hasattr(response, "text"):
            content = response.text
            content = content.replace("```json", "").replace("```", "").strip()
            return content
        else:
            return "Error: No content generated."
    except Exception as e:
        return f"Error: {str(e)}"
