/**
 * Generates a random walk through the state graph based on transition probabilities.
 * If no matrix is provided, uses uniform random selection among valid transitions.
 */
export function generateRandomWalk(data, maxSteps = 15) {
  const { states, transitions, transitionMatrix, startState } = data;
  const path = [startState];
  let current = startState;

  for (let step = 0; step < maxSteps; step++) {
    // Find valid transitions from current state
    const validTransitions = transitions.filter(([src]) => src === current);
    
    if (validTransitions.length === 0) break;

    let next;
    
    if (transitionMatrix) {
      // Use transition probabilities
      const currentIdx = states.indexOf(current);
      const probs = [];
      const targets = [];
      
      for (const [, target] of validTransitions) {
        const targetIdx = states.indexOf(target);
        const prob = transitionMatrix[currentIdx][targetIdx];
        if (prob > 0) {
          probs.push(prob);
          targets.push(target);
        }
      }

      if (targets.length === 0) break;

      // Weighted random selection
      const totalProb = probs.reduce((a, b) => a + b, 0);
      let rand = Math.random() * totalProb;
      let selected = 0;
      for (let i = 0; i < probs.length; i++) {
        rand -= probs[i];
        if (rand <= 0) {
          selected = i;
          break;
        }
      }
      next = targets[selected];
    } else {
      // Uniform random
      const idx = Math.floor(Math.random() * validTransitions.length);
      next = validTransitions[idx][1];
    }

    path.push(next);
    current = next;

    // Stop if we hit a terminal state
    if (data.terminalStates?.includes(current)) break;
  }

  return path;
}

/**
 * Computes coverage metrics for a set of walks
 */
export function computeCoverage(data, walks) {
  const coveredStates = new Set();
  const coveredTransitions = new Set();

  walks.forEach((walk) => {
    walk.forEach((state) => coveredStates.add(state));
    for (let i = 0; i < walk.length - 1; i++) {
      coveredTransitions.add(`${walk[i]}->${walk[i + 1]}`);
    }
  });

  const totalStates = data.states.length;
  const totalTransitions = data.transitions.length;

  return {
    stateCoverage: coveredStates.size / totalStates,
    transitionCoverage: coveredTransitions.size / totalTransitions,
    coveredStates: coveredStates.size,
    totalStates,
    coveredTransitions: coveredTransitions.size,
    totalTransitions,
  };
}

/**
 * Creates the random walk control panel
 */
export function createWalkController(container, graph, data, coverageChart = null) {
  container.innerHTML = `
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h4 class="text-sm font-semibold text-gray-900 dark:text-white">Test Walk Generator</h4>
        <div class="flex gap-2">
          <button id="walk-generate" class="btn-primary text-xs px-3 py-1.5">
            Generate Walk
          </button>
          <button id="walk-reset" class="btn-secondary text-xs px-3 py-1.5">
            Reset
          </button>
        </div>
      </div>

      <!-- Walk display -->
      <div id="walk-path" class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg min-h-[60px] font-mono text-xs text-gray-600 dark:text-gray-400">
        <span class="text-gray-400 italic">Click "Generate Walk" to simulate a test sequence...</span>
      </div>

      <!-- Coverage meters -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <div class="flex justify-between text-xs mb-1">
            <span class="text-gray-600 dark:text-gray-400">State Coverage</span>
            <span id="state-coverage-pct" class="font-medium text-gray-900 dark:text-white">0%</span>
          </div>
          <div class="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div id="state-coverage-bar" class="h-full bg-blue-500 rounded-full transition-all duration-500" style="width: 0%"></div>
          </div>
        </div>
        <div>
          <div class="flex justify-between text-xs mb-1">
            <span class="text-gray-600 dark:text-gray-400">Transition Coverage</span>
            <span id="transition-coverage-pct" class="font-medium text-gray-900 dark:text-white">0%</span>
          </div>
          <div class="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div id="transition-coverage-bar" class="h-full bg-green-500 rounded-full transition-all duration-500" style="width: 0%"></div>
          </div>
        </div>
      </div>

      <!-- Walk counter -->
      <div class="text-xs text-gray-500 dark:text-gray-400 text-center">
        <span id="walk-count">0</span> walks generated
      </div>
    </div>
  `;

  let walks = [];
  let isAnimating = false;

  const generateBtn = container.querySelector('#walk-generate');
  const resetBtn = container.querySelector('#walk-reset');
  const pathDisplay = container.querySelector('#walk-path');
  const stateCoverageBar = container.querySelector('#state-coverage-bar');
  const stateCoveragePct = container.querySelector('#state-coverage-pct');
  const transitionCoverageBar = container.querySelector('#transition-coverage-bar');
  const transitionCoveragePct = container.querySelector('#transition-coverage-pct');
  const walkCount = container.querySelector('#walk-count');

  generateBtn.addEventListener('click', async () => {
    if (isAnimating) return;
    isAnimating = true;
    generateBtn.disabled = true;
    generateBtn.classList.add('opacity-50');

    const walk = generateRandomWalk(data);
    walks.push(walk);

    // Display path
    pathDisplay.innerHTML = walk.map((state, i) => 
      `<span class="inline-block ${i === 0 ? 'text-blue-600 dark:text-blue-400 font-bold' : ''}">${state}</span>${i < walk.length - 1 ? '<span class="text-gray-400 mx-1">→</span>' : ''}`
    ).join('');

    // Animate walk on graph
    graph.reset();
    await graph.animateWalk(walk, 400);

    // Update coverage
    const coverage = computeCoverage(data, walks);
    const stPct = (coverage.stateCoverage * 100).toFixed(1);
    const trPct = (coverage.transitionCoverage * 100).toFixed(1);
    
    stateCoverageBar.style.width = `${stPct}%`;
    stateCoveragePct.textContent = `${stPct}%`;
    transitionCoverageBar.style.width = `${trPct}%`;
    transitionCoveragePct.textContent = `${trPct}%`;
    walkCount.textContent = walks.length;

    // Feed coverage chart
    if (coverageChart) {
      coverageChart.addDataPoint(coverage.stateCoverage, coverage.transitionCoverage);
    }

    isAnimating = false;
    generateBtn.disabled = false;
    generateBtn.classList.remove('opacity-50');
  });

  resetBtn.addEventListener('click', () => {
    walks = [];
    graph.reset();
    pathDisplay.innerHTML = '<span class="text-gray-400 italic">Click "Generate Walk" to simulate a test sequence...</span>';
    stateCoverageBar.style.width = '0%';
    stateCoveragePct.textContent = '0%';
    transitionCoverageBar.style.width = '0%';
    transitionCoveragePct.textContent = '0%';
    walkCount.textContent = '0';
    if (coverageChart) coverageChart.clear();
  });
}
