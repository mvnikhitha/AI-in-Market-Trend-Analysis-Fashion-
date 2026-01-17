// Kalainayam Render Results Module
// Utilities for rendering dynamic content to the UI

const RenderResults = (function() {
  
  // Render trends data (styles, colors, fabrics, market)
  function renderTrends(data) {
    if (!data) return;

    const { styles, colors, fabrics, overallGrowth } = data;

    // Render Styles
    const stylesList = document.getElementById('styles-list');
    if (stylesList && styles) {
      stylesList.innerHTML = '';
      styles.sort((a, b) => b.score - a.score).forEach(s => {
        const li = document.createElement('li');
        li.innerHTML = `<span>${s.name}</span><span class="muted small">${s.score}%</span>`;
        stylesList.appendChild(li);
      });
    }

    // Render Colors
    const colorsPalette = document.getElementById('colors-palette');
    if (colorsPalette && colors) {
      colorsPalette.innerHTML = '';
      colors.slice(0, 4).forEach(c => {
        const sw = document.createElement('span');
        sw.title = `${c.name} • ${c.share}%`;
        sw.setAttribute('style', `background:${c.hex}`);
        colorsPalette.appendChild(sw);
      });
    }

    // Render Fabrics
    const fabricsList = document.getElementById('fabrics-list');
    if (fabricsList && fabrics) {
      fabricsList.innerHTML = '';
      fabrics.sort((a, b) => b.demand - a.demand).forEach(f => {
        const li = document.createElement('li');
        const arrow = f.demand > 10 ? '▲' : (f.demand < 6 ? '▼' : '→');
        li.innerHTML = `<span>${f.name}</span><span class="muted small">${arrow} ${f.demand}%</span>`;
        fabricsList.appendChild(li);
      });
    }

    // Render Market Signals
    const growthElem = document.getElementById('growth-percent');
    const demandShift = document.getElementById('demand-shift');
    if (growthElem && overallGrowth !== undefined) {
      growthElem.textContent = `+${overallGrowth}%`;
      demandShift.textContent = overallGrowth > 8 ? 'High' : 'Moderate';
    }
  }

  // Render collection suggestions
  function renderSuggestions(picks) {
    const grid = document.getElementById('suggestions-grid');
    if (!grid || !picks) return;

    grid.innerHTML = '';
    picks.forEach(p => {
      const card = document.createElement('article');
      card.className = 'suggestion';
      card.innerHTML = `
        <h4>${p.design}</h4>
        <p class="muted small">${p.rationale}</p>
        <div class="swatches" aria-hidden="true" style="margin-top:.6rem">
          ${p.palette.map(c => `<span style="background:${c};display:inline-block;width:28px;height:28px;border-radius:6px;margin-right:.4rem;border:1px solid rgba(0,0,0,0.04)"></span>`).join('')}
        </div>
        <p style="margin-top:.6rem"><strong>Materials:</strong> ${p.materials.join(', ')}</p>
        <div style="margin-top:.6rem">
          <button class="btn btn-primary" onclick="RenderResults.exportSpec('${p.design}')">Export Spec</button>
          <button class="btn btn-outline" onclick="RenderResults.addToProject('${p.design}')">Add to Project</button>
        </div>
      `;
      grid.appendChild(card);
    });
  }

  // Render loading state
  function showLoading(elementId = 'suggestions-grid') {
    const element = document.getElementById(elementId);
    if (element) {
      element.innerHTML = '<div class="loading" style="text-align:center;padding:2rem;color:#7b1127;"><p>Generating suggestions...</p></div>';
    }
  }

  // Render error state
  function showError(message, elementId = 'suggestions-grid') {
    const element = document.getElementById(elementId);
    if (element) {
      element.innerHTML = `<div class="error" style="padding:1.5rem;background:#fee;border-left:4px solid #c9154a;border-radius:6px;"><p><strong>Error:</strong> ${message}</p></div>`;
    }
  }

  // Render success message
  function showSuccess(message, duration = 3000) {
    const toast = document.createElement('div');
    toast.style.cssText = `
      position:fixed;
      bottom:2rem;
      right:2rem;
      background:#4a0e1b;
      color:white;
      padding:1rem 1.5rem;
      border-radius:8px;
      box-shadow:0 8px 24px rgba(74,14,27,0.2);
      z-index:9999;
      animation:slideIn 300ms ease;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.remove();
    }, duration);
  }

  // Helper: Smooth scroll to element
  function scrollToElement(selector, offset = 0) {
    const element = document.querySelector(selector);
    if (element) {
      const top = element.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  }

  // Export spec pack
  function exportSpec(designName) {
    showSuccess(`Exporting spec pack for: ${designName}`);
    // In production, this would generate and download a PDF
    console.log('Export spec for:', designName);
  }

  // Add to project
  function addToProject(designName) {
    showSuccess(`Added "${designName}" to your project`);
    console.log('Add to project:', designName);
  }

  return {
    renderTrends,
    renderSuggestions,
    showLoading,
    showError,
    showSuccess,
    scrollToElement,
    exportSpec,
    addToProject,
  };
})();

// Export for use in modules if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = RenderResults;
}
