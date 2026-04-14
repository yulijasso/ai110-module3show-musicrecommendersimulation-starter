# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world music recommenders like Spotify and YouTube Music combine two strategies: **collaborative filtering**, which finds songs loved by users with similar taste, and **content-based filtering**, which matches song attributes (tempo, energy, mood) directly to a user's preferences. Our simulation focuses on content-based filtering — we score each song in a 20-song catalog against a user's taste profile and recommend the highest-scoring matches.

### Data Flow

```
Input (User Prefs)  -->  Process (Score Every Song)  -->  Output (Top K Ranked)
```

1. A user profile and the full song catalog are loaded
2. Each song is scored individually against the user's preferences
3. All scores are sorted highest-to-lowest
4. The top *k* songs are returned with explanations

### Song Features

Each `Song` object carries the following attributes from `data/songs.csv` (20 songs across 16 genres and 10 moods):

- **genre** — categorical (pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, hip-hop, classical, electronic, latin, metal, folk, funk, alternative)
- **mood** — categorical (happy, chill, intense, relaxed, moody, focused, romantic, energetic, melancholic, nostalgic, aggressive, dreamy)
- **energy** — float 0–1, how intense the track feels
- **valence** — float 0–1, emotional positivity (high = happy, low = dark/moody)
- **danceability** — float 0–1, how suitable for movement/rhythm
- **acousticness** — float 0–1, organic vs. electronic production style
- **tempo_bpm** — beats per minute (normalized to 0–1 scale for scoring)

### UserProfile

Each `UserProfile` stores seven preference fields:

- **favorite_genre** — preferred genre (categorical)
- **favorite_mood** — preferred mood (categorical)
- **target_energy** — desired energy level (float 0–1)
- **target_valence** — desired emotional positivity (float 0–1)
- **target_danceability** — desired rhythm/groove level (float 0–1)
- **target_acousticness** — preference for organic vs. electronic sound (float 0–1)
- **target_tempo_bpm** — desired tempo in BPM (normalized for scoring)

### Algorithm Recipe

#### Scoring Rule (one song)

Each song is scored against the user profile using two types of comparison:

**Categorical bonuses** — flat points for exact matches:

| Feature | Points | Rationale |
|---------|--------|-----------|
| Genre match | +2.0 | Strongest preference signal; defines the fundamental sound |
| Mood match | +1.5 | Important but more flexible; people shift moods more easily than genres |

**Numeric closeness** — rewards similarity to the user's target, not just high or low values:

```
feature_score = (1 - |user_preference - song_value|) x weight
```

| Feature | Weight | Rationale |
|---------|--------|-----------|
| Energy | x 1.0 | Core "vibe" indicator, strongest numeric signal |
| Danceability | x 0.8 | Activity-driven, separates workout from study music |
| Valence | x 0.7 | Emotional tone, distinguishes feel-good from brooding |
| Acousticness | x 0.5 | Production style axis, less decisive on its own |
| Tempo | x 0.3 | Correlates with energy, lowest independent contribution |

**Total score** = genre bonus + mood bonus + sum of all weighted closeness scores

**Maximum possible score: ~6.8** (all categorical matches + all numeric closeness near 1.0)

#### Ranking Rule (all songs)

All 20 songs are scored, sorted highest-to-lowest, and the top *k* results are returned with per-song explanations listing the point breakdown.

### Test Profiles

The system ships with three profiles to validate differentiation:

| Field | Rock Fan | Lofi Studier | Party Starter |
|-------|----------|-------------|---------------|
| genre | rock | lofi | electronic |
| mood | intense | chill | energetic |
| energy | 0.90 | 0.35 | 0.95 |
| valence | 0.50 | 0.58 | 0.75 |
| danceability | 0.65 | 0.60 | 0.92 |
| acousticness | 0.10 | 0.80 | 0.05 |
| tempo_bpm | 150 | 75 | 128 |

### CLI Output

![CLI Output - Pop/Happy & Rock Fan](screenshot1.jpeg)
![CLI Output - Lofi Studier & Party Starter](screenshot2.jpeg)

### Expected Biases and Limitations

- **Genre over-prioritization.** At 2.0 points, a genre match is worth more than any single numeric feature. A song that matches genre but misses on every other dimension can still outscore a near-perfect mood/energy match in a different genre. This means the system might ignore great songs that match the user's vibe but happen to be labeled differently.
- **Exact-match penalty for categorical features.** "Indie pop" and "pop" share significant overlap, but the system treats them as completely different genres (0 points). Similarly, "chill" and "relaxed" are close in meaning but score as a total mismatch.
- **No cross-user learning.** The system has no collaborative filtering — it cannot discover that users who like X also tend to like Y. Recommendations are limited to what the numeric attributes can capture.
- **Catalog size bias.** With only 20 songs, genres with more entries (e.g., 2 latin songs vs. 1 classical) have a higher chance of appearing in results, independent of quality of match.
- **Static taste assumption.** The profile is fixed — it cannot adapt to time of day, activity, or evolving taste within a session.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

