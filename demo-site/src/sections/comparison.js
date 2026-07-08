import ablationData from '../data/ablation.json';

export function renderComparison() {
  const section = document.getElementById('comparison');
  section.innerHTML = `
    <div class="section border-t border-gray-100 dark:border-gray-800/50">
      <div class="section-header animate-on-scroll">
        <h2 class="section-title">Ablation Study</h2>
        <p class="section-desc">
          Toggle components to see how each contributes to the final result.
        </p>
      </div>

      <!-- Toggles -->
      <div class="card mb-6 animate-on-scroll">
        <div class="flex flex-wrap items-center gap-6">
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" id="toggle-neural" checked disabled class="w-3.5 h-3.5 rounded text-blue-600">
            <span class="text-sm text-gray-700 dark:text-gray-300">Neural <span class="text-xs text-gray-400">(always on)</span></span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" id="toggle-symbolic" class="w-3.5 h-3.5 rounded text-emerald-600 cursor-pointer">
            <span class="text-sm text-gray-700 dark:text-gray-300">Symbolic</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" id="toggle-optimizer" class="w-3.5 h-3.5 rounded text-violet-600 cursor-pointer">
            <span class="text-sm text-gray-700 dark:text-gray-300">Optimizer</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" id="toggle-feedback" class="w-3.5 h-3.5 rounded text-indigo-600 cursor-pointer">
            <span class="text-sm text-gray-700 dark:text-gray-300">Feedback</span>
          </label>
        </div>
      </div>

      <!-- Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 animate-on-scroll">
        <div class="card text-center">
          <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">System F1</div>
          <div id="ablation-f1" class="text-3xl font-bold text-gray-900 dark:text-white tabular-nums transition-all duration-300">0.6559</div>
          <div class="mt-3 h-1.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
            <div id="ablation-f1-bar" class="h-full bg-gray-900 dark:bg-white rounded-full transition-all duration-500" style="width: 65.59%"></div>
          </div>
        </div>
        <div class="card text-center">
          <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">Coverage</div>
          <div id="ablation-coverage" class="text-3xl font-bold text-gray-900 dark:text-white tabular-nums transition-all duration-300">50.0%</div>
          <div class="mt-3 h-1.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
            <div id="ablation-coverage-bar" class="h-full bg-emerald-500 rounded-full transition-all duration-500" style="width: 50%"></div>
          </div>
        </div>
        <div class="card text-center">
          <div class="text-xs text-gray-500 dark:text-gray-400 mb-1">JSD (lower is better)</div>
          <div id="ablation-jsd" class="text-3xl font-bold text-gray-900 dark:text-white tabular-nums transition-all duration-300">0.157</div>
          <div class="mt-3 h-1.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
            <div id="ablation-jsd-bar" class="h-full bg-violet-500 rounded-full transition-all duration-500" style="width: 78.5%"></div>
          </div>
        </div>
      </div>

      <!-- Insight -->
      <div id="ablation-insight" class="mt-4 p-4 rounded-lg bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-800 text-sm text-gray-600 dark:text-gray-400 animate-on-scroll">
        Toggle on the Symbolic checker to see structural improvement, then Optimizer for probability calibration.
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

    let condition;
    if (feedback && optimizer && symbolic) condition = ablationData.conditions[3];
    else if (optimizer && symbolic) condition = ablationData.conditions[2];
    else if (symbolic) condition = ablationData.conditions[1];
    else condition = ablationData.conditions[0];

    document.getElementById('ablation-f1').textContent = condition.metrics.systemF1.toFixed(4);
    document.getElementById('ablation-f1-bar').style.width = `${condition.metrics.systemF1 * 100}%`;
    document.getElementById('ablation-coverage').textContent = `${(condition.metrics.transitionCoverage * 100).toFixed(1)}%`;
    document.getElementById('ablation-coverage-bar').style.width = `${condition.metrics.transitionCoverage * 100}%`;
    document.getElementById('ablation-jsd').textContent = condition.metrics.jsd.toFixed(3);
    document.getElementById('ablation-jsd-bar').style.width = `${(condition.metrics.jsd / 0.2) * 100}%`;

    const insights = {
      'pure-neural': 'Neural-only: incomplete structure (50% coverage) and poor probability calibration.',
      'neural-symbolic': 'Symbolic checker recovers missing transitions — coverage jumps from 50% to 85.7%.',
      'neural-symbolic-optimizer': 'Convex optimizer calibrates probabilities — JSD drops from 0.089 to 0.012.',
      'full-nesy': 'Complete system with closed-loop feedback for continuous refinement.',
    };
    document.getElementById('ablation-insight').textContent = insights[condition.id];

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

  Object.values(toggles).forEach((t) => t.addEventListener('change', update));
}
