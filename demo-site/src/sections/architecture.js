export function renderArchitecture() {
  const section = document.getElementById('architecture');
  section.innerHTML = `
    <div class="section-container">
      <div class="text-center mb-16 animate-on-scroll">
        <h2 class="section-title">Architecture</h2>
        <p class="section-subtitle mx-auto">
          A five-stage pipeline where each component is matched to its optimal computational paradigm.
        </p>
      </div>

      <!-- Pipeline Visualization -->
      <div class="max-w-5xl mx-auto mb-12 animate-on-scroll">
        <div class="relative">
          <!-- Pipeline SVG -->
          <svg id="pipeline-svg" class="w-full" viewBox="0 0 1000 200" preserveAspectRatio="xMidYMid meet">
            <!-- Connection lines -->
            <path d="M 140 100 L 240 100" class="pipeline-connector" stroke="#e5e7eb" stroke-width="2" stroke-dasharray="5,5"/>
            <path d="M 340 100 L 440 100" class="pipeline-connector" stroke="#e5e7eb" stroke-width="2" stroke-dasharray="5,5"/>
            <path d="M 540 100 L 640 100" class="pipeline-connector" stroke="#e5e7eb" stroke-width="2" stroke-dasharray="5,5"/>
            <path d="M 740 100 L 840 100" class="pipeline-connector" stroke="#e5e7eb" stroke-width="2" stroke-dasharray="5,5"/>
            
            <!-- Flow particles -->
            <circle class="flow-dot" r="4" fill="#3b82f6" opacity="0">
              <animateMotion dur="3s" repeatCount="indefinite" path="M 140 100 L 860 100"/>
              <animate attributeName="opacity" values="0;1;1;0" dur="3s" repeatCount="indefinite"/>
            </circle>
            <circle class="flow-dot" r="4" fill="#22c55e" opacity="0">
              <animateMotion dur="3s" repeatCount="indefinite" path="M 140 100 L 860 100" begin="1s"/>
              <animate attributeName="opacity" values="0;1;1;0" dur="3s" repeatCount="indefinite" begin="1s"/>
            </circle>
            <circle class="flow-dot" r="4" fill="#a855f7" opacity="0">
              <animateMotion dur="3s" repeatCount="indefinite" path="M 140 100 L 860 100" begin="2s"/>
              <animate attributeName="opacity" values="0;1;1;0" dur="3s" repeatCount="indefinite" begin="2s"/>
            </circle>
          </svg>

          <!-- Pipeline Stages -->
          <div class="grid grid-cols-5 gap-4 -mt-4">
            <!-- Stage 1: NL Input -->
            <div class="pipeline-stage group" data-stage="input">
              <div class="w-16 h-16 rounded-xl bg-gray-100 dark:bg-gray-700 flex items-center justify-center mb-3 group-hover:bg-gray-200 dark:group-hover:bg-gray-600 transition-colors">
                <svg class="w-8 h-8 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
              </div>
              <span class="text-xs font-medium text-gray-700 dark:text-gray-300 text-center">NL Requirements</span>
            </div>

            <!-- Stage 2: Neural Extraction -->
            <div class="pipeline-stage group" data-stage="neural">
              <div class="w-16 h-16 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-3 group-hover:bg-blue-200 dark:group-hover:bg-blue-800/40 transition-colors">
                <svg class="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                </svg>
              </div>
              <span class="tag-neural text-xs mb-1">Neural</span>
              <span class="text-xs font-medium text-gray-700 dark:text-gray-300 text-center">LLM Extraction</span>
            </div>

            <!-- Stage 3: Symbolic Verification -->
            <div class="pipeline-stage group" data-stage="symbolic">
              <div class="w-16 h-16 rounded-xl bg-green-100 dark:bg-green-900/30 flex items-center justify-center mb-3 group-hover:bg-green-200 dark:group-hover:bg-green-800/40 transition-colors">
                <svg class="w-8 h-8 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
              </div>
              <span class="tag-symbolic text-xs mb-1">Symbolic</span>
              <span class="text-xs font-medium text-gray-700 dark:text-gray-300 text-center">Verification</span>
            </div>

            <!-- Stage 4: Constraint Optimization -->
            <div class="pipeline-stage group" data-stage="optimizer">
              <div class="w-16 h-16 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-3 group-hover:bg-purple-200 dark:group-hover:bg-purple-800/40 transition-colors">
                <svg class="w-8 h-8 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.871 4A17.926 17.926 0 003 12c0 2.874.673 5.59 1.871 8m14.13 0A17.926 17.926 0 0021 12c0-2.874-.673-5.59-1.871-8M9 9h1.246a1 1 0 01.961.725l1.586 5.55a1 1 0 00.961.725H15m-6 0a1 1 0 00-1 1v2a1 1 0 001 1h6a1 1 0 001-1v-2a1 1 0 00-1-1"/>
                </svg>
              </div>
              <span class="tag-optimization text-xs mb-1">Optimization</span>
              <span class="text-xs font-medium text-gray-700 dark:text-gray-300 text-center">Constraint Solver</span>
            </div>

            <!-- Stage 5: Test Generation -->
            <div class="pipeline-stage group" data-stage="testing">
              <div class="w-16 h-16 rounded-xl bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center mb-3 group-hover:bg-indigo-200 dark:group-hover:bg-indigo-800/40 transition-colors">
                <svg class="w-8 h-8 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
                </svg>
              </div>
              <span class="text-xs font-medium text-gray-700 dark:text-gray-300 text-center">Test Generation</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Detail panels -->
      <div id="stage-details" class="max-w-5xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-on-scroll">
          <!-- Neural Detail -->
          <div class="card border-t-4 border-t-blue-500" id="detail-neural">
            <h4 class="font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
              <span class="tag-neural">Neural</span>
              LLM Oracle + L* Learning
            </h4>
            <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                Grammar-constrained membership queries
              </li>
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                Active automata learning (L* algorithm)
              </li>
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                NL constraint extraction
              </li>
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                Calibrated uncertainty estimation
              </li>
            </ul>
          </div>

          <!-- Symbolic Detail -->
          <div class="card border-t-4 border-t-green-500" id="detail-symbolic">
            <h4 class="font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
              <span class="tag-symbolic">Symbolic</span>
              Feasibility Checker
            </h4>
            <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                Invariant enforcement
              </li>
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                Blocked transition detection
              </li>
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                Reachability analysis
              </li>
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                Precondition validation
              </li>
            </ul>
          </div>

          <!-- Optimizer Detail -->
          <div class="card border-t-4 border-t-purple-500" id="detail-optimizer">
            <h4 class="font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
              <span class="tag-optimization">Optimization</span>
              Convex Solver
            </h4>
            <ul class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-purple-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                Row-stochastic constraint enforcement
              </li>
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-purple-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                Maximum entropy optimization (SLSQP)
              </li>
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-purple-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                NL constraint compilation
              </li>
              <li class="flex items-start gap-2">
                <svg class="w-4 h-4 text-purple-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                Guaranteed valid probability distributions
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Feedback loop indicator -->
      <div class="max-w-5xl mx-auto mt-8 animate-on-scroll">
        <div class="card bg-gradient-to-r from-blue-50 via-green-50 to-purple-50 dark:from-blue-900/10 dark:via-green-900/10 dark:to-purple-900/10 border-dashed">
          <div class="flex items-center justify-center gap-3">
            <svg class="w-5 h-5 text-gray-500 animate-spin" style="animation-duration: 3s" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <span class="text-sm font-medium text-gray-600 dark:text-gray-400">
              Closed-Loop Feedback: Runtime telemetry continuously refines the model via drift detection and adaptive learning
            </span>
          </div>
        </div>
      </div>
    </div>
  `;

  initPipelineInteraction();
}

function initPipelineInteraction() {
  const stages = document.querySelectorAll('.pipeline-stage');
  
  stages.forEach((stage) => {
    stage.addEventListener('click', () => {
      const stageId = stage.dataset.stage;
      const detail = document.getElementById(`detail-${stageId}`);
      if (detail) {
        detail.scrollIntoView({ behavior: 'smooth', block: 'center' });
        detail.classList.add('ring-2', 'ring-primary-500');
        setTimeout(() => detail.classList.remove('ring-2', 'ring-primary-500'), 2000);
      }
    });
  });
}
