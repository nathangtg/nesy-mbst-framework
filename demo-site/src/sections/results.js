import ablationData from '../data/ablation.json';

export function renderResults() {
  const section = document.getElementById('results');
  section.innerHTML = `
    <div class="section-container">
      <div class="text-center mb-16 animate-on-scroll">
        <h2 class="section-title">Results</h2>
        <p class="section-subtitle mx-auto">
          Evaluated on autonomous vehicle (9 states) and e-commerce platforms (24 and 42 states).
        </p>
      </div>

      <!-- Key Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto mb-16 animate-on-scroll">
        <div class="metric-card">
          <div class="metric-value" data-target="0.91" data-decimals="2">0</div>
          <div class="metric-label">System F1 Score</div>
          <div class="mt-2 text-xs text-green-600 dark:text-green-400 font-medium">
            Exceeds 0.90 safety threshold
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-value" data-target="85.7" data-decimals="1" data-suffix="%">0</div>
          <div class="metric-label">Fault-Path Coverage</div>
          <div class="mt-2 text-xs text-green-600 dark:text-green-400 font-medium">
            +35.7pp vs baseline
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-value" data-target="0.012" data-decimals="3">0</div>
          <div class="metric-label">Jensen-Shannon Divergence</div>
          <div class="mt-2 text-xs text-green-600 dark:text-green-400 font-medium">
            Near-identical distributions
          </div>
        </div>
        <div class="metric-card">
          <div class="metric-value" data-target="6" data-decimals="0" data-prefix="<" data-suffix="min">0</div>
          <div class="metric-label">Generation Time</div>
          <div class="mt-2 text-xs text-green-600 dark:text-green-400 font-medium">
            42-state model, fully automated
          </div>
        </div>
      </div>

      <!-- Comparison Chart -->
      <div class="max-w-4xl mx-auto mb-16 animate-on-scroll">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-6 text-center">
          vs. Pure-Neural Baselines
        </h3>
        <div class="card">
          <div class="space-y-6">
            ${ablationData.baselines.map((baseline) => `
              <div class="space-y-2">
                <div class="flex justify-between items-center">
                  <span class="text-sm font-medium text-gray-700 dark:text-gray-300">${baseline.label}</span>
                  <span class="text-sm font-mono font-bold ${baseline.id === 'nesy-mbst' ? 'text-primary-600 dark:text-primary-400' : 'text-gray-600 dark:text-gray-400'}">
                    F1 = ${baseline.systemF1.toFixed(4)}
                  </span>
                </div>
                <div class="relative h-8 bg-gray-100 dark:bg-gray-700 rounded-lg overflow-hidden">
                  <div class="absolute inset-y-0 left-0 rounded-lg transition-all duration-1000 flex items-center justify-end pr-3
                    ${baseline.id === 'nesy-mbst' ? 'bg-gradient-to-r from-primary-500 to-primary-600' : 'bg-gray-300 dark:bg-gray-600'}"
                    style="width: ${(baseline.systemF1 * 100).toFixed(1)}%"
                    data-bar-width="${(baseline.systemF1 * 100).toFixed(1)}">
                    <span class="text-xs font-medium ${baseline.id === 'nesy-mbst' ? 'text-white' : 'text-gray-700 dark:text-gray-300'}">
                      ${(baseline.systemF1 * 100).toFixed(1)}%
                    </span>
                  </div>
                  <!-- Safety threshold line -->
                  <div class="absolute top-0 bottom-0 w-0.5 bg-red-500" style="left: 90%">
                    <span class="absolute -top-5 -translate-x-1/2 text-[9px] text-red-500 whitespace-nowrap">0.90 threshold</span>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>

      <!-- Detailed Metrics Table -->
      <div class="max-w-5xl mx-auto animate-on-scroll">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-6 text-center">
          Detailed Comparison
        </h3>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-700">
                <th class="text-left py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Metric</th>
                <th class="text-center py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">Pure Neural</th>
                <th class="text-center py-3 px-4 font-semibold text-gray-700 dark:text-gray-300">+ Symbolic</th>
                <th class="text-center py-3 px-4 font-semibold text-primary-700 dark:text-primary-300 bg-primary-50 dark:bg-primary-900/10 rounded-t-lg">NeSy-MBST</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
              <tr>
                <td class="py-3 px-4 text-gray-600 dark:text-gray-400">System F1</td>
                <td class="py-3 px-4 text-center font-mono text-gray-700 dark:text-gray-300">0.6559</td>
                <td class="py-3 px-4 text-center font-mono text-gray-700 dark:text-gray-300">0.9036</td>
                <td class="py-3 px-4 text-center font-mono font-bold text-primary-600 dark:text-primary-400 bg-primary-50/50 dark:bg-primary-900/5">0.9818</td>
              </tr>
              <tr>
                <td class="py-3 px-4 text-gray-600 dark:text-gray-400">Transition Coverage</td>
                <td class="py-3 px-4 text-center font-mono text-gray-700 dark:text-gray-300">50.0%</td>
                <td class="py-3 px-4 text-center font-mono text-gray-700 dark:text-gray-300">85.7%</td>
                <td class="py-3 px-4 text-center font-mono font-bold text-primary-600 dark:text-primary-400 bg-primary-50/50 dark:bg-primary-900/5">85.7%</td>
              </tr>
              <tr>
                <td class="py-3 px-4 text-gray-600 dark:text-gray-400">JSD</td>
                <td class="py-3 px-4 text-center font-mono text-gray-700 dark:text-gray-300">0.157</td>
                <td class="py-3 px-4 text-center font-mono text-gray-700 dark:text-gray-300">0.089</td>
                <td class="py-3 px-4 text-center font-mono font-bold text-primary-600 dark:text-primary-400 bg-primary-50/50 dark:bg-primary-900/5">0.012</td>
              </tr>
              <tr>
                <td class="py-3 px-4 text-gray-600 dark:text-gray-400">Frobenius Distance</td>
                <td class="py-3 px-4 text-center font-mono text-gray-700 dark:text-gray-300">0.234</td>
                <td class="py-3 px-4 text-center font-mono text-gray-700 dark:text-gray-300">0.145</td>
                <td class="py-3 px-4 text-center font-mono font-bold text-primary-600 dark:text-primary-400 bg-primary-50/50 dark:bg-primary-900/5">0.065</td>
              </tr>
              <tr>
                <td class="py-3 px-4 text-gray-600 dark:text-gray-400">Probability Accuracy</td>
                <td class="py-3 px-4 text-center text-gray-700 dark:text-gray-300">Poor</td>
                <td class="py-3 px-4 text-center text-gray-700 dark:text-gray-300">Moderate</td>
                <td class="py-3 px-4 text-center font-bold text-primary-600 dark:text-primary-400 bg-primary-50/50 dark:bg-primary-900/5">Near-perfect</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `;

  // Animate counters on scroll
  initCounterAnimations();
}

function initCounterAnimations() {
  const counters = document.querySelectorAll('.metric-value');
  
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );

  counters.forEach((counter) => observer.observe(counter));
}

function animateCounter(el) {
  const target = parseFloat(el.dataset.target);
  const decimals = parseInt(el.dataset.decimals) || 0;
  const prefix = el.dataset.prefix || '';
  const suffix = el.dataset.suffix || '';
  const duration = 2000;
  const start = performance.now();

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Easing: ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = target * eased;
    
    el.textContent = `${prefix}${current.toFixed(decimals)}${suffix}`;

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      el.textContent = `${prefix}${target.toFixed(decimals)}${suffix}`;
    }
  }

  requestAnimationFrame(update);
}
