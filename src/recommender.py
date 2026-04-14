import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# ── Weight constants for the Algorithm Recipe ──
WEIGHT_GENRE = 2.0
WEIGHT_MOOD = 1.5
WEIGHT_ENERGY = 1.0
WEIGHT_DANCEABILITY = 0.8
WEIGHT_VALENCE = 0.7
WEIGHT_ACOUSTICNESS = 0.5
WEIGHT_TEMPO = 0.3

# Used to normalize tempo_bpm to 0–1 range
TEMPO_MIN = 50
TEMPO_MAX = 200


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_danceability: float
    target_acousticness: float
    target_tempo_bpm: float


def _normalize_tempo(bpm: float) -> float:
    """Normalize a tempo value to 0–1 range."""
    return max(0.0, min(1.0, (bpm - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)))


def _score_profile(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Score a Song against a UserProfile (OOP path). Returns (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Categorical matches
    if song.genre.lower() == user.favorite_genre.lower():
        score += WEIGHT_GENRE
        reasons.append(f"genre match ({song.genre}) +{WEIGHT_GENRE}")

    if song.mood.lower() == user.favorite_mood.lower():
        score += WEIGHT_MOOD
        reasons.append(f"mood match ({song.mood}) +{WEIGHT_MOOD}")

    # Numeric closeness: 1 - |user - song| for each feature
    energy_sim = 1 - abs(user.target_energy - song.energy)
    score += WEIGHT_ENERGY * energy_sim
    reasons.append(f"energy closeness {energy_sim:.2f} * {WEIGHT_ENERGY}")

    valence_sim = 1 - abs(user.target_valence - song.valence)
    score += WEIGHT_VALENCE * valence_sim
    reasons.append(f"valence closeness {valence_sim:.2f} * {WEIGHT_VALENCE}")

    dance_sim = 1 - abs(user.target_danceability - song.danceability)
    score += WEIGHT_DANCEABILITY * dance_sim
    reasons.append(f"danceability closeness {dance_sim:.2f} * {WEIGHT_DANCEABILITY}")

    acoustic_sim = 1 - abs(user.target_acousticness - song.acousticness)
    score += WEIGHT_ACOUSTICNESS * acoustic_sim
    reasons.append(f"acousticness closeness {acoustic_sim:.2f} * {WEIGHT_ACOUSTICNESS}")

    user_tempo_norm = _normalize_tempo(user.target_tempo_bpm)
    song_tempo_norm = _normalize_tempo(song.tempo_bpm)
    tempo_sim = 1 - abs(user_tempo_norm - song_tempo_norm)
    score += WEIGHT_TEMPO * tempo_sim
    reasons.append(f"tempo closeness {tempo_sim:.2f} * {WEIGHT_TEMPO}")

    return score, reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score against the user profile."""
        scored = [(song, _score_profile(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        score, reasons = _score_profile(user, song)
        return f"Score {score:.2f}: " + "; ".join(reasons)


# ── Functional API (used by src/main.py) ──

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    # Categorical matches
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += WEIGHT_GENRE
        reasons.append(f"genre match ({song['genre']}) +{WEIGHT_GENRE}")

    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += WEIGHT_MOOD
        reasons.append(f"mood match ({song['mood']}) +{WEIGHT_MOOD}")

    # Numeric closeness
    numeric_features = [
        ("energy", WEIGHT_ENERGY),
        ("danceability", WEIGHT_DANCEABILITY),
        ("valence", WEIGHT_VALENCE),
        ("acousticness", WEIGHT_ACOUSTICNESS),
    ]
    for feature, weight in numeric_features:
        if feature in user_prefs and feature in song:
            sim = 1 - abs(float(user_prefs[feature]) - float(song[feature]))
            score += weight * sim
            reasons.append(f"{feature} closeness {sim:.2f} * {weight}")

    # Tempo (needs normalization)
    if "tempo_bpm" in user_prefs and "tempo_bpm" in song:
        user_tempo = _normalize_tempo(float(user_prefs["tempo_bpm"]))
        song_tempo = _normalize_tempo(float(song["tempo_bpm"]))
        sim = 1 - abs(user_tempo - song_tempo)
        score += WEIGHT_TEMPO * sim
        reasons.append(f"tempo closeness {sim:.2f} * {WEIGHT_TEMPO}")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        song_score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, song_score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
