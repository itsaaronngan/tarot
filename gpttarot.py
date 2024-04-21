import streamlit as st
from openai import OpenAI
import random
import time

# Initialize your API key using Streamlit secrets
openai_api_key = st.secrets["openai"]["api_key"]

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Tarot Cards Definitions
major_arcana = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World"
]
suits = ["Cups", "Pentacles", "Swords", "Wands"]
minor_arcana = [f"{rank} of {suit}" for suit in suits for rank in [
    "Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
    "Page", "Knight", "Queen", "King"
]]
tarot_cards = major_arcana + minor_arcana

# Function to generate a tarot reading
def generate_tarot_reading(tarot_draw, context):
    gpt_model = "gpt-4"
    gpt_temperature = 1
    system_prompt = f"""
    Give me a warm and empathetic 'thesis, antithesis, synthesis' tarot card reading for these cards: {tarot_draw}. Interpret how these cards interact in the context of real life challenges and opportunities. Give me a 700 word reading.
    """
    response = client.chat.completions.create(
        model=gpt_model,
        temperature=gpt_temperature,
        messages=[
            {"role": "system", "content": system_prompt}
        ],
    )
    return response.choices[0].message.content

# Streamlit Layout
st.title("Thesis Antithesis Synthesis Tarot Reading App")

# User inputs
context = st.text_input("Please provide the context of the reading:", "")

if st.button("Draw Tarot Cards and Generate Reading"):
    # Picking 3 random cards
    tarot_draw = random.sample(tarot_cards, 3)

    # Generate tarot reading
    tarot_reading = generate_tarot_reading(tarot_draw, context)

    # Display the results
    st.text(f"Context: {context} ({', '.join(tarot_draw)})")
    st.text(f"Date and Time of Reading: {current_datetime}")
    st.text(f"Model: GPT-4, Temperature: 1")
    st.text(f"Date and Time of Log Entry: {current_datetime}")
    st.subheader("Your Tarot Cards:")
    st.write(tarot_reading)
    st.text("========End of Reading========")
