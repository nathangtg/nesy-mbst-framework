export function renderArchitecture() {
  const section = document.getElementById('architecture');
  section.innerHTML = `
    <div class="section border-t border-gray-100 dark:border-gray-800/50">
      <div class="section-header animate-on-scroll">
        <h2 class="section-title">Architecture</h2>
        <p class="section-desc">
          Five stages, each matched to its optimal computational paradigm.
        </p>
      </div>

      <!-- Pipeline -->
      <div class="animate-on-scroll">
        <div class="grid grid-cols-5 gap-2 md:gap-4 mb-10">
          <div class="text-center">
            <div class="w-10 h-10 mx-auto rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-2">
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <div class="text-[11px] font-medium text-gray-700 dark:text-gray-300">Input</div>
            <div class="text-[10px] text-gray-400">NL Requirements</div>
          </div>
          <div class="text-center">
            <div class="w-10 h-10 mx-auto rounded-lg bg-blue-50 dark:bg-blue-950 flex items-center justify-center mb-2">
              <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
            </div>
            <div class="text-[11px] font-medium text-gray-700 dark:text-gray-300">Extract</div>
            <div class="text-[10px] text-blue-600 dark:text-blue-400">Neural</div>
          </div>
          <div class="text-center">
            <div class="w-10 h-10 mx-auto rounded-lg bg-emerald-50 dark:bg-emerald-950 flex items-center justify-center mb-2">
              <svg class="w-5 h-5 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <div class="text-[11px] font-medium text-gray-700 dark:text-gray-300">Verify</div>
            <div class="text-[10px] text-emerald-600 dark:text-emerald-400">Symbolic</div>
          </div>
          <div class="text-center">
            <div class="w-10 h-10 mx-auto rounded-lg bg-violet-50 dark:bg-violet-950 flex items-center justify-center mb-2">
              <svg class="w-5 h-5 text-violet-600 dark:text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/>
              </svg>
            </div>
            <div class="text-[11px] font-medium text-gray-700 dark:text-gray-300">Optimize</div>
            <div class="text-[10px] text-violet-600 dark:text-violet-400">Convex Solver</div>
          </div>
          <div class="text-center">
            <div class="w-10 h-10 mx-auto rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-2">
              <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
              </svg>
            </div>
            <div class="text-[11px] font-medium text-gray-700 dark:text-gray-300">Test</div>
            <div class="text-[10px] text-gray-400">Generation</div>
          </div>
        </div>

        <!-- Connector line -->
        <div class="relative h-px bg-gray-200 dark:bg-gray-800 -mt-[52px] mb-12 mx-[10%]">
          <div class="absolute inset-0 bg-gradient-to-r from-gray-200 via-blue-300 to-emerald-300 dark:from-gray-700 dark:via-blue-600 dark:to-emerald-600 opacity-60"></div>
        </div>
      </div>

      <!-- Details grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 animate-on-scroll">
        <div class="card border-t-2 border-t-blue-500">
          <div class="tag-neural mb-3">Neural Layer</div>
          <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
            <li>Grammar-constrained LLM oracle</li>
            <li>L* active automata learning</li>
            <li>Constraint extraction from NL</li>
            <li>Calibrated uncertainty estimation</li>
          </ul>
        </div>
        <div class="card border-t-2 border-t-emerald-500">
          <div class="tag-symbolic mb-3">Symbolic Layer</div>
          <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
            <li>Invariant enforcement</li>
            <li>Blocked transition detection</li>
            <li>Reachability analysis</li>
            <li>Precondition validation</li>
          </ul>
        </div>
        <div class="card border-t-2 border-t-violet-500">
          <div class="tag-optimization mb-3">Optimization</div>
          <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
            <li>Row-stochastic enforcement</li>
            <li>Maximum entropy (SLSQP)</li>
            <li>NL constraint compilation</li>
            <li>Guaranteed valid distributions</li>
          </ul>
        </div>
      </div>
    </div>
  `;
}
