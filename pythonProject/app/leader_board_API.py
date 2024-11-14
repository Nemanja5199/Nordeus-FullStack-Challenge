import requests


class LeaderBoardAPI:
    def __init__(self):
        self.base_url = "https://how-high-up-api.onrender.com"

    def get_leaderboard(self, game_mode=None):

        url = f"{self.base_url}/leaderboard"
        if game_mode:
            url += f"?game_mode={game_mode}"

        try:
            response = requests.get(url)
            response.raise_for_status()  
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching leaderboard: {e}")
            return []

    def submit_score(self, player_name, score, streak, game_mode):

        url = f"{self.base_url}/leaderboard"
        data = {
            "player_name": player_name,
            "score": score,
            "streak": streak,
            "game_mode": game_mode
        }

        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error submitting score: {e}")
            return False