from openai import OpenAI
import os
from pathlib import Path
import json
import re
import time
from tqdm import tqdm
import random
from notion_client import Client

client = OpenAI()

notion_token = 'secret_5C4IHyThkjKAp69mrW8mfStb78LSKjzZqLlOa1Y6NlZ'
notion_page_id = '1d913f45a7994e04b09b3b2fe67111e5'

notion = Client(auth=notion_token)

# Major Arcana
major_arcana = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World"
]

# Minor Arcana
suits = ["Cups", "Pentacles", "Swords", "Wands"]
minor_arcana = [f"{rank} of {suit}" for suit in suits for rank in [
    "Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
    "Page", "Knight", "Queen", "King"
]]

# Combine Major and Minor Arcana
tarot_cards = major_arcana + minor_arcana

# Picking 3 random cards
tarot_draw = []
for _ in range(3):
    card = random.choice(tarot_cards)
    tarot_draw.append(card)
    tarot_cards.remove(card)

gpt_model="gpt-4"
gpt_temperature=1

def generate_tarot_reading(tarot_draw, context):
    system_prompt = f"""
    Give me a warm and empathetic "thesis, antithesis, synthesis" tarot card reading for these cards: {tarot_draw}. Interpret how these cards interact in the context of real life challenges and opportunities. give me a 700 word reading
    """
    response = client.chat.completions.create(
        model=gpt_model,
        temperature=gpt_temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            #{"role": "user", "content": context}
        ],
    )
    return response.choices[0].message.content

print(f"starting tarot card reading for {tarot_draw}")

# Get the context from the user
context = input("Please provide the context of the reading: ")

tarot_reading = generate_tarot_reading(tarot_draw, context)

print("Tarot Reading:")
print(tarot_reading)

# Get the current date and time
current_datetime = time.strftime("%Y-%m-%d %H:%M:%S")

# Create the log file path
log_file_path = f"/Users/aaronnganm1/Documents/Coding/tarot/tarot_log.txt"

# Write the tarot reading to the log file
with open(log_file_path, "a") as log_file:
    log_file.write(f"\n\n##Context: {context} ({tarot_draw})\n")
    log_file.write(f"Date and Time of Reading: {current_datetime}\n\n")
    log_file.write(f"Model: {gpt_model}, Temperature: {gpt_temperature}\n")
    log_file.write(f"Date and Time of Log Entry: {current_datetime}\n\n")
    log_file.write("Tarot Reading:\n")
    log_file.write(tarot_reading)
    log_file.write("\n========End of Reading========\n")

print(f"Tarot reading logged to: {log_file_path}")

def add_tarot_reading_to_notion(context, tarot_draw, tarot_reading, current_datetime):
    try:
        notion.pages.create(
            parent={"page_id": notion_page_id},
            properties={
                'title': {
                    'title': [
                        {
                            'text': {
                                'content': f'{context}:Tarot Reading for {current_datetime}',
                            },
                        },
                    ],
                },
            },
            children=[
                {
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'rich_text': [
                            {
                                'type': 'text',
                                'text': {
                                    'content': f"Context: {context} ({tarot_draw})\nDate and Time of Reading: {current_datetime}\n\nTarot Reading:\n{tarot_reading}\n========End of Reading========\n\n",
                                },
                            },
                        ],
                    },
                },
            ]
        )
        print("Tarot reading added to Notion successfully!")
    except Exception as e:
        print(f"Failed to add tarot reading to Notion: {e}")

# Example usage
# add_tarot_reading_to_notion(context, tarot_draw, tarot_reading, current_datetime)Aa