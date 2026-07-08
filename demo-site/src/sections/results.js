import ablationData from '../data/ablation.json';

export function renderResults() {
  const section = document.getElementById('results');
  section.innerHTML = `
    <div class="section border-t border-gray-100 dark:border-gray-800/50">
      <div class="section-header animate-on-scroll">
        <h2 class="section-title">Results</h2>
        <p class="section-desc">
          Evaluated on autonomous vehicle (9 states) and e-commerce platforms (24 and 42 states).
        </p>
      </div>

      <!-- Metrics row -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12 animate-on-scroll">
        <div class="metric-card card">
          <div class="metric-value" data-target="0.91" data-decimals="2">0</div>
          <div class="metric-label">System F1</div>
        </div>
        <div class="metric-card card">
          <div class="metric-value" data-target="85.7" data-decimals="1" data-suffix="%">0</div>
          <div class="metric-label">Coverage</div>
        </div>
        <div class="metric-card card">
          <div class="metric-value" data-target="0.012" data-decimals="3">0</div>
          <div class="metric-label">JSD</div>
        </div>
        <div class="metric-card card">
          <div class="metric-value" data-target="6" data-decimals="0" data-prefix="<" data-suffix="min">0</div>
          <div class="metric-label">Time</div>
        </div>
      </div>

      <!-- Comparison bars -->
      <div class="card mb-8 animate-on-scroll">
        <div class="text-sm font-semibold text-gray-900 dark:text-white mb-5">Baseline Comparison (System F1)</div>
        <div class="space-y-4">
          ${ablationData.baselines.map((b) => `
            <div>
              <div class="flex justify-between text-xs mb-1.5">
                <span class="font-medium text-gray-700 dark:text-gray-300">${b.label}</span>
                <span class="font-mono text-gray-500">${b.systemF1.toFixed(4)}</span>
              </div>
              <div class="h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden relative">
                <div class="h-full rounded-full transition-all duration-700 ${b.id === 'nesy-mbst' ? 'bg-gray-900 dark:bg-white' : 'bg-gray-300 dark:bg-gray-600'}" 
                  style="width: ${(b.systemF1 * 100).toFixed(1)}%"></div>
                <div class="absolute top-0 bottom-0 w-px bg-red-400" style="left: 90%" title="0.90 safety threshold"></div>
              </div>
            </div>
          `).join('')}
          <div class="text-[10px] text-gray-400 text-right mt-1">Red line = 0.90 safety-critical threshold</div>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto animate-on-scroll">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200 dark:border-gray-800">
              <th class="text-left py-2.5 px-3 text-xs font-medium text-gray-500 uppercase tracking-wide">Metric</th>
              <th class="text-center py-2.5 px-3 text-xs font-medium text-gray-500 uppercase tracking-wide">Pure Neural</th>
              <th class="text-center py-2.5 px-3 text-xs font-medium text-gray-500 uppercase tracking-wide">+ Symbolic</th>
              <th class="text-center py-2.5 px-3 text-xs font-medium text-gray-900 dark:text-white uppercase tracking-wide">NeSy-MBST</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-800/50">
            <tr>
              <td class="py-2.5 px-3 text-gray-600 dark:text-gray-400">System F1</td>
              <td class="py-2.5 px-3 text-center font-mono text-gray-500">0.6559</td>
              <td class="py-2.5 px-3 text-center font-mono text-gray-500">0.9036</td>
              <td class="py-2.5 px-3 text-center font-mono font-semibold text-gray-900 dark:text-white">0.9818</td>
            </tr>
            <tr>
              <td class="py-2.5 px-3 text-gray-600 dark:text-gray-400">Coverage</td>
              <td class="py-2.5 px-3 text-center font-mono text-gray-500">50.0%</td>
              <td class="py-2.5 px-3 text-center font-mono text-gray-500">85.7%</td>
              <td class="py-2.5 px-3 text-center font-mono font-semibold text-gray-900 dark:text-white">85.7%</td>
            </tr>
            <tr>
              <td class="py-2.5 px-3 text-gray-600 dark:text-gray-400">JSD</td>
              <td class="py-2.5 px-3 text-center font-mono text-gray-500">0.157</td>
              <td class="py-2.5 px-3 text-center font-mono text-gray-500">0.089</td>
              <td class="py-2.5 px-3 text-center font-mono font-semibold text-gray-900 dark:text-white">0.012</td>
            </tr>
            <tr>
              <td class="py-2.5 px-3 text-gray-600 dark:text-gray-400">Frobenius</td>
              <td class="py-2.5 px-3 text-center font-mono text-gray-500">0.234</td>
              <td class="py-2.5 px-3 text-center font-mono text-gray-500">0.145</td>
              <td class="py-2.5 px-3 text-center font-mono font-semibold text-gray-900 dark:text-white">0.065</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `;

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
  counters.forEach((c) => observer.observe(c));
}

function animateCounter(el) {
  const target = parseFloat(el.dataset.target);
  const decimals = parseInt(el.dataset.decimals) || 0;
  const prefix = el.dataset.prefix || '';
  const suffix = el.dataset.suffix || '';
  const duration = 1500;
  const start = performance.now();

  function update(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = target * eased;
    el.textContent = `${prefix}${current.toFixed(decimals)}${suffix}`;
    if (progress < 1) requestAnimationFrame(update);
    else el.textContent = `${prefix}${target.toFixed(decimals)}${suffix}`;
  }
  requestAnimationFrame(update);
}
