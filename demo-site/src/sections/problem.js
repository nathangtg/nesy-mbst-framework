export function renderProblem() {
  const section = document.getElementById('problem');
  section.innerHTML = `
    <div class="section border-t border-gray-100 dark:border-gray-800/50">
      <div class="section-header animate-on-scroll">
        <h2 class="section-title">The Problem</h2>
        <p class="section-desc">
          Model-Based Statistical Testing needs Markov usage models that nobody wants to build by hand. 
          Pure-AI approaches fail systematically.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 animate-on-scroll">
        <div class="card">
          <div class="text-sm font-semibold text-gray-900 dark:text-white mb-2">Hallucination</div>
          <p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
            AI invents transitions that cannot happen in the real system.
          </p>
        </div>
        <div class="card">
          <div class="text-sm font-semibold text-gray-900 dark:text-white mb-2">Bad Probabilities</div>
          <p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
            Row sums exceed 1.0, breaking all downstream statistics.
          </p>
        </div>
        <div class="card">
          <div class="text-sm font-semibold text-gray-900 dark:text-white mb-2">State Explosion</div>
          <p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
            Large systems cause mid-generation contradictions and dropped states.
          </p>
        </div>
        <div class="card">
          <div class="text-sm font-semibold text-gray-900 dark:text-white mb-2">Logic Violations</div>
          <p class="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
            Semantically plausible but logically impossible paths pass unchecked.
          </p>
        </div>
      </div>

      <div class="mt-8 p-4 rounded-lg bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-800 animate-on-scroll">
        <p class="text-sm text-gray-600 dark:text-gray-300">
          <span class="font-semibold">Our approach:</span> Assign each sub-task to the paradigm best suited for it — 
          <span class="text-blue-600 dark:text-blue-400 font-medium">neural inference</span> for language reasoning, 
          <span class="text-emerald-600 dark:text-emerald-400 font-medium">symbolic computation</span> for formal precision.
        </p>
      </div>
    </div>
  `;
}
