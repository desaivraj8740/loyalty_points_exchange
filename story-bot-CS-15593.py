import requests
import json

BASE_URL = "https://api.closerouter.com/v1/chat/completions"
API_KEY = "HEHE"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "text/event-stream"
}

def generate_story(title, genre, language):
    """
    Generate story using Closerouter streaming API in selected language
    """
    system_prompt = "You are a helpful assistant."
    
    
    if language == "Hindi (Hinglish)":
        lang_instruction = (
            "Write the story in Hindi using Hinglish (Roman script). "
            "Keep it readable and engaging."
        )
    else:  
        lang_instruction = "Write the story in English in a creative and engaging way."

    user_prompt = (
        f"Write a {genre} story titled '{title}'. {lang_instruction}"
    )

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "model": "gpt-4o",
        "stream": True,
        "temperature": 0.7,
        "max_tokens": 4000
    }

    story_text = ""
    try:
        with requests.post(BASE_URL, headers=HEADERS, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith('data:'):
                        data = decoded_line[5:].strip()
                        if data == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data)
                            content = chunk["choices"][0]["delta"].get("content")
                            if content:
                                print(content, end="", flush=True)
                                story_text += content
                        except json.JSONDecodeError:
                            pass
        print("\n")  
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")

    return story_text

def save_story_to_file(story):
    filename = input("Enter the filename to save the story (with .txt extension): ")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(story)
        print(f"Story saved successfully as '{filename}'!")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    print("Welcome to the AI Storyteller Bot!")
    print("Create engaging stories in your preferred language.\n")

    genre = input("Enter the genre of your story (fantasy, mystery, sci-fi, horror, adventure): ").strip()
    title = input("Enter the title of your story: ").strip()

    print("\nSelect the language for your story:")
    print("1) English")
    print("2) Hindi (Hinglish)")
    lang_choice = input("Enter choice (1/2): ").strip()

    language_map = {
        "1": "English",
        "2": "Hindi (Hinglish)"
    }
    language = language_map.get(lang_choice, "English")

    print(f"\nGenerating your story in {language}...\n")
    story = generate_story(title, genre, language)

    
    choice = input("Do you want to view the story here or save to a text file? (view/save): ").lower()
    if choice == "save":
        save_story_to_file(story)
    else:
        print("\n----- Your Story -----\n")
        print(story)
        print("\n---------------------\n")

if __name__ == "__main__":
    main()
=======
import requests
import json

BASE_URL = "https://api.closerouter.com/v1/chat/completions"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJkMzMzN2Y3NS0zYzkyLTQ5ODMtYjFhNS1hZjI5NjI3OWJiMTUiLCJlbWFpbCI6ImRlc2FpdnJhajczQGdtYWlsLmNvbSIsImtleUlkIjoiODUyZGRjMGMtZTViYy00OWNhLTgzODMtODJhYjgyMTNiNmUzIiwidHlwZSI6ImFwaV9rZXkiLCJpYXQiOjE3NTU1OTIyMzl9.mEehlbrI854THJ2PrdE7pR-a2DlLRGUpMvG5FzotK50"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "text/event-stream"
}

def generate_story(title, genre, language):
    """
    Generate story using Closerouter streaming API in selected language
    """
    system_prompt = "You are a helpful assistant."
    
    
    if language == "Hindi (Hinglish)":
        lang_instruction = (
            "Write the story in Hindi using Hinglish (Roman script). "
            "Keep it readable and engaging."
        )
    else:  
        lang_instruction = "Write the story in English in a creative and engaging way."

    user_prompt = (
        f"Write a {genre} story titled '{title}'. {lang_instruction}"
    )

    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "model": "gpt-4o",
        "stream": True,
        "temperature": 0.7,
        "max_tokens": 4000
    }

    story_text = ""
    try:
        with requests.post(BASE_URL, headers=HEADERS, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith('data:'):
                        data = decoded_line[5:].strip()
                        if data == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data)
                            content = chunk["choices"][0]["delta"].get("content")
                            if content:
                                print(content, end="", flush=True)
                                story_text += content
                        except json.JSONDecodeError:
                            pass
        print("\n")  
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")

    return story_text

def save_story_to_file(story):
    filename = input("Enter the filename to save the story (with .txt extension): ")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(story)
        print(f"Story saved successfully as '{filename}'!")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    print("Welcome to the AI Storyteller Bot!")
    print("Create engaging stories in your preferred language.\n")

    genre = input("Enter the genre of your story (fantasy, mystery, sci-fi, horror, adventure): ").strip()
    title = input("Enter the title of your story: ").strip()

    print("\nSelect the language for your story:")
    print("1) English")
    print("2) Hindi (Hinglish)")
    lang_choice = input("Enter choice (1/2): ").strip()

    language_map = {
        "1": "English",
        "2": "Hindi (Hinglish)"
    }
    language = language_map.get(lang_choice, "English")

    print(f"\nGenerating your story in {language}...\n")
    story = generate_story(title, genre, language)

    
    choice = input("Do you want to view the story here or save to a text file? (view/save): ").lower()
    if choice == "save":
        save_story_to_file(story)
    else:
        print("\n----- Your Story -----\n")
        print(story)
        print("\n---------------------\n")

if __name__ == "__main__":
    main()
