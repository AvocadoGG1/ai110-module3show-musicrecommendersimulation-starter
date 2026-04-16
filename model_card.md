# Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder is designed to suggest songs from a small catalog based on a user's preferred genre, mood, and energy level. It is built for classroom exploration — to demonstrate how content-based filtering works before adding complexity like machine learning or user behavior data.

It is **not** intended for real users in a production app. It should not be used to make decisions about what music gets promoted or surface-leveled to real listeners, because the catalog is too small and the scoring is too simple for that.

---

## 3. How the Model Works

Every song in the catalog is scored against the user's preferences using three rules:

1. **Genre match** — If the song's genre matches what the user wants, it gets 2 points. Genre is the heaviest factor because it is the most reliable signal of compatibility.

2. **Mood match** — If the song's mood matches the user's target mood, it gets 1 point. Mood matters but is treated as a secondary signal.

3. **Energy proximity** — The closer the song's energy level is to the user's target energy, the more points it gets — up to 1.0 point for a perfect match. This rewards songs that are "in the neighborhood," not just songs that are simply high or low energy.

After every song is scored, the list is sorted from highest to lowest and the top 5 are returned, each with a plain-language explanation like `"genre match (+2.0), mood match (+1.0), energy similarity (+0.97)"`.

---

## 4. Data

The catalog contains **18 songs** stored in `data/songs.csv`. The starter set had 10 songs, and 8 were added to fill out underrepresented genres. Each song has these features: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.

Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop, edm, hiphop.
Moods represented: happy, chill, intense, relaxed, moody, focused, energetic, euphoric, confident, nostalgic.

**Limitations:** Most songs were generated for this simulation and do not reflect real listening data. Genres like classical, country, R&B, and metal are absent. The catalog skews toward electronic and independent music styles.

---

## 5. Strengths

- Works well for users with a clear, consistent preference (e.g., the Chill Lofi profile gets a near-perfect match because multiple lofi chill songs exist in the catalog).
- The scoring is fully transparent — every recommendation comes with a reason, which is rare in real systems.
- Fast and deterministic — given the same profile, it returns the same results every time, making it easy to reason about.
- The energy proximity scoring is better than a simple threshold: it rewards *closeness*, not just direction.

---

## 6. Limitations and Bias

The system has a significant **genre filter bubble** problem. Because genre is worth 2.0 points and mood is only worth 1.0 point, a user who wants a "chill EDM" vibe will still receive high-energy EDM recommendations — the genre match overrides the mood mismatch. Real users with cross-genre or mood-first preferences are underserved.

The catalog itself also introduces bias: lofi and EDM have multiple songs, while genres like jazz and rock each have only one or two entries. Users who prefer jazz will always get worse results because there is less catalog diversity to pull from.

Additionally, the system ignores `valence`, `danceability`, `tempo_bpm`, and `acousticness` when scoring (except for the optional acoustic bonus in the OOP interface). This means it cannot distinguish between a sad rock song and a happy rock song beyond the mood label.

---

## 7. Evaluation

Five user profiles were tested:

| Profile | Top Result | Score | Felt Right? |
|---|---|---|---|
| Happy Pop | Sunrise City | 3.98 | Yes — perfect genre/mood/energy match |
| Chill Lofi | Rain Tape Vol 2 | 4.00 | Yes — expected top result |
| EDM Hype | Club Voltage | 3.99 | Yes — energetic EDM |
| Hip-Hop Confident | Street Cipher | 3.99 | Yes — matched well |
| Conflicted Vibes (EDM + chill) | Festival Rush | 2.99 | Partially — genre drove it, mood ignored |

The Conflicted Vibes profile was the most revealing. It showed that when genre and mood conflict, genre always wins due to weighting. This is an accurate simulation of real filter bubble behavior — users in a niche often get more of the same genre regardless of other signals.

A weight shift experiment was also run: halving genre weight to 1.0 and doubling energy weight to 0–2.0. The rock song Storm Runner started ranking in the EDM Hype top 5 solely due to energy proximity. This confirmed that the default genre weight is appropriate and necessary for sensible results.

---

## 8. Future Work

1. **Add valence and danceability to scoring** — These features are already in the CSV and would let the system distinguish "sad pop" from "happy pop" beyond just the mood label.

2. **Enforce diversity in results** — Right now the top 5 can all be the same artist or same sub-genre. A diversity penalty (e.g., no more than 2 songs per genre in the top 5) would improve the feel of results.

3. **Collaborative filtering layer** — If user listening history were available, adding a "users like you also liked..." component would dramatically improve recall and help surface songs the content-based rules would never find.

---

## 9. Personal Reflection

The biggest thing this project made me realize is how much "intelligent behavior" can come out of a 3-rule scoring function. The recommendations for Chill Lofi and Hip-Hop Confident looked genuinely good — it felt like the system *understood* the request. But it didn't. It was just arithmetic. That gap between "feels smart" and "is smart" is something I'll think about every time I use a recommendation system now.

Using AI to help design the scoring logic was useful for generating ideas quickly — things like "use `1 - abs(energy_diff)` instead of just checking if energy is above a threshold" were good suggestions I wouldn't have landed on as fast. But I had to verify and adjust the weights myself. The AI's first instinct was to weight everything equally, which produced muddy results. Deciding that genre should be worth 2x mood was a judgment call that required testing, not just code generation.

What I'd try next: I'd add a second pass after the initial ranking that enforces genre diversity — making sure the top 5 covers at least 2–3 different genres. That single change would make the system feel much more like a real music discovery tool rather than a "more of what you already said you like" machine.
