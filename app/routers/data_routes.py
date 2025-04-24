from flask import Blueprint, request, jsonify ,session
from utils.app import convo, process_user_input
from utils.ticketing_system import get_ticket_info
from utils.stadium_info import  get_stadium_info, get_match_data
import logging
logging.basicConfig(level=logging.DEBUG)
data_routes = Blueprint('data_routes', __name__)

from flask import Blueprint, request, jsonify, session
# Assuming utils.app, utils.ticketing_system, utils.stadium_info are correctly defined
from utils.app import convo, process_user_input # Assuming process_user_input is needed elsewhere
from utils.ticketing_system import get_ticket_info
from utils.stadium_info import get_stadium_info, get_match_data
import logging

logging.basicConfig(level=logging.DEBUG)
data_routes = Blueprint('data_routes', __name__)

@data_routes.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('prompt', '')
    logging.debug(f"Received raw input: '{user_input}'")
    logging.debug(f"Session state at start of request: {dict(session)}") # Log the whole session

    if not user_input:
        return jsonify({'error': 'Prompt is required'}), 400

    lower_input = user_input.lower()

    if "ticket" in lower_input or "where is my" in lower_input or "seat" in lower_input:
        logging.debug("Detected ticket query. Setting awaiting_ticket_id flag.")
        session['awaiting_ticket_id'] = True
        logging.debug(f"Session state after setting flag: {dict(session)}")
        return jsonify({
            'response': "Captain: What is your ticket ID?",
            'awaiting_ticket_id': True # Signal to frontend we are waiting
        })
    
    elif session.get('awaiting_ticket_id'):
        logging.debug("State: Awaiting ticket ID.")
        ticket_id = lower_input # Assuming the entire input is the ID
        logging.debug(f"Processing '{ticket_id}' as ticket ID.")

        # Important: Clear the flag *after* successfully processing
        session['awaiting_ticket_id'] = False
        logging.debug(f"Session state after clearing flag: {dict(session)}")

        ticket_response = get_ticket_info(ticket_id)
        return jsonify({'response': ticket_response, 'awaiting_ticket_id': False }) # Explicitly send state back if needed


    # --- Handle other specific queries ---
    elif "stadium" in lower_input:
        logging.debug("Detected stadium query.")
        # Basic parsing, might need refinement
        stadium_name = lower_input.split("stadium")[-1].strip()
        if not stadium_name: # Handle cases like "tell me about the stadium"
             stadium_name = "default" # Or ask for clarification
             # return jsonify({'response': "Which stadium are you asking about?"})
        response = get_stadium_info(stadium_name)
        return jsonify({'response': response})

    elif "match" in lower_input or "game" in lower_input or "matches" in lower_input:
        logging.debug("Detected match query.")
        response = get_match_data(user_input) # Pass original input if needed by the function
        return jsonify({'response': response})

    # --- Fallback for general conversation ---
    else:
        logging.debug("No specific keywords matched. Using fallback.")
        fallback = convo.send_message(user_input).text # Assuming convo is initialized
        return jsonify({'response': fallback})


# Minor fix for the /ticket endpoint (extra parenthesis)
@data_routes.route('/ticket', methods=['POST'])
def get_ticket():
    data = request.get_json()
    user_input = data.get('ticket_query', '')

    if not user_input:
        return jsonify({'error': 'ticket_query is required'}), 400

    response = get_ticket_info(user_input)
    return jsonify({'response': response})