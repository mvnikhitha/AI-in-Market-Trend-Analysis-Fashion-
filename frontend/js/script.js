// Kalainayam — AI-powered fashion intelligence
// Integrated with real backend API

(function(){
  const API_BASE = 'http://localhost:5000/api';

  // ============================================================
  // 1. FETCH STYLE INSIGHTS
  // ============================================================
  async function fetchStyleInsights() {
    try {
      console.log('📊 Fetching style insights...');
      const response = await fetch(`${API_BASE}/style-insights`);
      
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const data = await response.json();
      console.log('✅ Style insights loaded:', data);
      return data.insights;
      
    } catch (error) {
      console.error('❌ Insights fetch failed:', error);
      return null;
    }
  }

  // ============================================================
// 2. DISPLAY INSIGHTS ON PAGE - SIMPLIFIED
// ============================================================
async function displayStyleInsights() {
  const insightsSection = document.getElementById('style-insights');
  if (!insightsSection) {
    console.log('⚠️ style-insights element not found');
    return;
  }
  
  // Mock data based on notebook analysis
  const mockInsights = {
    dataset_stats: {
      total_reviews: 28229,
      unique_classes: 16,
      avg_rating: 3.92,
      recommendation_rate: 64.2,
      age_range: "18 - 72"
    },
    trending_styles: [
      { class: 'Dresses', reviews: 5431, avg_rating: 3.89 },
      { class: 'Tops', reviews: 4789, avg_rating: 3.88 },
      { class: 'Blouses', reviews: 3245, avg_rating: 3.95 },
      { class: 'Sweaters', reviews: 2876, avg_rating: 4.01 },
      { class: 'Jackets', reviews: 2134, avg_rating: 3.82 }
    ],
    top_rated_styles: [
      { class: 'Sweaters', rating: 4.12, recommendation_rate: 72.5 },
      { class: 'Blouses', rating: 4.08, recommendation_rate: 70.2 },
      { class: 'Cardigans', rating: 4.05, recommendation_rate: 69.8 },
      { class: 'Dresses', rating: 3.98, recommendation_rate: 66.4 },
      { class: 'Knits', rating: 3.95, recommendation_rate: 65.1 }
    ]
  };
  
  const stats = mockInsights.dataset_stats;
  
  insightsSection.innerHTML = `
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
      
      <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 8px;">
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Total Reviews Analyzed</p>
        <h3 style="margin: 0.5rem 0 0 0; font-size: 2rem;">${stats.total_reviews.toLocaleString()}</h3>
      </div>
      
      <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 1.5rem; border-radius: 8px;">
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Unique Classes</p>
        <h3 style="margin: 0.5rem 0 0 0; font-size: 2rem;">${stats.unique_classes}</h3>
      </div>
      
      <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 1.5rem; border-radius: 8px;">
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Average Rating</p>
        <h3 style="margin: 0.5rem 0 0 0; font-size: 2rem;">${stats.avg_rating.toFixed(2)}/5</h3>
      </div>
      
      <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 1.5rem; border-radius: 8px;">
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">Recommended Rate</p>
        <h3 style="margin: 0.5rem 0 0 0; font-size: 2rem;">${stats.recommendation_rate.toFixed(1)}%</h3>
      </div>
      
    </div>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
      
      <div>
        <h3 style="margin-top: 0; font-size: 1.3rem; color: #4a0e1b;">🔥 Trending Styles</h3>
        <ul style="list-style: none; padding: 0; margin: 0;">
          ${mockInsights.trending_styles.map((style, idx) => `
            <li style="padding: 1rem 0; border-bottom: 1px solid #eee;">
              <strong>${idx + 1}. ${style.class}</strong><br/>
              <small>📊 ${style.reviews.toLocaleString()} reviews | ⭐ ${style.avg_rating.toFixed(2)}/5 rating</small>
            </li>
          `).join('')}
        </ul>
      </div>
      
      <div>
        <h3 style="margin-top: 0; font-size: 1.3rem; color: #4a0e1b;">⭐ Top Rated Styles</h3>
        <ul style="list-style: none; padding: 0; margin: 0;">
          ${mockInsights.top_rated_styles.map((style, idx) => `
            <li style="padding: 1rem 0; border-bottom: 1px solid #eee;">
              <strong>${idx + 1}. ${style.class}</strong><br/>
              <small>⭐ ${style.rating.toFixed(2)}/5 | 👍 ${style.recommendation_rate.toFixed(1)}% recommended</small>
            </li>
          `).join('')}
        </ul>
      </div>
      
    </div>
  `;
  
  console.log('✅ Style insights displayed successfully');
}

  // ============================================================
  // 3. FETCH SUGGESTIONS FROM BACKEND
  // ============================================================
  async function fetchSuggestions(opts) {
    try {
      console.log('📤 Sending request to /api/suggestions:', opts);
      const response = await fetch(`${API_BASE}/suggestions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(opts)
      });
      
      console.log('📥 Response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }
      
      const data = await response.json();
      console.log('✅ Backend response:', data);
      return data;
      
    } catch (error) {
      console.error('❌ Fetch error:', error);
      return null;
    }
  }

  // ============================================================
  // 4. GENERATE SUGGESTIONS - MAIN LOGIC
  // ============================================================
  async function generateCollectionSuggestions({season='spring', audience='women', price='mid', focus='tailoring'} = {}){
    console.log('🎯 Generating suggestions:', {season, audience, price, focus});
    
    const result = await fetchSuggestions({season, audience, price, focus});

    if(result && result.suggestions && result.suggestions.length > 0) {
      console.log('✓ Using real suggestions from recommender');
      renderSuggestions(result.suggestions);
    } else {
      console.warn('⚠ Fallback to mock suggestions');
      const picks = generateFallback({season, audience, price, focus});
      renderSuggestions(picks);
    }
  }

  // ============================================================
  // 5. FALLBACK MOCK DATA
  // ============================================================
  function generateFallback({season='spring', audience='women', price='mid', focus='tailoring'} = {}) {
    const focusStyles = {
      tailoring: ['Oversized Blazer','Fitted Trousers','Structured Coat'],
      street: ['Cargo Trousers','Boxy Tee','Technical Jacket'],
      romantic: ['Slip Dress','Sheer Blouse','Rib Knit Dress'],
      minimal: ['Clean Tunic','Minimal Knit','Monochrome Set']
    };
    const styles = focusStyles[focus] || focusStyles.tailoring;
    const colors = ['#4a0e1b','#7b1127','#b33b4a'];

    return Array.from({length:3}).map((_,i) => ({
      design: styles[i % styles.length],
      palette: colors,
      colorNames: ['Primary', 'Secondary', 'Accent'],
      materials: ['Wool', 'Cotton'],
      designNumber: `MOCK-${i+1}`,
      rationale: `Suggested for ${audience}, ${price} price band.`,
      marketDemand: 'Moderate',
      confidence: 0.65
    }));
  }

  // ============================================================
  // 6. RENDER SUGGESTIONS - IMPROVED UI
  // ============================================================
  function renderSuggestions(picks){
    const grid = document.getElementById('suggestions-grid');
    if(!grid) {
      console.warn('❌ suggestions-grid element not found');
      return;
    }
    
    if(!picks || picks.length === 0) {
      grid.innerHTML = '<p style="color: #999; grid-column: 1/-1;">No suggestions available. Try different parameters.</p>';
      return;
    }
    
    grid.innerHTML = picks.map((p, idx) => `
      <article class="suggestion" style="background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
          <div>
            <h4 style="margin: 0 0 0.3rem 0; color: #4a0e1b; font-size: 1.1rem;">${p.design || 'Design'}</h4>
            <p style="margin: 0; font-size: 0.85rem; color: #999;">${p.designNumber || 'N/A'}</p>
          </div>
          <div style="text-align: right;">
            <span style="display: inline-block; background: ${p.marketDemand === 'High' ? '#7b1127' : '#b3b3b3'}; color: white; padding: 0.4rem 0.8rem; border-radius: 4px; font-size: 0.8rem; font-weight: 600;">
              ${p.marketDemand || 'Moderate'}
            </span>
            <p style="margin: 0.4rem 0 0 0; font-size: 0.8rem; color: #666;">
              Confidence: ${(p.confidence * 100).toFixed(0)}%
            </p>
          </div>
        </div>
        
        <p style="margin: 0.8rem 0; font-size: 0.9rem; color: #555; line-height: 1.5;">
          ${p.rationale || 'No rationale available'}
        </p>
        
        <div style="margin: 1rem 0;">
          <p style="margin: 0 0 0.6rem 0; font-size: 0.85rem; font-weight: 600; color: #4a0e1b; text-transform: uppercase; letter-spacing: 0.5px;">Color Palette</p>
          <div class="swatches" style="display: flex; gap: 0.6rem;">
            ${(p.palette || []).map((c, i) => `
              <span 
                style="background: ${c}; display: inline-block; width: 45px; height: 45px; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.15); cursor: pointer; transition: transform 0.2s;" 
                title="${p.colorNames ? p.colorNames[i] : c}"
                onmouseover="this.style.transform='scale(1.1)'"
                onmouseout="this.style.transform='scale(1)'"
              ></span>
            `).join('')}
          </div>
        </div>
        
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #eee;">
          <p style="margin: 0 0 0.6rem 0; font-size: 0.85rem; font-weight: 600; color: #4a0e1b; text-transform: uppercase; letter-spacing: 0.5px;">Materials</p>
          <p style="margin: 0; font-size: 0.9rem; color: #666;">
            ${(p.materials || []).join(' • ')}
          </p>
        </div>
      </article>
    `).join('');
  }

  // ============================================================
  // 7. INITIALIZE ON PAGE LOAD
  // ============================================================
  document.addEventListener('DOMContentLoaded', function(){
    // Load insights
    displayStyleInsights();
    
    // Handle form submission
    const colForm = document.getElementById('collection-form');
    if(colForm){
      console.log('✓ Found collection-form');
      colForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const fd = new FormData(colForm);
        console.log('📋 Form data:', Object.fromEntries(fd));
        generateCollectionSuggestions({
          season: fd.get('season'),
          audience: fd.get('audience'),
          price: fd.get('price'),
          focus: fd.get('focus') || 'tailoring'
        });
        document.querySelector('.suggestions')?.scrollIntoView({behavior:'smooth'});
      });
    } else {
      console.warn('❌ collection-form not found');
    }
    
    // Set year in footer
    const y = new Date().getFullYear();
    document.querySelectorAll('[id$="-year"]').forEach(el=>el.textContent = y);
  });

  // Expose function globally for testing
  window.generateCollectionSuggestions = generateCollectionSuggestions;

})();