import pandas as pd
import os

TICKETS_CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'combined_stadiums_matches_tickets_2034.csv')

def get_ticket_info(ticket_id):
    try:
        df = pd.read_csv(TICKETS_CSV_PATH)
        ticket_id = ticket_id.lower().strip()
        print(f"DEBUG: Processed ticket_id input: '{ticket_id}'")
        df['ticket_serial_processed'] = df['ticket_serial'].str.lower().str.strip()
        print(f"DEBUG: First few processed ticket_serials in CSV: {df['ticket_serial_processed'].head().tolist()}")
        match = df[df['ticket_serial_processed'] == ticket_id]
        print(f"DEBUG: Number of matching tickets found: {len(match)}")

        match = df[df['ticket_serial'].str.lower() == ticket_id]

        if not match.empty:
            row = match.iloc[0]
            seat = row['seat_number']
            price = row['price']
            status = row['status']
            home_team = row['home_team']
            away_team = row['away_team']
            match_date = row['match_date']
            stadium = row['name']
            city = row['city']

            return (
                f"Captain: Your seat is {seat} at {stadium}, {city}.\n"
                f"The match is {home_team} vs {away_team} on {match_date}.\n"
                f"Status: {status.capitalize()}, Price: {price} SAR."
            )
        else:
            return f"Captain: I have no information about ticket ID {ticket_id}."

    except Exception as e:
        return f"Captain: Error fetching ticket info: {e}"
