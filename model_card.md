# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This recommender suggests 5 songs from a 20-song catalog based on a user's preferred genre, mood, energy level, valence, danceability, acousticness, and tempo. It is a classroom simulation designed for exploring how content-based filtering works — not for real users or production use.

It assumes the user can express their taste as a single fixed profile with numeric targets. It does not learn from listening history or adapt over time.

---

## 3. How the Model Works

The system scores every song in the catalog against the user's taste profile using two types of comparison:

- **Categorical matching:** If a song's genre or mood matches the user's preference exactly, it earns bonus points (genre is worth more than mood because genre defines the fundamental sound).
- **Numeric closeness:** For features like energy, danceability, valence, acousticness, and tempo, the system measures how close the song's value is to the user's target. A perfect match scores 1.0; a complete mismatch scores 0.0. Each feature is multiplied by a weight reflecting its importance.

All the points are added up into a single score per song. The songs are sorted from highest to lowest, and the top 5 are returned with an explanation of why each one was chosen.

---

## 4. Data

The catalog contains **20 songs** across **16 genres** and **12 moods**. The original starter dataset had 10 songs; 10 more were added to diversify representation.

- **Most represented genre:** lofi (3 songs, 15%)
- **Most represented mood:** happy (4 songs, 20%)
- **Energy skew:** 10 songs (50%) have energy >= 0.7, while only 5 songs (25%) have energy < 0.4. The catalog leans high-energy.
- **Missing tastes:** No country, no reggae, no K-pop, no classical vocal — the catalog reflects a narrow slice of Western indie/electronic taste. Users who prefer these genres will get poor recommendations since there are no matching songs.

---

## 5. Strengths

- **Clear-cut profiles get excellent results.** When a user's genre and mood both exist in the catalog, the #1 recommendation is almost always the right song (e.g., Rock Fan → Storm Runner, Lofi Studier → Library Rain).
- **Transparent scoring.** Every recommendation comes with a point-by-point explanation, making it easy to understand and debug.
- **Handles missing genres gracefully.** When a user requests a genre not in the catalog (like "reggaeton"), the system doesn't crash — it falls back to mood and numeric matching, producing reasonable results.
- **Distinct results per profile.** Across 9 test profiles, every one got a different #1 song, confirming the system differentiates well.

---

## 6. Limitations and Bias

**Genre over-prioritization creates a filter bubble.** At 2.0 points, a genre match is the single strongest signal in the system. This means the system will always prefer a mediocre same-genre song over a great song from a neighboring genre. For example, "indie pop" and "pop" are treated as completely unrelated (0 bonus), even though they share significant musical overlap. A user who likes pop will never be recommended "Rooftop Lights" (indie pop) ahead of "Gym Hero" (pop), even when Rooftop Lights is a better vibe match on every numeric feature.

**The "Conflicted" profile exposed mood blindness.** When a user asks for pop genre but melancholic mood, the system recommends Gym Hero — an upbeat gym anthem — because genre (+2.0) outweighs mood (+1.5). Musically, this is wrong. A sad person does not want a hype track. The system has no concept of preference conflict or emotional priority.

**High-energy bias in the catalog.** Half the songs (10 out of 20) have energy >= 0.7, while only 5 have energy < 0.4. This means low-energy users have fewer options, and the system may repeatedly recommend the same small pool of quiet songs while high-energy users enjoy variety. This is a form of representation bias — the catalog itself is skewed.

**No discovery or diversity.** The system always returns the closest matches. It will never suggest something unexpected that the user might love but hasn't considered. Real recommenders like Spotify inject "exploration" tracks to break filter bubbles; this system has no such mechanism.

**Static profiles ignore context.** The same user might want lofi at midnight and metal at the gym. The profile has no notion of time, activity, or mood evolution within a session.

---

## 7. Evaluation

- Tested 9 user profiles: 4 standard (Pop/Happy, Rock Fan, Lofi Studier, Party Starter) and 5 adversarial (Conflicted, Ghost Genre, All Zeros, All Maxed, Middle of the Road).
- Confirmed every profile produces a unique #1 song.
- Tracked song frequency: "Gym Hero" appeared in 5/9 top-5 lists, flagged as a generalist.
- Ran a weight shift experiment (genre 2.0→1.0, energy 1.0→2.0) and compared results. Found that lower genre weight improved edge-case accuracy but reduced decisiveness for typical profiles.
- All changes validated with automated tests (2/2 passing).

---

## 8. Future Work

- **Fuzzy genre matching.** Treat "indie pop" and "pop" as partial matches instead of binary yes/no. Could use a genre similarity map.
- **Dynamic weight adjustment.** Detect when preferences conflict (high energy + sad mood) and shift weights automatically to prioritize mood over genre.
- **Diversity injection.** After selecting the top 3 matches, fill remaining slots with songs from different genres to break filter bubbles.
- **Multi-profile support.** Allow users to have multiple taste profiles (e.g., "workout" vs. "study") and switch between them.
- **Collaborative filtering.** Incorporate signals from other users with similar tastes to discover songs the content-based system would miss.

---

## 9. Personal Reflection

**Biggest learning moment:** The "Conflicted" profile (pop + melancholic) was the turning point. Seeing the system recommend Gym Hero — an upbeat gym anthem — to someone who said they were feeling sad made the concept of algorithmic bias click in a way that reading about it never did. The system was doing exactly what we told it to do (prioritize genre), but the result was musically tone-deaf. It showed me that a system can be mathematically correct and still be wrong in a way that matters to real people.

**How AI tools helped and where I double-checked:** AI tools were most useful for scaffolding — generating the CSV expansion with diverse genres, suggesting the closeness formula (`1 - |diff|`), and formatting the CLI output. But I had to double-check the weight rationale myself. The AI suggested weights, but deciding that genre should be 2.0 vs. 1.5 required thinking about what actually matters musically. I also caught that tempo needed normalization to a 0-1 scale before it could be compared fairly to the other features — the AI generated the formula, but I verified the math by testing extreme BPM values.

**What surprised me about simple algorithms:** I was genuinely surprised that a scoring function with just 7 weighted features could produce results that "felt" like real recommendations. When the Lofi Studier got Library Rain and Midnight Coding, or the Party Starter got Bass Cathedral, those felt like playlists a human curator might build. The illusion of intelligence comes from the combination of multiple simple comparisons — no single feature is smart, but together they approximate taste. It also surprised me how quickly that illusion breaks. One adversarial profile (Conflicted) was enough to expose a fundamental flaw.

**What I'd try next:** I would implement fuzzy genre matching so that "indie pop" and "pop" earn partial credit instead of zero. I would also add a diversity constraint — after picking the top 3 closest matches, fill the remaining 2 slots with songs from different genres to break filter bubbles. Finally, I'd want to let users have multiple profiles (workout, study, commute) because a single fixed profile can't capture how taste shifts with context.
