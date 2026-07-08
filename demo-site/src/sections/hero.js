export function renderHero() {
  const section = document.getElementById('hero');
  section.innerHTML = `
    <div class="relative min-h-screen flex items-center justify-center overflow-hidden">
      <!-- Animated background -->
      <canvas id="hero-canvas" class="absolute inset-0 opacity-20 dark:opacity-10"></canvas>
      
      <div class="relative z-10 section-container text-center">
        <div class="animate-on-scroll">
          <p class="text-sm font-mono text-primary-600 dark:text-primary-400 mb-4 tracking-wider uppercase">
            Neuro-Symbolic Model-Based Statistical Testing
          </p>
          
          <h1 class="text-4xl md:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
            The Machine <span class="gradient-text">Proposes</span>.<br/>
            The Proof <span class="gradient-text">Disposes</span>.
          </h1>
          
          <p class="text-xl md:text-2xl text-academic-muted dark:text-gray-400 max-w-3xl mx-auto mb-4" id="hero-subtitle">
            <span id="typing-text"></span><span class="typing-cursor"></span>
          </p>
          
          <p class="text-base text-gray-500 dark:text-gray-500 max-w-2xl mx-auto mb-10">
            Automatically building formally verified Markov usage models from natural language requirements — combining LLM intelligence with symbolic precision.
          </p>
          
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a href="#demo" class="btn-primary">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Explore the Demo
            </a>
            <a href="#architecture" class="btn-secondary">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
              View Architecture
            </a>
          </div>
          
          <!-- Key metrics preview -->
          <div class="mt-16 grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            <div class="text-center">
              <div class="text-2xl md:text-3xl font-bold text-primary-600 dark:text-primary-400">0.91</div>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">System F1 Score</div>
            </div>
            <div class="text-center">
              <div class="text-2xl md:text-3xl font-bold text-symbolic dark:text-green-400">85.7%</div>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">Fault-Path Coverage</div>
            </div>
            <div class="text-center">
              <div class="text-2xl md:text-3xl font-bold text-optimization dark:text-purple-400">0.012</div>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">JSD (Near-Zero)</div>
            </div>
            <div class="text-center">
              <div class="text-2xl md:text-3xl font-bold text-gray-700 dark:text-gray-300">&lt;6min</div>
              <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">Full Generation</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Scroll indicator -->
      <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"/>
        </svg>
      </div>
    </div>
  `;

  // Typing animation
  initTypingAnimation();
  // Background animation
  initHeroCanvas();
}

function initTypingAnimation() {
  const phrases = [
    'From plain English to verified test plans.',
    'AI reads. Symbolic engine verifies. Solver calibrates.',
    '39.1% more accurate than pure-neural baselines.',
    'No domain expertise required.',
  ];

  const el = document.getElementById('typing-text');
  let phraseIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let delay = 80;

  function type() {
    const currentPhrase = phrases[phraseIndex];

    if (isDeleting) {
      el.textContent = currentPhrase.substring(0, charIndex - 1);
      charIndex--;
      delay = 40;
    } else {
      el.textContent = currentPhrase.substring(0, charIndex + 1);
      charIndex++;
      delay = 80;
    }

    if (!isDeleting && charIndex === currentPhrase.length) {
      delay = 2000;
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      delay = 500;
    }

    setTimeout(type, delay);
  }

  setTimeout(type, 1000);
}

function initHeroCanvas() {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  let width, height, nodes, edges;
  let animationId;

  function resize() {
    width = canvas.width = canvas.offsetWidth;
    height = canvas.height = canvas.offsetHeight;
    initNodes();
  }

  function initNodes() {
    nodes = [];
    const count = Math.floor((width * height) / 25000);
    for (let i = 0; i < count; i++) {
      nodes.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        radius: Math.random() * 3 + 2,
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);
    
    const isDark = document.documentElement.classList.contains('dark');
    const nodeColor = isDark ? 'rgba(96, 165, 250, 0.6)' : 'rgba(59, 130, 246, 0.4)';
    const lineColor = isDark ? 'rgba(96, 165, 250, 0.15)' : 'rgba(59, 130, 246, 0.1)';

    // Draw edges
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 150) {
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.strokeStyle = lineColor;
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      }
    }

    // Draw and update nodes
    nodes.forEach((node) => {
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
      ctx.fillStyle = nodeColor;
      ctx.fill();

      node.x += node.vx;
      node.y += node.vy;

      if (node.x < 0 || node.x > width) node.vx *= -1;
      if (node.y < 0 || node.y > height) node.vy *= -1;
    });

    animationId = requestAnimationFrame(draw);
  }

  resize();
  draw();
  window.addEventListener('resize', resize);
}
