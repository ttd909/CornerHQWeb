# Dashboard Preview Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `preview.html` — a static, realistic-looking CornerHQ admin dashboard preview page at `cornerhq.com.au/preview`.

**Architecture:** Single `preview.html` file in the repo root alongside `index.html`. All styles in an embedded `<style>` block. Chart.js loaded from CDN for 4 interactive charts. All data hardcoded. No build step, no dependencies to install.

**Tech Stack:** HTML5, CSS (embedded), Chart.js 4.x (CDN), Git, GitHub (ttd909/CornerHQWeb)

---

## File Map

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `preview.html` | Complete dashboard preview — sidebar, 3 sections, 4 Chart.js charts, CSS horizontal bar chart |

---

## Task 1: Create `preview.html`

**Files:**
- Create: `preview.html`

- [ ] **Step 1: Write the file**

Create `preview.html` in the repo root with the following complete content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CornerHQ — Dashboard Preview</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #eef0f4;
      color: #333;
      display: flex;
      height: 100vh;
      overflow: hidden;
    }

    /* ── Sidebar ── */
    .sidebar {
      width: 190px;
      background: #0A1628;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      padding: 24px 0 20px;
      height: 100vh;
      position: fixed;
      left: 0;
      top: 0;
    }

    .sidebar-logo { padding: 0 18px 22px; }
    .sidebar-logo .brand {
      color: #FF6B00;
      font-size: 0.65rem;
      font-weight: 800;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }
    .sidebar-logo .admin {
      color: #fff;
      font-size: 1rem;
      font-weight: 800;
      letter-spacing: -0.2px;
    }

    .nav-item {
      padding: 8px 18px;
      color: rgba(255,255,255,0.4);
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      cursor: default;
      user-select: none;
    }
    .nav-item.active {
      background: #FF6B00;
      color: #fff;
      margin: 2px 10px;
      border-radius: 6px;
      padding: 8px 10px;
    }

    /* ── Main ── */
    .main {
      margin-left: 190px;
      flex: 1;
      overflow-y: auto;
      padding: 20px 28px 48px;
      height: 100vh;
    }

    /* ── Page header ── */
    .page-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid #dde2ea;
    }
    .page-header h1 {
      font-size: 0.85rem;
      font-weight: 800;
      color: #0A1628;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }
    .page-header .period {
      font-size: 0.68rem;
      font-weight: 700;
      color: #aaa;
      letter-spacing: 0.08em;
    }

    /* ── Sections ── */
    .section { margin-bottom: 32px; }

    .section-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 14px;
    }
    .section-header h2 {
      font-size: 0.7rem;
      font-weight: 800;
      color: #FF6B00;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      white-space: nowrap;
    }
    .section-line { flex: 1; height: 1px; background: #dde2ea; }

    /* ── Stat cards ── */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 12px;
    }
    .stats-grid.cols-3 { grid-template-columns: repeat(3, 1fr); }

    .stat-card {
      background: #fff;
      border-radius: 8px;
      padding: 14px 16px;
      border: 1px solid #e4e9f0;
    }
    .stat-label {
      font-size: 0.62rem;
      font-weight: 700;
      color: #bbb;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 5px;
    }
    .stat-value {
      font-size: 1.7rem;
      font-weight: 800;
      color: #0A1628;
      line-height: 1;
      margin-bottom: 4px;
    }
    .stat-desc { font-size: 0.7rem; color: #aaa; }

    /* ── Chart cards ── */
    .charts-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 12px;
    }
    .charts-row.split { grid-template-columns: 2fr 1fr; }

    .chart-card {
      background: #fff;
      border-radius: 8px;
      padding: 18px 20px;
      border: 1px solid #e4e9f0;
    }
    .chart-title {
      font-size: 0.68rem;
      font-weight: 800;
      color: #0A1628;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 14px;
    }

    /* ── Doughnut ── */
    .doughnut-wrap {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .doughnut-legend {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.75rem;
      color: #555;
    }
    .legend-dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      flex-shrink: 0;
    }

    /* ── Cash payments ── */
    .payment-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      padding: 8px 0;
      border-bottom: 1px solid #f3f4f6;
    }
    .payment-row:last-child { border-bottom: none; }
    .payment-name { font-size: 0.8rem; font-weight: 700; color: #0A1628; }
    .payment-desc { font-size: 0.72rem; color: #aaa; }
    .payment-amount { font-size: 0.8rem; font-weight: 700; color: #0A1628; text-align: right; }
    .payment-date { font-size: 0.68rem; color: #aaa; text-align: right; }

    /* ── Top classes bars ── */
    .class-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 14px;
    }
    .by-label { font-size: 0.65rem; font-weight: 700; color: #bbb; letter-spacing: 0.06em; }

    .bar-row {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
    }
    .bar-row:last-child { margin-bottom: 0; }
    .bar-label { font-size: 0.75rem; font-weight: 600; color: #444; width: 160px; flex-shrink: 0; }
    .bar-track { flex: 1; background: #f0f0f0; border-radius: 3px; height: 9px; }
    .bar-fill { height: 100%; background: #FF6B00; border-radius: 3px; }
    .bar-count { font-size: 0.75rem; font-weight: 700; color: #0A1628; width: 28px; text-align: right; flex-shrink: 0; }

    /* ── Responsive ── */
    @media (max-width: 900px) {
      .stats-grid { grid-template-columns: repeat(2, 1fr); }
      .stats-grid.cols-3 { grid-template-columns: repeat(2, 1fr); }
      .charts-row, .charts-row.split { grid-template-columns: 1fr; }
    }
    @media (max-width: 640px) {
      .sidebar { display: none; }
      .main { margin-left: 0; padding: 16px 16px 40px; }
      .stats-grid { grid-template-columns: repeat(2, 1fr); }
    }
  </style>
</head>
<body>

  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="sidebar-logo">
      <div class="brand">CornerHQ</div>
      <div class="admin">ADMIN</div>
    </div>
    <div class="nav-item">Today</div>
    <div class="nav-item">Schedule</div>
    <div class="nav-item">Members</div>
    <div class="nav-item">Memberships</div>
    <div class="nav-item">Class Setup</div>
    <div class="nav-item">PT</div>
    <div class="nav-item active">Analytics</div>
    <div class="nav-item">Settings</div>
  </aside>

  <!-- Main -->
  <main class="main">

    <div class="page-header">
      <h1>Analytics</h1>
      <span class="period">LAST 30 DAYS</span>
    </div>

    <!-- MEMBERS -->
    <div class="section">
      <div class="section-header">
        <h2>Members</h2>
        <div class="section-line"></div>
      </div>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Attendance</div>
          <div class="stat-value">247</div>
          <div class="stat-desc">Total check-ins</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">First-Timers</div>
          <div class="stat-value">18</div>
          <div class="stat-desc">First seen in the period</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Retention</div>
          <div class="stat-value">78%</div>
          <div class="stat-desc">66 of 89 members seen</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">No-Shows</div>
          <div class="stat-value">3</div>
          <div class="stat-desc">Booked, not checked in</div>
        </div>
      </div>
      <div class="charts-row">
        <div class="chart-card">
          <div class="chart-title">Attendance Over Time</div>
          <canvas id="chart-attendance" height="110"></canvas>
        </div>
        <div class="chart-card">
          <div class="chart-title">Retention Rate Trend</div>
          <canvas id="chart-retention" height="110"></canvas>
        </div>
      </div>
    </div>

    <!-- FINANCE -->
    <div class="section">
      <div class="section-header">
        <h2>Finance</h2>
        <div class="section-line"></div>
      </div>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Cash This Month</div>
          <div class="stat-value">$1,240</div>
          <div class="stat-desc">Recorded cash passes</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">One-Off Received</div>
          <div class="stat-value">$3,890</div>
          <div class="stat-desc">Cash and Stripe passes</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Weekly Run-Rate</div>
          <div class="stat-value">$1,120</div>
          <div class="stat-desc">Active Stripe weekly passes</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Active Subscriptions</div>
          <div class="stat-value">34</div>
          <div class="stat-desc">Stripe recurring memberships</div>
        </div>
      </div>
      <div class="charts-row split">
        <div class="chart-card">
          <div class="chart-title">Revenue Over Time</div>
          <canvas id="chart-revenue" height="110"></canvas>
        </div>
        <div class="chart-card">
          <div class="chart-title">Membership Breakdown</div>
          <div class="doughnut-wrap">
            <canvas id="chart-membership" width="110" height="110"></canvas>
            <div class="doughnut-legend">
              <div class="legend-item">
                <div class="legend-dot" style="background:#FF6B00"></div>Monthly — 60%
              </div>
              <div class="legend-item">
                <div class="legend-dot" style="background:#0A1628"></div>Casual — 30%
              </div>
              <div class="legend-item">
                <div class="legend-dot" style="background:#d0d7df"></div>Annual — 10%
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="chart-card">
        <div class="chart-title">Cash Payments This Month</div>
        <div class="payment-row">
          <div><div class="payment-name">Sarah Mitchell</div><div class="payment-desc">10-Class Pass</div></div>
          <div><div class="payment-amount">$180.00</div><div class="payment-date">Mon, 29/6</div></div>
        </div>
        <div class="payment-row">
          <div><div class="payment-name">James Tran</div><div class="payment-desc">Monthly Membership</div></div>
          <div><div class="payment-amount">$120.00</div><div class="payment-date">Fri, 26/6</div></div>
        </div>
        <div class="payment-row">
          <div><div class="payment-name">Priya Sharma</div><div class="payment-desc">Casual Drop-In</div></div>
          <div><div class="payment-amount">$25.00</div><div class="payment-date">Wed, 24/6</div></div>
        </div>
        <div class="payment-row">
          <div><div class="payment-name">Connor Walsh</div><div class="payment-desc">5-Class Pass</div></div>
          <div><div class="payment-amount">$95.00</div><div class="payment-date">Mon, 22/6</div></div>
        </div>
      </div>
    </div>

    <!-- CLASSES -->
    <div class="section">
      <div class="section-header">
        <h2>Classes</h2>
        <div class="section-line"></div>
      </div>
      <div class="stats-grid cols-3">
        <div class="stat-card">
          <div class="stat-label">Total Classes Run</div>
          <div class="stat-value">62</div>
          <div class="stat-desc">This period</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Avg. Class Size</div>
          <div class="stat-value">12</div>
          <div class="stat-desc">Members per session</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Busiest Day</div>
          <div class="stat-value">Tue</div>
          <div class="stat-desc">Highest avg. attendance</div>
        </div>
      </div>
      <div class="chart-card">
        <div class="class-header">
          <div class="chart-title" style="margin-bottom:0;">Top Classes</div>
          <span class="by-label">BY CHECK-INS</span>
        </div>
        <div class="bar-row">
          <div class="bar-label">Muay Thai All Levels</div>
          <div class="bar-track"><div class="bar-fill" style="width:100%"></div></div>
          <div class="bar-count">89</div>
        </div>
        <div class="bar-row">
          <div class="bar-label">Boxing Fundamentals</div>
          <div class="bar-track"><div class="bar-fill" style="width:72%"></div></div>
          <div class="bar-count">64</div>
        </div>
        <div class="bar-row">
          <div class="bar-label">Sparring</div>
          <div class="bar-track"><div class="bar-fill" style="width:55%"></div></div>
          <div class="bar-count">49</div>
        </div>
        <div class="bar-row">
          <div class="bar-label">Strength &amp; Conditioning</div>
          <div class="bar-track"><div class="bar-fill" style="width:38%"></div></div>
          <div class="bar-count">34</div>
        </div>
        <div class="bar-row">
          <div class="bar-label">Kids Muay Thai</div>
          <div class="bar-track"><div class="bar-fill" style="width:12%"></div></div>
          <div class="bar-count">11</div>
        </div>
      </div>
    </div>

  </main>

  <script>
    Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    Chart.defaults.font.size = 11;
    Chart.defaults.color = '#aaa';

    // Attendance Over Time — bar chart
    new Chart(document.getElementById('chart-attendance'), {
      type: 'bar',
      data: {
        labels: ['2 Jun', '9 Jun', '16 Jun', '23 Jun', '30 Jun'],
        datasets: [{
          label: 'Check-ins',
          data: [52, 61, 48, 72, 66],
          backgroundColor: '#FF6B00',
          borderRadius: 4,
          borderSkipped: false,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.y} check-ins` } }
        },
        scales: {
          x: { grid: { display: false }, border: { display: false } },
          y: { grid: { color: '#f0f0f0' }, border: { display: false }, ticks: { stepSize: 20 } }
        }
      }
    });

    // Retention Rate Trend — line chart
    new Chart(document.getElementById('chart-retention'), {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: 'Retention %',
          data: [62, 65, 68, 71, 75, 78],
          borderColor: '#FF6B00',
          backgroundColor: 'rgba(255,107,0,0.08)',
          pointBackgroundColor: '#FF6B00',
          pointRadius: 4,
          tension: 0.3,
          fill: true,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.y}% retention` } }
        },
        scales: {
          x: { grid: { display: false }, border: { display: false } },
          y: {
            grid: { color: '#f0f0f0' }, border: { display: false },
            min: 50, max: 90,
            ticks: { callback: val => val + '%' }
          }
        }
      }
    });

    // Revenue Over Time — line chart
    new Chart(document.getElementById('chart-revenue'), {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: 'Revenue',
          data: [3200, 3800, 3500, 4100, 4600, 5130],
          borderColor: '#0A1628',
          backgroundColor: 'rgba(10,22,40,0.06)',
          pointBackgroundColor: '#0A1628',
          pointRadius: 4,
          tension: 0.3,
          fill: true,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: ctx => ` $${ctx.parsed.y.toLocaleString()}` } }
        },
        scales: {
          x: { grid: { display: false }, border: { display: false } },
          y: {
            grid: { color: '#f0f0f0' }, border: { display: false },
            ticks: { callback: val => '$' + (val / 1000).toFixed(0) + 'k' }
          }
        }
      }
    });

    // Membership Breakdown — doughnut
    new Chart(document.getElementById('chart-membership'), {
      type: 'doughnut',
      data: {
        labels: ['Monthly', 'Casual', 'Annual'],
        datasets: [{
          data: [60, 30, 10],
          backgroundColor: ['#FF6B00', '#0A1628', '#d0d7df'],
          borderWidth: 0,
          hoverOffset: 4,
        }]
      },
      options: {
        responsive: false,
        cutout: '65%',
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: ctx => ` ${ctx.parsed}%` } }
        }
      }
    });
  </script>

</body>
</html>
```

- [ ] **Step 2: Open in browser to verify**

Open `preview.html` directly in Chrome (double-click the file or drag into browser).

Check:
- Navy sidebar visible, "Analytics" highlighted in orange
- Three sections — Members, Finance, Classes — each with orange label + divider line
- 4 stat cards per section, compact header at top
- Bar chart (attendance), two line charts (retention, revenue), doughnut (membership) all rendered with axes and tooltips
- CSS horizontal bars for top classes
- Cash payments list shows 4 rows

- [ ] **Step 3: Commit**

```bash
git add preview.html
git commit -m "Add dashboard preview page at /preview"
```

---

## Task 2: Push and Deploy

**Files:** None (git operation only)

- [ ] **Step 1: Push to GitHub**

```bash
git push origin main
```

Expected: pushed to `https://github.com/ttd909/CornerHQWeb`

- [ ] **Step 2: Confirm deployment**

If the site auto-deploys (Vercel/Netlify connected to GitHub), `cornerhq.com.au/preview` should be live within ~60 seconds of the push completing. Open it to verify.
