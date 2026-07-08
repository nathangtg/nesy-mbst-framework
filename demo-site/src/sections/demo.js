import { createStateGraph } from '../components/state-graph.js';
import { createHeatmap } from '../components/heatmap.js';
import { createWalkController } from '../components/random-walk.js';
import { createCoverageChart } from '../components/coverage-chart.js';
import avData from '../data/av-benchmark.json';
import ecommerceUserData from '../data/ecommerce-user.json';
import ecommerceAdminData from '../data/ecommerce-admin.json';

const scenarios = {
  av: { data: avData, label: 'Autonomous Vehicle' },
  'ecom-user': { data: ecommerceUserData, label: 'E-Commerce User' },
  'ecom-admin': { data: ecommerceAdminData, label: 'E-Commerce Admin' },
};

let currentGraph = null;

export function renderDemo() {
  const section = document.getElementById('demo');
  section.innerHTML = `
    <div class="section border-t border-gray-100 dark:border-gray-800/50">
      <div class="section-header animate-on-scroll">
        <h2 class="section-title">Interactive Demo</h2>
        <p class="section-desc">
          Explore generated Markov models. Drag nodes, generate test walks, inspect probabilities.
        </p>
      </div>

      <!-- Scenario selector -->
      <div class="flex gap-2 mb-6 animate-on-scroll">
        <button class="scenario-btn active" data-scenario="av">AV (9 states)</button>
        <button class="scenario-btn" data-scenario="ecom-user">E-Commerce User (24)</button>
        <button class="scenario-btn" data-scenario="ecom-admin">E-Commerce Admin (17)</button>
      </div>

      <!-- Requirements -->
      <div class="card mb-6 animate-on-scroll">
        <div class="text-xs font-medium text-gray-400 dark:text-gray-500 uppercase tracking-wide mb-2">Requirements</div>
        <p id="demo-requirements" class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed"></p>
      </div>

      <!-- Main demo grid -->
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-4 animate-on-scroll">
        <!-- Graph (larger) -->
        <div class="lg:col-span-3 card">
          <div class="flex items-center justify-between mb-3">
            <div class="text-sm font-semibold text-gray-900 dark:text-white">State Graph</div>
            <div class="text-[11px] text-gray-400">Drag nodes to rearrange</div>
          </div>
          <div id="graph-container" class="w-full" style="min-height: 380px;"></div>
        </div>

        <!-- Right column -->
        <div class="lg:col-span-2 space-y-4">
          <!-- Walk controller -->
          <div class="card">
            <div id="walk-controller"></div>
          </div>

          <!-- Coverage chart -->
          <div class="card">
            <div id="coverage-chart-container"></div>
          </div>
        </div>
      </div>

      <!-- Heatmap + Constraints row -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mt-4 animate-on-scroll">
        <div class="lg:col-span-2 card">
          <div class="text-sm font-semibold text-gray-900 dark:text-white mb-3">Transition Matrix</div>
          <div id="heatmap-container" class="w-full overflow-x-auto"></div>
        </div>
        <div class="card">
          <div class="text-sm font-semibold text-gray-900 dark:text-white mb-3">Constraints</div>
          <div id="constraints-list" class="space-y-2"></div>
        </div>
      </div>
    </div>
  `;

  initScenarioSwitcher();
  loadScenario('av');
}

function initScenarioSwitcher() {
  const buttons = document.querySelectorAll('.scenario-btn');
  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      buttons.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      loadScenario(btn.dataset.scenario);
    });
  });
}

function loadScenario(scenarioId) {
  const { data } = scenarios[scenarioId];

  document.getElementById('demo-requirements').textContent = data.requirements;

  // Constraints
  const constraintsList = document.getElementById('constraints-list');
  if (data.constraints) {
    constraintsList.innerHTML = data.constraints.map((c) => `
      <div class="p-2 bg-violet-50 dark:bg-violet-950/30 rounded-md">
        <code class="text-[11px] text-violet-700 dark:text-violet-300 font-mono break-all">${c}</code>
      </div>
    `).join('');
  }

  // Graph
  if (currentGraph) currentGraph.destroy();
  const graphContainer = document.getElementById('graph-container');
  currentGraph = createStateGraph(graphContainer, data, { width: 600, height: 380 });

  // Coverage chart
  const coverageChartContainer = document.getElementById('coverage-chart-container');
  const coverageChart = createCoverageChart(coverageChartContainer);

  // Heatmap
  const heatmapContainer = document.getElementById('heatmap-container');
  createHeatmap(heatmapContainer, data);

  // Walk controller
  const walkController = document.getElementById('walk-controller');
  createWalkController(walkController, currentGraph, data, coverageChart);
}
