import os
from dataclasses import dataclass
from pathlib import Path

import openai
import requests
from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent

env_file = os.path.join(BASE_DIR, ".env")
env = Env()
env.read_env(env_file, recurse=False)

token = 'Bearer ' + env.str('TOKEN')
url = env.str('URL')

openai.api_key = env.str("OPENAI_API_KEY")

messages = [{"role": "system", "content": "Welcome! I am your intelligent jobseeker assistant."}]


@dataclass
class JobSeekerAssistant:
    profile_name: str
    phone_number_id: str
    whatsApp_id: str
    from_id: str
    text_message: str
    reply: str = None

    def send_whatsapp_message(self):
        headers = {"Authorization": token}
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self.from_id,
            "type": "text",
            "text": {"body": self.reply}
        }
        res = requests.post(url, headers=headers, json=payload)
        return res.json()

    def ask_agent(self):
        messages.append(
            {"role": "user", "content": self.text_message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

        # Run the prompt through the agent.
        self.reply = chat['choices'][0]['message']['content']

        messages.append({"role": "assistant", "content": self.reply})
