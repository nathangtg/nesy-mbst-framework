# Presentation: LLM-Augmented Model-Based Statistical Testing

**Course:** SWE3033 Software Processes  
**Duration:** 10 min talk · 5 min Q&A = 15 min total  
**Authors:** Nathan G., Jaeden Ting YiYong, Wai Phyo Hein, Jordan Chay  
**Affiliation:** School of Computing and Artificial Intelligence, Sunway University

---

## Slide 1 — Title
**Time: 20 sec**

**On screen:**
> *The Machine Proposes. The Proof Disposes.*  
> Automatically building test plans from plain English — without the math headache

Nathan G. · Jaeden Ting YiYong · Wai Phyo Hein · Jordan Chay  
Sunway University · Mercedes-Benz Tech Innovation · July 2026

**Speaker notes:**
> "Hi everyone. Our project answers a simple question: can we get an AI to write a proper software test plan from a plain English description — one that's actually mathematically correct? That's what we built."

---

## Slide 2 — The Problem in One Sentence
**Time: 1 min**

**On screen:**
> 🔴 Writing good software tests is expensive.  
> Formal statistical testing works great — but it needs a **model** that nobody wants to build by hand.

- A usage model is a map of how users actually move through software
- Building one correctly takes **weeks of expert effort**
- So most teams skip it and use weaker, ad-hoc testing instead
- Result: bugs that only appear in real usage slip through

**Speaker notes:**
> "Imagine drawing a flowchart of every possible way a user could interact with your app — every button, every path, every error state — and then labelling each arrow with a probability. That's a usage model. It's powerful because tests generated from it mirror real-world behaviour. The problem is, nobody builds them because it takes forever and requires formal methods expertise. Teams just skip it."

---

## Slide 3 — What We Built
**Time: 1 min**

**On screen:**
> ✅ **NeSy-MBST:** You give it your requirements document.  
> It gives you a complete, mathematically valid test plan — automatically.

How it works in plain terms:
1. **AI reads** your requirements and extracts the states and transitions
2. **Symbolic checker** removes any impossible or contradictory paths
3. **Math solver** assigns correct probabilities (no guessing)
4. **Feedback loop** keeps the model up to date as the system evolves

**Speaker notes:**
> "We built NeSy-MBST — Neuro-Symbolic Model-Based Statistical Testing. You feed it a plain English requirements doc. It reads it, builds the usage model, checks every path for logical errors using a rule engine, assigns mathematically correct probabilities using a solver, and then keeps recalibrating itself as the real system produces data. The key idea is: let the AI do the language part, but let math do the math part."

---

## Slide 4 — Why AI Alone Doesn't Work
**Time: 1 min**

**On screen:**
> ❌ Just asking ChatGPT to write test plans has 4 failure modes:

| Problem | Plain English |
|---|---|
| **Hallucination** | AI invents transitions that can't actually happen |
| **Bad probabilities** | Numbers don't add up to 100% |
| **Too many states** | AI loses track of large systems mid-generation |
| **Logic violations** | AI suggests "checkout with empty cart" as a valid path |

**Speaker notes:**
> "You might ask — why not just use ChatGPT directly? We tried. Four things go wrong every time. The AI makes up paths that the software can't actually take. The probabilities it assigns don't sum to one, which breaks all the statistics downstream. On big systems it runs out of context and starts contradicting itself. And it routinely suggests flows that are semantically sensible but logically impossible — like checking out when there's nothing in the cart. Our framework fixes all four."

---

## Slide 5 — The Architecture (Simple Version)
**Time: 1 min 30 sec**

**On screen:**
```
Plain English Requirements
         ↓
   [ AI reads & extracts ]   ← Neural layer
         ↓
   [ Symbolic checker ]      ← Removes bad paths
         ↓
   [ Math solver ]           ← Sets correct probabilities  
         ↓
   Markov chain usage model
         ↓
   [ Test generator ]        ← Produces test sequences
         ↑
   [ Feedback loop ]         ← Updates as system runs
```

**Speaker notes:**
> "Here's the full pipeline. Natural language in at the top, test sequences out at the bottom. The AI handles the reading and extraction. A symbolic rule engine acts as a bouncer — anything that violates a system invariant gets rejected. A convex math solver then assigns probabilities correctly. And a feedback loop watches real execution data and recalibrates over time. No step requires a human domain expert."

---

## Slide 6 — Results: Did It Work?
**Time: 1 min 30 sec**

**On screen:**
> Tested on: Autonomous Vehicle software (9 states) + E-commerce platform (24 and 42 states)

| What we measured | Our system | Best AI-only baseline |
|---|---|---|
| Model accuracy (F1 score) | **0.91** ✅ | 0.66 |
| Safety-critical threshold | Passes (≥ 0.90) | Fails |
| Fault-finding path coverage | **85.7%** | 50.0% |
| Time to generate full model | **< 6 minutes** | — |
| Statistical fidelity (JSD) | **0.012** | 0.157 |

> A **35.7 percentage-point** improvement in paths that can catch bugs.

**Speaker notes:**
> "The numbers tell a clear story. Against the best pure-AI baseline, our system is 39% more accurate at extracting the correct model structure — and it's the only approach that clears the 0.90 threshold required for safety-critical work. More importantly for fault detection: our generated test suites cover 85.7% of the paths that could reveal a bug, compared to just 50% for the AI-only approach. And it does all this in under six minutes for a 42-state model."

---

## Slide 7 — What Drives the Improvement?
**Time: 1 min**

**On screen:**
> We ran an **ablation study** — switching components on/off one at a time:

| What's active | Bug-finding coverage | Probability accuracy |
|---|---|---|
| AI only (no checking) | 50% | Poor |
| + Symbolic checker | **85.7%** ← big jump | Moderate |
| + Math solver | 85.7% | **Near-perfect** ← big jump |
| + Feedback loop | 85.7% | Fine-tuned |

> **Takeaway:** Symbolic checker fixes *structure*. Math solver fixes *probabilities*. Both are necessary.

**Speaker notes:**
> "We wanted to know which part of the system actually does the work. So we ran an ablation — turning pieces on and off. The symbolic checker is the biggest structural win: it takes coverage from 50% to 85.7% by recovering the missing paths the AI missed. The math solver then brings the probability accuracy from poor to near-perfect. They solve different problems and you need both."

---

## Slide 8 — Fault Detection in Real Terms
**Time: 45 sec**

**On screen:**
> Why does 85.7% vs 50% coverage matter?

- Every **uncovered transition** = a path the test suite is **blind to**
- Bugs that live on those paths **will not be caught before release**
- Industry studies show structured MBT catches **25–40% more real defects** than unstructured scripting
- Our system recovers that advantage — **automatically**

**Speaker notes:**
> "Here's the practical meaning. If your test suite only covers 50% of the transitions in your usage model, there are entire classes of user behaviour your tests can never catch. Those are the bugs that reach production. Our system — by recovering those transitions automatically — closes that gap without requiring anyone to manually draw the model."

---

## Slide 9 — Adoption Guidelines
**Time: 45 sec**

**On screen:**
> 5 rules for using AI in test model generation:

1. **Always run a symbolic checker** before assigning probabilities
2. **Never let the AI assign numbers** — use a solver
3. **Decompose large systems** into layers to avoid state explosion
4. **Feed runtime data back** to keep the model current
5. **Treat AI output as a draft**, not a finished artefact — verify it

**Speaker notes:**
> "If you take one thing from this talk, it's this: AI is great at reading requirements and drafting a structure. It is terrible at math and logic enforcement. The right architecture keeps them separate. Use the AI for language, use formal tools for correctness."

---

## Slide 10 — What's Next
**Time: 30 sec**

**On screen:**
> Open questions we haven't solved yet:

- **Direct fault-seeding study** — measure actual bug catch rates, not proxies
- **Larger industrial systems** — hundreds of states, real codebases
- **More domains** — medical devices, telecom protocols, ISO 26262 automotive
- **Multi-annotator validation** — remove single-author bias

**Speaker notes:**
> "Our results are on benchmarks up to 42 states. The next milestone is a real industrial case study with fault seeding — actually planting known bugs and measuring what our system catches versus a manual approach. We're also targeting ISO 26262 automotive safety as a domain where this would have immediate regulatory impact."

---

## Slide 11 — Summary
**Time: 20 sec**

**On screen:**
> **The problem:** Manual usage model construction blocks statistical testing  
> **Our solution:** NeSy-MBST — AI reads, symbolic engine verifies, solver calibrates  
> **The result:** 0.91 F1 · 85.7% fault-path coverage · < 6 minutes · fully automated  
> **The message:** Let AI propose. Let formal methods dispose.

**Speaker notes:**
> "To close: we've shown that combining AI with symbolic verification and convex optimization can automate a task that previously required weeks of expert effort. The output is not just faster — it's mathematically guaranteed to be correct. Thank you."

---

## Slide 12 — Q&A
**Time: 5 min**

**Likely questions and short answers:**

**"Why not just use ChatGPT directly for testing?"**
> ChatGPT can draft test cases but can't guarantee that the probabilities are correct or that the model is structurally valid. Our system adds the verification and calibration layers that make it reliable.

**"What is a Markov chain in simple terms?"**
> It's a flowchart where every arrow has a probability. If you're on Screen A, there's a 70% chance the user goes to Screen B and a 30% chance they go back. That structure tells you exactly how to allocate test effort.

**"How is this different from just writing unit tests?"**
> Unit tests check individual functions. MBST checks realistic user journeys — entire sequences of interactions weighted by how often real users take them. It catches integration-level and usage-pattern bugs that unit tests miss.

**"What does 0.012 JSD actually mean?"**
> JSD is a distance measure between two probability distributions — 0 means identical, 0.693 means completely different. At 0.012 our generated model's behaviour is less than 2% away from the reference. In practice, test effort lands on almost exactly the right paths.

**"Is this production-ready?"**
> Not yet — it's a proof of concept. The framework works and the results are strong, but it needs industrial case studies with real fault seeding before we'd recommend it for a production pipeline.
