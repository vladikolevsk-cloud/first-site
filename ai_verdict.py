import json
import sys
from dotenv import load_dotenv

from openai import OpenAI
import os

load_dotenv()

sys.stdout.reconfigure(encoding="utf-8")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def get_build_verdict(hero: str, items: list[str]) -> dict:

    system_prompt = """
    Ты эксперт по билдам в dota 2 с смешным дотерским юмором основываясь на популярных фразах в сообществе игроков.
    Твоя работа это отвечать СТРОГО в формате JSON без разметки markdown: ({"winrate": число_от_0_до_100, "reason": "твой_комментарий"}).
    Длина комментария одно предложение и не должна превышать больше 15 слов, не используй сленг других игр.
    Пример идеального ответа:
    -Герой: Anti-Mage, Предметы: Dagon
    {"winrate": 5, "reason": "С таким билдом и Larl не победит."}
    """

    user_prompt = f"Герой: {hero}, Предметы: {items}."

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            max_tokens=1300,
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {"winrate": 0, "reason": "Габэн забанил ответ."}
