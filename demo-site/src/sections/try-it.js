import { createStateGraph } from '../components/state-graph.js';
import templates from '../data/templates.json';

let currentTemplate = null;
let tryGraph = null;

export function renderTryIt() {
  const section = document.getElementById('try-it');
  section.innerHTML = `
    <div class="section-container">
      <div class="text-center mb-16 animate-on-scroll">
        <h2 class="section-title">Try It Yourself</h2>
        <p class="section-subtitle mx-auto">
          Select a template, modify the requirements, and watch the pipeline build a model.
        </p>
      </div>

      <div class="max-w-6xl mx-auto animate-on-scroll">
        <!-- Template Selector -->
        <div class="flex flex-wrap justify-center gap-3 mb-8">
          ${templates.templates.map((t, i) => `
            <button class="template-btn ${i === 0 ? 'active' : ''}" data-template="${t.id}">
              ${t.name}
            </button>
          `).join('')}
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Left: Input -->
          <div class="space-y-4">
            <div class="card">
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-3">Requirements Input</h4>
              <textarea id="try-requirements" rows="8" 
                class="w-full p-3 border border-gray-200 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-900 text-sm text-gray-700 dark:text-gray-300 font-mono resize-y focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Enter your requirements here..."></textarea>
              <div class="mt-3 flex items-center gap-3">
                <button id="try-build" class="btn-primary">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                  Build Model
                </button>
                <span class="text-xs text-gray-500 dark:text-gray-400">Uses pre-computed results for templates</span>
              </div>
            </div>

            <!-- Pipeline Progress -->
            <div id="try-pipeline" class="card hidden">
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-4">Pipeline Progress</h4>
              <div class="space-y-3">
                <div class="pipeline-step" data-step="extract">
                  <div class="flex items-center gap-3">
                    <div class="w-6 h-6 rounded-full border-2 border-gray-300 dark:border-gray-600 flex items-center justify-center" id="step-icon-extract">
                      <span class="text-xs text-gray-400">1</span>
                    </div>
                    <span class="text-sm text-gray-600 dark:text-gray-400">Extracting states and transitions...</span>
                  </div>
                </div>
                <div class="pipeline-step" data-step="verify">
                  <div class="flex items-center gap-3">
                    <div class="w-6 h-6 rounded-full border-2 border-gray-300 dark:border-gray-600 flex items-center justify-center" id="step-icon-verify">
                      <span class="text-xs text-gray-400">2</span>
                    </div>
                    <span class="text-sm text-gray-600 dark:text-gray-400">Symbolic feasibility checking...</span>
                  </div>
                </div>
                <div class="pipeline-step" data-step="optimize">
                  <div class="flex items-center gap-3">
                    <div class="w-6 h-6 rounded-full border-2 border-gray-300 dark:border-gray-600 flex items-center justify-center" id="step-icon-optimize">
                      <span class="text-xs text-gray-400">3</span>
                    </div>
                    <span class="text-sm text-gray-600 dark:text-gray-400">Optimizing transition probabilities...</span>
                  </div>
                </div>
                <div class="pipeline-step" data-step="generate">
                  <div class="flex items-center gap-3">
                    <div class="w-6 h-6 rounded-full border-2 border-gray-300 dark:border-gray-600 flex items-center justify-center" id="step-icon-generate">
                      <span class="text-xs text-gray-400">4</span>
                    </div>
                    <span class="text-sm text-gray-600 dark:text-gray-400">Generating test sequences...</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Extracted Info -->
            <div id="try-info" class="card hidden">
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-3">Extracted Model</h4>
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span class="text-gray-500 dark:text-gray-400">States:</span>
                  <span id="try-state-count" class="font-bold text-gray-900 dark:text-white ml-1"></span>
                </div>
                <div>
                  <span class="text-gray-500 dark:text-gray-400">Transitions:</span>
                  <span id="try-transition-count" class="font-bold text-gray-900 dark:text-white ml-1"></span>
                </div>
              </div>
              <div class="mt-3">
                <span class="text-xs text-gray-500 dark:text-gray-400">Constraints:</span>
                <div id="try-constraints" class="mt-1 space-y-1"></div>
              </div>
            </div>
          </div>

          <!-- Right: Output Graph -->
          <div class="card">
            <h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-4">Generated State Graph</h4>
            <div id="try-graph-container" class="w-full relative" style="min-height: 400px;">
              <div class="absolute inset-0 flex items-center justify-center text-gray-400 dark:text-gray-600">
                <div class="text-center">
                  <svg class="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"/>
                  </svg>
                  <p class="text-sm">Select a template and click "Build Model"</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <style>
      .template-btn {
        @apply px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 border;
        @apply bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border-gray-200 dark:border-gray-700;
        @apply hover:bg-gray-50 dark:hover:bg-gray-700;
      }
      .template-btn.active {
        @apply bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 border-primary-300 dark:border-primary-700;
      }
    </style>
  `;

  initTryIt();
}

function initTryIt() {
  const textarea = document.getElementById('try-requirements');
  const buildBtn = document.getElementById('try-build');
  const templateBtns = document.querySelectorAll('.template-btn');

  // Load first template
  loadTemplate(templates.templates[0].id);

  // Template switching
  templateBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      templateBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      loadTemplate(btn.dataset.template);
    });
  });

  // Build button
  buildBtn.addEventListener('click', () => {
    if (!currentTemplate) return;
    runPipeline();
  });
}

function loadTemplate(templateId) {
  const template = templates.templates.find((t) => t.id === templateId);
  if (!template) return;
  
  currentTemplate = template;
  document.getElementById('try-requirements').value = template.requirements;
  
  // Hide previous results
  document.getElementById('try-pipeline').classList.add('hidden');
  document.getElementById('try-info').classList.add('hidden');
}

async function runPipeline() {
  const pipelineEl = document.getElementById('try-pipeline');
  const infoEl = document.getElementById('try-info');
  
  pipelineEl.classList.remove('hidden');
  infoEl.classList.add('hidden');

  const steps = ['extract', 'verify', 'optimize', 'generate'];
  
  // Reset all steps
  steps.forEach((step) => {
    const icon = document.getElementById(`step-icon-${step}`);
    icon.innerHTML = '<span class="text-xs text-gray-400">' + (steps.indexOf(step) + 1) + '</span>';
    icon.className = 'w-6 h-6 rounded-full border-2 border-gray-300 dark:border-gray-600 flex items-center justify-center';
  });

  // Animate through steps
  for (let i = 0; i < steps.length; i++) {
    const step = steps[i];
    const icon = document.getElementById(`step-icon-${step}`);
    
    // Mark as in-progress
    icon.className = 'w-6 h-6 rounded-full border-2 border-blue-500 flex items-center justify-center animate-pulse';
    icon.innerHTML = '<svg class="w-3 h-3 text-blue-500 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>';
    
    await sleep(600 + Math.random() * 400);
    
    // Mark as complete
    icon.className = 'w-6 h-6 rounded-full bg-green-500 flex items-center justify-center';
    icon.innerHTML = '<svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>';
  }

  // Show results
  await sleep(300);
  showResults();
}

function showResults() {
  const infoEl = document.getElementById('try-info');
  infoEl.classList.remove('hidden');

  document.getElementById('try-state-count').textContent = currentTemplate.states.length;
  document.getElementById('try-transition-count').textContent = currentTemplate.transitions.length;

  // Show constraints
  const constraintsEl = document.getElementById('try-constraints');
  constraintsEl.innerHTML = currentTemplate.constraints.map((c) => `
    <div class="p-1.5 bg-purple-50 dark:bg-purple-900/10 rounded text-xs font-mono text-purple-700 dark:text-purple-300">${c}</div>
  `).join('');

  // Build graph data
  const graphData = {
    states: currentTemplate.states,
    transitions: currentTemplate.transitions,
    startState: currentTemplate.states[0],
    terminalStates: [],
    stateCategories: {},
  };

  // Assign categories based on position
  currentTemplate.states.forEach((state, i) => {
    if (i === 0) graphData.stateCategories[state] = 'navigation';
    else if (i === currentTemplate.states.length - 1) graphData.stateCategories[state] = 'control';
    else graphData.stateCategories[state] = i % 3 === 0 ? 'neural' : i % 3 === 1 ? 'symbolic' : 'control';
  });

  // Destroy previous
  if (tryGraph) tryGraph.destroy();

  const container = document.getElementById('try-graph-container');
  container.innerHTML = '';
  
  tryGraph = createStateGraph(container, graphData, {
    width: 600,
    height: 400,
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
