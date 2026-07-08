import ablationData from '../data/ablation.json';

export function renderComparison() {
  const section = document.getElementById('comparison');
  section.innerHTML = `
    <div class="section-container">
      <div class="text-center mb-16 animate-on-scroll">
        <h2 class="section-title">Ablation Study</h2>
        <p class="section-subtitle mx-auto">
          Toggle components on and off to see how each contributes to the final result.
        </p>
      </div>

      <!-- Toggle Controls -->
      <div class="max-w-3xl mx-auto mb-12 animate-on-scroll">
        <div class="card">
          <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-6">Active Components</h4>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <label class="flex items-center gap-3 cursor-pointer group">
              <input type="checkbox" id="toggle-neural" checked disabled class="w-4 h-4 rounded text-blue-600 focus:ring-blue-500">
              <span class="text-sm text-gray-700 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white">
                <span class="tag-neural text-xs">Neural</span>
                <br/><span class="text-xs text-gray-500">LLM Oracle</span>
              </span>
            </label>
            <label class="flex items-center gap-3 cursor-pointer group">
              <input type="checkbox" id="toggle-symbolic" class="w-4 h-4 rounded text-green-600 focus:ring-green-500 cursor-pointer">
              <span class="text-sm text-gray-700 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white">
                <span class="tag-symbolic text-xs">Symbolic</span>
                <br/><span class="text-xs text-gray-500">Feasibility Check</span>
              </span>
            </label>
            <label class="flex items-center gap-3 cursor-pointer group">
              <input type="checkbox" id="toggle-optimizer" class="w-4 h-4 rounded text-purple-600 focus:ring-purple-500 cursor-pointer">
              <span class="text-sm text-gray-700 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white">
                <span class="tag-optimization text-xs">Optimizer</span>
                <br/><span class="text-xs text-gray-500">Convex Solver</span>
              </span>
            </label>
            <label class="flex items-center gap-3 cursor-pointer group">
              <input type="checkbox" id="toggle-feedback" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500 cursor-pointer">
              <span class="text-sm text-gray-700 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white">
                <span class="tag bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300 text-xs">Feedback</span>
                <br/><span class="text-xs text-gray-500">Closed Loop</span>
              </span>
            </label>
          </div>
        </div>
      </div>

      <!-- Ablation Results -->
      <div class="max-w-5xl mx-auto animate-on-scroll">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="ablation-metrics">
          <!-- System F1 -->
          <div class="card text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-2">System F1 Score</div>
            <div id="ablation-f1" class="text-4xl font-bold text-primary-600 dark:text-primary-400 transition-all duration-500">
              0.6559
            </div>
            <div class="mt-3 h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div id="ablation-f1-bar" class="h-full bg-primary-500 rounded-full transition-all duration-700" style="width: 65.59%"></div>
            </div>
            <div class="mt-2 flex justify-between text-[10px] text-gray-400">
              <span>0</span>
              <span class="text-red-400">0.90 threshold</span>
              <span>1.0</span>
            </div>
          </div>

          <!-- Coverage -->
          <div class="card text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-2">Transition Coverage</div>
            <div id="ablation-coverage" class="text-4xl font-bold text-green-600 dark:text-green-400 transition-all duration-500">
              50.0%
            </div>
            <div class="mt-3 h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div id="ablation-coverage-bar" class="h-full bg-green-500 rounded-full transition-all duration-700" style="width: 50%"></div>
            </div>
            <div class="mt-2 flex justify-between text-[10px] text-gray-400">
              <span>0%</span>
              <span>100%</span>
            </div>
          </div>

          <!-- JSD -->
          <div class="card text-center">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-2">Jensen-Shannon Divergence</div>
            <div id="ablation-jsd" class="text-4xl font-bold text-purple-600 dark:text-purple-400 transition-all duration-500">
              0.157
            </div>
            <div class="mt-3 h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div id="ablation-jsd-bar" class="h-full bg-purple-500 rounded-full transition-all duration-700" style="width: 78.5%"></div>
            </div>
            <div class="mt-2 flex justify-between text-[10px] text-gray-400">
              <span>0 (perfect)</span>
              <span>0.2 (poor)</span>
            </div>
          </div>
        </div>

        <!-- Insight box -->
        <div class="mt-8 max-w-3xl mx-auto">
          <div id="ablation-insight" class="card bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/10 dark:to-purple-900/10 border-l-4 border-l-primary-500">
            <p class="text-sm text-gray-700 dark:text-gray-300">
              <strong>Insight:</strong> The neural component alone produces a structurally incomplete model. 
              Toggle on the Symbolic checker to see the structural improvement, then the Optimizer for probability calibration.
            </p>
          </div>
        </div>
      </div>
    </div>
  `;

  initAblationToggles();
}

function initAblationToggles() {
  const toggles = {
    symbolic: document.getElementById('toggle-symbolic'),
    optimizer: document.getElementById('toggle-optimizer'),
    feedback: document.getElementById('toggle-feedback'),
  };

  const update = () => {
    const symbolic = toggles.symbolic.checked;
    const optimizer = toggles.optimizer.checked;
    const feedback = toggles.feedback.checked;

    // Determine condition
    let condition;
    if (feedback && optimizer && symbolic) {
      condition = ablationData.conditions[3]; // Full
    } else if (optimizer && symbolic) {
      condition = ablationData.conditions[2]; // +Optimizer
    } else if (symbolic) {
      condition = ablationData.conditions[1]; // +Symbolic
    } else {
      condition = ablationData.conditions[0]; // Pure Neural
    }

    // Update metrics
    document.getElementById('ablation-f1').textContent = condition.metrics.systemF1.toFixed(4);
    document.getElementById('ablation-f1-bar').style.width = `${condition.metrics.systemF1 * 100}%`;
    
    document.getElementById('ablation-coverage').textContent = `${(condition.metrics.transitionCoverage * 100).toFixed(1)}%`;
    document.getElementById('ablation-coverage-bar').style.width = `${condition.metrics.transitionCoverage * 100}%`;
    
    document.getElementById('ablation-jsd').textContent = condition.metrics.jsd.toFixed(3);
    document.getElementById('ablation-jsd-bar').style.width = `${(condition.metrics.jsd / 0.2) * 100}%`;

    // Update insight
    const insights = {
      'pure-neural': 'The neural component alone produces a structurally incomplete model with 50% coverage and poor probability calibration.',
      'neural-symbolic': '<strong>Big jump!</strong> The symbolic checker recovers missing transitions, boosting coverage from 50% to 85.7%. Structure is now complete.',
      'neural-symbolic-optimizer': '<strong>Calibrated!</strong> The convex optimizer brings JSD from 0.089 down to 0.012 — near-perfect probability alignment.',
      'full-nesy': '<strong>Complete system.</strong> The feedback loop fine-tunes probabilities from runtime telemetry. All components work synergistically.',
    };

    document.getElementById('ablation-insight').innerHTML = `
      <p class="text-sm text-gray-700 dark:text-gray-300">
        <strong>Insight:</strong> ${insights[condition.id]}
      </p>
    `;

    // Enforce dependency: optimizer requires symbolic
    if (!symbolic) {
      toggles.optimizer.checked = false;
      toggles.optimizer.disabled = true;
      toggles.feedback.checked = false;
      toggles.feedback.disabled = true;
    } else {
      toggles.optimizer.disabled = false;
      if (!optimizer) {
        toggles.feedback.checked = false;
        toggles.feedback.disabled = true;
      } else {
        toggles.feedback.disabled = false;
      }
    }
  };

  Object.values(toggles).forEach((toggle) => {
    toggle.addEventListener('change', update);
  });
}
