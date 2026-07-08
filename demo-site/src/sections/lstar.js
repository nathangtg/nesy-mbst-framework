import { createLStarAnimation } from '../components/lstar-animation.js';

export function renderLStar() {
  const section = document.getElementById('lstar');
  section.innerHTML = `
    <div class="section-container">
      <div class="text-center mb-12 animate-on-scroll">
        <h2 class="section-title">L* Active Learning</h2>
        <p class="section-subtitle mx-auto">
          Step through the L* algorithm as it discovers the state machine structure through membership and equivalence queries.
        </p>
      </div>

      <div class="max-w-4xl mx-auto animate-on-scroll">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Main animation -->
          <div class="lg:col-span-2 card">
            <div id="lstar-container"></div>
          </div>

          <!-- Explanation sidebar -->
          <div class="space-y-4">
            <div class="card">
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-3">How L* Works</h4>
              <ol class="space-y-3 text-xs text-gray-600 dark:text-gray-400">
                <li class="flex gap-2">
                  <span class="flex-shrink-0 w-5 h-5 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400 font-bold text-[10px]">1</span>
                  <span>Build an <strong>observation table</strong> (prefixes x suffixes → accept/reject)</span>
                </li>
                <li class="flex gap-2">
                  <span class="flex-shrink-0 w-5 h-5 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400 font-bold text-[10px]">2</span>
                  <span>Ask <strong>membership queries</strong>: "Does the SUT accept this sequence?"</span>
                </li>
                <li class="flex gap-2">
                  <span class="flex-shrink-0 w-5 h-5 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400 font-bold text-[10px]">3</span>
                  <span>When table is <strong>closed and consistent</strong>, build a hypothesis DFA</span>
                </li>
                <li class="flex gap-2">
                  <span class="flex-shrink-0 w-5 h-5 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400 font-bold text-[10px]">4</span>
                  <span>Submit hypothesis via <strong>equivalence query</strong>. If wrong, get a counterexample</span>
                </li>
                <li class="flex gap-2">
                  <span class="flex-shrink-0 w-5 h-5 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center text-green-600 dark:text-green-400 font-bold text-[10px]">5</span>
                  <span>Repeat until hypothesis equals the target — <strong>convergence guaranteed</strong></span>
                </li>
              </ol>
            </div>

            <div class="card bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/10 dark:to-indigo-900/10">
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">NeSy-MBST Innovation</h4>
              <p class="text-xs text-gray-600 dark:text-gray-400">
                Instead of a traditional oracle, NeSy-MBST uses a <strong>grammar-constrained LLM</strong> as the membership oracle. Responses are restricted to {Yes, No, Unsure} — preventing hallucination while leveraging the LLM's language understanding.
              </p>
            </div>

            <div class="card">
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-2">Key Properties</h4>
              <div class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
                <div class="flex justify-between">
                  <span>Convergence</span>
                  <span class="font-medium text-green-600 dark:text-green-400">Guaranteed</span>
                </div>
                <div class="flex justify-between">
                  <span>Query Complexity</span>
                  <span class="font-mono">O(kn<sup>2</sup>m)</span>
                </div>
                <div class="flex justify-between">
                  <span>Oracle Type</span>
                  <span class="font-medium">Grammar-Constrained LLM</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Initialize animation
  const container = document.getElementById('lstar-container');
  createLStarAnimation(container);
}
