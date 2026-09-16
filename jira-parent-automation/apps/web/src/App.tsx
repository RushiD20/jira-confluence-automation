import { useState } from 'react';

type Action = 'close' | 'reopen' | 'noop' | 'ignored';

type Evaluation = {
  eventId: string;
  parentKey?: string;
  action: Action;
  reason: string;
};

const executions = [
  { id: 'evt-002', parent: 'ARE-1842', trigger: 'Sub-task left Done', result: 'Reopened', time: '2 min ago', tone: 'amber' },
  { id: 'evt-001', parent: 'ARE-1837', trigger: 'All sub-tasks complete', result: 'Closed', time: '18 min ago', tone: 'green' },
  { id: 'evt-000', parent: 'ARE-1829', trigger: 'Partial completion', result: 'No-op', time: '41 min ago', tone: 'slate' },
  { id: 'evt-998', parent: 'ARE-1814', trigger: 'Transition unavailable', result: 'Needs review', time: '1 hr ago', tone: 'red' }
];

const workflowChecks = [
  ['Done category', 'Verified', 'green'],
  ['Close transition', 'Configured', 'green'],
  ['Reopen transition', 'Needs review', 'amber'],
  ['Assignee notify', 'Verified', 'green']
] as const;

function App() {
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [isTesting, setIsTesting] = useState(false);
  const [apiState, setApiState] = useState<'online' | 'offline'>('online');

  async function testScenario() {
    setIsTesting(true);
    setEvaluation(null);
    try {
      const response = await fetch('/api/automation/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          eventId: `ui-${Date.now()}`,
          projectKey: 'ARE',
          issueKey: 'ARE-1842-1',
          issueType: 'sub-task',
          parentKey: 'ARE-1842',
          sourceStatusCategory: 'done',
          destinationStatusCategory: 'in_progress',
          parentStatusCategory: 'done',
          parentSubTasks: [
            { key: 'ARE-1842-1', statusCategory: 'in_progress' },
            { key: 'ARE-1842-2', statusCategory: 'done' }
          ]
        })
      });
      if (!response.ok) throw new Error('API request failed');
      setEvaluation(await response.json());
      setApiState('online');
    } catch {
      setApiState('offline');
      setEvaluation(null);
    } finally {
      setIsTesting(false);
    }
  }

  return (
    <main className="shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">O</span><span>orbit</span></div>
        <div className="workspace-label">AUTOMATION OPS</div>
        <nav className="nav-list" aria-label="Main navigation">
          <a className="nav-item active" href="#overview"><span className="nav-icon">+</span>Overview</a>
          <a className="nav-item" href="#executions"><span className="nav-icon">/</span>Executions <span className="nav-count">12</span></a>
          <a className="nav-item" href="#workflow"><span className="nav-icon">#</span>Workflow checks</a>
          <a className="nav-item" href="#scenarios"><span className="nav-icon">*</span>Test scenarios</a>
        </nav>
        <div className="sidebar-bottom">
          <div className="connection-card">
            <div className="connection-top"><span className="status-dot" /> API connected</div>
            <span className="connection-url">127.0.0.1:3000</span>
          </div>
          <div className="user-row"><span className="avatar">RD</span><span><strong>Project owner</strong><small>ARE automation</small></span><span className="more">...</span></div>
        </div>
      </aside>

      <section className="content">
        <header className="topbar">
          <div className="crumb"><span>ARE / Automation</span><b>/</b><strong>Overview</strong></div>
          <div className="top-actions"><span className={`api-pill ${apiState}`}><span className="status-dot" /> {apiState === 'online' ? 'Live' : 'Offline'}</span><button className="icon-button" aria-label="Notifications">!</button><span className="avatar small">RD</span></div>
        </header>

        <div className="page-heading" id="overview">
          <div><p className="eyebrow">WEDNESDAY, 16 SEPTEMBER 2026</p><h1>Good morning, Rushikesh.</h1><p className="subheading">Here is the pulse of your Jira parent automation.</p></div>
          <button className="primary-button" onClick={testScenario} disabled={isTesting}><span>{isTesting ? 'Testing...' : 'Run test scenario'}</span><span className="button-arrow">-&gt;</span></button>
        </div>

        <section className="metrics" aria-label="Automation metrics">
          <article className="metric-card dark"><div className="metric-label">AUTOMATIONS HEALTHY <span className="metric-icon">+</span></div><strong>3 <small>/ 4</small></strong><div className="metric-foot good">+1 since yesterday</div></article>
          <article className="metric-card"><div className="metric-label">ACTIONS THIS WEEK <span className="metric-icon">~</span></div><strong>128</strong><div className="metric-foot">18 close &middot; 7 reopen</div></article>
          <article className="metric-card"><div className="metric-label">SUCCESS RATE <span className="metric-icon">%</span></div><strong>96.8%</strong><div className="metric-foot good">+2.4% vs last week</div></article>
          <article className="metric-card warning"><div className="metric-label">NEEDS ATTENTION <span className="metric-icon">!</span></div><strong>4</strong><div className="metric-foot warn">2 transition &middot; 2 notify</div></article>
        </section>

        <section className="main-grid">
          <article className="panel activity-panel" id="executions">
            <div className="panel-header"><div><p className="eyebrow">LIVE FEED</p><h2>Recent executions</h2></div><a href="#all">View all <span>-&gt;</span></a></div>
            <div className="execution-list">{executions.map((item) => <div className="execution-row" key={item.id}><span className={`execution-status ${item.tone}`} /> <div className="execution-main"><strong>{item.parent}</strong><span>{item.trigger}</span></div><div className={`result-tag ${item.tone}`}>{item.result}</div><time>{item.time}</time></div>)}</div>
            {evaluation && <div className="test-result"><span className="result-check">OK</span><div><strong>Test returned {evaluation.action}</strong><span>{evaluation.parentKey} &middot; {evaluation.reason}</span></div></div>}
          </article>

          <article className="panel workflow-panel" id="workflow">
            <div className="panel-header"><div><p className="eyebrow">CONFIGURATION</p><h2>Workflow health</h2></div><button className="text-button">Manage <span>-&gt;</span></button></div>
            <div className="workflow-score"><div className="score-ring"><span>82</span><small>/100</small></div><div><strong>Mostly ready</strong><p>One check needs your attention before full rollout.</p></div></div>
            <div className="check-list">{workflowChecks.map(([name, status, tone]) => <div className="check-row" key={name}><span className={`check-icon ${tone}`}>{tone === 'green' ? 'OK' : '!'}</span><span>{name}</span><strong className={tone}>{status}</strong></div>)}</div>
          </article>
        </section>

        <section className="bottom-grid" id="scenarios">
          <article className="panel scenario-panel"><div className="panel-header"><div><p className="eyebrow">SAFE TO RUN</p><h2>Test scenarios</h2></div><button className="round-button" aria-label="Add scenario">+</button></div><div className="scenario-row"><span className="scenario-number">01</span><div><strong>Final sub-task completes</strong><span>Parent should transition to Done</span></div><span className="ready-badge">Ready</span></div><div className="scenario-row"><span className="scenario-number">02</span><div><strong>Sub-task leaves Done</strong><span>Parent should reopen</span></div><span className="ready-badge">Ready</span></div></article>
          <article className="panel note-panel"><div className="note-kicker">OPERATOR NOTE</div><h2>Keep the signal clear.</h2><p>Every no-op is intentional. Review the four attention items before enabling the daily refresh.</p><button className="outline-button">Open checklist <span>-&gt;</span></button></article>
        </section>
        <footer><span>Orbit automation control room</span><span>Last sync 09:42:18 UTC</span></footer>
      </section>
    </main>
  );
}

export default App;
