# Music Recommendation Systems Research

## How Streaming Platforms Recommend Music

### Collaborative Filtering (Using Other Users' Behavior)

Collaborative filtering works by finding patterns across millions of users. The core idea: **if User A and User B both love songs X and Y, then a song User A loves but User B hasn't heard yet is a strong candidate to recommend to User B.**

There are two sub-approaches:

- **User-based filtering** — finds users with similar listening histories, search patterns, and playlists, then recommends what those "taste neighbors" enjoy.
- **Item-based filtering** — finds songs that frequently co-occur. Spotify trains its model on ~700 million user-generated playlists. If two songs appear on the same playlists repeatedly, the system treats them as related — a stronger signal than simple play counts.

**Strengths:** Discovers unexpected connections across genres; doesn't need to "understand" the music itself.
**Weaknesses:** Suffers from the *cold-start problem* (new songs with no user data get zero recommendations) and *sparsity* (users interact with less than 0.1% of a large catalog).

---

### Content-Based Filtering (Using Song Attributes)

Content-based filtering analyzes **the music itself** rather than who listens to it. The system builds a profile of each song's characteristics and matches them to a user's demonstrated preferences.

Platforms extract features through:

- **Raw audio analysis** — tempo (BPM), key, loudness, energy, danceability, acousticness
- **Metadata** — genre tags, artist info, release date, instrumentation
- **NLP on lyrics and cultural context** — sentiment, mood, themes; even web-crawled descriptions from blogs and reviews

**Strengths:** Works for brand-new songs (solves the cold-start problem); explains *why* a recommendation was made.
**Weaknesses:** Tends to recommend "more of the same" — less serendipity than collaborative filtering.

---

## Main Data Types Involved

| Category | Data Signals | Used By |
|---|---|---|
| **Explicit feedback** | Likes, dislikes, ratings, follows | Both approaches |
| **Implicit feedback** | Play counts, skip rate, listen duration, repeat plays, saves to library | Collaborative |
| **Playlist behavior** | Songs added to the same playlist, playlist co-occurrence | Collaborative |
| **Audio features** | Tempo/BPM, key, loudness, energy, danceability, acousticness, valence | Content-based |
| **Mood & emotion** | Mood tags (happy, melancholic, chill), lyric sentiment | Content-based |
| **Metadata** | Genre, artist, album, release year, instrumentation | Content-based |
| **Context signals** | Time of day, device type, activity (workout vs. study) | Both (hybrid) |
| **NLP-derived** | Lyric themes, blog/review descriptors, playlist titles | Content-based |

---

## How Platforms Combine Both (Hybrid Systems)

Both Spotify and YouTube Music use **hybrid approaches**:

- **Spotify** combines collaborative filtering (playlist co-occurrence across 700M+ playlists), content-based filtering (audio analysis + metadata), and NLP (lyrics, blog text) to build a holistic profile of every track.
- **YouTube Music** adds **multimodal understanding** (audio + video + text) and uses transformer-based models for **context-aware recommendations** — e.g., recommending uptempo tracks during a workout session without permanently shifting the user's overall taste profile.

The hybrid model is essential because collaborative filtering alone can't handle new music, and content-based filtering alone can't capture the social dynamics of taste.

---

## Key Takeaway for the Recommender Project

The data types in this simulation — likes, skips, playlists, tempo, mood — map directly to what real platforms use. Likes and skips are **user interaction signals** (collaborative filtering input), while tempo and mood are **song attributes** (content-based filtering input). A realistic simulation should model both.

---

## Sources

- [Inside Spotify's Recommendation System: A Complete Guide](https://www.music-tomorrow.com/blog/how-spotify-recommendation-system-works-complete-guide)
- [Spotify Recommendation Algorithm: What's The Secret?](https://stratoflow.com/spotify-recommendation-algorithm/)
- [Content-Based vs Collaborative Filtering - GeeksforGeeks](https://www.geeksforgeeks.org/machine-learning/content-based-vs-collaborative-filtering-difference/)
- [Complete Guide to YouTube's Recommendations for Music & Artists](https://www.music-tomorrow.com/blog/a-complete-guide-to-youtube-recommendation-algorithms-for-music-and-artists)
- [How Recommendation Systems Work: The Magic Behind YouTube Music](https://medium.com/@gupta.rosh1210/how-recommendation-systems-work-the-magic-behind-youtube-music-53e0552e2c06)
- [Transformers in Music Recommendation - Google Research](https://research.google/blog/transformers-in-music-recommendation/)
- [Content Filtering Methods for Music Recommendation: A Review](https://arxiv.org/html/2507.02282v1)
- [Collaborative Filtering: Your Guide to Smarter Recommendations - DataCamp](https://www.datacamp.com/tutorial/collaborative-filtering)
