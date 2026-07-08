export function createHeatmap(container, data) {
  const { states, transitionMatrix } = data;
  
  if (!transitionMatrix || !states) {
    container.innerHTML = `
      <div class="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
        <p class="text-sm">Transition matrix not available for this scenario.<br/>
        The matrix is computed at runtime via convex optimization.</p>
      </div>
    `;
    return;
  }

  const size = states.length;
  const cellSize = Math.min(50, Math.floor(500 / size));
  const margin = { top: 80, right: 20, bottom: 20, left: 100 };
  const width = size * cellSize + margin.left + margin.right;
  const height = size * cellSize + margin.top + margin.bottom;

  container.innerHTML = '';

  const isDark = document.documentElement.classList.contains('dark');

  // Create SVG
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  svg.setAttribute('class', 'w-full h-auto max-h-[500px]');
  container.appendChild(svg);

  // Color scale
  function getColor(value) {
    if (value === 0) return isDark ? '#1f2937' : '#f9fafb';
    const intensity = Math.pow(value, 0.5); // sqrt for better visibility
    if (isDark) {
      const r = Math.floor(30 + intensity * 59);
      const g = Math.floor(41 + intensity * 89);
      const b = Math.floor(55 + intensity * 200);
      return `rgb(${r}, ${g}, ${b})`;
    } else {
      const r = Math.floor(239 - intensity * 180);
      const g = Math.floor(246 - intensity * 180);
      const b = Math.floor(255 - intensity * 25);
      return `rgb(${r}, ${g}, ${b})`;
    }
  }

  // Draw cells
  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      const value = transitionMatrix[i][j];
      const x = margin.left + j * cellSize;
      const y = margin.top + i * cellSize;

      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('x', x);
      rect.setAttribute('y', y);
      rect.setAttribute('width', cellSize - 1);
      rect.setAttribute('height', cellSize - 1);
      rect.setAttribute('fill', getColor(value));
      rect.setAttribute('rx', '2');
      rect.setAttribute('class', 'transition-colors duration-200 cursor-pointer');
      
      // Hover effect
      rect.addEventListener('mouseover', () => {
        rect.setAttribute('stroke', isDark ? '#60a5fa' : '#3b82f6');
        rect.setAttribute('stroke-width', '2');
        showTooltip(x + cellSize / 2, y - 10, `${states[i]} → ${states[j]}: ${value.toFixed(3)}`);
      });
      rect.addEventListener('mouseout', () => {
        rect.setAttribute('stroke', 'none');
        hideTooltip();
      });
      
      svg.appendChild(rect);

      // Cell text for significant values
      if (value > 0.05) {
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', x + cellSize / 2);
        text.setAttribute('y', y + cellSize / 2 + 4);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('class', 'text-[8px] pointer-events-none');
        text.setAttribute('fill', value > 0.5 ? 'white' : (isDark ? '#d1d5db' : '#374151'));
        text.textContent = value.toFixed(2);
        svg.appendChild(text);
      }
    }
  }

  // Row labels (source states)
  for (let i = 0; i < size; i++) {
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', margin.left - 5);
    text.setAttribute('y', margin.top + i * cellSize + cellSize / 2 + 3);
    text.setAttribute('text-anchor', 'end');
    text.setAttribute('class', 'text-[9px]');
    text.setAttribute('fill', isDark ? '#d1d5db' : '#4b5563');
    text.textContent = states[i].length > 12 ? states[i].substring(0, 10) + '..' : states[i];
    svg.appendChild(text);
  }

  // Column labels (target states)
  for (let j = 0; j < size; j++) {
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', margin.left + j * cellSize + cellSize / 2);
    text.setAttribute('y', margin.top - 8);
    text.setAttribute('text-anchor', 'start');
    text.setAttribute('transform', `rotate(-45, ${margin.left + j * cellSize + cellSize / 2}, ${margin.top - 8})`);
    text.setAttribute('class', 'text-[9px]');
    text.setAttribute('fill', isDark ? '#d1d5db' : '#4b5563');
    text.textContent = states[j].length > 12 ? states[j].substring(0, 10) + '..' : states[j];
    svg.appendChild(text);
  }

  // Tooltip element
  let tooltipEl = null;

  function showTooltip(x, y, text) {
    if (!tooltipEl) {
      tooltipEl = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      svg.appendChild(tooltipEl);
    }
    tooltipEl.innerHTML = '';
    
    const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    const txt = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    txt.setAttribute('x', x);
    txt.setAttribute('y', y - 5);
    txt.setAttribute('text-anchor', 'middle');
    txt.setAttribute('class', 'text-[10px] font-medium');
    txt.setAttribute('fill', isDark ? '#f9fafb' : '#1f2937');
    txt.textContent = text;
    
    tooltipEl.appendChild(txt);
  }

  function hideTooltip() {
    if (tooltipEl) {
      tooltipEl.innerHTML = '';
    }
  }
}
