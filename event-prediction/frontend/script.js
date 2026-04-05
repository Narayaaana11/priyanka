const FI_COLORS = {
  retweets: 'linear-gradient(90deg, #ff6b35, #ff3d71)',
  users:    'linear-gradient(90deg, #7c3aed, #a855f7)',
  tweets:   'linear-gradient(90deg, #0ea5e9, #00e5ff)',
  time:     'linear-gradient(90deg, #10b981, #34d399)',
};

const FI_ICONS = {
  retweets: '🔁',
  users:    '👥',
  tweets:   '🐦',
  time:     '⏱',
};

async function predict() {
  const btn = document.getElementById('predict-btn');
  const errorEl = document.getElementById('error-container');

  const tweet_count  = Number(document.getElementById('tweet_count').value);
  const unique_users = Number(document.getElementById('unique_users').value);
  const retweet_sum  = Number(document.getElementById('retweet_sum').value);
  const time_span    = Number(document.getElementById('time_span').value);

  if (!tweet_count && !retweet_sum) {
    showError('Please fill in at least Tweet Count and Retweet Sum.');
    return;
  }

  btn.classList.add('loading');
  btn.innerHTML = '<span class="spinner"></span>Analyzing signals...';
  errorEl.innerHTML = '';

  try {
    const response = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tweet_count, unique_users, retweet_sum, time_span })
    });

    if (!response.ok) throw new Error('Backend returned ' + response.status);

    const result = await response.json();
    renderResult(result);

  } catch (err) {
    console.error(err);
    // Fallback demo mode when backend is not running
    const demo = simulateResult(tweet_count, unique_users, retweet_sum, time_span);
    renderResult(demo, true);
  } finally {
    btn.classList.remove('loading');
    btn.innerHTML = 'Run Prediction';
  }
}

function resetPrediction() {
  const inputIds = ['tweet_count', 'unique_users', 'retweet_sum', 'time_span'];
  inputIds.forEach(id => {
    document.getElementById(id).value = '';
  });

  const empty = document.getElementById('result-empty');
  const content = document.getElementById('result-content');
  const card = document.getElementById('result-card');
  const fiPanel = document.getElementById('fi-panel');
  const fiRows = document.getElementById('fi-rows');
  const errorEl = document.getElementById('error-container');
  const fill = document.getElementById('prob-fill');
  const predictBtn = document.getElementById('predict-btn');

  document.getElementById('verdict-badge').textContent = '—';
  document.getElementById('verdict-badge').className = 'verdict-badge';
  document.getElementById('verdict-text').textContent = '—';
  document.getElementById('verdict-text').className = 'verdict-text';
  document.getElementById('prob-val').textContent = '—';
  document.getElementById('tags-container').innerHTML = '';

  fill.className = 'prob-fill';
  fill.style.width = '0%';

  errorEl.innerHTML = '';
  fiRows.innerHTML = '';
  fiPanel.style.display = 'none';
  card.style.borderColor = 'var(--border)';
  empty.style.display = 'block';
  content.style.display = 'none';
  content.classList.remove('show');
  predictBtn.classList.remove('loading');
  predictBtn.innerHTML = 'Run Prediction';
}

function simulateResult(tweets, users, retweets, time) {
  let pred = 0, prob = 0.35;
  const rt = retweets * 5;
  const uc = users * 2;

  if (rt > 7500 && time < 200)       { pred = 1; prob = 0.95; }
  else if (uc > 90 && rt > 4000)     { pred = 1; prob = 0.85; }
  else if (rt > 4000)                { pred = 1; prob = Math.min(0.5 + rt / 20000, 0.93); }
  else if (rt < 500)                 { pred = 0; prob = 0.25; }

  const total = retweets + users + tweets + time;
  return {
    prediction: pred,
    probability: prob,
    explanations: [
      retweets > 800 ? 'High engagement (retweets)' : 'Low engagement',
      users > 40     ? 'Wide user spread'            : 'Limited user reach',
      time < 400     ? 'Fast growth'                 : 'Slow growth',
      tweets > 50    ? 'High activity'               : 'Low activity',
    ],
    feature_importance: {
      retweets: total ? +((retweets / total) * 100).toFixed(2) : 0,
      users:    total ? +((users    / total) * 100).toFixed(2) : 0,
      tweets:   total ? +((tweets   / total) * 100).toFixed(2) : 0,
      time:     total ? +((time     / total) * 100).toFixed(2) : 0,
    }
  };
}

function renderResult(result, isDemo = false) {
  const empty   = document.getElementById('result-empty');
  const content = document.getElementById('result-content');
  const card    = document.getElementById('result-card');

  const isHot = result.prediction === 1;
  const pct   = (result.probability * 100).toFixed(1);

  // Verdict
  document.getElementById('verdict-badge').textContent  = isHot ? '🔥 HOT' : '❄️ NOT HOT';
  document.getElementById('verdict-badge').className    = 'verdict-badge ' + (isHot ? 'hot' : 'cold');
  document.getElementById('verdict-text').textContent   = isHot ? 'Trending Event' : 'Low Traction';
  document.getElementById('verdict-text').className     = 'verdict-text ' + (isHot ? 'hot' : 'cold');

  // Probability
  document.getElementById('prob-val').textContent = pct + '%';
  const fill = document.getElementById('prob-fill');
  fill.className = 'prob-fill ' + (isHot ? 'hot' : 'cold');
  setTimeout(() => { fill.style.width = pct + '%'; }, 50);

  // Tags
  const tagsEl = document.getElementById('tags-container');
  tagsEl.innerHTML = result.explanations.map(e => {
    const isPositive = e.includes('High') || e.includes('Wide') || e.includes('Fast');
    return `<span class="tag ${isPositive ? 'positive' : 'negative'}">${e}</span>`;
  }).join('');

  if (isDemo) {
    tagsEl.innerHTML += `<span class="tag" style="border-color:rgba(251,191,36,0.3);color:#fbbf24;background:rgba(251,191,36,0.07);">⚠ Demo mode — start Flask backend</span>`;
  }

  // Show content
  empty.style.display = 'none';
  content.style.display = 'block';
  content.classList.remove('show');
  void content.offsetWidth;
  content.classList.add('show');

  // Card border glow
  card.style.borderColor = isHot ? 'rgba(255,107,53,0.3)' : 'rgba(59,130,246,0.25)';

  // Feature importance
  renderFI(result.feature_importance);
}

function renderFI(data) {
  const panel = document.getElementById('fi-panel');
  const rows  = document.getElementById('fi-rows');

  if (!data) { panel.style.display = 'none'; return; }

  panel.style.display = 'block';

  const sorted = Object.entries(data).sort((a, b) => b[1] - a[1]);
  const max    = sorted[0][1];

  rows.innerHTML = sorted.map(([key, val], i) => `
    <div class="fi-row">
      <span class="fi-rank">${i + 1}</span>
      <span class="fi-label">${FI_ICONS[key] || ''} ${key}</span>
      <div class="fi-bar-track">
        <div class="fi-bar" id="fi-bar-${key}" style="background: ${FI_COLORS[key] || '#4CAF50'}; width: 0%"></div>
      </div>
      <span class="fi-pct">${val}%</span>
    </div>
  `).join('');

  setTimeout(() => {
    sorted.forEach(([key, val]) => {
      const el = document.getElementById('fi-bar-' + key);
      if (el) el.style.width = (max > 0 ? (val / max) * 100 : 0) + '%';
    });
  }, 100);
}

function showError(msg) {
  document.getElementById('error-container').innerHTML = `<div class="error-msg">${msg}</div>`;
  const empty   = document.getElementById('result-empty');
  const content = document.getElementById('result-content');
  empty.style.display   = 'none';
  content.style.display = 'block';
  content.classList.add('show');
}

// Allow Enter key to trigger prediction
document.addEventListener('keydown', e => {
  if (e.key === 'Enter') predict();
});
