# The Mathematics Behind the Engine

*A brief for the curious — what actually computes the numbers you see move.*

The Analytical Language Engine is a **working model, not a mock-up**. When its
gauges rise, they are driven by real arithmetic performed live in your browser.

---

## 1. What kind of engine it is

A modern Large Language Model (LLM) predicts the next token with a neural network of
hundreds of billions of learned parameters. This cabinet does something far humbler
that nonetheless has the **same shape**: it is an **n-gram Markov model** — it
predicts the next word by counting how often words followed one another in a small
library of **79 sentences**. We call it, fondly, an *Infinitesimal Language Model*.
The mechanism — read the text, turn it into numbers, weigh every candidate, and draw
one by weighted chance — is faithfully the same, and can therefore teach the shape of
the real thing.

## 2. From text to numbers (tokenisation)

The prompt is divided by a regular expression into **tokens**: words and individual
marks of punctuation. Each distinct token is assigned an integer from a fixed
catalogue (here, ~231 entries; a real model holds 50,000–200,000). Everything that
happens in the model is arithmetic on these integers. This is identical in kind to
what an LLM does.

## 3. The heart: an interpolated n-gram model

During training (a single, fast pass over the 79 sentences) the engine tallies three
frequency tables:

- **Unigrams** — how often each token appears, `P₁(w)`.
- **Bigrams** — how often token *w* follows token *a*, `P₂(w | a)`.
- **Trigrams** — how often *w* follows the pair *(a, b)*, `P₃(w | a, b)`.

To score every possible next token given the current context, it blends all three by
**linear interpolation with back-off**:

```
P(w | context) ∝ λ₃·P₃(w | a,b) + λ₂·P₂(w | b) + λ₁·P₁(w)
```

with weights **λ₃ = 0.72, λ₂ = 0.21, λ₁ = 0.07**. When the higher-order context has
never been seen, its term drops out and the weights renormalise. The model
gracefully **backs off** from trigram to bigram to unigram evidence. Rarer contexts
lean on the general word frequencies; familiar ones are sharply predicted. This
back-off is the counting-model ancestor of what a neural network learns to do
smoothly and implicitly.

The result is a genuine **probability distribution over the entire catalogue** — one
number per token, all summing to 1. Those numbers are precisely what the
Manometer Wall (Station VI) displays.

## 4. Temperature: reshaping the odds

Before a word is drawn, the distribution is reshaped by a single dial —
**temperature, T** — using exactly the exponentiation a real sampler uses:

```
q(w) ∝ P(w)^(1/T)          (then renormalised so Σ q = 1)
```

- **T → 0 (frost):** the exponent grows, the favourite's share approaches 1 — nearly
  deterministic, and repetitive.
- **T = 1:** the distribution is used as-is.
- **T large (fever):** the exponent shrinks toward 0, flattening every candidate
  toward equal chance — inventive, and eventually incoherent.

Move the boiler lever and the gauges re-compute this in real time. This is the same
mathematics as *softmax temperature* in a production model; only the source of the
underlying `P(w)` differs.

## 5. Sampling: drawing the lot

One token is chosen by a **weighted lottery** (inverse-CDF sampling): draw a uniform
random number *r* ∈ [0, 1), evaluate the candidates accumulating their probabilities, and
take the one in whose interval *r* falls. High-probability tokens own wider intervals
and are drawn more often — but not always. This is why the same prompt, asked twice,
can answer differently. The Lottery Drum (Station VII) is literally this draw.

## 6. The loop, and stopping

The drawn token is appended to the context and the whole computation runs again for
the next word — the model is **autoregressive**. A special **stop token** sits in the
catalogue like any other; when the lottery draws it, the engine rests. There is no
finished sentence waiting inside — each word is minted the instant before you read it.

---

## What is genuine, and what is illustrative

In the spirit of the cabinet's candour:

| Element | Status |
|---|---|
| Tokenisation, n-gram counts, interpolation, temperature, sampling, stop token | **Genuine** — real arithmetic, computed live |
| The probability gauges (Station VI) | **Genuine** — the true distribution for the present context |
| Embeddings / dial-columns (Station III) | **Illustrative** — hashed pseudo-vectors nudged toward hand-drawn "meaning" clusters, to show that *meaning becomes position*; a real model learns these |
| Attention linkages (Station IV) | **Illustrative** — a recency curve and a co-occurrence "affinity", to show *a word attending to context*; a real model computes these from the vectors at every layer |
| The Grand Mill's floors (Station V) | **Illustrative** — the refinement of one token's numbers layer by layer, shown as shifting bars; the count-based engine has no such interior |

## Model and Reality

The pipeline is the same; the scale and the source of the probabilities are not.
A frontier model replaces *counting* with a hundred layers of learned attention and
arithmetic over a **thousand milliard (10¹²) parameters**, against this cabinet's
~1,334 counting-wheels. It is the difference between a music box and an orchestra —
both can play the same tune, just at different scales.

*Every formula above is implemented in the single HTML file; there is nothing to
install and nothing hidden. Read the source, and you have read the whole engine.*
