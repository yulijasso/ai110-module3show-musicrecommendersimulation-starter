"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
from recommender import load_songs, recommend_songs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    songs = load_songs(os.path.join(BASE_DIR, "data", "songs.csv"))
    print(f"Loaded songs: {len(songs)}")

    # ---------- User Profiles ----------
    profiles = {
        "Pop/Happy Listener": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.80,
            "valence": 0.82,
            "danceability": 0.80,
            "acousticness": 0.20,
            "tempo_bpm": 120,
        },
        "Rock Fan": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.90,
            "valence": 0.50,
            "danceability": 0.65,
            "acousticness": 0.10,
            "tempo_bpm": 150,
        },
        "Lofi Studier": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "valence": 0.58,
            "danceability": 0.60,
            "acousticness": 0.80,
            "tempo_bpm": 75,
        },
        "Party Starter": {
            "genre": "electronic",
            "mood": "energetic",
            "energy": 0.95,
            "valence": 0.75,
            "danceability": 0.92,
            "acousticness": 0.05,
            "tempo_bpm": 128,
        },
        # ── Edge Case / Adversarial Profiles ──
        "Conflicted (High Energy + Sad)": {
            "genre": "pop",
            "mood": "melancholic",
            "energy": 0.92,
            "valence": 0.30,
            "danceability": 0.80,
            "acousticness": 0.15,
            "tempo_bpm": 135,
        },
        "Ghost Genre (genre not in catalog)": {
            "genre": "reggaeton",
            "mood": "happy",
            "energy": 0.70,
            "valence": 0.80,
            "danceability": 0.85,
            "acousticness": 0.30,
            "tempo_bpm": 95,
        },
        "All Zeros (minimum everything)": {
            "genre": "ambient",
            "mood": "chill",
            "energy": 0.0,
            "valence": 0.0,
            "danceability": 0.0,
            "acousticness": 1.0,
            "tempo_bpm": 50,
        },
        "All Maxed (maximum everything)": {
            "genre": "metal",
            "mood": "aggressive",
            "energy": 1.0,
            "valence": 1.0,
            "danceability": 1.0,
            "acousticness": 0.0,
            "tempo_bpm": 200,
        },
        "Middle of the Road (all 0.5)": {
            "genre": "jazz",
            "mood": "relaxed",
            "energy": 0.50,
            "valence": 0.50,
            "danceability": 0.50,
            "acousticness": 0.50,
            "tempo_bpm": 100,
        },
    }

    for profile_name, user_prefs in profiles.items():
        header = f" {profile_name} "
        print(f"\n{'=' * 50}")
        print(f"{header:=^50}")
        print(f"{'=' * 50}")
        prefs_str = ", ".join(f"{k}: {v}" for k, v in user_prefs.items())
        print(f"  Prefs: {prefs_str}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n  {'Rank':<6}{'Title':<25}{'Score':>6}")
        print(f"  {'-' * 37}")
        for rank, (song, score, explanation) in enumerate(recommendations, 1):
            print(f"  {rank:<6}{song['title']:<25}{score:>6.2f}")
            reasons = explanation.split("; ")
            for reason in reasons:
                print(f"         {reason}")
            print()


if __name__ == "__main__":
    main()
