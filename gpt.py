
import requests
import json

def bot(history, url, acsses_key, top_p):

  API_KEY = acsses_key

  payload = json.dumps({
    "model": "gpt-3.5-turbo",
    "messages": history,
    "stream": False,
    "model_params": {"temperature": 0.8, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0, "context": "off"}
    })
  headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)


  data = [response.json()['choices'][0]['message']['content'], response.json()['usage']['total_tokens']]

  return data