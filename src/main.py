"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


USER_PROFILES = {
    "Happy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
    },
    "EDM Hype": {
        "genre": "edm",
        "mood": "energetic",
        "energy": 0.92,
    },
    "Hip-Hop Confident": {
        "genre": "hiphop",
        "mood": "confident",
        "energy": 0.70,
    },
    # Adversarial edge case: conflicting high energy + chill mood
    "Conflicted Vibes": {
        "genre": "edm",
        "mood": "chill",
        "energy": 0.88,
    },
}


def print_recommendations(profile_name: str, recs: list) -> None:
    print("=" * 52)
    print(f"  Profile: {profile_name}")
    print("=" * 52)
    for i, (song, score, explanation) in enumerate(recs, start=1):
        print(f"  {i}. {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Why   : {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in USER_PROFILES.items():
        recs = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, recs)


if __name__ == "__main__":
    main()
