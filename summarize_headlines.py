# summarize_headlines.py

import requests

# Your OpenAI API key
api_key = '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'  # Replace with your actual API key

# Function to send the headlines to OpenAI for filtering
def filter_headlines(titles):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    # Crafting the prompt to instruct GPT to filter the relevant headlines
    messages = [
        {"role": "system", "content": "Je bent een assistent gespecialiseerd in de Nederlandse vastgoedmarkt."},
        {"role": "user", "content": f"Hier is een lijst met krantenkoppen:\n{titles}\nSelecteer alleen de krantenkoppen die relevant zijn voor de Nederlandse commerciële vastgoedmarkt. Geef alleen de kop en niks anders"}
    ]
    
    data = {
        "model": "gpt-4",  # or "gpt-3.5-turbo"
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.5
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
