import './style.css';
import { initTheme } from './theme.js';
import { renderHero } from './sections/hero.js';
import { renderProblem } from './sections/problem.js';
import { renderArchitecture } from './sections/architecture.js';
import { renderLStar } from './sections/lstar.js';
import { renderDemo } from './sections/demo.js';
import { renderResults } from './sections/results.js';
import { renderComparison } from './sections/comparison.js';
import { renderTryIt } from './sections/try-it.js';
import { renderFooter } from './sections/footer.js';
import { initScrollAnimations } from './components/scroll-animations.js';
import { initNavigation } from './components/nav.js';

// Initialize the application
function init() {
  // Initialize theme
  initTheme();

  // Render all sections
  renderHero();
  renderProblem();
  renderArchitecture();
  renderLStar();
  renderDemo();
  renderResults();
  renderComparison();
  renderTryIt();
  renderFooter();

  // Initialize interactions
  initScrollAnimations();
  initNavigation();
}

// Wait for DOM
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
