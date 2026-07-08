import * as d3 from 'd3';

const CATEGORY_COLORS = {
  control: '#6b7280',
  neural: '#3b82f6',
  symbolic: '#22c55e',
  navigation: '#6366f1',
  browsing: '#8b5cf6',
  purchase: '#f59e0b',
  account: '#06b6d4',
  system: '#ef4444',
  management: '#22c55e',
  operation: '#14b8a6',
  analytics: '#8b5cf6',
  auth: '#6366f1',
};

export function createStateGraph(container, data, options = {}) {
  const {
    width = 700,
    height = 500,
    onNodeClick = null,
    highlightPath = null,
  } = options;

  // Clear existing
  d3.select(container).selectAll('*').remove();

  const svg = d3.select(container)
    .append('svg')
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('class', 'w-full h-full')
    .style('max-height', `${height}px`);

  // Arrow marker
  svg.append('defs').append('marker')
    .attr('id', 'arrowhead')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 20)
    .attr('refY', 0)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#9ca3af');

  // Active arrow marker
  svg.append('defs').append('marker')
    .attr('id', 'arrowhead-active')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 20)
    .attr('refY', 0)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#3b82f6');

  // Build nodes and links from data
  const nodes = data.states.map((state, i) => ({
    id: state,
    index: i,
    category: data.stateCategories?.[state] || 'control',
    isStart: state === data.startState,
    isTerminal: data.terminalStates?.includes(state),
  }));

  const links = data.transitions.map(([source, target]) => ({
    source: source,
    target: target,
    probability: data.transitionMatrix 
      ? data.transitionMatrix[data.states.indexOf(source)]?.[data.states.indexOf(target)] 
      : null,
  }));

  // Create force simulation
  const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(80))
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide(30));

  // Draw links
  const link = svg.append('g')
    .selectAll('line')
    .data(links)
    .join('line')
    .attr('class', 'transition-link')
    .attr('stroke', '#d1d5db')
    .attr('stroke-width', d => d.probability ? Math.max(1, d.probability * 5) : 1.5)
    .attr('marker-end', 'url(#arrowhead)');

  // Draw link labels (probabilities)
  const linkLabels = svg.append('g')
    .selectAll('text')
    .data(links.filter(l => l.probability && l.probability > 0))
    .join('text')
    .attr('class', 'text-[9px] fill-gray-500 dark:fill-gray-400')
    .attr('text-anchor', 'middle')
    .attr('dy', -5)
    .text(d => d.probability ? d.probability.toFixed(2) : '');

  // Draw nodes
  const node = svg.append('g')
    .selectAll('g')
    .data(nodes)
    .join('g')
    .attr('class', 'state-node')
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended));

  // Node circles
  node.append('circle')
    .attr('r', d => d.isStart ? 18 : d.isTerminal ? 16 : 14)
    .attr('fill', d => CATEGORY_COLORS[d.category] || '#6b7280')
    .attr('stroke', d => d.isStart ? '#1f2937' : d.isTerminal ? '#dc2626' : 'white')
    .attr('stroke-width', d => d.isStart || d.isTerminal ? 3 : 2)
    .attr('opacity', 0.9);

  // Double circle for terminal states
  node.filter(d => d.isTerminal)
    .append('circle')
    .attr('r', 12)
    .attr('fill', 'none')
    .attr('stroke', '#dc2626')
    .attr('stroke-width', 1.5);

  // Node labels
  node.append('text')
    .attr('dy', 30)
    .attr('text-anchor', 'middle')
    .attr('class', 'text-[10px] font-medium fill-gray-700 dark:fill-gray-300')
    .text(d => d.id.length > 12 ? d.id.substring(0, 10) + '..' : d.id);

  // Start state indicator
  node.filter(d => d.isStart)
    .append('text')
    .attr('dy', -25)
    .attr('text-anchor', 'middle')
    .attr('class', 'text-[9px] font-bold fill-gray-500')
    .text('START');

  // Tooltip
  const tooltip = d3.select(container)
    .append('div')
    .attr('class', 'absolute hidden bg-gray-900 text-white text-xs rounded-lg px-3 py-2 pointer-events-none z-50')
    .style('position', 'absolute');

  node.on('mouseover', (event, d) => {
    tooltip
      .html(`<strong>${d.id}</strong><br/>Category: ${d.category}${d.isStart ? '<br/>Start State' : ''}${d.isTerminal ? '<br/>Terminal State' : ''}`)
      .style('left', `${event.offsetX + 10}px`)
      .style('top', `${event.offsetY - 30}px`)
      .classed('hidden', false);
  })
  .on('mouseout', () => {
    tooltip.classed('hidden', true);
  });

  if (onNodeClick) {
    node.on('click', (event, d) => onNodeClick(d));
  }

  // Update positions on tick
  simulation.on('tick', () => {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);

    linkLabels
      .attr('x', d => (d.source.x + d.target.x) / 2)
      .attr('y', d => (d.source.y + d.target.y) / 2);

    node.attr('transform', d => `translate(${d.x},${d.y})`);
  });

  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }

  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

  // Return control methods
  return {
    highlightPath(path) {
      // Reset all
      link.attr('stroke', '#d1d5db').attr('stroke-width', d => d.probability ? Math.max(1, d.probability * 5) : 1.5).attr('marker-end', 'url(#arrowhead)');
      node.selectAll('circle').first?.().attr('opacity', 0.9);

      if (!path || path.length < 2) return;

      // Highlight edges in path
      for (let i = 0; i < path.length - 1; i++) {
        const source = path[i];
        const target = path[i + 1];
        link.filter(d => d.source.id === source && d.target.id === target)
          .attr('stroke', '#3b82f6')
          .attr('stroke-width', 4)
          .attr('marker-end', 'url(#arrowhead-active)');
      }

      // Highlight nodes in path
      node.selectAll('circle:first-child')
        .attr('opacity', d => path.includes(d.id) ? 1 : 0.3);
    },
    
    animateWalk(path, speed = 500) {
      return new Promise((resolve) => {
        let step = 0;
        
        const interval = setInterval(() => {
          if (step >= path.length) {
            clearInterval(interval);
            resolve();
            return;
          }

          // Highlight current node
          node.selectAll('circle:first-child')
            .attr('opacity', d => d.id === path[step] ? 1 : 0.4)
            .attr('r', d => d.id === path[step] ? 22 : (d.isStart ? 18 : d.isTerminal ? 16 : 14));

          // Highlight edge to current
          if (step > 0) {
            link.filter(d => d.source.id === path[step - 1] && d.target.id === path[step])
              .attr('stroke', '#3b82f6')
              .attr('stroke-width', 4)
              .attr('marker-end', 'url(#arrowhead-active)');
          }

          step++;
        }, speed);
      });
    },

    reset() {
      link.attr('stroke', '#d1d5db').attr('stroke-width', d => d.probability ? Math.max(1, d.probability * 5) : 1.5).attr('marker-end', 'url(#arrowhead)');
      node.selectAll('circle:first-child')
        .attr('opacity', 0.9)
        .attr('r', d => d.isStart ? 18 : d.isTerminal ? 16 : 14);
    },

    destroy() {
      simulation.stop();
    }
  };
}
