import openai
import os  # Make sure to import the os module

# Fetch the API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')  # This will fetch the API key from the environment variable

def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with your model if necessary
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return str(e)
