# Reflection

## Profile Comparisons

### Chill Lofi vs. EDM Hype

The Chill Lofi profile consistently surfaced low-tempo, acoustic-heavy tracks (Rain Tape Vol 2, Library Rain, Midnight Coding) while the EDM Hype profile surfaced high-tempo electronic tracks (Club Voltage, Drop Zone, Festival Rush). This makes sense — the genre weight of 2.0 almost guarantees that the top results will belong to the user's preferred genre, and energy proximity finishes the job of sorting within that genre. The difference between these two profiles is basically the clearest possible demo of what the algorithm is actually doing.

### Hip-Hop Confident vs. Happy Pop

Both profiles produce results with high scores (3.93–3.99), but the reasoning differs. Pop results score well on genre + mood + energy simultaneously. Hip-hop results score well on genre + mood but energy proximity is narrower (hiphop songs cluster around 0.60–0.71 energy). Once the genre and mood buckets are exhausted, the fallback results for both profiles become energy-proximity picks from completely unrelated genres — Night Drive Loop (synthwave) shows up in the hip-hop fallback top 5. That reveals a gap: when there are only 3 genre matches in the catalog, the 4th and 5th slots are essentially random relative to the user's preferences.

### Conflicted Vibes (adversarial) vs. EDM Hype

This is the most interesting comparison. Both profiles target EDM and high energy. The only difference is the Conflicted Vibes profile asks for `mood: chill`. The top 3 results are identical (Festival Rush, Club Voltage, Drop Zone) — the mood signal had zero influence because there are no chill EDM songs in the catalog. The genre weight of 2.0 completely dominates when genre and mood conflict. This is exactly what a "filter bubble" looks like in practice: the system confidently recommends songs that match the genre, and the user's actual mood request gets silently ignored.

## What I Learned About Recommenders

Simple scoring systems feel more personalized than they have any right to. The formula is just three if-statements and some subtraction, but the output reads like a thoughtful suggestion. That's partly because we're comparing against a tiny catalog — with 18 songs, a 4.0 score really does mean "this is the best fit." At real Spotify scale, a score of 4.0 might match thousands of songs and the ranking within that group would need much more nuance.

The hardest part wasn't implementing the logic — it was deciding the weights. I ran the weight-shift experiment (genre halved to 1.0, energy doubled to 0–2.0) and the results got worse: Storm Runner started showing up in EDM results purely because of energy, even though it's rock. That taught me that content-based filtering only works when the weights actually reflect what the user cares about in that order, not just what's mathematically convenient.
