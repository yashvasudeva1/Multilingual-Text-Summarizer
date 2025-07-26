#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set. Please set it.")

client = Groq(api_key=groq_api_key)

def summarize_text_groq(text):
    """Summarizes the given text using the Groq API."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text:\n\n{text}"
                }
            ],
            model="llama3-8b-8192", # Using a suitable Groq model for summarization
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error during summarization: {e}")
        return None

def translate_text_groq(text, target_language):
    """Translates the given text to the target language using the Groq API."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant that translates text to {target_language}."
                },
                {
                    "role": "user",
                    "content": f"Translate the following text to {target_language}:\n\n{text}"
                }
            ],
            model="llama3-8b-8192", # Using a suitable Groq model for translation
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

print("Groq client instantiated and functions defined.")

user_text = input("Please enter the text you want to summarize: ")
target_language = input("Please enter the target language for the translated summary (e.g., French, Spanish): ")

summary = summarize_text_groq(user_text)

if summary:
    print("\nSummarization successful. Translating...")
    translated_summary = translate_text_groq(summary, target_language)

    if translated_summary:
        print("\nTranslation successful. Here is the translated summary:")
        print(translated_summary)
    else:
        print("\nError: Could not translate the summary.")
else:
    print("\nError: Could not summarize the text.")


# In[ ]:




