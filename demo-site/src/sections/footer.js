export function renderFooter() {
  const footer = document.getElementById('footer');
  footer.innerHTML = `
    <div class="section border-t border-gray-100 dark:border-gray-800/50">
      <div class="max-w-3xl mx-auto text-center">
        <!-- Authors -->
        <div class="mb-8 animate-on-scroll">
          <div class="text-sm font-semibold text-gray-900 dark:text-white mb-3">Authors</div>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            Nathan Aldyth Prananta G.
          </p>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
            Sunway University &middot; Mercedes-Benz Tech Innovation &middot; 2026
          </p>
        </div>

        <!-- Citation -->
        <div class="mb-8 animate-on-scroll">
          <div class="text-sm font-semibold text-gray-900 dark:text-white mb-3">Citation</div>
          <div class="relative text-left">
            <pre class="code-block text-[11px] leading-relaxed" id="bibtex-content">@article{nathang2026nesy,
  title={The Machine Proposes. The Proof Disposes.},
  author={Nathan Aldyth Prananta G.},
  institution={Sunway University},
  year={2026}
}</pre>
            <button id="copy-bibtex" class="absolute top-2 right-2 p-1.5 rounded bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors" title="Copy">
              <svg class="w-3.5 h-3.5 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Links -->
        <div class="flex justify-center gap-3 mb-8 animate-on-scroll">
          <a href="https://github.com/nathangtg/llm-mbst-research" target="_blank" class="btn-ghost text-xs">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            GitHub
          </a>
          <a href="#hero" class="btn-ghost text-xs">Back to top</a>
        </div>

        <p class="text-[11px] text-gray-400 dark:text-gray-600">
          Research prototype for demonstration purposes.
        </p>
      </div>
    </div>
  `;

  document.getElementById('copy-bibtex')?.addEventListener('click', () => {
    const bibtex = document.getElementById('bibtex-content').textContent;
    navigator.clipboard.writeText(bibtex).then(() => {
      const btn = document.getElementById('copy-bibtex');
      const orig = btn.innerHTML;
      btn.innerHTML = '<svg class="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>';
      setTimeout(() => { btn.innerHTML = orig; }, 1500);
    });
  });
}
