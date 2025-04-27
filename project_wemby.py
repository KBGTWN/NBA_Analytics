import time
import pandas as pd
from tqdm import tqdm
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

# Get all NBA players
nba_players = players.get_players()

# Create an empty list to store data
all_career_stats = []

# Loop through each player and fetch their career stats
for player in tqdm(nba_players[:50], desc="Fetching Player Stats"):  # Limit to first 50 players for demo
    player_id = player['id']
    player_name = player['full_name']

    try:
        # Fetch career stats
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        df = career.get_data_frames()[0]

        # Add player name to the dataframe
        df['Player'] = player_name

        # Append to list
        all_career_stats.append(df)

        # Avoid rate limiting
        time.sleep(0.6)  # Adjust delay if necessary

    except Exception as e:
        print(f"Error fetching data for {player_name}: {e}")

# Concatenate all data into a single DataFrame
career_stats_df = pd.concat(all_career_stats, ignore_index=True)

# Save to CSV (optional)
career_stats_df.to_csv("nba_career_stats.csv", index=False)

# Display the first few rows
print(career_stats_df.head())