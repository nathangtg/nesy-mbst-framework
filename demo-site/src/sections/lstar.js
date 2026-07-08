import { createLStarAnimation } from '../components/lstar-animation.js';

export function renderLStar() {
  const section = document.getElementById('lstar');
  section.innerHTML = `
    <div class="section border-t border-gray-100 dark:border-gray-800/50">
      <div class="section-header animate-on-scroll">
        <h2 class="section-title">L* Active Learning</h2>
        <p class="section-desc">
          Step through the algorithm as it discovers state machine structure via membership and equivalence queries.
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-on-scroll">
        <div class="lg:col-span-2 card">
          <div id="lstar-container"></div>
        </div>

        <div class="space-y-4">
          <div class="card">
            <div class="text-sm font-semibold text-gray-900 dark:text-white mb-3">How It Works</div>
            <ol class="space-y-2.5 text-xs text-gray-600 dark:text-gray-400">
              <li class="flex gap-2">
                <span class="flex-shrink-0 w-4 h-4 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-[10px] font-bold text-gray-500">1</span>
                <span>Build observation table (prefixes x suffixes)</span>
              </li>
              <li class="flex gap-2">
                <span class="flex-shrink-0 w-4 h-4 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-[10px] font-bold text-gray-500">2</span>
                <span>Ask membership queries via grammar-constrained LLM</span>
              </li>
              <li class="flex gap-2">
                <span class="flex-shrink-0 w-4 h-4 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-[10px] font-bold text-gray-500">3</span>
                <span>When closed + consistent, build hypothesis DFA</span>
              </li>
              <li class="flex gap-2">
                <span class="flex-shrink-0 w-4 h-4 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-[10px] font-bold text-gray-500">4</span>
                <span>Equivalence query; refine with counterexample</span>
              </li>
              <li class="flex gap-2">
                <span class="flex-shrink-0 w-4 h-4 rounded-full bg-emerald-100 dark:bg-emerald-950 flex items-center justify-center text-[10px] font-bold text-emerald-600 dark:text-emerald-400">5</span>
                <span>Repeat until convergence (guaranteed)</span>
              </li>
            </ol>
          </div>

          <div class="card bg-gray-50 dark:bg-gray-900">
            <div class="text-xs font-semibold text-gray-700 dark:text-gray-300 mb-2">Key Properties</div>
            <div class="space-y-1.5 text-xs text-gray-500 dark:text-gray-400">
              <div class="flex justify-between">
                <span>Convergence</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-medium">Guaranteed</span>
              </div>
              <div class="flex justify-between">
                <span>Query Complexity</span>
                <span class="font-mono">O(kn&sup2;m)</span>
              </div>
              <div class="flex justify-between">
                <span>Oracle</span>
                <span class="font-medium">Grammar-Constrained LLM</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  const container = document.getElementById('lstar-container');
  createLStarAnimation(container);
}
