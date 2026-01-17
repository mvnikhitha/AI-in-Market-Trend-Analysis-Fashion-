// Kalainayam Charts & Visualizations Module
// Utilities for creating sparklines and simple chart visualizations

const Charts = (function() {
  
  // Create a simple SVG sparkline
  function sparkline(values = [], width = 120, height = 28, stroke = '#7b1127', fill = 'none') {
    if (values.length === 0) return '';
    
    const max = Math.max(...values);
    const points = values.map((v, i) => {
      const x = (i / (values.length - 1 || 1)) * width;
      const y = height - (v / (max || 1)) * height;
      return `${x},${y}`;
    }).join(' ');

    return `<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-hidden="true" style="display:inline-block;vertical-align:middle">
      <polyline fill="${fill}" stroke="${stroke}" stroke-width="2" points="${points}" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`;
  }

  // Render all sparklines in the page
  function renderSparklines() {
    document.querySelectorAll('.sparkline').forEach(el => {
      const raw = el.getAttribute('data-values') || '2,3,5,8,12';
      const vals = raw.split(',').map(n => Number(n));
      const color = el.getAttribute('data-color') || '#7b1127';
      el.innerHTML = sparkline(vals, 180, 36, color);
    });
  }

  // Create a simple bar chart (CSS-based)
  function barChart(data, containerId, maxValue = null) {
    const container = document.getElementById(containerId);
    if (!container || !data) return;

    const max = maxValue || Math.max(...data.map(d => d.value));
    
    container.innerHTML = '';
    data.forEach(item => {
      const percentage = (item.value / max) * 100;
      const bar = document.createElement('div');
      bar.style.cssText = `margin-bottom:1rem`;
      bar.innerHTML = `
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.25rem">
          <span style="flex:0 0 100px;font-weight:500;font-size:0.85rem">${item.label}</span>
          <span style="color:#7b1127;font-weight:600;font-size:0.85rem">${item.value}%</span>
        </div>
        <div style="background:rgba(123,17,39,0.08);height:24px;border-radius:6px;overflow:hidden">
          <div style="background:linear-gradient(90deg,#7b1127,#b33b4a);height:100%;width:${percentage}%;border-radius:6px;transition:width 300ms ease"></div>
        </div>
      `;
      container.appendChild(bar);
    });
  }

  // Create a simple color swatch grid
  function colorGrid(colors, containerId) {
    const container = document.getElementById(containerId);
    if (!container || !colors) return;

    container.innerHTML = '';
    colors.forEach(color => {
      const swatch = document.createElement('div');
      swatch.style.cssText = `
        text-align:center;
        cursor:pointer;
        transition:transform 200ms ease;
      `;
      swatch.innerHTML = `
        <div style="
          background:${color.hex};
          width:80px;
          height:80px;
          border-radius:8px;
          margin:0 auto 0.5rem;
          border:2px solid rgba(0,0,0,0.04);
          box-shadow:0 4px 12px rgba(0,0,0,0.08);
        "></div>
        <p style="margin:0.25rem 0;font-weight:600;font-size:0.85rem">${color.name}</p>
        <p style="margin:0;color:#78736f;font-size:0.75rem">${color.hex}</p>
      `;
      swatch.addEventListener('mouseenter', () => {
        swatch.style.transform = 'translateY(-4px)';
      });
      swatch.addEventListener('mouseleave', () => {
        swatch.style.transform = 'translateY(0)';
      });
      container.appendChild(swatch);
    });
  }

  // Create a growth indicator with arrow
  function growthIndicator(value, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const isPositive = value >= 0;
    const arrow = isPositive ? '▲' : '▼';
    const color = isPositive ? '#4a9d6f' : '#c9154a';
    const sign = isPositive ? '+' : '';

    container.innerHTML = `
      <div style="display:flex;align-items:baseline;gap:0.5rem">
        <span style="font-size:2rem;font-weight:700;color:#0b0b0b">${sign}${value}%</span>
        <span style="color:${color};font-weight:600">${arrow} ${isPositive ? 'Growth' : 'Decline'}</span>
      </div>
    `;
  }

  // Create a comparison card (two values side by side)
  function comparisonCard(label1, value1, label2, value2, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
        <div>
          <p style="margin:0;color:#78736f;font-size:0.85rem;margin-bottom:0.25rem">${label1}</p>
          <p style="margin:0;font-size:1.5rem;font-weight:700;color:#0b0b0b">${value1}</p>
        </div>
        <div>
          <p style="margin:0;color:#78736f;font-size:0.85rem;margin-bottom:0.25rem">${label2}</p>
          <p style="margin:0;font-size:1.5rem;font-weight:700;color:#0b0b0b">${value2}</p>
        </div>
      </div>
    `;
  }

  // Animate number counter (counts up from 0 to target)
  function counterAnimate(elementId, targetValue, duration = 1000) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const startValue = 0;
    const startTime = Date.now();
    
    const animate = () => {
      const currentTime = Date.now();
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      const current = Math.floor(startValue + (targetValue - startValue) * progress);
      element.textContent = current + '%';
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    animate();
  }

  return {
    sparkline,
    renderSparklines,
    barChart,
    colorGrid,
    growthIndicator,
    comparisonCard,
    counterAnimate,
  };
})();

// Export for use in modules if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Charts;
}
