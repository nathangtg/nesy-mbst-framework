- 100% state recall, system F1 of 0.98 — the pipeline correctly recovers the full state space from NL requirements
- JSD of 0.012 means the synthesized Markov chain's steady-state behavior is nearly identical to the reference — statistical fidelity is proven
- The full neuro-symbolic loop (LLM → symbolic validation → convex optimization → test generation → visualization) runs end-to-end
- Visualizations make the results tangible for a paper/demo
What's soft (and worth addressing for a real evaluation):
- Transition coverage of 85.7% and state coverage of 88.9% are solid but not saturation — the test generator should hit 100% with enough sequences; you may want to increase max_sequences or verify the generator converges
- Transition precision of 0.93 (one false positive transition from the symbolic layer) — the feasibility memory added transitions that weren't in the ground truth
- 10 LLM queries on single symbols isn't exercising the oracle on multi-step sequences; for a stronger proof, you'd query longer paths (e.g., 3-5 state sequences)