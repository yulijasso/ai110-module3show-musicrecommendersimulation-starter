# Recommender System — Data Flow Design

## Text Map

```
INPUT                    PROCESS                           OUTPUT
─────                    ───────                           ──────
User Prefs               The Loop                          The Ranking
  genre: "rock"    ┐
  mood: "intense"  │     For EACH song in songs.csv:       Sorted list
  energy: 0.90     ├──>    1. Compare genre  (+2.0)  ──>   #1 Storm Runner   6.76
  valence: 0.50    │       2. Compare mood   (+1.5)        #2 Gym Hero       4.34
  danceability: 0.65│      3. Calc energy closeness         #3 Concrete Jungle 2.98
  acousticness: 0.10│      4. Calc valence closeness        #4 Night Drive    2.94
  tempo_bpm: 150   ┘       5. Calc dance closeness          #5 Iron Chorus    2.87
                           6. Calc acoustic closeness
songs.csv (20 songs)       7. Calc tempo closeness
                           8. Sum weighted scores
                                    │
                                    v
                           Sort all scores descending
                                    │
                                    v
                           Return top K songs
```

## Mermaid.js Flowchart

```mermaid
flowchart TD
    A["fa:fa-user User Preferences\ngenre, mood, energy,\nvalence, danceability,\nacousticness, tempo"] --> C

    B["fa:fa-database songs.csv\n20 songs with attributes"] --> C

    C["fa:fa-repeat Loop Through Each Song"]

    C --> D{"Genre Match?"}
    D -- Yes --> D1["+2.0 points"]
    D -- No --> D2["+0 points"]

    D1 --> E{"Mood Match?"}
    D2 --> E

    E -- Yes --> E1["+1.5 points"]
    E -- No --> E2["+0 points"]

    E1 --> F["Numeric Closeness Scores"]
    E2 --> F

    F --> F1["energy: (1 - |diff|) x 1.0"]
    F --> F2["danceability: (1 - |diff|) x 0.8"]
    F --> F3["valence: (1 - |diff|) x 0.7"]
    F --> F4["acousticness: (1 - |diff|) x 0.5"]
    F --> F5["tempo: (1 - |diff|) x 0.3"]

    F1 --> G["Sum All Points\n= Total Song Score"]
    F2 --> G
    F3 --> G
    F4 --> G
    F5 --> G

    G --> H{"More songs\nin CSV?"}
    H -- Yes --> C
    H -- No --> I["Sort All Scores\nHighest to Lowest"]

    I --> J["Return Top K\nRecommendations"]

    J --> K["fa:fa-list-ol Output\n#1 Song Title — Score\n#2 Song Title — Score\n#3 Song Title — Score\n+ Explanation for each"]

    style A fill:#4a90d9,color:#fff
    style B fill:#f5a623,color:#fff
    style G fill:#7b68ee,color:#fff
    style I fill:#e74c3c,color:#fff
    style K fill:#2ecc71,color:#fff
```

## How a Single Song Moves Through the Pipeline

Taking **"Storm Runner"** (rock, intense, energy 0.91) scored against the **Rock Fan** profile:

```mermaid
flowchart LR
    CSV["songs.csv\nRow 3: Storm Runner"] --> GENRE{"genre == rock?"}
    GENRE -- "Yes: +2.0" --> MOOD{"mood == intense?"}
    MOOD -- "Yes: +1.5" --> NUM["Numeric Closeness"]

    NUM --> E["energy\n|0.90 - 0.91| = 0.01\nsim = 0.99\n0.99 x 1.0 = 0.99"]
    NUM --> D["danceability\n|0.65 - 0.66| = 0.01\nsim = 0.99\n0.99 x 0.8 = 0.79"]
    NUM --> V["valence\n|0.50 - 0.48| = 0.02\nsim = 0.98\n0.98 x 0.7 = 0.69"]
    NUM --> AC["acousticness\n|0.10 - 0.10| = 0.00\nsim = 1.00\n1.00 x 0.5 = 0.50"]
    NUM --> T["tempo\nnorm diff = 0.01\nsim = 0.99\n0.99 x 0.3 = 0.30"]

    E --> SUM["TOTAL\n2.0 + 1.5 + 0.99\n+ 0.79 + 0.69\n+ 0.50 + 0.30\n= 6.76"]
    D --> SUM
    V --> SUM
    AC --> SUM
    T --> SUM

    SUM --> RANK["Ranked #1\nout of 20 songs"]

    style CSV fill:#f5a623,color:#fff
    style SUM fill:#7b68ee,color:#fff
    style RANK fill:#2ecc71,color:#fff
```
