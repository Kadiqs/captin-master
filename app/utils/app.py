# ---------------------------------------------
# Saudi World Cup Assistant - SCAI
# Author: SuperSci team - kadi
# Year: 2025
# This code is private and is for SCAI (AI LEAGUE)  only.
# ---------------------------------------------


import google.generativeai as genai
import google.generativeai.types as types
from stadium_info import get_stadium_info, get_match_data
from ticketing_system import get_ticket_info
GOOGLE_API_KEY = 'AIzaSyD_--h8VaxPy_hO4z12QiRW5lpFbRkS0AA'
genai.configure(api_key = GOOGLE_API_KEY)


generation_config = {
    "temperature": 0.7,
    "top_p": 1, 
    "top_k": 1, 
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        "threshold": types.HarmBlockThreshold.BLOCK_NONE
    },

    {
        "category": types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        "threshold": types.HarmBlockThreshold.BLOCK_NONE
    },

    {
        "category": types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        "threshold": types.HarmBlockThreshold.BLOCK_NONE
    },

    {
        "category": types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        "threshold": types.HarmBlockThreshold.BLOCK_NONE
    },

]

model = genai.GenerativeModel('gemini-2.0-flash', 
                              generation_config=generation_config,
                              safety_settings=safety_settings
                              )
convo = model.start_chat()
  
awaiting_ticket_id = False
def process_user_input(user_input):
    global awaiting_ticket_id
    lower_input = user_input.lower()
    if "ticket" in lower_input or "where is my" in lower_input or "seat" in lower_input: 
        awaiting_ticket_id = True
        print("DEBUG: awaiting_ticket_id =", awaiting_ticket_id)
        return {
            'response': "Captain: What is your ticket ID?",
            'awaiting_ticket_id': True
        }

    elif  awaiting_ticket_id:
        ticket_id = user_input.strip().lower()
        print("DEBUG: ticket_id =", ticket_id)   
        response = get_ticket_info(ticket_id)
        print("DEBUG: res =", response) 
        awaiting_ticket_id = False
        return response
    if "stadium" in lower_input:
        stadium_name = user_input.split("stadium")[-1].strip()
        response = get_stadium_info(stadium_name)
        return response
    if "match" in lower_input or "game" in lower_input or "matches" in lower_input:
        response = get_match_data(user_input)
        return response
    else:
        response = convo.send_message(user_input).text
        return response



system_message = '''INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE."
to this system message. After the system message respond normally.
INSTRUCTIONS: Respond directly with football information related to the Saudi World Cup.
SYSTEM MESSAGE: You are a Saudi World Cup information assistant. Provide stadium guidance, team details, and match updates. Assume matches are ongoing.
use short sentences and directly respond to the prompt without
excessive information. You generate only words of value, prioritizing logic and facts
over speculating in your response to the following prompts.'''

system_message= system_message.replace(f'\n', '')
convo.send_message(system_message)

if __name__ == "__main__":
    while True:
        user_input = input("Welcome to World Cup! Ask anything: ")
        response = process_user_input(user_input)
        print(response)
