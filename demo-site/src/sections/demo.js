import { createStateGraph } from '../components/state-graph.js';
import { createHeatmap } from '../components/heatmap.js';
import { createWalkController } from '../components/random-walk.js';
import { createCoverageChart } from '../components/coverage-chart.js';
import avData from '../data/av-benchmark.json';
import ecommerceUserData from '../data/ecommerce-user.json';
import ecommerceAdminData from '../data/ecommerce-admin.json';

const scenarios = {
  av: { data: avData, label: 'Autonomous Vehicle' },
  'ecom-user': { data: ecommerceUserData, label: 'E-Commerce (User)' },
  'ecom-admin': { data: ecommerceAdminData, label: 'E-Commerce (Admin)' },
};

let currentGraph = null;
let currentScenario = 'av';

export function renderDemo() {
  const section = document.getElementById('demo');
  section.innerHTML = `
    <div class="section-container">
      <div class="text-center mb-12 animate-on-scroll">
        <h2 class="section-title">Interactive Demo</h2>
        <p class="section-subtitle mx-auto">
          Explore the generated Markov usage models. Drag nodes, generate random walks, and inspect transition probabilities.
        </p>
      </div>

      <!-- Scenario Selector -->
      <div class="flex flex-wrap justify-center gap-3 mb-8 animate-on-scroll">
        <button class="scenario-btn active" data-scenario="av">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
          </svg>
          Autonomous Vehicle
          <span class="ml-2 text-xs opacity-60">9 states</span>
        </button>
        <button class="scenario-btn" data-scenario="ecom-user">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/>
          </svg>
          E-Commerce (User)
          <span class="ml-2 text-xs opacity-60">24 states</span>
        </button>
        <button class="scenario-btn" data-scenario="ecom-admin">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
          E-Commerce (Admin)
          <span class="ml-2 text-xs opacity-60">17 states</span>
        </button>
      </div>

      <!-- Requirements Display -->
      <div class="max-w-4xl mx-auto mb-8 animate-on-scroll">
        <div class="card">
          <div class="flex items-center gap-2 mb-3">
            <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300">Natural Language Requirements</h4>
          </div>
          <p id="demo-requirements" class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed"></p>
        </div>
      </div>

      <!-- Main Demo Area -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-7xl mx-auto animate-on-scroll">
        <!-- Left: State Graph -->
        <div class="card">
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-sm font-semibold text-gray-900 dark:text-white">State Machine Graph</h4>
            <div class="flex items-center gap-2">
              <span class="text-xs text-gray-500">Drag nodes to rearrange</span>
            </div>
          </div>
          <div id="graph-container" class="relative w-full" style="min-height: 400px;"></div>
          
          <!-- Legend -->
          <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <div class="flex flex-wrap gap-3 text-xs">
              <div class="flex items-center gap-1.5">
                <div class="w-3 h-3 rounded-full bg-gray-500 border-2 border-gray-900"></div>
                <span class="text-gray-600 dark:text-gray-400">Start</span>
              </div>
              <div class="flex items-center gap-1.5">
                <div class="w-3 h-3 rounded-full bg-gray-500 border-2 border-red-600"></div>
                <span class="text-gray-600 dark:text-gray-400">Terminal</span>
              </div>
              <div class="flex items-center gap-1.5">
                <div class="w-3 h-3 rounded-full bg-blue-500"></div>
                <span class="text-gray-600 dark:text-gray-400">Neural</span>
              </div>
              <div class="flex items-center gap-1.5">
                <div class="w-3 h-3 rounded-full bg-green-500"></div>
                <span class="text-gray-600 dark:text-gray-400">Symbolic</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Controls & Heatmap -->
        <div class="space-y-6">
          <!-- Walk Controller -->
          <div class="card">
            <div id="walk-controller"></div>
          </div>

          <!-- Coverage Chart -->
          <div class="card">
            <div id="coverage-chart-container"></div>
          </div>

          <!-- Heatmap -->
          <div class="card">
            <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-4">Transition Probability Matrix</h4>
            <div id="heatmap-container" class="w-full overflow-x-auto"></div>
          </div>
        </div>
      </div>

      <!-- Constraints Display -->
      <div class="max-w-4xl mx-auto mt-8 animate-on-scroll">
        <div class="card">
          <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-3">Extracted Constraints</h4>
          <div id="constraints-list" class="space-y-2"></div>
        </div>
      </div>
    </div>

    <style>
      .scenario-btn {
        @apply inline-flex items-center px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 border;
        @apply bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border-gray-200 dark:border-gray-700;
        @apply hover:bg-gray-50 dark:hover:bg-gray-700 hover:border-gray-300 dark:hover:border-gray-600;
      }
      .scenario-btn.active {
        @apply bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 border-primary-300 dark:border-primary-700;
      }
    </style>
  `;

  // Initialize
  initScenarioSwitcher();
  loadScenario('av');
}

function initScenarioSwitcher() {
  const buttons = document.querySelectorAll('.scenario-btn');
  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      buttons.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const scenario = btn.dataset.scenario;
      loadScenario(scenario);
    });
  });
}

function loadScenario(scenarioId) {
  currentScenario = scenarioId;
  const { data } = scenarios[scenarioId];

  // Update requirements
  document.getElementById('demo-requirements').textContent = data.requirements;

  // Update constraints
  const constraintsList = document.getElementById('constraints-list');
  if (data.constraints) {
    constraintsList.innerHTML = data.constraints.map((c) => `
      <div class="flex items-center gap-2 p-2 bg-purple-50 dark:bg-purple-900/10 rounded-lg">
        <svg class="w-4 h-4 text-purple-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"/>
        </svg>
        <code class="text-xs text-purple-700 dark:text-purple-300 font-mono">${c}</code>
      </div>
    `).join('');
  }

  // Destroy previous graph
  if (currentGraph) {
    currentGraph.destroy();
  }

  // Create state graph
  const graphContainer = document.getElementById('graph-container');
  currentGraph = createStateGraph(graphContainer, data, {
    width: 650,
    height: 400,
  });

  // Create coverage chart
  const coverageChartContainer = document.getElementById('coverage-chart-container');
  const coverageChart = createCoverageChart(coverageChartContainer);

  // Create heatmap
  const heatmapContainer = document.getElementById('heatmap-container');
  createHeatmap(heatmapContainer, data);

  // Create walk controller
  const walkController = document.getElementById('walk-controller');
  createWalkController(walkController, currentGraph, data, coverageChart);
}
