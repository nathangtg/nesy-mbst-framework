import { createStateGraph } from '../components/state-graph.js';
import templates from '../data/templates.json';

let currentTemplate = null;
let tryGraph = null;

export function renderTryIt() {
  const section = document.getElementById('try-it');
  section.innerHTML = `
    <div class="section border-t border-gray-100 dark:border-gray-800/50">
      <div class="section-header animate-on-scroll">
        <h2 class="section-title">Try It Yourself</h2>
        <p class="section-desc">
          Select a template, modify the requirements, and watch the pipeline build a model.
        </p>
      </div>

      <div class="animate-on-scroll">
        <!-- Templates -->
        <div class="flex gap-2 mb-6">
          ${templates.templates.map((t, i) => `
            <button class="template-btn ${i === 0 ? 'active' : ''}" data-template="${t.id}">${t.name}</button>
          `).join('')}
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <!-- Input -->
          <div class="space-y-4">
            <div class="card">
              <textarea id="try-requirements" rows="6" 
                class="w-full p-3 border border-gray-200 dark:border-gray-800 rounded-lg bg-gray-50 dark:bg-gray-950 text-sm text-gray-700 dark:text-gray-300 font-mono resize-y focus:outline-none focus:ring-1 focus:ring-gray-400"
                placeholder="Enter requirements..."></textarea>
              <button id="try-build" class="btn-primary mt-3">Build Model</button>
            </div>

            <!-- Pipeline progress -->
            <div id="try-pipeline" class="card hidden">
              <div class="space-y-2.5" id="pipeline-steps"></div>
            </div>

            <!-- Info -->
            <div id="try-info" class="card hidden">
              <div class="grid grid-cols-2 gap-3 text-sm">
                <div><span class="text-gray-500">States:</span> <span id="try-state-count" class="font-semibold text-gray-900 dark:text-white"></span></div>
                <div><span class="text-gray-500">Transitions:</span> <span id="try-transition-count" class="font-semibold text-gray-900 dark:text-white"></span></div>
              </div>
              <div id="try-constraints" class="mt-3 space-y-1"></div>
            </div>
          </div>

          <!-- Output graph -->
          <div class="card">
            <div id="try-graph-container" class="w-full" style="min-height: 360px;">
              <div class="h-full flex items-center justify-center text-sm text-gray-400">
                Select a template and click "Build Model"
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;

  initTryIt();
}

function initTryIt() {
  const textarea = document.getElementById('try-requirements');
  const buildBtn = document.getElementById('try-build');
  const templateBtns = document.querySelectorAll('.template-btn');

  loadTemplate(templates.templates[0].id);

  templateBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      templateBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      loadTemplate(btn.dataset.template);
    });
  });

  buildBtn.addEventListener('click', () => {
    if (currentTemplate) runPipeline();
  });
}

function loadTemplate(id) {
  const template = templates.templates.find((t) => t.id === id);
  if (!template) return;
  currentTemplate = template;
  document.getElementById('try-requirements').value = template.requirements;
  document.getElementById('try-pipeline').classList.add('hidden');
  document.getElementById('try-info').classList.add('hidden');
}

async function runPipeline() {
  const pipelineEl = document.getElementById('try-pipeline');
  const stepsEl = document.getElementById('pipeline-steps');
  pipelineEl.classList.remove('hidden');
  document.getElementById('try-info').classList.add('hidden');

  const steps = ['Extracting states & transitions', 'Symbolic feasibility check', 'Optimizing probabilities', 'Generating tests'];
  stepsEl.innerHTML = steps.map((s, i) => `
    <div class="flex items-center gap-2.5" id="pstep-${i}">
      <div class="w-5 h-5 rounded-full border border-gray-300 dark:border-gray-700 flex items-center justify-center">
        <span class="text-[10px] text-gray-400">${i + 1}</span>
      </div>
      <span class="text-sm text-gray-500 dark:text-gray-400">${s}</span>
    </div>
  `).join('');

  for (let i = 0; i < steps.length; i++) {
    const el = document.getElementById(`pstep-${i}`);
    el.querySelector('div').className = 'w-5 h-5 rounded-full bg-blue-500 flex items-center justify-center animate-pulse';
    el.querySelector('div').innerHTML = '';
    await sleep(500 + Math.random() * 300);
    el.querySelector('div').className = 'w-5 h-5 rounded-full bg-emerald-500 flex items-center justify-center';
    el.querySelector('div').innerHTML = '<svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>';
  }

  await sleep(200);
  showResults();
}

function showResults() {
  document.getElementById('try-info').classList.remove('hidden');
  document.getElementById('try-state-count').textContent = currentTemplate.states.length;
  document.getElementById('try-transition-count').textContent = currentTemplate.transitions.length;

  document.getElementById('try-constraints').innerHTML = currentTemplate.constraints.map((c) => `
    <div class="p-1.5 bg-violet-50 dark:bg-violet-950/30 rounded text-[11px] font-mono text-violet-700 dark:text-violet-300">${c}</div>
  `).join('');

  const graphData = {
    states: currentTemplate.states,
    transitions: currentTemplate.transitions,
    startState: currentTemplate.states[0],
    terminalStates: [],
    stateCategories: Object.fromEntries(currentTemplate.states.map((s, i) => [s, i === 0 ? 'navigation' : 'control'])),
  };

  if (tryGraph) tryGraph.destroy();
  const container = document.getElementById('try-graph-container');
  container.innerHTML = '';
  tryGraph = createStateGraph(container, graphData, { width: 550, height: 360 });
}

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }
