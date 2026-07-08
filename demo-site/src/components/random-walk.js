/**
 * Generates a random walk through the state graph based on transition probabilities.
 */
export function generateRandomWalk(data, maxSteps = 15) {
  const { states, transitions, transitionMatrix, startState } = data;
  const path = [startState];
  let current = startState;

  for (let step = 0; step < maxSteps; step++) {
    const validTransitions = transitions.filter(([src]) => src === current);
    if (validTransitions.length === 0) break;

    let next;
    if (transitionMatrix) {
      const currentIdx = states.indexOf(current);
      const probs = [];
      const targets = [];
      for (const [, target] of validTransitions) {
        const targetIdx = states.indexOf(target);
        const prob = transitionMatrix[currentIdx][targetIdx];
        if (prob > 0) { probs.push(prob); targets.push(target); }
      }
      if (targets.length === 0) break;
      const total = probs.reduce((a, b) => a + b, 0);
      let rand = Math.random() * total;
      let sel = 0;
      for (let i = 0; i < probs.length; i++) { rand -= probs[i]; if (rand <= 0) { sel = i; break; } }
      next = targets[sel];
    } else {
      next = validTransitions[Math.floor(Math.random() * validTransitions.length)][1];
    }

    path.push(next);
    current = next;
    if (data.terminalStates?.includes(current)) break;
  }
  return path;
}

export function computeCoverage(data, walks) {
  const coveredStates = new Set();
  const coveredTransitions = new Set();
  walks.forEach((walk) => {
    walk.forEach((s) => coveredStates.add(s));
    for (let i = 0; i < walk.length - 1; i++) coveredTransitions.add(`${walk[i]}->${walk[i + 1]}`);
  });
  return {
    stateCoverage: coveredStates.size / data.states.length,
    transitionCoverage: coveredTransitions.size / data.transitions.length,
    coveredStates: coveredStates.size,
    totalStates: data.states.length,
    coveredTransitions: coveredTransitions.size,
    totalTransitions: data.transitions.length,
  };
}

export function createWalkController(container, graph, data, coverageChart = null) {
  container.innerHTML = `
    <div class="space-y-3">
      <div class="flex items-center justify-between">
        <div class="text-sm font-semibold text-gray-900 dark:text-white">Test Walks</div>
        <div class="flex gap-2">
          <button id="walk-generate" class="btn-primary text-xs px-3 py-1.5">Generate</button>
          <button id="walk-reset" class="btn-ghost text-xs px-3 py-1.5">Reset</button>
        </div>
      </div>
      <div id="walk-path" class="p-2.5 bg-gray-50 dark:bg-gray-950 rounded-lg min-h-[48px] font-mono text-[11px] text-gray-500 leading-relaxed">
        Click "Generate" to simulate a test sequence...
      </div>
      <div class="grid grid-cols-2 gap-3">
        <div>
          <div class="flex justify-between text-[11px] mb-1">
            <span class="text-gray-500">States</span>
            <span id="state-coverage-pct" class="font-medium text-gray-700 dark:text-gray-300">0%</span>
          </div>
          <div class="h-1.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
            <div id="state-coverage-bar" class="h-full bg-blue-500 rounded-full transition-all duration-400" style="width: 0%"></div>
          </div>
        </div>
        <div>
          <div class="flex justify-between text-[11px] mb-1">
            <span class="text-gray-500">Transitions</span>
            <span id="transition-coverage-pct" class="font-medium text-gray-700 dark:text-gray-300">0%</span>
          </div>
          <div class="h-1.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
            <div id="transition-coverage-bar" class="h-full bg-emerald-500 rounded-full transition-all duration-400" style="width: 0%"></div>
          </div>
        </div>
      </div>
      <div class="text-[10px] text-gray-400 text-center"><span id="walk-count">0</span> walks</div>
    </div>
  `;

  let walks = [];
  let isAnimating = false;
  const generateBtn = container.querySelector('#walk-generate');
  const resetBtn = container.querySelector('#walk-reset');
  const pathDisplay = container.querySelector('#walk-path');

  generateBtn.addEventListener('click', async () => {
    if (isAnimating) return;
    isAnimating = true;
    generateBtn.classList.add('opacity-50');

    const walk = generateRandomWalk(data);
    walks.push(walk);

    pathDisplay.innerHTML = walk.map((s, i) =>
      `<span class="${i === 0 ? 'text-blue-600 dark:text-blue-400 font-semibold' : ''}">${s}</span>${i < walk.length - 1 ? ' <span class="text-gray-300 dark:text-gray-600">&#8594;</span> ' : ''}`
    ).join('');

    graph.reset();
    await graph.animateWalk(walk, 350);

    const cov = computeCoverage(data, walks);
    const sp = (cov.stateCoverage * 100).toFixed(0);
    const tp = (cov.transitionCoverage * 100).toFixed(0);
    container.querySelector('#state-coverage-bar').style.width = `${sp}%`;
    container.querySelector('#state-coverage-pct').textContent = `${sp}%`;
    container.querySelector('#transition-coverage-bar').style.width = `${tp}%`;
    container.querySelector('#transition-coverage-pct').textContent = `${tp}%`;
    container.querySelector('#walk-count').textContent = walks.length;

    if (coverageChart) coverageChart.addDataPoint(cov.stateCoverage, cov.transitionCoverage);

    isAnimating = false;
    generateBtn.classList.remove('opacity-50');
  });

  resetBtn.addEventListener('click', () => {
    walks = [];
    graph.reset();
    pathDisplay.textContent = 'Click "Generate" to simulate a test sequence...';
    container.querySelector('#state-coverage-bar').style.width = '0%';
    container.querySelector('#state-coverage-pct').textContent = '0%';
    container.querySelector('#transition-coverage-bar').style.width = '0%';
    container.querySelector('#transition-coverage-pct').textContent = '0%';
    container.querySelector('#walk-count').textContent = '0';
    if (coverageChart) coverageChart.clear();
  });
}
