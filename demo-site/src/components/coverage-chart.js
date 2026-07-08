/**
 * Coverage convergence chart - shows how coverage grows with number of test walks
 */
export function createCoverageChart(container) {
  const data = {
    walks: [],
    stateCoverage: [],
    transitionCoverage: [],
  };

  const width = 400;
  const height = 200;
  const margin = { top: 20, right: 20, bottom: 30, left: 40 };
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;

  container.innerHTML = `
    <div>
      <div class="flex items-center justify-between mb-2">
        <h5 class="text-xs font-semibold text-gray-700 dark:text-gray-300">Coverage Convergence</h5>
        <button id="coverage-clear" class="text-[10px] text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">Clear</button>
      </div>
      <svg id="coverage-svg" viewBox="0 0 ${width} ${height}" class="w-full" style="max-height: 200px;">
        <!-- Grid -->
        <g transform="translate(${margin.left}, ${margin.top})">
          <!-- Y axis grid lines -->
          ${[0, 25, 50, 75, 100].map(v => `
            <line x1="0" y1="${plotHeight - (v / 100) * plotHeight}" x2="${plotWidth}" y2="${plotHeight - (v / 100) * plotHeight}" 
              stroke="${v === 0 ? '#d1d5db' : '#f3f4f6'}" stroke-width="1" class="dark:stroke-gray-700"/>
            <text x="-5" y="${plotHeight - (v / 100) * plotHeight + 3}" text-anchor="end" 
              class="text-[9px] fill-gray-400">${v}%</text>
          `).join('')}
          
          <!-- Axes -->
          <line x1="0" y1="${plotHeight}" x2="${plotWidth}" y2="${plotHeight}" stroke="#d1d5db" stroke-width="1" class="dark:stroke-gray-600"/>
          <line x1="0" y1="0" x2="0" y2="${plotHeight}" stroke="#d1d5db" stroke-width="1" class="dark:stroke-gray-600"/>
          
          <!-- X axis label -->
          <text x="${plotWidth / 2}" y="${plotHeight + 25}" text-anchor="middle" class="text-[9px] fill-gray-500">Number of test walks</text>
          
          <!-- Lines will be drawn here -->
          <path id="state-coverage-line" fill="none" stroke="#3b82f6" stroke-width="2"/>
          <path id="transition-coverage-line" fill="none" stroke="#22c55e" stroke-width="2"/>
        </g>
      </svg>
      <div class="flex justify-center gap-4 mt-1">
        <div class="flex items-center gap-1.5 text-[10px]">
          <div class="w-3 h-0.5 bg-blue-500"></div>
          <span class="text-gray-500 dark:text-gray-400">State Coverage</span>
        </div>
        <div class="flex items-center gap-1.5 text-[10px]">
          <div class="w-3 h-0.5 bg-green-500"></div>
          <span class="text-gray-500 dark:text-gray-400">Transition Coverage</span>
        </div>
      </div>
    </div>
  `;

  const stateLine = container.querySelector('#state-coverage-line');
  const transLine = container.querySelector('#transition-coverage-line');
  const clearBtn = container.querySelector('#coverage-clear');

  clearBtn.addEventListener('click', () => {
    data.walks = [];
    data.stateCoverage = [];
    data.transitionCoverage = [];
    updateChart();
  });

  function updateChart() {
    if (data.walks.length === 0) {
      stateLine.setAttribute('d', '');
      transLine.setAttribute('d', '');
      return;
    }

    const maxWalks = Math.max(data.walks.length, 5);
    const xScale = (i) => (i / maxWalks) * plotWidth;
    const yScale = (v) => plotHeight - (v * plotHeight);

    // Build path for state coverage
    const statePathData = data.stateCoverage.map((v, i) => 
      `${i === 0 ? 'M' : 'L'} ${xScale(i + 1)} ${yScale(v)}`
    ).join(' ');

    const transPathData = data.transitionCoverage.map((v, i) => 
      `${i === 0 ? 'M' : 'L'} ${xScale(i + 1)} ${yScale(v)}`
    ).join(' ');

    stateLine.setAttribute('d', statePathData);
    transLine.setAttribute('d', transPathData);
  }

  return {
    addDataPoint(stateCov, transCov) {
      data.walks.push(data.walks.length + 1);
      data.stateCoverage.push(stateCov);
      data.transitionCoverage.push(transCov);
      updateChart();
    },
    clear() {
      data.walks = [];
      data.stateCoverage = [];
      data.transitionCoverage = [];
      updateChart();
    }
  };
}
