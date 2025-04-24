import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent 


def get_stadium_info(stadium_name):
    try:
        stadiums_path = base_dir / 'data' / 'Stadiums_in_SaudiArabia.csv'
        stadiums_df = pd.read_csv(stadiums_path)
    except FileNotFoundError:
        return "Stadium data file not found."

    stadium = stadiums_df[stadiums_df['Stadium Name'].str.contains(stadium_name, case=False, na=False)]
    if not stadium.empty:
        stadium_info = stadium.iloc[0]
        response = f"{stadium_info['Stadium Name']} - {stadium_info['Location']} (Capacity: {stadium_info['Capacity']}): {stadium_info['Notes']}"
    else:
        response = "Stadium not found."
    return response

def get_match_data(user_input):
    try:
        match_path = base_dir / 'data' / 'wcmatches.csv'
        match_df = pd.read_csv(match_path)
    except FileNotFoundError:
        return "Stadium data file not found."
    print(f"Original Input: {user_input}")
    user_input = user_input.lower()
    filtered_df = match_df.copy()

    # Month check
    months = match_df['month'].str.lower().unique()
    for month in months:
        if month in user_input:
            filtered_df = filtered_df[filtered_df['month'].str.lower() == month]
            print(f"Filtered by month: {month} → {len(filtered_df)} matches")

    # Year check
    for word in user_input.split():
        if word.isdigit() and len(word) == 4:
            filtered_df = filtered_df[filtered_df['year'] == int(word)]
            print(f"Filtered by year: {word} → {len(filtered_df)} matches")

    # Country check
    for country in match_df['country'].str.lower().unique():
        if country in user_input:
            filtered_df = filtered_df[filtered_df['country'].str.lower() == country]
            print(f"Filtered by country: {country} → {len(filtered_df)} matches")

    # Team check
    for team in pd.concat([match_df['home_team'], match_df['away_team']]).str.lower().unique():
        if team in user_input:
            filtered_df = filtered_df[
                (filtered_df['home_team'].str.lower() == team) |
                (filtered_df['away_team'].str.lower() == team)
            ]
            print(f"Filtered by team: {team} → {len(filtered_df)} matches")

    # Group/stage check
    if "group" in user_input:
        filtered_df = filtered_df[filtered_df['stage'].str.lower().str.contains("group")]
        print(f" Filtered by group stage → {len(filtered_df)} matches")

    # Wins/losses
    if "win" in user_input or "won" in user_input:
        filtered_df = filtered_df[filtered_df['outcome'].str.lower().str.contains("win")]
        print(f"Filtered by outcome (win) → {len(filtered_df)} matches")

    if filtered_df.empty:
        print(" No matches found.")
        return "No matches found for your query."

    # Format response
    response = "\n".join(
        f"{row['date']} - {row['home_team']} vs {row['away_team']} in {row['city']} ({row['stage']})"
        for _, row in filtered_df.head(10).iterrows()
    )
    print("Final results:")
    print(response)
    return response
