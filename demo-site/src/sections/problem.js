export function renderProblem() {
  const section = document.getElementById('problem');
  section.innerHTML = `
    <div class="section-container">
      <div class="text-center mb-16 animate-on-scroll">
        <h2 class="section-title">The Problem</h2>
        <p class="section-subtitle mx-auto">
          Model-Based Statistical Testing is powerful but nobody uses it — because building the models takes weeks of expert effort.
        </p>
      </div>

      <!-- Main problem statement -->
      <div class="max-w-4xl mx-auto mb-16 animate-on-scroll">
        <div class="card border-l-4 border-l-red-500">
          <div class="flex items-start gap-4">
            <div class="flex-shrink-0 w-12 h-12 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">The Manual Bottleneck</h3>
              <p class="text-gray-600 dark:text-gray-300">
                A Markov usage model maps every possible user journey through software, with probabilities on each transition. Building one correctly requires <strong>formal methods expertise</strong> and takes <strong>weeks per system</strong>. Most teams skip it entirely, leaving bugs that only appear in real usage undetected.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Why AI alone fails -->
      <div class="mb-8 animate-on-scroll">
        <h3 class="text-2xl font-semibold text-center text-gray-900 dark:text-white mb-8">
          Why Can't AI Just Do It?
        </h3>
        <p class="text-center text-gray-600 dark:text-gray-400 mb-10 max-w-2xl mx-auto">
          Asking an LLM to generate a complete usage model has four systematic failure modes:
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
        <!-- Failure mode 1 -->
        <div class="card animate-on-scroll group">
          <div class="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900/30 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <svg class="w-5 h-5 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
          </div>
          <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Hallucination</h4>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            AI invents transitions that can't actually happen in the system. States are connected without logical basis.
          </p>
          <div class="mt-4 p-3 bg-red-50 dark:bg-red-900/10 rounded-lg">
            <code class="text-xs text-red-700 dark:text-red-300">Login → Admin (no auth check)</code>
          </div>
        </div>

        <!-- Failure mode 2 -->
        <div class="card animate-on-scroll group" style="animation-delay: 100ms">
          <div class="w-10 h-10 rounded-lg bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <svg class="w-5 h-5 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/>
            </svg>
          </div>
          <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Bad Probabilities</h4>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Assigned probabilities don't sum to 1.0 per row, breaking all downstream statistical guarantees.
          </p>
          <div class="mt-4 p-3 bg-orange-50 dark:bg-orange-900/10 rounded-lg">
            <code class="text-xs text-orange-700 dark:text-orange-300">Row sum: 0.7 + 0.5 = 1.2</code>
          </div>
        </div>

        <!-- Failure mode 3 -->
        <div class="card animate-on-scroll group" style="animation-delay: 200ms">
          <div class="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900/30 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"/>
            </svg>
          </div>
          <h4 class="font-semibold text-gray-900 dark:text-white mb-2">State Explosion</h4>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            On large systems, the AI loses track mid-generation. It contradicts earlier outputs and drops states.
          </p>
          <div class="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/10 rounded-lg">
            <code class="text-xs text-yellow-700 dark:text-yellow-300">42 states → 29 in output</code>
          </div>
        </div>

        <!-- Failure mode 4 -->
        <div class="card animate-on-scroll group" style="animation-delay: 300ms">
          <div class="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <svg class="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
            </svg>
          </div>
          <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Logic Violations</h4>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Semantically plausible but logically impossible paths pass through. No invariant checking.
          </p>
          <div class="mt-4 p-3 bg-purple-50 dark:bg-purple-900/10 rounded-lg">
            <code class="text-xs text-purple-700 dark:text-purple-300">Checkout → (empty cart)</code>
          </div>
        </div>
      </div>

      <!-- Solution teaser -->
      <div class="max-w-3xl mx-auto mt-16 text-center animate-on-scroll">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-300 text-sm font-medium mb-4">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          Our Solution
        </div>
        <p class="text-lg text-gray-700 dark:text-gray-300">
          <strong>NeSy-MBST</strong> assigns each sub-task to the computational paradigm best suited for it — <span class="text-neural font-medium">neural inference</span> for ambiguous language reasoning, and <span class="text-symbolic font-medium">symbolic computation</span> for tasks demanding formal precision.
        </p>
      </div>
    </div>
  `;
}
