import os
import json
import openai


api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found in environment variables.")

openai.api_key = api_key


def openai_response(full_prompt):
    openai_answer = ' '  
    status = '-- '
    explanation = ' '
    
    
    message=[{"role": "user", "content": full_prompt}]
    response = openai.chat.completions.create(
        model="gpt-4.1",
        max_tokens=5000,
        temperature=0.0,
        messages = message
    )
    
    # Access the "content" field inside the "message" within the "choices" array
    openai_answer = response.choices[0].message.content
    
    
    secure_index = openai_answer.lower().find('secure')
    insecure_index = openai_answer.lower().find('insecure')
    inconclusive_index = openai_answer.lower().find('inconclusive')

    # Check which occurs first and set the status accordingly
    if secure_index != -1 and ((insecure_index == -1 or secure_index < insecure_index) and (inconclusive_index == -1 or secure_index < inconclusive_index)):
        status = 'Secure'
    elif insecure_index != -1 and ((secure_index == -1 or insecure_index < secure_index) and (inconclusive_index == -1 or insecure_index < inconclusive_index)):
        status = 'Insecure'
    elif inconclusive_index != -1 and ((secure_index == -1 or inconclusive_index < secure_index) and (insecure_index == -1 or inconclusive_index < insecure_index)):
        status = 'Inconclusive'
    else:
        status = 'Not answered'
    
    return openai_answer, status
    

