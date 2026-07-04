# Literature Review: Model-Based Testing, Statistical Model Checking, and Probabilistic Verification Under Uncertainty

This review examines twenty papers spanning three interconnected research threads: (1) model-based testing (MBT) and its practical/industrial adoption, (2) statistical model checking (SMC) as a scalable alternative to exhaustive probabilistic verification, and (3) probabilistic/uncertainty-aware extensions that bridge testing and formal verification. Each paper is discussed in turn, covering its context, contribution, methodology, and relevance to research on probabilistic model-based testing under uncertainty.

---

## 1. Test Model Coverage Analysis Under Uncertainty: Extended Version

**Authors:** I.S.W.B. Prasetya, Rick Klomp
**Venue:** *Software and Systems Modeling*, Vol. 20, No. 2, pp. 383–403 (2021); extended from a SEFM 2019 conference paper
**DOI:** 10.1007/s10270-020-00848-9

This paper directly targets the problem of measuring test coverage when the underlying test model is non-deterministic — a situation that arises either because the model is an abstraction of the real system or because the system under test is itself non-deterministic. In such settings a single test case may trigger different execution paths depending on internal decisions of the software, which makes exact coverage computation impossible. The authors' solution is to let developers annotate each model transition with an estimated probability, enabling a probabilistic model-checking algorithm to compute probabilistic coverage. The paper's key extension over prior model-checking approaches is that it moves beyond simple *reachability*-style coverage queries (which can be answered by standard probabilistic model checkers) toward **aggregate coverage** goals — e.g., "80% of states covered" — and **k-wise coverage**, which is known from the testing literature to substantially increase fault-detection potential. Because aggregate and k-wise goals cannot be expressed in LTL/CTL and are not answerable by conventional model checkers, the authors present a new, efficient labelling algorithm to compute these probabilistic aggregate/k-wise coverage measures directly. This paper is highly relevant to any research studying probabilistic MBT under uncertainty, as it provides one of the few rigorous formal treatments of *coverage measurement itself* becoming a probabilistic quantity when models are non-deterministic — a foundational concern for any downstream uncertainty-aware testing framework.

---

## 2. Practitioners' Best Practices to Adopt, Use or Abandon Model-Based Testing with Graphical Models for Software-Intensive Systems

**Authors:** Emil Alégroth, Kristian Karl, Helena Rosshagen, Tomas Helmfridsson, Nils Olsson
**Venue:** *Empirical Software Engineering*, 2022
**DOI:** 10.1007/s10664-022-10145-2

This is an industrial, interview-based empirical study addressing a persistent puzzle in the MBT literature: despite decades of academic research, industrial adoption of graphical-model-based MBT remains sparse. The authors conducted semi-structured interviews with 17 international MBT experts across different industrial roles, then synthesized the results through semantic equivalence analysis, later verified by additional practitioners. The study yields 13 synthesized conclusions and 23 concrete best-practice guidelines covering the full lifecycle of adoption, use, and (where appropriate) abandonment of graphical MBT. Importantly, the paper's conclusions span not just technical dimensions (model design, tool choice, maintainability) but organizational and process factors — mindset, knowledge, mandate, and resource allocation — that the authors argue are just as decisive in determining whether MBT succeeds in practice. This paper is valuable to the literature not for its formal/mathematical contribution but as a counterweight: it grounds more theoretical work on probabilistic coverage and uncertainty-aware testing in the practical reality that most industrial MBT failures are organizational, not algorithmic.

---

## 3. On Transforming Model-Based Tests into Code: A Systematic Literature Review

**Authors:** Fabiano C. Ferrari, Vinicius H. S. Durelli, Sten F. Andler, Jeff Offutt, Mehrdad Saadatmand, Nils Müllner
**Venue:** *Software Testing, Verification and Reliability* (Wiley), 2023

This systematic literature review (SLR) investigates a question central to the practical value of MBT: does coverage achieved at the abstract model level actually translate into meaningful coverage of the underlying source code once abstract tests are transformed into concrete, executable tests? Using a snowballing methodology starting from three seed papers, the authors expanded their search to 30 primary studies. The review characterizes how test sets generated from models are mapped onto code, catalogs the transformation techniques used across the literature, and critically examines the (surprisingly thin) empirical evidence connecting model coverage criteria to code coverage outcomes. As an SLR, its main contribution to the field is a structured map of the model-to-code transformation landscape together with an explicit identification of gaps — most notably the lack of large-scale empirical validation that model-level testing effort reliably produces code-level assurance. This is directly relevant background for any argument that model coverage analysis (as in Paper 1) needs empirical grounding in code-level outcomes, and it complements Paper 19 (an industrial account of a similar transformation pipeline in practice).

---

## 4. Generative Model-Based Testing on Decision-Making Policies

**Authors:** Zhuo Li, Xiongfei Wu, Derui Zhu, Mengshi Cheng, Siyuan Chen, Fuyuan Zhang, Xiaofei Xie, Lei Ma, Jianjun Zhao
**Venue:** ASE 2023 (38th IEEE/ACM International Conference on Automated Software Engineering)
**DOI:** 10.1109/ASE56229.2023.00153

This paper tackles the modern problem of testing decision-making policies that solve Markov decision processes (MDPs) — for example, DNN-based policies deployed in autonomous driving or robotics. Because such policies operate over deep-neural-network-based, effectively infinite state spaces, exhaustive or even conventional model-based test generation is impractical. The authors propose a generative testing framework built around a **diffusion-model-based test case generator**, chosen for its ability to adapt flexibly to different search spaces while producing valid, in-distribution test cases. A key algorithmic contribution is a **termination-state novelty-based guidance mechanism**, which steers the generative process toward diversifying agent behavior at episode termination, thereby increasing the likelihood of discovering diverse and influential failure-triggering scenarios. The framework is evaluated across five benchmarks, including autonomous driving and aircraft collision avoidance, and is shown to surface more diverse and impactful failures than prior state-of-the-art baselines. This paper represents the modern generative-AI evolution of model-based test generation — replacing hand-crafted model traversal strategies with learned generative models — and is squarely relevant to any survey that wants to show how classical MBT ideas (models of behavior, coverage-directed exploration) have been re-instantiated using generative deep learning for MDP-based systems.

---

## 5. Coverage Measurement in Model-Based Testing of Web Applications: Tool Support and an Industrial Experience Report

**Authors:** Vahid Garousi, Alper Buğra Keleş, Yunus Balaman, Alper Mermer, Zeynep Özdemir Güler
**Venue:** 2024 IEEE International Conference on Software Testing, Verification and Validation Workshops (ICSTW); arXiv:2408.06148
**DOI:** 10.1109/icstw60967.2024.00019

This is an applied, tool-oriented paper arising from a large-scale industrial web-application-testing context. The authors identify a concrete practical gap: existing coverage tools typically report only one type of coverage (either code coverage or requirements/test coverage), whereas practitioners running large MBT test suites needed to integrate front-end code coverage, back-end code coverage, and requirements coverage into a single "live" view as tests executed. Unable to find any suitable off-the-shelf toolset, the authors built an open-source tool, **MBTCover**, purpose-built for MBT contexts, which reports code, requirements, and model coverage simultaneously and in real time during test execution. The paper presents the tool's architecture and the authors' experience deploying it across multiple large test-automation projects. As a direct, applied companion to Paper 1 (which is theoretical) and Paper 19 (a broader MBT experience report from the same research group), this paper demonstrates that the practical challenges of coverage measurement in MBT are as much about tooling and integration as about the underlying probabilistic or combinatorial theory.

---

## 6. PASTA: An Efficient Proactive Adaptation Approach Based on Statistical Model Checking for Self-Adaptive Systems

**Authors:** Yong-Jun Shin, Eunho Cho, Doo-Hwan Bae
**Venue:** FASE 2021 (24th International Conference on Fundamental Approaches to Software Engineering)
**DOI:** 10.1007/978-3-030-71500-7_15

PASTA addresses proactive adaptation in self-adaptive systems (SAS) — adaptation triggered by *predicting* future environmental changes rather than reacting after the fact. Because predictions are inherently uncertain, adaptation consequences must be verified before being executed, and prior work relied on probabilistic model checking (PMC) for this verification. The authors identify two limitations of PMC-based verification in this setting: the state-explosion problem for complex SAS models, and restrictive support for particular modeling languages. PASTA replaces PMC with **statistical model checking (SMC)**, generating statistically sufficient samples to verify the effects of adaptation tactics far faster than exhaustive PMC approaches. The paper contributes not just an algorithm but a reference architecture and an open-source implementation skeleton, evaluated on two real self-adaptive systems using actual operational data, alongside a comparative analysis of the relative advantages/disadvantages of PMC versus SMC for proactive adaptation. This paper is a strong example of SMC being adopted specifically to overcome the scalability limitations of exhaustive probabilistic verification — precisely the trade-off that motivates much of the broader SMC literature reviewed below (Papers 8–17).

---

## 7. Uncertainty-Aware Exploration in Model-Based Testing

**Authors:** Matteo Camilli, Angelo Gargantini, Patrizia Scandurra, Catia Trubiani
**Venue:** ICST 2021 (14th IEEE Conference on Software Testing, Verification and Validation)

This paper is among the most directly relevant to the theme of probabilistic MBT under uncertainty, since it explicitly frames uncertainty as a first-class testing concern rather than an incidental complication. The authors propose novel model-based exploration strategies for generating test cases that specifically target the *uncertain* components of a system under test, using **Markov Decision Processes** as the underlying modeling formalism. Testers explicitly attach *beliefs* (probability distributions) to transition probabilities to represent their confidence (or lack thereof) in the model's fidelity to the real system. The structural properties of the model, together with the uncertainty specification, drive test-case generation, and **Bayesian inference** is used to update the initial beliefs as evidence accumulates from testing. The paper introduces several concrete test-selection strategies (Flat/random, History-based, Distance-based, Frequency-based) and empirically evaluates them on synthetic systems of varying structural complexity, finding that the best strategy depends on system complexity and the overall uncertainty level. This paper — together with a related follow-on piece envisioning online, reinforcement-learning-based uncertainty testing — represents one of the clearest bridges in the literature between classical MBT and formal treatment of epistemic uncertainty via Bayesian updating.

---

## 8. Sound Statistical Model Checking for Probabilities and Expected Rewards

**Authors:** Carlos E. Budde, Arnd Hartmanns, Tobias Meggendorfer, Maximilian Weininger, Patrick Wienhöft
**Venue:** TACAS 2025 (31st International Conference on Tools and Algorithms for the Construction and Analysis of Systems), LNCS 15696, pp. 167–190
**DOI:** 10.1007/978-3-031-90643-5_9

This is a rigorous, foundational contribution to the theory underpinning SMC tools. The authors observe that many existing and even newly developed SMC tools are either **unsound** (their statistical guarantees are not actually valid, often because confidence intervals are computed via central-limit-theorem approximations that do not hold in the finite-sample regime) or **inefficient** (relying on overly conservative bounds such as the Okamoto bound, requiring far more samples than necessary). The paper provides a comprehensive survey of existing SMC tools' correctness and of sound statistical estimation methods from the literature, applied to the problem of estimating both probabilities and **expected rewards**. For expected rewards specifically, the authors show how to bound the path-reward distribution so that sound statistical methods designed for bounded distributions can be applied; they recommend the **Dvoretzky–Kiefer–Wolfowitz (DKW) inequality**, previously unused in SMC, and formally prove that even reachability rewards can, in theory, be bounded — introducing the concept of *limit-PAC procedures* as a practical solution when exact bounds are unavailable. These methods are implemented in the "modes" SMC tool and experimentally validated. This paper is essential reading for understanding the current (2025) state-of-the-art in statistically rigorous SMC, and it directly informs any research that wants to make quantitative uncertainty claims about test/verification outcomes with genuine statistical guarantees.

---

## 9. Statistical Model Checking the 2024 Edition!

**Authors:** Shibashis Kanav, Jan Křetínský, Kim G. Larsen
**Venue:** AISoLA 2024, published in *Bridging the Gap Between AI and Reality*, LNCS 15217 (2025)
**DOI:** 10.1007/978-3-031-75434-0_21

This is a short introductory/overview note accompanying a dedicated SMC session at AISoLA 2024. It briefly reintroduces the core ideas of statistical model checking and surveys the field's trajectory — effectively an updated, contemporary companion to the earlier "past, present, and future" retrospectives (Papers 15–17). While brief, the note situates recent SMC developments (e.g., PAC statistical model checking of mean payoff, decision-tree-based controller representation via *dtcontrol*, and applications to security-critical code analysis) within the longer arc of the field, and signals which open problems the community considers current priorities. Its main value to a literature review is as a fast-moving pulse-check on the field as of 2024, complementing the more technically dense contemporary papers (Papers 8 and 12) with a broader, session-introduction-level perspective.

---

## 10. Running PRISM / Statistical Model Checking (PRISM Manual)

**Source:** PRISM Model Checker official documentation, University of Oxford
**Type:** Tool documentation (not a peer-reviewed paper)

This entry is drawn from the official PRISM manual rather than a conventional research publication, but it remains highly relevant because PRISM is one of the most widely used probabilistic model checkers in the field, and its built-in statistical model checking functionality is frequently used as a baseline or comparison point in SMC research (including several other papers in this list). The documentation explains how PRISM's discrete-event simulator can approximate property values via sampling rather than exact numerical solution — a technique particularly valuable for very large models where exhaustive model checking is infeasible, since simulation proceeds directly from the PRISM language description without constructing the full underlying probabilistic model. It details the two default statistical methods available (Confidence Interval estimation for quantitative properties, and the Sequential Probability Ratio Test for bounded properties), the configurable parameters (sample count, confidence level, interval width), and the practical restrictions on which properties and modeling-language features SMC in PRISM supports (currently limited to P/R operators, no LTL-style path properties or filters). While not an original research contribution, this documentation is an important practical reference underpinning much of the applied SMC literature reviewed here.

---

## 11. Rigorous Evaluation of Computer Processors with Statistical Model Checking

**Venue:** 56th Annual IEEE/ACM International Symposium on Microarchitecture (MICRO 2023)
**DOI:** 10.1145/3613424.3623785

This paper introduces SMC to an entirely new application domain: **computer architecture and processor evaluation**. The authors observe that experiments with real computer processors necessarily exhibit variability, and that prior work injects randomness into simulators to mimic this variability, generating distributions of benchmark results across multiple runs. However, existing evaluation practice typically applies standard statistical techniques that implicitly (and often incorrectly) assume these result distributions are Gaussian. To enable rigorous evaluation for arbitrary, unknown result distributions, the authors adapt statistical model checking — a technique previously confined largely to formal verification and cyber-physical systems research — to processor performance analysis, framing the "SMC for Processor Analysis" (SPA) methodology. SMC's statistical guarantees allow architecture researchers to determine, with a specified confidence level, whether a system satisfies a performance property for at least a given fraction of executions, without assuming any particular underlying distribution. This paper is a good illustration of SMC's methodological portability: the same statistical machinery developed for verifying stochastic system models (as in Papers 8, 15–17) is directly repurposed for empirical systems evaluation, and the SPA framework has since been extended (e.g., to quantum device calibration and microarchitectural side-channel evaluation), underscoring the broader applicability of the technique family surveyed in this review.

---

## 12. Optimal Spare Management via Statistical Model Checking: A Case Study in Research Reactors

**Authors:** Reza Soltani, Matthias Volk, Leonardo Diamonte, Milan Lopuhaä-Zwakenberg, Mariëlle Stoelinga
**Venue:** FMICS 2023 (28th International Conference on Formal Methods for Industrial Critical Systems), LNCS 14290, pp. 205–223; journal version in *International Journal on Software Tools for Technology Transfer*, Vol. 27, pp. 361–376 (2025)
**DOI:** 10.1007/978-3-031-43681-9_12 (conference); 10.1007/s10009-025-00791-4 (journal)

This paper applies statistical model checking to a concrete industrial reliability-engineering problem: determining the optimal number of spare parts to stock in order to balance the twin goals of system reliability and cost. The authors combine **fault tree analysis** with SMC by modeling spare-part management as a **stochastic priced timed game automaton (SPTGA)**, then use **Uppaal Stratego** to find the spare-part count that minimizes total costs from downtime and purchasing, while the resulting SPTGA model can also be queried for other metrics such as expected availability. The technique is applied to the emergency shutdown system of a research nuclear reactor — a rare-event setting in which the relevant failure probabilities are extremely low, requiring the authors to adjust Uppaal Stratego's settings to obtain statistically reliable estimates despite the rarity of the events of interest. The reported result — an optimal spare configuration achieving 99.96% expected availability, computed in minutes rather than the days required by exhaustive alternatives — exemplifies SMC's core value proposition (tractable analysis of otherwise intractable stochastic models) in a genuinely safety-critical, real-world application, complementing the more purely methodological contributions elsewhere in this review (Papers 8, 11).

---

## 13. PRG4CNN: A Probabilistic Model Checking-Driven Robustness Guarantee Framework for CNNs

**Authors:** Yang Liu, Aohui Fang
**Venue:** *Entropy*, Vol. 27, No. 2, Article 163 (2025)
**DOI:** 10.3390/e27020163

This paper extends probabilistic model checking into the domain of neural-network robustness verification. Motivated by the well-known fragility of convolutional neural networks (CNNs) to small input perturbations, and noting that existing robustness verification methods focus predominantly on *local* robustness (which is computationally expensive) and cannot automatically *repair* a network once a robustness violation is found, the authors propose **PRG4CNN** — described as the first automated and complete framework for guaranteeing *probabilistic* robustness of CNNs. The framework operates in four steps: (1) model the CNN as a **Markov Decision Process** via model learning, (2) specify the desired probabilistic robustness property using **PCTL** (Probabilistic Computational Tree Logic), (3) verify this property using a probabilistic model checker, and (4) if the property does not hold, perform **probabilistic robustness repair** via counterexample-guided sensitivity analysis. The framework is validated on CNNs of varying scale trained on MNIST. This paper is relevant to the broader review as an example of probabilistic model checking being extended from classical reactive/stochastic-system verification toward machine learning model assurance — an increasingly important adjacent application area for the model-checking and MBT communities, and one that shares PRISM/PCTL-style formalisms with the classical probabilistic verification tradition discussed in Papers 10 and 20.

---

## 14. Statistical Model Checking Meets Property-Based Testing

**Authors:** Bernhard K. Aichernig, Richard Alexander Schumi
**Venue:** ICST 2017 (10th IEEE International Conference on Software Testing, Verification and Validation), pp. 390–400
**DOI:** 10.1109/ICST.2017.42

This paper is a key methodological bridge between the testing community and the formal-verification-oriented SMC community — one of the most direct precedents for combining statistical model checking with mainstream software testing practice. The authors note that SMC scales well to large stochastic models and is relatively simple to implement precisely because it avoids the state-space-explosion problem inherent to exhaustive model checking, by instead simulating finitely many executions and applying hypothesis testing to infer whether the observed samples support or refute a given property. Their contribution is to show how SMC can be integrated into a **property-based testing** framework — specifically **FsCheck** for C# — yielding a flexible combined testing/simulation environment in which programmers define both models and properties in an ordinary programming language, without needing an external, specialized modeling language. This design has two key advantages highlighted by the authors: it eliminates the need for a separate modeling formalism, and it allows both stochastic *models* and actual *implementations* to be checked using the same property-based machinery. This work directly anticipates later applications (e.g., statistical model checking of response times for different system deployments, by the same research group) and is an important conceptual precursor for any framework that wants to unify probabilistic testing with statistical formal verification, as is the aim of much of the uncertainty-aware MBT literature surveyed above (Paper 7).

---

## 15. A Survey of Statistical Model Checking

**Authors:** Gul Agha, Karl Palmskog
**Venue:** *ACM Transactions on Modeling and Computer Simulation*, Vol. 28, No. 1, Article 6 (2018)
**DOI:** 10.1145/3158668

This is one of the most comprehensive and widely cited surveys of the SMC field, covering algorithms, techniques, and tools for statistical model checking of stochastic systems whose quantitative properties (e.g., "the probability that a message queue exceeds five items within a given time bound is less than 0.01") are typically specified in probabilistic temporal logics. The survey systematically covers both **hypothesis-testing-based** approaches (e.g., the sequential probability ratio test, following Younes and Sen et al.) and **estimation-based** approaches (including Bayesian estimation methods, such as those of Zuliani et al., which bound the probability of an incorrect answer using a prior distribution and posterior estimation), as well as variance-reduction techniques like importance sampling with the cross-entropy method for analyzing rare-event properties in models such as Stateflow/Simulink fault-tolerant control systems. The authors explicitly emphasize the tradeoffs between precision and scalability that define the practical usability of different SMC algorithms. As a survey published in 2018, this paper offers the most thorough single reference point for understanding the algorithmic landscape that underlies nearly every applied SMC paper in this review (Papers 6, 8, 9, 11–14), and is an indispensable background source for anyone entering the field.

---

## 16. Statistical Model Checking: An Overview

**Authors:** Axel Legay, Benoît Delahaye, Saddek Bensalem
**Venue:** Runtime Verification 2010 (RV 2010), LNCS 6418, pp. 122–135
**DOI:** 10.1007/978-3-642-16612-9_11

This earlier, foundational tutorial-style paper is one of the field's most frequently cited introductions to statistical model checking, and it is cited by a large fraction of the other papers reviewed here (including Papers 6, 9, 12, 15, and 17). The authors contrast the traditional **numerical approach** to model checking stochastic systems — which iteratively computes or approximates the exact measure of executions satisfying a temporal-logic subformula — with the **statistical/simulation-based approach**: simulating the system for a finite number of executions and applying hypothesis testing to infer whether the observed samples provide statistical evidence for or against the property of interest. The paper's stated purpose is to survey this statistical approach and articulate its principal advantages: *efficiency* (avoiding exhaustive state-space construction), *uniformity* (applicability across many modeling formalisms, since only a simulator is required), and *simplicity* (conceptually straightforward compared to symbolic or numerical probabilistic model checking algorithms). While largely superseded in technical depth by later, more comprehensive surveys (Paper 15) and later foundational advances in soundness (Paper 8), this 2010 paper remains historically important as one of the field-defining tutorial references establishing SMC as a distinct research area separate from exhaustive probabilistic model checking.

---

## 17. Statistical Model Checking: Past, Present, and Future

**Authors:** Kim G. Larsen, Axel Legay
**Venue:** ISoLA 2014 (6th International Symposium on Leveraging Applications of Formal Methods, Verification and Validation), LNCS 8803, pp. 135–142
**DOI:** 10.1007/978-3-662-45231-8_10

This paper — an invited track introduction accompanying a dedicated "Statistical Model Checking: Past, Present, and Future" session at ISoLA 2014 — provides historical framing for the SMC field, tracing its development from early formal-methods work through to (as of 2014) contemporary applications and tools. The authors characterize SMC as fundamentally a **compromise between formal verification and testing**: system executions are monitored (as in testing) until a statistical algorithm can produce a rigorous estimate of the property of interest (echoing the rigor traditionally associated with exhaustive formal verification methods, which by contrast can ensure full correctness for all possible scenarios but at far greater computational cost). The session and paper survey a range of contemporaneous developments referenced throughout this review's other entries, including real-time statistical model checking (David et al.), optimizing control strategies via SMC (also David et al.), and applications to measuring systems more broadly. Read together with Papers 9, 15, and 16, this paper — despite being over a decade old at the time of this review — completes a useful chronological arc documenting how the SMC field's foundational concerns (efficiency, soundness, scope of applicability) evolved from 2010 through to the 2023–2025 wave of papers reviewed above (Papers 6, 8, 11–14).

---

## 18. Model-Based Testing of Probabilistic Systems

**Authors:** Marcus Gerhold, Mariëlle Stoelinga
**Venue:** FASE 2016 (19th International Conference on Fundamental Approaches to Software Engineering), LNCS 9633, pp. 251–268; journal version in *Formal Aspects of Computing* (2018)
**DOI:** 10.1007/978-3-662-49665-7_15 (conference); 10.1007/s00165-017-0440-4 (journal)

This is a foundational paper for probabilistic model-based testing, directly connecting classical **ioco-theory** (input/output conformance testing) with **statistical hypothesis testing**. The authors present an executable MBT framework for black-box probabilistic systems that also exhibit non-determinism, providing algorithms to automatically generate, execute, and evaluate test cases from a probabilistic requirements model. Functionally, the ioco-style algorithms handle correctness of the traditional (non-probabilistic) input/output behavior; statistically, χ² hypothesis tests and distribution-fitting methods assess whether the *frequencies* observed during repeated test execution correspond to the *probabilities* specified in the requirements model. A key technical challenge the authors solve is that non-determinism in the underlying probabilistic input/output transition systems (pIOTS) prevents a direct application of the χ² test; instead, the authors formulate a non-linear optimization problem to find the "best resolution" of the non-determinism that could explain the observed test data, enabling the χ² test to then be applied meaningfully. The paper's central theoretical results are the **soundness** (every test case receives the mathematically correct verdict) and **completeness** (the framework can, in principle, detect any probabilistic deviation from the specification with arbitrary precision) of the resulting **probabilistic input/output conformance (pioco)** relation. This paper — later extended to stochastic continuous time by the same authors — is arguably the most rigorous formal foundation among all twenty papers reviewed here for probabilistic model-based testing specifically, and is essential background for Paper 1's coverage-analysis extensions and Paper 7's uncertainty-aware exploration strategies.

---

## 19. Model-Based Testing in Practice: An Experience Report from the Web Applications Domain

**Authors:** Vahid Garousi, Alper Buğra Keleş, Yunus Balaman, Zeynep Özdemir Güler, Andrea Arcuri
**Venue:** *Journal of Systems and Software*, Vol. 180, Article 111032 (2021)
**DOI:** 10.1016/j.jss.2021.111032

This industrial experience report documents the deployment of model-based testing at a large software testing company (Testinium A.Ş.) to elevate the maturity of its test-automation practices for large-scale web and mobile applications. Based on an "action research" methodology, the authors selected the open-source tool **GraphWalker** from among available open-source/commercial MBT tools and pragmatically applied MBT for end-to-end test automation. The reported benefits are both tangible (improved test coverage measured as number of distinct paths tested, and improved real-fault detection effectiveness) and intangible (improved test-design discipline across the organization). The paper's central argument — echoed by Paper 2's findings on adoption barriers — is that the practical value of any MBT technique is inseparable from its usability by working test engineers under real resource constraints (time, effort, existing skillsets, management priorities), and that heavyweight, academically sophisticated MBT approaches often fail in enterprise contexts like web/mobile testing precisely because they neglect this. This paper's authorship overlaps substantially with Paper 5 (the MBTCover tool paper), and together the two form a coherent, practice-grounded narrative of a real industrial MBT adoption journey — first establishing the MBT practice itself (Paper 19), then building the coverage-integration tooling that practice subsequently required (Paper 5).

---

## 20. Approximate Planning and Verification for Large Markov Decision Processes

**Authors:** Richard Lassaigne, Sylvain Peyronnet
**Venue:** *International Journal on Software Tools for Technology Transfer* (journal version); originally presented at ACM Symposium on Applied Computing (SAC) 2012, pp. 1314–1319
**DOI:** 10.1007/s10009-014-0344-z

This paper addresses the planning and verification problems for very large probabilistic systems — specifically Markov decision processes — from a computational complexity perspective. The authors' central concern is designing **efficient approximation methods** for two related problems: (1) computing a near-optimal policy for the planning problem in discounted MDPs, and (2) computing the satisfaction probabilities of properties of interest (such as reachability or safety) over the Markov chain that results from restricting the MDP to that near-optimal policy. Two distinct approximation approaches are presented: the first is based on **sparse sampling**, whose complexity is notably independent of the size of the state space and requires only a probabilistic generator of the MDP rather than full access to its transition structure — making it applicable even when the state space is too large to represent explicitly; the second uses a variant of the **multiplicative weights update algorithm**. The paper provides a complete complexity analysis of the sparse-sampling approach, parameterized primarily by the desired approximation quality. Because MDPs are the common underlying formalism connecting several other papers in this review — Paper 4's generative testing of MDP-based decision policies, Paper 7's uncertainty-aware MBT over MDPs, and Paper 13's MDP-based CNN robustness verification — this paper's complexity-theoretic treatment of MDP planning/verification approximation provides useful theoretical grounding for why sampling-based (rather than exhaustive) approaches are necessary once MDP-based models scale beyond small, hand-crafted examples.

---

## Synthesis

Taken together, these twenty papers trace three converging lines of research. First, the **model-based testing** tradition (Papers 1–5, 18–19) has matured from academic proposals toward serious grappling with practical adoption barriers, coverage-measurement rigor, and the model-to-code transformation gap. Second, the **statistical model checking** tradition (Papers 8–17) has evolved from foundational tutorials (2010–2014) through a comprehensive survey (2018) to a current wave (2023–2025) of papers establishing genuine statistical soundness and extending SMC into entirely new domains — computer architecture, spare-parts logistics, quantum calibration — that share nothing with SMC's original formal-verification roots except the underlying statistical machinery. Third, a smaller but conceptually pivotal set of papers (6, 7, 13, 14, 20) explicitly **bridges** testing and statistical/probabilistic verification, using MDPs, PCTL, and hypothesis testing as the common mathematical vocabulary. Collectively, they support the view that treating uncertainty as a first-class, quantifiable concern — rather than an obstacle to be abstracted away — is now a mainstream, multi-disciplinary concern spanning software testing, formal methods, computer architecture, and machine-learning assurance.