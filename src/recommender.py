import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its audio/genre attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's listening preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Score a single song against user preferences and return (score, explanation)."""
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    target_energy = float(user_prefs.get("energy", 0.5))
    energy_score = round(1.0 - abs(song["energy"] - target_energy), 2)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score})")

    explanation = ", ".join(reasons)
    return round(score, 2), explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs and return the top k sorted by score descending."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]


class Recommender:
    """OOP wrapper around the scoring logic — used by tests."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by weighted score for the given user."""
        def song_score(song: Song) -> float:
            score = 0.0
            if song.genre.lower() == user.favorite_genre.lower():
                score += 2.0
            if song.mood.lower() == user.favorite_mood.lower():
                score += 1.0
            score += 1.0 - abs(song.energy - user.target_energy)
            if user.likes_acoustic and song.acousticness > 0.5:
                score += 0.5
            return score

        return sorted(self.songs, key=song_score, reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        reasons = []
        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append("genre match (+2.0)")
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append("mood match (+1.0)")
        energy_score = round(1.0 - abs(song.energy - user.target_energy), 2)
        reasons.append(f"energy similarity (+{energy_score})")
        if user.likes_acoustic and song.acousticness > 0.5:
            reasons.append("acoustic preference (+0.5)")
        return ", ".join(reasons) if reasons else "no strong match"
