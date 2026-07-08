export function renderFooter() {
  const footer = document.getElementById('footer');
  footer.innerHTML = `
    <div class="section-container">
      <div class="max-w-5xl mx-auto">
        <!-- Authors -->
        <div class="text-center mb-12 animate-on-scroll">
          <h3 class="text-2xl font-semibold text-gray-900 dark:text-white mb-6">Authors</h3>
          <div class="flex flex-wrap justify-center gap-8">
            <div class="text-center">
              <div class="w-16 h-16 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center mx-auto mb-2">
                <span class="text-xl font-bold text-primary-600 dark:text-primary-400">NG</span>
              </div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">Nathan G.</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">Lead Author</p>
            </div>
            <div class="text-center">
              <div class="w-16 h-16 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center mx-auto mb-2">
                <span class="text-xl font-bold text-green-600 dark:text-green-400">JT</span>
              </div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">Jaeden Ting YiYong</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">Co-Author</p>
            </div>
            <div class="text-center">
              <div class="w-16 h-16 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mx-auto mb-2">
                <span class="text-xl font-bold text-purple-600 dark:text-purple-400">WH</span>
              </div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">Wai Phyo Hein</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">Co-Author</p>
            </div>
            <div class="text-center">
              <div class="w-16 h-16 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center mx-auto mb-2">
                <span class="text-xl font-bold text-indigo-600 dark:text-indigo-400">JC</span>
              </div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">Jordan Chay</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">Co-Author</p>
            </div>
          </div>
          <p class="mt-4 text-sm text-gray-500 dark:text-gray-400">
            School of Computing and Artificial Intelligence, Sunway University
          </p>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            In collaboration with Mercedes-Benz Tech Innovation
          </p>
        </div>

        <!-- Citation -->
        <div class="mb-12 animate-on-scroll">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4 text-center">Citation</h3>
          <div class="relative">
            <div class="code-block text-xs">
              <pre id="bibtex-content">@article{nathang2026nesy,
  title={The Machine Proposes. The Proof Disposes. -- Neuro-Symbolic Synthesis 
         of Formally Verified Markov Usage Models from Natural Language Requirements},
  author={Nathan G. and Ting, Jaeden YiYong and Hein, Wai Phyo and Chay, Jordan},
  journal={SWE3033 Software Processes},
  institution={Sunway University},
  year={2026}
}</pre>
            </div>
            <button id="copy-bibtex" class="absolute top-3 right-3 p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors" title="Copy BibTeX">
              <svg class="w-4 h-4 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Links -->
        <div class="flex flex-wrap justify-center gap-4 mb-12 animate-on-scroll">
          <a href="https://github.com/nathangtg/llm-mbst-research" target="_blank" class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            GitHub Repository
          </a>
          <a href="#hero" class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
            </svg>
            Back to Top
          </a>
        </div>

        <!-- Bottom -->
        <div class="border-t border-gray-200 dark:border-gray-700 pt-8 text-center">
          <p class="text-sm text-gray-500 dark:text-gray-400">
            NeSy-MBST Demo &middot; Sunway University &middot; July 2026
          </p>
          <p class="text-xs text-gray-400 dark:text-gray-500 mt-2">
            Built for demonstration purposes. The system described is a research prototype.
          </p>
        </div>
      </div>
    </div>
  `;

  // Copy BibTeX functionality
  document.getElementById('copy-bibtex')?.addEventListener('click', () => {
    const bibtex = document.getElementById('bibtex-content').textContent;
    navigator.clipboard.writeText(bibtex).then(() => {
      const btn = document.getElementById('copy-bibtex');
      btn.innerHTML = '<svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>';
      setTimeout(() => {
        btn.innerHTML = '<svg class="w-4 h-4 text-gray-600 dark:text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>';
      }, 2000);
    });
  });
}
