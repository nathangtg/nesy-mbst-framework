/**
 * L* Learning Algorithm Step-Through Animation
 * Shows the observation table construction process
 */

const DEMO_STEPS = [
  {
    step: 1,
    title: 'Initialize',
    description: 'Start with empty observation table. S = {empty}, E = {empty}',
    table: {
      prefixes: ['ε'],
      suffixes: ['ε'],
      values: [['?']],
    },
    query: null,
    hypothesis: null,
  },
  {
    step: 2,
    title: 'Membership Query',
    description: 'Ask oracle: "Does the system accept the empty word?" → Yes (Idle is a valid state)',
    table: {
      prefixes: ['ε'],
      suffixes: ['ε'],
      values: [['Yes']],
    },
    query: { type: 'membership', input: 'ε', response: 'Yes' },
    hypothesis: null,
  },
  {
    step: 3,
    title: 'Extend Prefixes',
    description: 'Add transitions from Idle: sense → Sensing. Extend S with new prefix.',
    table: {
      prefixes: ['ε', 'sense'],
      suffixes: ['ε'],
      values: [['Yes'], ['Yes']],
    },
    query: { type: 'membership', input: 'sense', response: 'Yes' },
    hypothesis: null,
  },
  {
    step: 4,
    title: 'Check Closure',
    description: 'Table is not closed — "sense" row differs from "ε" row in context. Promote to state.',
    table: {
      prefixes: ['ε', 'sense'],
      suffixes: ['ε', 'scene_ready'],
      values: [['Yes', 'No'], ['Yes', 'Yes']],
    },
    query: { type: 'membership', input: 'sense·scene_ready', response: 'Yes' },
    hypothesis: null,
  },
  {
    step: 5,
    title: 'Build Hypothesis',
    description: 'Construct DFA hypothesis H1 with 2 states: {Idle, Sensing}',
    table: {
      prefixes: ['ε', 'sense'],
      suffixes: ['ε', 'scene_ready'],
      values: [['Yes', 'No'], ['Yes', 'Yes']],
    },
    query: null,
    hypothesis: {
      states: ['Idle', 'Sensing'],
      transitions: [['Idle', 'sense', 'Sensing']],
    },
  },
  {
    step: 6,
    title: 'Equivalence Query',
    description: 'Submit H1 to SUT. Counterexample found: "sense·scene_ready·plan_local" (3 states needed)',
    table: {
      prefixes: ['ε', 'sense', 'sense·scene_ready'],
      suffixes: ['ε', 'scene_ready', 'plan_local'],
      values: [['Yes', 'No', 'No'], ['Yes', 'Yes', 'No'], ['Yes', 'No', 'Yes']],
    },
    query: { type: 'equivalence', counterexample: 'sense·scene_ready·plan_local' },
    hypothesis: {
      states: ['Idle', 'Sensing'],
      transitions: [['Idle', 'sense', 'Sensing']],
      rejected: true,
    },
  },
  {
    step: 7,
    title: 'Process Counterexample',
    description: 'Add new state SceneGraphReady. Table now has 3 distinct rows.',
    table: {
      prefixes: ['ε', 'sense', 'sense·scene_ready'],
      suffixes: ['ε', 'scene_ready', 'plan_local'],
      values: [['Yes', 'No', 'No'], ['Yes', 'Yes', 'No'], ['Yes', 'No', 'Yes']],
    },
    query: null,
    hypothesis: {
      states: ['Idle', 'Sensing', 'SceneGraphReady'],
      transitions: [
        ['Idle', 'sense', 'Sensing'],
        ['Sensing', 'scene_ready', 'SceneGraphReady'],
      ],
    },
  },
  {
    step: 8,
    title: 'Continue Learning',
    description: 'After 12 more iterations: 9 states discovered, 13 transitions verified. L* converges.',
    table: {
      prefixes: ['ε', 'sense', 'sense·sr', '...', 'act·eb'],
      suffixes: ['ε', 'sr', 'pl', '...', 'ss'],
      values: [['Y', '-', '-', '...', '-'], ['Y', 'Y', '-', '...', '-'], ['Y', '-', 'Y', '...', '-'], ['...', '...', '...', '...', '...'], ['Y', '-', '-', '...', 'Y']],
    },
    query: null,
    hypothesis: {
      states: ['Idle', 'Sensing', 'SceneGraphReady', 'PlanningLocal', 'PlanningGlobal', 'TrajectorySet', 'Actuating', 'SafeStop', 'EmergencyBrake'],
      transitions: [
        ['Idle', 'sense', 'Sensing'],
        ['Sensing', 'scene_ready', 'SceneGraphReady'],
        ['SceneGraphReady', 'plan_local', 'PlanningLocal'],
        ['SceneGraphReady', 'plan_global', 'PlanningGlobal'],
        ['PlanningLocal', 'trajectory', 'TrajectorySet'],
        ['PlanningGlobal', 'trajectory', 'TrajectorySet'],
        ['TrajectorySet', 'actuate', 'Actuating'],
      ],
      complete: true,
    },
  },
];

export function createLStarAnimation(container) {
  let currentStep = 0;

  container.innerHTML = `
    <div class="space-y-4">
      <!-- Step indicator -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-xs font-medium text-gray-500 dark:text-gray-400">Step</span>
          <span id="lstar-step-num" class="text-sm font-bold text-primary-600 dark:text-primary-400">1</span>
          <span class="text-xs text-gray-400">/ ${DEMO_STEPS.length}</span>
        </div>
        <div class="flex gap-2">
          <button id="lstar-prev" class="px-3 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-40" disabled>
            Prev
          </button>
          <button id="lstar-next" class="px-3 py-1 text-xs rounded bg-primary-600 text-white hover:bg-primary-700 disabled:opacity-40">
            Next Step
          </button>
          <button id="lstar-auto" class="px-3 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
            Auto-play
          </button>
        </div>
      </div>

      <!-- Step title and description -->
      <div class="p-3 rounded-lg bg-blue-50 dark:bg-blue-900/10 border border-blue-200 dark:border-blue-800">
        <h5 id="lstar-title" class="text-sm font-semibold text-blue-900 dark:text-blue-200">Initialize</h5>
        <p id="lstar-desc" class="text-xs text-blue-700 dark:text-blue-300 mt-1">Start with empty observation table</p>
      </div>

      <!-- Query indicator -->
      <div id="lstar-query" class="hidden p-2 rounded-lg border text-xs font-mono">
      </div>

      <!-- Observation Table -->
      <div class="overflow-x-auto">
        <table id="lstar-table" class="w-full text-xs border-collapse">
        </table>
      </div>

      <!-- Current hypothesis -->
      <div id="lstar-hypothesis" class="hidden p-3 rounded-lg bg-green-50 dark:bg-green-900/10 border border-green-200 dark:border-green-800">
      </div>

      <!-- Progress bar -->
      <div class="h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <div id="lstar-progress" class="h-full bg-primary-500 rounded-full transition-all duration-300" style="width: 12.5%"></div>
      </div>
    </div>
  `;

  const prevBtn = container.querySelector('#lstar-prev');
  const nextBtn = container.querySelector('#lstar-next');
  const autoBtn = container.querySelector('#lstar-auto');
  let autoInterval = null;

  function render() {
    const step = DEMO_STEPS[currentStep];
    
    container.querySelector('#lstar-step-num').textContent = step.step;
    container.querySelector('#lstar-title').textContent = step.title;
    container.querySelector('#lstar-desc').textContent = step.description;
    container.querySelector('#lstar-progress').style.width = `${((currentStep + 1) / DEMO_STEPS.length) * 100}%`;

    // Query indicator
    const queryEl = container.querySelector('#lstar-query');
    if (step.query) {
      queryEl.classList.remove('hidden');
      if (step.query.type === 'membership') {
        queryEl.className = 'p-2 rounded-lg border text-xs font-mono border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/10 text-blue-700 dark:text-blue-300';
        queryEl.innerHTML = `<strong>MQ:</strong> "${step.query.input}" → <span class="font-bold">${step.query.response}</span>`;
      } else {
        queryEl.className = 'p-2 rounded-lg border text-xs font-mono border-orange-200 dark:border-orange-800 bg-orange-50 dark:bg-orange-900/10 text-orange-700 dark:text-orange-300';
        queryEl.innerHTML = `<strong>EQ:</strong> Counterexample = "${step.query.counterexample}"`;
      }
    } else {
      queryEl.classList.add('hidden');
    }

    // Observation table
    const tableEl = container.querySelector('#lstar-table');
    const { prefixes, suffixes, values } = step.table;
    tableEl.innerHTML = `
      <thead>
        <tr>
          <th class="p-1.5 border border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 text-left text-gray-600 dark:text-gray-400">S \\ E</th>
          ${suffixes.map(s => `<th class="p-1.5 border border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 text-center text-gray-600 dark:text-gray-400">${s}</th>`).join('')}
        </tr>
      </thead>
      <tbody>
        ${prefixes.map((p, i) => `
          <tr>
            <td class="p-1.5 border border-gray-200 dark:border-gray-700 font-medium text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-800/50">${p}</td>
            ${values[i].map(v => {
              let cls = 'text-gray-500';
              if (v === 'Yes' || v === 'Y') cls = 'text-green-600 dark:text-green-400 font-bold';
              else if (v === 'No' || v === '-') cls = 'text-red-500 dark:text-red-400';
              else if (v === '?') cls = 'text-yellow-500 animate-pulse';
              return `<td class="p-1.5 border border-gray-200 dark:border-gray-700 text-center ${cls}">${v}</td>`;
            }).join('')}
          </tr>
        `).join('')}
      </tbody>
    `;

    // Hypothesis
    const hypEl = container.querySelector('#lstar-hypothesis');
    if (step.hypothesis) {
      hypEl.classList.remove('hidden');
      const h = step.hypothesis;
      let statusClass = 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/10';
      let statusText = '';
      if (h.rejected) {
        statusClass = 'border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/10';
        statusText = '<span class="text-red-600 dark:text-red-400 font-bold">REJECTED</span>';
      } else if (h.complete) {
        statusText = '<span class="text-green-600 dark:text-green-400 font-bold">CONVERGED</span>';
      }
      hypEl.className = `p-3 rounded-lg border text-xs ${statusClass}`;
      hypEl.innerHTML = `
        <div class="flex items-center justify-between mb-1">
          <strong class="text-gray-700 dark:text-gray-300">Hypothesis DFA</strong>
          ${statusText}
        </div>
        <div class="text-gray-600 dark:text-gray-400">
          States: ${h.states.join(', ')}<br/>
          Transitions: ${h.transitions.length} verified
        </div>
      `;
    } else {
      hypEl.classList.add('hidden');
    }

    // Button states
    prevBtn.disabled = currentStep === 0;
    nextBtn.disabled = currentStep === DEMO_STEPS.length - 1;
  }

  prevBtn.addEventListener('click', () => {
    if (currentStep > 0) { currentStep--; render(); }
  });

  nextBtn.addEventListener('click', () => {
    if (currentStep < DEMO_STEPS.length - 1) { currentStep++; render(); }
  });

  autoBtn.addEventListener('click', () => {
    if (autoInterval) {
      clearInterval(autoInterval);
      autoInterval = null;
      autoBtn.textContent = 'Auto-play';
      return;
    }
    autoBtn.textContent = 'Pause';
    autoInterval = setInterval(() => {
      if (currentStep < DEMO_STEPS.length - 1) {
        currentStep++;
        render();
      } else {
        clearInterval(autoInterval);
        autoInterval = null;
        autoBtn.textContent = 'Auto-play';
      }
    }, 2000);
  });

  render();
}
