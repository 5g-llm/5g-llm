import os
#import openai
from openai import OpenAI

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("DeepSeek API key not found in environment variables.")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

def deepseek_response(full_prompt):
    status = '--'
    deepseek_answer = ''

    messages = [{"role": "user", "content": full_prompt}]
    
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages
    )

    # Extract reasoning and answer
    reasoning_content = response.choices[0].message.reasoning_content
    deepseek_answer = response.choices[0].message.content

    return deepseek_answer, status
