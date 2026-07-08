export function renderHero() {
  const section = document.getElementById('hero');
  section.innerHTML = `
    <div class="section pt-32 pb-20 md:pt-40 md:pb-28">
      <div class="max-w-3xl animate-on-scroll">
        <p class="text-sm font-medium text-gray-400 dark:text-gray-500 mb-4 font-mono">
          Neuro-Symbolic Model-Based Statistical Testing
        </p>
        
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white leading-[1.1] mb-6">
          The Machine Proposes.<br/>
          <span class="text-gray-400 dark:text-gray-500">The Proof Disposes.</span>
        </h1>
        
        <p class="text-lg text-gray-500 dark:text-gray-400 leading-relaxed max-w-xl mb-8">
          Automatically building verified Markov usage models from natural language requirements — combining LLM intelligence with symbolic precision.
        </p>
        
        <div class="flex items-center gap-3 mb-16">
          <a href="#demo" class="btn-primary">Explore Demo</a>
          <a href="#architecture" class="btn-ghost">How it works</a>
        </div>

        <!-- Key stats -->
        <div class="grid grid-cols-4 gap-8 pt-8 border-t border-gray-100 dark:border-gray-800">
          <div>
            <div class="text-2xl font-bold text-gray-900 dark:text-white tabular-nums">0.91</div>
            <div class="text-xs text-gray-500 dark:text-gray-500 mt-0.5">System F1</div>
          </div>
          <div>
            <div class="text-2xl font-bold text-gray-900 dark:text-white tabular-nums">85.7%</div>
            <div class="text-xs text-gray-500 dark:text-gray-500 mt-0.5">Coverage</div>
          </div>
          <div>
            <div class="text-2xl font-bold text-gray-900 dark:text-white tabular-nums">0.012</div>
            <div class="text-xs text-gray-500 dark:text-gray-500 mt-0.5">JSD</div>
          </div>
          <div>
            <div class="text-2xl font-bold text-gray-900 dark:text-white tabular-nums">&lt;6m</div>
            <div class="text-xs text-gray-500 dark:text-gray-500 mt-0.5">Generation</div>
          </div>
        </div>
      </div>
    </div>
  `;
}
