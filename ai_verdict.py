import json
import sys
from dotenv import load_dotenv

from google import genai
from google.genai import types
import os

load_dotenv()

sys.stdout.reconfigure(encoding="utf-8")

client = genai.Client()

def get_build_verdict(hero: str, items: list[str]) -> dict:

    system_prompt = f"""
    Ты эксперт по билдам в dota 2 с смешным дотерским юмором основываясь на популярных фразах в сообществе игроков.
    Твоя работа это отвечать СТРОГО в формате JSON без разметки markdown: ({{"winrate": число_от_0_до_100, "reason": "твой_комментарий"}}).
    Длина комментария одно предложение и не должна превышать больше 15 слов, не используй сленг других игр.
    Пример идеального ответа:
    -Герой: Anti-Mage, Предметы: Dagon
    {{"winrate": 5, "reason": "С таким билдом и Larl не победит."}}
    Герой: {hero}, Предметы: {items}.
    """

    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=system_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=1300,
            ),
        )
        result = json.loads(response.text)
        return result
    except Exception as e:
        return {"winrate": 0, "reason": "Габэн забанил ответ."}

