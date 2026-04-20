# Landing Page Template — index.html

Template HTML đầy đủ cho landing page. Điền trực tiếp data phân tích được vào các `{{PLACEHOLDER}}` — không cần file JSON trung gian.

---

## Full HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{REPO_NAME}} — Repo Knowledge</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Sora:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  /* ── Base surfaces ── */
  --bg:#f5f4f0;--bg2:#ffffff;--bg3:#eeecea;--bg4:#e4e2de;
  --line:rgba(0,0,0,0.07);--line2:rgba(0,0,0,0.11);
  --text:#1a1917;--text2:#5a5750;--text3:#9a978f;

  /* ── Single UI accent (sections, links, badges) ── */
  --accent:#4e6b9e;        /* slate blue — muted */
  --accent-bg:rgba(78,107,158,0.09);
  --accent-bd:rgba(78,107,158,0.28);
  --accent2:#3d7a60;       /* sage green — code/success */
  --accent2-bg:rgba(61,122,96,0.09);
  --accent2-bd:rgba(61,122,96,0.28);
  --warn:#8a6030;          /* warm brown — warnings */
  --warn-bg:rgba(138,96,48,0.09);
  --warn-bd:rgba(138,96,48,0.28);

  /* ── Layer palette (arch diagram + workflow) ── */
  --p-blue:#3d5a8a;   --p-blue-bg:#dde6f2;  --p-blue-bd:rgba(61,90,138,0.30);
  --p-green:#2e7058;  --p-green-bg:#d8eee6; --p-green-bd:rgba(46,112,88,0.30);
  --p-purple:#5b4890; --p-purple-bg:#e4dff2;--p-purple-bd:rgba(91,72,144,0.30);
  --p-warn:#7a5a20;   --p-warn-bg:#f0e8d5;  --p-warn-bd:rgba(122,90,32,0.30);
  --p-gray:#6a6560;   --p-gray-bg:#e8e6e2;  --p-gray-bd:rgba(106,101,96,0.25);

  --mono:'IBM Plex Mono',monospace;--sans:'Sora',sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:var(--sans);background:var(--bg);color:var(--text);line-height:1.6;font-size:14px;}
.wrap{max-width:940px;margin:0 auto;padding:48px 28px 100px;}

/* ── Header ── */
.hdr{margin-bottom:48px;padding-bottom:32px;border-bottom:1px solid var(--line);}
.hdr-top{display:flex;align-items:center;gap:14px;margin-bottom:10px;flex-wrap:wrap;}
.hdr h1{font-size:2rem;font-weight:600;letter-spacing:-0.03em;color:var(--text);}
.vtag{font-family:var(--mono);font-size:12px;color:var(--accent);background:var(--accent-bg);border:1px solid var(--accent-bd);padding:2px 10px;border-radius:4px;}
.hdr-desc{font-size:14px;color:var(--text2);max-width:600px;line-height:1.75;margin-bottom:14px;}
.hdr-meta{display:flex;gap:20px;flex-wrap:wrap;font-size:12px;color:var(--text3);font-family:var(--mono);}
.hdr-meta span::before{content:'// ';}

/* ── Section shell ── */
details{background:var(--bg2);border:1px solid var(--line2);border-radius:10px;overflow:hidden;margin-bottom:8px;}
summary{padding:18px 22px;font-size:12px;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;align-items:center;list-style:none;user-select:none;letter-spacing:0.06em;text-transform:uppercase;color:var(--text);}
summary::-webkit-details-marker{display:none;}
.sl{display:flex;align-items:center;gap:14px;}
.sn{font-family:var(--mono);font-size:10px;font-weight:500;letter-spacing:0.04em;width:20px;}
details .sn{color:var(--accent);}
details summary{border-left:3px solid var(--accent);}
.tog{width:20px;height:20px;border:1px solid var(--line2);border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:15px;color:var(--text3);font-weight:300;flex-shrink:0;}
details[open] .tog::after{content:'−';}
.tog::after{content:'+';}
.sb{padding:0 22px 28px;border-top:1px solid var(--line);}
.pt{padding-top:22px;}
.sec-intro{font-size:13px;color:var(--text2);line-height:1.75;margin-bottom:22px;}

/* ── Architecture ── */
.arch-wrap{display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start;}
@media(max-width:640px){.arch-wrap{grid-template-columns:1fr;}}
.layer-diagram{display:flex;flex-direction:column;gap:3px;}
.layer-box{border:1px solid var(--line2);border-radius:8px;padding:14px 16px;cursor:pointer;transition:border-color .18s,background .18s;}
.layer-arrow{text-align:center;color:var(--text3);font-size:12px;padding:2px 0;}
.layer-tag{font-size:9px;font-family:var(--mono);text-transform:uppercase;letter-spacing:0.09em;color:var(--text3);margin-bottom:4px;font-weight:500;}
.layer-name{font-size:14px;font-weight:700;color:var(--text);margin-bottom:4px;letter-spacing:-0.01em;}
.layer-files{font-family:var(--mono);font-size:11px;color:var(--text3);line-height:1.6;}
.layer-box[data-color="blue"]{border-color:var(--p-blue-bd);background:var(--p-blue-bg);}
.layer-box[data-color="green"]{border-color:var(--p-green-bd);background:var(--p-green-bg);}
.layer-box[data-color="purple"]{border-color:var(--p-purple-bd);background:var(--p-purple-bg);}
.layer-box[data-color="gray"]{border-color:var(--p-gray-bd);background:var(--p-gray-bg);}
.layer-box[data-color="blue"]:hover,.layer-box[data-color="blue"].active{border-color:var(--p-blue);filter:brightness(0.95);}
.layer-box[data-color="green"]:hover,.layer-box[data-color="green"].active{border-color:var(--p-green);filter:brightness(0.95);}
.layer-box[data-color="purple"]:hover,.layer-box[data-color="purple"].active{border-color:var(--p-purple);filter:brightness(0.95);}
.layer-box[data-color="gray"]:hover,.layer-box[data-color="gray"].active{border-color:var(--p-gray);filter:brightness(0.95);}
.arch-detail{background:var(--bg3);border:1px solid var(--line2);border-radius:10px;padding:20px;min-height:260px;position:sticky;top:20px;}
.arch-detail-placeholder{display:flex;align-items:center;justify-content:center;height:200px;color:var(--text3);font-size:13px;font-family:var(--mono);}
.detail-tag{font-size:9px;font-family:var(--mono);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;}
.detail-title{font-size:16px;font-weight:700;color:var(--text);margin-bottom:12px;letter-spacing:-0.01em;}
.detail-desc{font-size:13px;color:var(--text2);line-height:1.75;margin-bottom:16px;}
.detail-comps{display:flex;flex-direction:column;gap:7px;}
.detail-comp{background:var(--bg4);border-radius:6px;padding:9px 12px;display:flex;gap:10px;align-items:baseline;}
.detail-comp-name{font-family:var(--mono);font-size:12px;font-weight:500;min-width:130px;flex-shrink:0;}
.detail-comp-role{font-size:12px;color:var(--text2);}
.detail-comp-name.blue{color:var(--p-blue);}
.detail-comp-name.green{color:var(--p-green);}
.detail-comp-name.purple{color:var(--p-purple);}
.detail-comp-name.warn{color:var(--p-warn);}

/* ── Workflow ── */
.wf-tabs{display:flex;gap:4px;margin-bottom:20px;flex-wrap:wrap;}
.wf-tab{font-size:12px;font-family:var(--mono);padding:6px 14px;border-radius:6px;border:1px solid var(--line2);background:transparent;color:var(--text3);cursor:pointer;transition:all .15s;}
.wf-tab:hover{color:var(--text);}
.wf-tab.active{background:var(--accent-bg);border-color:var(--accent-bd);color:var(--accent);font-weight:600;}
.wf-panel{display:none;}
.wf-panel.active{display:block;}
.flow{display:flex;flex-direction:column;gap:0;}
.flow-step{display:flex;align-items:stretch;gap:0;}
.flow-left{display:flex;flex-direction:column;align-items:center;width:36px;flex-shrink:0;}
.flow-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0;margin-top:14px;}
.flow-dot.blue{background:var(--p-blue);}
.flow-dot.green{background:var(--p-green);}
.flow-dot.purple{background:var(--p-purple);}
.flow-dot.warn{background:var(--p-warn);}
.flow-dot.gray{background:var(--p-gray);}
.flow-line{width:1px;background:var(--line2);flex:1;margin-top:2px;margin-bottom:2px;}
.flow-step:last-child .flow-line{display:none;}
.flow-card{flex:1;background:var(--bg3);border:1px solid var(--line2);border-radius:8px;padding:13px 16px;margin-bottom:8px;margin-left:4px;}
.flow-card.blue{background:var(--p-blue-bg);border-color:var(--p-blue-bd);}
.flow-card.green{background:var(--p-green-bg);border-color:var(--p-green-bd);}
.flow-card.purple{background:var(--p-purple-bg);border-color:var(--p-purple-bd);}
.flow-card.warn{background:var(--p-warn-bg);border-color:var(--p-warn-bd);}
.flow-card.gray{background:var(--p-gray-bg);border-color:var(--p-gray-bd);}
.flow-card-layer{font-size:9px;font-family:var(--mono);text-transform:uppercase;letter-spacing:0.07em;margin-bottom:4px;}
.flow-card-layer.blue{color:var(--p-blue);}
.flow-card-layer.green{color:var(--p-green);}
.flow-card-layer.purple{color:var(--p-purple);}
.flow-card-layer.warn{color:var(--p-warn);}
.flow-card-layer.gray{color:var(--p-gray);}
.flow-card-title{font-size:13px;font-weight:700;color:var(--text);margin-bottom:4px;}
.flow-card-desc{font-size:12px;color:var(--text2);line-height:1.6;}
.flow-card code{font-family:var(--mono);font-size:11px;color:var(--accent2);background:var(--accent2-bg);padding:1px 5px;border-radius:3px;}

/* ── Function table ── */
.fn-table{width:100%;border-collapse:collapse;font-size:13px;}
.fn-table thead tr{border-bottom:1px solid var(--line2);}
.fn-table th{padding:10px 14px;text-align:left;font-size:10px;font-family:var(--mono);text-transform:uppercase;letter-spacing:0.08em;color:var(--text3);font-weight:400;}
.fn-table td{padding:11px 14px;border-bottom:1px solid var(--line);vertical-align:middle;}
.fn-table tbody tr:last-child td{border-bottom:none;}
.fn-table tbody tr:hover td{background:var(--bg3);}
.fn-n{font-family:var(--mono);font-weight:500;}
.fn-n.h{color:var(--text);font-weight:600;}.fn-n.m{color:var(--text);}.fn-n.l{color:var(--text2);}
.fn-f{font-family:var(--mono);font-size:11px;color:var(--text3);}
.ftype{display:inline-block;font-family:var(--mono);font-size:10px;padding:2px 7px;border-radius:3px;border:1px solid;}
.ftype.cls{color:var(--p-purple);border-color:var(--p-purple-bd);background:var(--p-purple-bg);}
.ftype.fn{color:var(--accent2);border-color:var(--accent2-bd);background:var(--accent2-bg);}
.bgs{display:inline-flex;gap:4px;}
.bep{font-size:9px;font-family:var(--mono);padding:1px 6px;border-radius:3px;background:var(--accent-bg);color:var(--accent);border:1px solid var(--accent-bd);}
.bpb{font-size:9px;font-family:var(--mono);padding:1px 6px;border-radius:3px;background:var(--accent2-bg);color:var(--accent2);border:1px solid var(--accent2-bd);}
.bfx{font-size:9px;font-family:var(--mono);padding:1px 6px;border-radius:3px;background:var(--warn-bg);color:var(--warn);border:1px solid var(--warn-bd);}
.sb2{display:flex;align-items:center;gap:8px;}
.st{height:4px;background:var(--bg4);border-radius:2px;flex:1;min-width:60px;overflow:hidden;}
.sf{height:100%;border-radius:2px;}
.sf.h{background:var(--accent2);}.sf.m{background:var(--accent);}.sf.l{background:var(--text3);}
.sn2{font-family:var(--mono);font-size:11px;min-width:28px;text-align:right;}
.sn2.h{color:var(--accent2);font-weight:500;}.sn2.m{color:var(--accent);}.sn2.l{color:var(--text3);}
.fn-hidden{display:none;}
.fn-more{display:block;width:100%;margin-top:10px;padding:8px;background:none;border:1px solid var(--line2);border-radius:6px;font-size:12px;font-family:var(--mono);color:var(--text3);cursor:pointer;letter-spacing:0.04em;}
.fn-more:hover{background:var(--bg3);color:var(--text);}

/* ── Onboarding ── */
.og{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
@media(max-width:620px){.og{grid-template-columns:1fr;}}
.oc{background:var(--bg3);border:1px solid var(--line2);border-radius:8px;padding:18px;}
.oc h4{font-size:10px;font-family:var(--mono);text-transform:uppercase;letter-spacing:0.1em;color:var(--text3);margin-bottom:14px;}
.cb{background:var(--bg);border:1px solid var(--line2);border-radius:6px;padding:13px 15px;margin-bottom:8px;}
.cb-label{font-size:9px;font-family:var(--mono);text-transform:uppercase;letter-spacing:0.07em;color:var(--accent);margin-bottom:8px;font-weight:500;}
.cb pre{font-family:var(--mono);font-size:12px;color:var(--text2);line-height:1.85;white-space:pre-wrap;}
.cb pre .cmd{color:var(--accent2);}
.cb pre .cmt{color:var(--text3);font-style:italic;}
.cb pre .kw{color:var(--accent);}
.cb pre .str{color:var(--warn);}
.cb pre .fn{color:var(--text);font-weight:600;}
.kl{display:flex;flex-direction:column;gap:10px;}
.ki{display:flex;gap:10px;align-items:flex-start;}
.kd{width:6px;height:6px;border-radius:50%;background:var(--accent);flex-shrink:0;margin-top:5px;}
.ki p{font-size:13px;color:var(--text2);line-height:1.65;}
.ki p strong{color:var(--text);font-weight:500;}
.ki code{font-family:var(--mono);font-size:11px;color:var(--accent);background:var(--accent-bg);padding:1px 5px;border-radius:3px;}
.sr{margin-top:8px;padding:11px 14px;background:var(--bg);border:1px solid var(--line2);border-radius:6px;}
.sr-lbl{font-size:9px;font-family:var(--mono);text-transform:uppercase;letter-spacing:0.07em;color:var(--text3);margin-bottom:4px;}
.sr code{font-family:var(--mono);font-size:12px;color:var(--accent2);}

/* ── Requirements ── */
.req-list{display:flex;flex-direction:column;gap:6px;}
.req-item{font-size:13px;color:var(--text2);display:flex;gap:8px;align-items:flex-start;line-height:1.55;}
.req-item::before{content:'—';color:var(--text3);flex-shrink:0;font-family:var(--mono);}
.req-item code{font-family:var(--mono);font-size:11px;color:var(--accent);background:var(--accent-bg);padding:1px 5px;border-radius:3px;}
</style>
</head>
<body>
<div class="wrap">

<!-- ── HEADER ── -->
<div class="hdr">
  <div class="hdr-top">
    <h1>{{REPO_NAME}}</h1>
    <span class="vtag">{{VERSION}}</span>
  </div>
  <p class="hdr-desc">{{REPO_DESCRIPTION}}</p>
  <div class="hdr-meta">
    <span>{{REPO_URL}}</span>
    <span>{{PRIMARY_LANGUAGE}}</span>
    <span>{{TOTAL_FILES}} files · {{TOTAL_LINES}} lines</span>
    <span>Analyzed {{ANALYZED_DATE}}</span>
  </div>
</div>

<!-- ── 01 ARCHITECTURE ── -->
<details open>
  <summary><div class="sl"><span class="sn">01</span> Architecture</div><div class="tog"></div></summary>
  <div class="sb pt">
    <p class="sec-intro">{{ARCH_INTRO}} Click vào từng layer để xem chi tiết các thành phần bên trong.</p>
    <div class="arch-wrap">
      <div class="layer-diagram">
        {{LAYER_BOXES}}
        <!-- Each layer box:
        <div class="layer-box" data-color="blue|green|purple|gray" data-id="LAYER_ID" onclick="selectLayer(this)">
          <div class="layer-tag">Layer N · Label</div>
          <div class="layer-name">Name</div>
          <div class="layer-files">file1 · file2 · ...</div>
        </div>
        <div class="layer-arrow">↓</div>
        -->
      </div>
      <div class="arch-detail" id="arch-detail">
        <div class="arch-detail-placeholder">← click một layer để xem chi tiết</div>
      </div>
    </div>
  </div>
</details>

<!-- ── 02 WORKFLOW ── -->
<details>
  <summary><div class="sl"><span class="sn">02</span> Workflow</div><div class="tog"></div></summary>
  <div class="sb pt">
    <p class="sec-intro">Mỗi workflow được map trực tiếp lên các layer trong Architecture — màu của từng bước tương ứng với layer nào đang xử lý.</p>
    <div class="wf-tabs">
      {{WORKFLOW_TABS}}
      <!-- <button class="wf-tab active" onclick="switchWf(this,'wf-a')">A · Name</button> -->
    </div>
    {{WORKFLOW_PANELS}}
    <!--
    <div class="wf-panel active" id="wf-a">
      <div class="flow">
        <div class="flow-step">
          <div class="flow-left"><div class="flow-dot blue|green|purple|warn|gray"></div><div class="flow-line"></div></div>
          <div class="flow-card blue|green|purple|warn|gray">
            <div class="flow-card-layer blue|green|purple|warn|gray">Layer N · Name</div>
            <div class="flow-card-title">Step title</div>
            <div class="flow-card-desc">Description with <code>code</code> inline.</div>
          </div>
        </div>
      </div>
    </div>
    -->
  </div>
</details>

<!-- ── 03 FUNCTION IMPORTANCE ── -->
<details>
  <summary><div class="sl"><span class="sn">03</span> Function importance</div><div class="tog"></div></summary>
  <div class="sb pt">
    <p class="sec-intro" style="margin-bottom:16px;">Score = usage count ×0.35 + public ×0.25 + entry point ×0.25 + side effects ×0.15 · normalized 0–100. Showing top 10.</p>
    <table class="fn-table">
      <thead><tr><th>Name</th><th>Type</th><th>File</th><th>Flags</th><th style="min-width:120px;">Score</th></tr></thead>
      <tbody>
        {{FUNCTION_ROWS}}
        <!--
        Top 10 rows: plain <tr>...</tr>
        Rows 11+: add class="fn-hidden" to <tr>

        Tier h (score ≥ 80):
        <tr [class="fn-hidden"]><td><span class="fn-n h">name</span></td><td><span class="ftype fn|cls">function|class</span></td><td><span class="fn-f">file.py</span></td>
            <td><div class="bgs"><span class="bep">entry</span><span class="bpb">public</span><span class="bfx">side fx</span></div></td>
            <td><div class="sb2"><div class="st"><div class="sf h" style="width:NN%"></div></div><span class="sn2 h">NN</span></div></td></tr>

        Tier m (score 50–79): same but class="m" on fn-n, sf, sn2
        Tier l (score < 50):  same but class="l"
        -->
      </tbody>
    </table>
    <button class="fn-more" onclick="(function(b){var o=b.dataset.open==='1';b.parentElement.querySelectorAll('table .fn-hidden').forEach(function(r){r.style.display=o?'':'table-row';});b.dataset.open=o?'':'1';b.textContent=o?'▼ see more':'▲ see less';})(this)">▼ see more</button>
  </div>
</details>

<!-- ── 04 ONBOARDING ── -->
<details>
  <summary><div class="sl"><span class="sn">04</span> Onboarding quick start</div><div class="tog"></div></summary>
  <div class="sb pt">
    <div class="og">
      <div>
        <div class="oc" style="margin-bottom:12px;">
          <h4>Install &amp; run</h4>
          {{ONBOARDING_CODE_STEPS}}
          <!--
          <div class="cb">
            <div class="cb-label">Step 1 — create &amp; activate virtualenv</div>
            <pre><span class="cmd">python -m venv .venv</span>
<span class="cmt"># Windows:</span>
<span class="cmd">.venv\Scripts\activate</span>
<span class="cmt"># macOS / Linux:</span>
<span class="cmd">source .venv/bin/activate</span></pre>
          </div>
          <div class="cb">
            <div class="cb-label">Step 2 — install dependencies</div>
            <pre><span class="cmd">pip install -r requirements.txt</span></pre>
          </div>
          <div class="cb">
            <div class="cb-label">Step 3 — setup config</div>
            <pre><span class="cmt"># tạo .env và điền các biến cần thiết</span>
<span class="str">API_KEY</span>=your-key-here</pre>
          </div>
          <div class="cb">
            <div class="cb-label">Step 4 — prepare &amp; run</div>
            <pre><span class="cmt"># bước chuẩn bị riêng của project (nếu có)</span>
<span class="cmd">python setup_script.py</span>
<span class="cmd">python main.py</span></pre>
          </div>
          -->
        </div>
        <div class="oc">
          <h4>Start reading code at</h4>
          {{READING_ORDER}}
          <!--
          <div class="sr"><div class="sr-lbl">Step 1 — label</div><code>path/to/file.py</code></div>
          -->
        </div>
      </div>
      <div class="oc">
        <h4>Key things to know</h4>
        <div class="kl">
          {{KEY_POINTS}}
          <!--
          <div class="ki">
            <div class="kd"></div>
            <p><strong>Point title.</strong> Explanation with <code>inline code</code> if needed.</p>
          </div>
          -->
        </div>
      </div>
    </div>
  </div>
</details>

<!-- ── 05 PROJECT REQUIREMENTS ── -->
<details>
  <summary><div class="sl"><span class="sn">05</span> Project requirements</div><div class="tog"></div></summary>
  <div class="sb pt">
    <div class="req-list">{{REQUIREMENT_ITEMS}}</div>
  </div>
</details>

</div>

<script>
// ── ARCHITECTURE DATA ──
// Điền từ kết quả phân tích: architecture.layers
const LAYERS = {
  {{LAYERS_JS_DATA}}
  /*
  layer_id: {
    color: 'blue|green|purple|warn',
    tag: 'Layer N · Label',
    title: 'Layer name',
    desc: 'Description of what this layer does.',
    comps: [
      {name: 'ClassName', cls: 'blue|green|purple|warn', role: 'What it does'},
    ]
  },
  */
};

function selectLayer(el) {
  document.querySelectorAll('.layer-box').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
  const d = LAYERS[el.dataset.id];
  if (!d) return;
  const colorMap = {blue:'var(--p-blue)', green:'var(--p-green)', purple:'var(--p-purple)', warn:'var(--p-warn)'};
  const color = colorMap[d.color] || 'var(--text2)';
  document.getElementById('arch-detail').innerHTML = `
    <div class="detail-tag" style="color:${color}">${d.tag}</div>
    <div class="detail-title">${d.title}</div>
    <div class="detail-desc">${d.desc}</div>
    <div class="detail-comps">
      ${d.comps.map(c=>`
        <div class="detail-comp">
          <span class="detail-comp-name ${c.cls}">${c.name}</span>
          <span class="detail-comp-role">${c.role}</span>
        </div>`).join('')}
    </div>`;
}

// ── WORKFLOW TABS ──
function switchWf(btn, panelId) {
  document.querySelectorAll('.wf-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.wf-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(panelId).classList.add('active');
}

// Auto-select first layer
document.querySelector('.layer-box')?.click();
</script>
</body>
</html>
```

---

## Placeholder map

| Placeholder | Nguồn trong JSON | Ví dụ |
|---|---|---|
| `{{REPO_NAME}}` | `meta.repo_name` | `click` |
| `{{VERSION}}` | `meta.version` | `v8.3.2` |
| `{{REPO_DESCRIPTION}}` | Tóm tắt ngắn từ README | `Composable CLI toolkit…` |
| `{{REPO_URL}}` | `meta.repo_url` | `github.com/pallets/click` |
| `{{PRIMARY_LANGUAGE}}` | `meta.primary_language` | `Python 3.10+` |
| `{{TOTAL_FILES}}` | `meta.total_files` | `17` |
| `{{TOTAL_LINES}}` | `meta.total_lines` | `22.6k` |
| `{{ANALYZED_DATE}}` | `meta.analyzed_at` (format đẹp) | `April 11, 2026` |
| `{{ARCH_INTRO}}` | `architecture.description` | `Click có 4 layer…` |
| `{{LAYER_BOXES}}` | `architecture.layers[]` | HTML layer-box × N |
| `{{LAYERS_JS_DATA}}` | `architecture.layers[]` | JS object literal |
| `{{WORKFLOW_TABS}}` | `workflows[]` | button × N |
| `{{WORKFLOW_PANELS}}` | `workflows[].steps[]` | div.wf-panel × N |
| `{{FUNCTION_ROWS}}` | `functions[]` sorted by score | tr × N |
| `{{ONBOARDING_CODE_STEPS}}` | `onboarding.steps[]` | div.cb × 4 |
| `{{READING_ORDER}}` | `onboarding.start_reading[]` | div.sr × N |
| `{{KEY_POINTS}}` | `onboarding.key_points[]` | div.ki × N |
| `{{REQUIREMENT_ITEMS}}` | danh sách requirements để chạy project | div.req-item × N |

## Function row tiers

- **Tier h** (score ≥ 80): `fn-n h`, `sf h`, `sn2 h` — teal bar, trắng/đậm
- **Tier m** (score 50–79): `fn-n m`, `sf m`, `sn2 m` — blue bar
- **Tier l** (score < 50): `fn-n l`, `sf l`, `sn2 l` — gray bar, mờ

## req-item format

```html
<div class="req-item"><strong>Key term</strong> — mô tả ngắn</div>
<!-- hoặc nếu không có term nổi bật: -->
<div class="req-item">Mô tả thẳng</div>
```