#!/usr/bin/env python3
"""Render an outcome-backward capability tree to a standalone map HTML page."""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
from pathlib import Path
from typing import Any


STATUS_LABELS = {
    "target": "目标",
    "ruler": "尺子",
    "exists": "可复用",
    "partial": "部分可用",
    "weak": "薄弱",
    "missing": "缺口",
    "risk": "风险",
    "done": "完成",
}

WORK_LABELS = {
    "active": "施工中",
    "done": "已修复",
    "next": "下一步",
    "pending": "待处理",
    "blocked": "卡住",
    "deferred": "后置",
}

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Top-level JSON must be an object.")
    return data


def _validate(data: dict[str, Any]) -> None:
    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("`nodes` must be a non-empty list.")

    seen: set[str] = set()
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise ValueError(f"nodes[{index}] must be an object.")
        node_id = node.get("id")
        if not node_id:
            raise ValueError(f"nodes[{index}] is missing id.")
        if node_id in seen:
            raise ValueError(f"Duplicate node id: {node_id}")
        seen.add(node_id)

    roots = [n for n in nodes if not n.get("parentId")]
    if len(roots) != 1:
        raise ValueError("Outcome tree must have exactly one root node.")

    for node in nodes:
        parent_id = node.get("parentId")
        if parent_id and parent_id not in seen:
            raise ValueError(f"Node {node.get('id')} references missing parent {parent_id}.")


def _metrics(data: dict[str, Any]) -> dict[str, Any]:
    nodes = data.get("nodes") or []
    status_counts: dict[str, int] = {}
    work_counts: dict[str, int] = {}
    priority_counts: dict[str, int] = {}
    scores = []
    for node in nodes:
        status = node.get("status") or "partial"
        status_counts[status] = status_counts.get(status, 0) + 1
        work_status = node.get("workStatus")
        if work_status:
            work_counts[work_status] = work_counts.get(work_status, 0) + 1
        priority = node.get("priority")
        if priority:
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        score = node.get("score")
        if isinstance(score, (int, float)):
            scores.append(float(score))
    return {
        "nodeCount": len(nodes),
        "statusCounts": status_counts,
        "workCounts": work_counts,
        "priorityCounts": dict(
            sorted(priority_counts.items(), key=lambda item: PRIORITY_ORDER.get(item[0], 99))
        ),
        "averageScore": round(sum(scores) / len(scores), 1) if scores else None,
    }


def _render_html(data: dict[str, Any], source_path: Path) -> str:
    generated_at = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    data = dict(data)
    data.setdefault("project", {})
    data["project"] = dict(data["project"])
    data["project"].setdefault("generatedAt", generated_at)
    data["project"].setdefault("sourcePath", str(source_path))
    data["metrics"] = _metrics(data)

    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    labels = json.dumps(STATUS_LABELS, ensure_ascii=False)
    work_labels = json.dumps(WORK_LABELS, ensure_ascii=False)
    title = html.escape(data.get("goal", {}).get("title") or data.get("project", {}).get("name") or "Outcome Map")

    return (
        _HTML_TEMPLATE.replace("__TITLE__", title)
        .replace("__OUTCOME_DATA__", blob)
        .replace("__STATUS_LABELS__", labels)
        .replace("__WORK_LABELS__", work_labels)
    )


_HTML_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    :root {
      --bg: #f6f7f2;
      --panel: #fffdf7;
      --ink: #17202a;
      --muted: #627083;
      --line: #bcc7d4;
      --target: #0f766e;
      --ruler: #2f63b7;
      --exists: #2f7d32;
      --partial: #b45f06;
      --weak: #b42318;
      --missing: #7a3db8;
      --risk: #bd1550;
      --done: #59667a;
      --work-active: #2563eb;
      --work-done: #16803c;
      --work-next: #c76f00;
      --work-pending: #64748b;
      --work-blocked: #c02626;
      --work-deferred: #6b7280;
      --shadow: 0 14px 28px rgba(23, 32, 42, 0.12);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--ink);
      background: var(--bg);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
      overflow: hidden;
    }
    .app {
      display: grid;
      grid-template-rows: auto 1fr;
      height: 100vh;
      min-height: 640px;
    }
    header {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 16px;
      align-items: center;
      padding: 16px 18px 12px;
      background: #fff9ed;
      border-bottom: 1px solid #e6dcc8;
    }
    h1 {
      margin: 0 0 6px;
      font-size: 22px;
      line-height: 1.25;
    }
    .subtitle {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
      max-width: 1080px;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(4, minmax(66px, auto));
      gap: 8px;
    }
    .stat {
      border: 1px solid #e1d7c4;
      background: rgba(255,255,255,0.72);
      border-radius: 8px;
      padding: 7px 9px;
      min-width: 68px;
    }
    .stat b {
      display: block;
      font-size: 17px;
      line-height: 1.1;
    }
    .stat span {
      display: block;
      color: var(--muted);
      font-size: 11px;
      margin-top: 3px;
    }
    .workspace {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 390px;
      min-height: 0;
    }
    .map-wrap {
      position: relative;
      min-width: 0;
      min-height: 0;
      background:
        linear-gradient(rgba(42, 51, 61, 0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(42, 51, 61, 0.045) 1px, transparent 1px),
        #f8f5ec;
      background-size: 48px 48px;
    }
    .toolbar {
      position: absolute;
      z-index: 5;
      top: 12px;
      left: 12px;
      right: 12px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      pointer-events: none;
    }
    .toolbar > * {
      pointer-events: auto;
    }
    input, select, button {
      height: 34px;
      border: 1px solid #c9c1b1;
      background: rgba(255,255,255,0.92);
      color: var(--ink);
      border-radius: 7px;
      padding: 0 10px;
      font-size: 13px;
      box-shadow: 0 4px 12px rgba(23, 32, 42, 0.08);
    }
    input {
      min-width: 280px;
      flex: 1 1 280px;
      max-width: 520px;
    }
    button {
      cursor: pointer;
    }
    button:hover {
      border-color: #796f5f;
    }
    body.edit-mode .map-wrap {
      outline: 2px solid rgba(37, 99, 235, 0.28);
      outline-offset: -2px;
    }
    .edit-only {
      display: none;
    }
    body.edit-mode .edit-only {
      display: inline-flex;
      align-items: center;
    }
    .save-status {
      min-height: 24px;
      display: inline-flex;
      align-items: center;
      padding: 2px 8px;
      border: 1px solid #d6dee9;
      border-radius: 999px;
      background: rgba(255,255,255,0.92);
      color: #526070;
      font-size: 12px;
      box-shadow: 0 4px 12px rgba(23, 32, 42, 0.08);
    }
    body.edit-mode #edit-toggle {
      background: #17202a;
      border-color: #17202a;
      color: #fffdf7;
    }
    body.edit-mode .map-node {
      cursor: move;
    }
    body.edit-mode .map-node .node-card {
      stroke-dasharray: 5 3;
    }
    #map {
      display: block;
      width: 100%;
      height: 100%;
      cursor: grab;
      touch-action: none;
    }
    #map.dragging {
      cursor: grabbing;
    }
    .band {
      fill: rgba(255, 255, 255, 0.34);
      stroke: rgba(100, 116, 139, 0.12);
    }
    .band-label {
      fill: #7b6e59;
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
    }
    .link {
      fill: none;
      stroke: #94a3b8;
      stroke-width: 2.2;
      opacity: 0.72;
    }
    .link.p0 { stroke: #d9483b; stroke-width: 3.2; }
    .link.p1 { stroke: #c98122; stroke-width: 2.7; }
    .link.dimmed { opacity: 0.12; }
    .link.highlight { opacity: 1; stroke-width: 4.2; }
    .map-node {
      cursor: pointer;
      transition: opacity 120ms ease;
    }
    .map-node.dimmed {
      opacity: 0.22;
    }
    .node-card {
      fill: #fffefa;
      stroke: #cbd5e1;
      stroke-width: 1.2;
      filter: drop-shadow(0 5px 10px rgba(23, 32, 42, 0.12));
    }
    .map-node.selected .node-card {
      stroke: #111827;
      stroke-width: 2.4;
    }
    .map-node.work-active .node-card {
      stroke: var(--work-active);
      stroke-width: 2.6;
      stroke-dasharray: 7 4;
    }
    .map-node.work-done .node-card {
      stroke: var(--work-done);
      stroke-width: 2.1;
    }
    .map-node.work-next .node-card {
      stroke: var(--work-next);
      stroke-width: 2.1;
    }
    .map-node.work-blocked .node-card {
      stroke: var(--work-blocked);
      stroke-width: 2.4;
    }
    .status-strip { width: 8px; }
    .status-target { fill: var(--target); }
    .status-ruler { fill: var(--ruler); }
    .status-exists { fill: var(--exists); }
    .status-partial { fill: var(--partial); }
    .status-weak { fill: var(--weak); }
    .status-missing { fill: var(--missing); }
    .status-risk { fill: var(--risk); }
    .status-done { fill: var(--done); }
    .node-title {
      fill: #17202a;
      font-size: 13px;
      font-weight: 750;
    }
    .node-summary {
      fill: #5f6f82;
      font-size: 11px;
    }
    .pill-text {
      fill: #334155;
      font-size: 10px;
      font-weight: 700;
    }
    .pill-bg {
      fill: #eef2f7;
      stroke: #d6dee9;
    }
    .work-dot {
      stroke: #fffefa;
      stroke-width: 2;
    }
    .work-active-fill { fill: var(--work-active); }
    .work-done-fill { fill: var(--work-done); }
    .work-next-fill { fill: var(--work-next); }
    .work-pending-fill { fill: var(--work-pending); }
    .work-blocked-fill { fill: var(--work-blocked); }
    .work-deferred-fill { fill: var(--work-deferred); }
    .score-ring {
      fill: #fffefa;
      stroke: #cbd5e1;
      stroke-width: 1.3;
    }
    .score-text {
      fill: #111827;
      font-size: 12px;
      font-weight: 800;
      text-anchor: middle;
      dominant-baseline: central;
    }
    .minimap {
      position: absolute;
      right: 14px;
      bottom: 14px;
      width: 220px;
      height: 142px;
      border: 1px solid #c9c1b1;
      background: rgba(255, 253, 247, 0.9);
      border-radius: 8px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }
    .minimap-title {
      position: absolute;
      top: 7px;
      left: 9px;
      color: var(--muted);
      font-size: 11px;
      font-weight: 700;
      z-index: 1;
    }
    #mini {
      width: 100%;
      height: 100%;
    }
    .inspector {
      min-width: 0;
      min-height: 0;
      overflow: hidden;
      background: #fffdf7;
      border-left: 1px solid #e1d7c4;
      display: flex;
      flex-direction: column;
    }
    .inspector-tabs {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 6px;
      padding: 12px 12px 8px;
      border-bottom: 1px solid #e1d7c4;
      background: #fffdf7;
      flex: 0 0 auto;
    }
    .inspector-tab {
      height: 31px;
      padding: 0 6px;
      border-radius: 7px;
      box-shadow: none;
      font-size: 12px;
      white-space: nowrap;
    }
    .inspector-tab.active {
      background: #17202a;
      border-color: #17202a;
      color: #fffdf7;
    }
    .inspector-body {
      min-height: 0;
      overflow: auto;
      padding: 14px;
      flex: 1 1 auto;
    }
    .inspector-panel[hidden] {
      display: none;
    }
    .panel {
      border: 1px solid #e3dac8;
      border-radius: 8px;
      padding: 12px;
      background: #fffefa;
      box-shadow: 0 6px 14px rgba(23, 32, 42, 0.07);
      margin-bottom: 12px;
    }
    .panel h2 {
      margin: 0 0 9px;
      font-size: 15px;
      line-height: 1.3;
    }
    .panel h3 {
      margin: 13px 0 5px;
      color: #526070;
      font-size: 12px;
      text-transform: uppercase;
    }
    .panel p, .panel li {
      font-size: 13px;
      line-height: 1.45;
    }
    .panel p {
      margin: 0;
    }
    .panel ul {
      margin: 0;
      padding-left: 18px;
    }
    .badges {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin: 8px 0;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      min-height: 22px;
      padding: 2px 7px;
      border-radius: 999px;
      background: #eef2f7;
      color: #334155;
      border: 1px solid #d6dee9;
      font-size: 12px;
      white-space: nowrap;
    }
    .p0 { background: #fee2e2; color: #991b1b; border-color: #fecaca; }
    .p1 { background: #ffedd5; color: #9a3412; border-color: #fed7aa; }
    .p2 { background: #dbeafe; color: #1e40af; border-color: #bfdbfe; }
    .p3 { background: #e2e8f0; color: #334155; border-color: #cbd5e1; }
    .work-active-badge { background: #dbeafe; color: #1d4ed8; border-color: #bfdbfe; }
    .work-done-badge { background: #dcfce7; color: #166534; border-color: #bbf7d0; }
    .work-next-badge { background: #fef3c7; color: #92400e; border-color: #fde68a; }
    .work-pending-badge { background: #e2e8f0; color: #334155; border-color: #cbd5e1; }
    .work-blocked-badge { background: #fee2e2; color: #991b1b; border-color: #fecaca; }
    .work-deferred-badge { background: #f3f4f6; color: #4b5563; border-color: #d1d5db; }
    .queue-item {
      border-top: 1px solid #ece3d4;
      padding: 9px 0;
    }
    .queue-item:first-child {
      border-top: 0;
      padding-top: 0;
    }
    .queue-item b {
      display: block;
      margin-top: 5px;
      font-size: 13px;
      line-height: 1.35;
    }
    .queue-note {
      display: block;
      margin-top: 4px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
      overflow-wrap: anywhere;
    }
    .queue-item .badge {
      display: inline-flex;
      width: auto;
      margin: 0 4px 3px 0;
      vertical-align: middle;
    }
    .queue-item button[data-focus-node] {
      height: auto;
      margin: 0;
      padding: 0;
      border: 0;
      background: transparent;
      color: #17202a;
      box-shadow: none;
      font: inherit;
      text-align: left;
      cursor: pointer;
    }
    .queue-item button[data-focus-node]:hover {
      color: #1d4ed8;
      text-decoration: underline;
    }
    .legend {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 7px;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: #344054;
    }
    .swatch {
      width: 12px;
      height: 12px;
      border-radius: 3px;
      display: inline-block;
    }
    .editor-form {
      display: grid;
      gap: 9px;
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid #ece3d4;
    }
    .editor-form label {
      display: grid;
      gap: 4px;
      color: #526070;
      font-size: 12px;
      font-weight: 700;
    }
    .editor-form input,
    .editor-form select,
    .editor-form textarea {
      width: 100%;
      max-width: none;
      min-width: 0;
      height: auto;
      min-height: 32px;
      box-shadow: none;
      font: inherit;
      font-size: 13px;
    }
    .editor-form textarea {
      resize: vertical;
      min-height: 62px;
      padding: 8px 10px;
      line-height: 1.4;
    }
    .editor-row {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
    }
    @media (max-width: 1040px) {
      body { overflow: auto; }
      .app { height: auto; min-height: 100vh; }
      header { grid-template-columns: 1fr; }
      .workspace { grid-template-columns: 1fr; }
      .map-wrap { height: 68vh; min-height: 520px; }
      .inspector { border-left: 0; border-top: 1px solid #e1d7c4; }
      .inspector-tabs { grid-template-columns: repeat(3, minmax(0, 1fr)); }
      .minimap { width: 180px; height: 116px; }
      .stats { grid-template-columns: repeat(2, minmax(66px, auto)); }
    }
  </style>
</head>
<body>
  <div class="app">
    <header>
      <div>
        <h1 id="page-title"></h1>
        <div id="page-subtitle" class="subtitle"></div>
      </div>
      <div id="stats" class="stats"></div>
    </header>
    <main class="workspace">
      <section class="map-wrap">
        <div class="toolbar">
          <input id="search" type="search" placeholder="搜索目标、能力、缺口、P0 子任务">
          <select id="status-filter" aria-label="状态筛选"><option value="all">全部状态</option></select>
          <select id="work-filter" aria-label="施工状态筛选"><option value="all">全部施工</option></select>
          <select id="priority-filter" aria-label="优先级筛选">
            <option value="all">全部优先级</option>
            <option value="P0">P0</option>
            <option value="P1">P1</option>
            <option value="P2">P2</option>
            <option value="P3">P3</option>
          </select>
          <button id="zoom-out" title="缩小">-</button>
          <button id="zoom-in" title="放大">+</button>
          <button id="fit" title="全图适配">Fit</button>
          <button id="reset" title="重置筛选">Reset</button>
          <button id="edit-toggle" title="开启手动编辑">编辑</button>
          <button id="add-child" class="edit-only" title="给当前节点新增一个子节点">新增子节点</button>
          <button id="auto-layout" class="edit-only" title="清除手动坐标并重新自动排布">自动布局</button>
          <button id="bind-json" class="edit-only" title="授权后自动写回一个 JSON 文件">绑定JSON</button>
          <button id="export-json" class="edit-only" title="导出当前编辑后的 JSON">导出JSON</button>
          <button id="discard-draft" class="edit-only" title="删除浏览器本地草稿并恢复内嵌数据">丢弃草稿</button>
          <span id="save-status" class="save-status">只读</span>
        </div>
        <svg id="map" role="img" aria-label="Outcome backward capability map">
          <g id="viewport">
            <g id="bands"></g>
            <g id="links"></g>
            <g id="nodes"></g>
          </g>
        </svg>
        <div class="minimap">
          <div class="minimap-title">Overview</div>
          <svg id="mini"></svg>
        </div>
      </section>
      <aside class="inspector">
        <nav class="inspector-tabs" aria-label="右侧面板">
          <button class="inspector-tab active" type="button" data-panel-tab="details">节点</button>
          <button class="inspector-tab" type="button" data-panel-tab="work">施工</button>
          <button class="inspector-tab" type="button" data-panel-tab="queue">队列</button>
          <button class="inspector-tab" type="button" data-panel-tab="coverage">审查</button>
          <button class="inspector-tab" type="button" data-panel-tab="legend">图例</button>
        </nav>
        <div class="inspector-body">
          <section class="panel inspector-panel" data-panel="details" id="details"></section>
          <section class="panel inspector-panel" data-panel="work" id="work-board" hidden></section>
          <section class="panel inspector-panel" data-panel="queue" hidden>
            <h2>P0-P3 队列</h2>
            <div id="queue"></div>
          </section>
          <section class="panel inspector-panel" data-panel="coverage" hidden>
            <h2>覆盖审查</h2>
            <div id="coverage"></div>
          </section>
          <section class="panel inspector-panel" data-panel="legend" hidden>
            <h2>图例</h2>
            <div id="legend" class="legend"></div>
          </section>
        </div>
      </aside>
    </main>
  </div>
  <script id="outcome-data" type="application/json">__OUTCOME_DATA__</script>
  <script>
    const data = JSON.parse(document.getElementById('outcome-data').textContent);
    const embeddedData = typeof structuredClone === 'function'
      ? structuredClone(data)
      : JSON.parse(JSON.stringify(data));
    const labels = __STATUS_LABELS__;
    const workLabels = __WORK_LABELS__;
    const priorityRank = { P0: 0, P1: 1, P2: 2, P3: 3 };
    const statusRank = { target: 0, ruler: 1, weak: 2, missing: 3, risk: 4, partial: 5, exists: 6, done: 7 };
    const workRank = { active: 0, done: 1, next: 2, blocked: 3, pending: 4, deferred: 5 };
    const draftBaseKey = `outcome-tree-draft:${data.project?.sourcePath || location.pathname}`;
    const embeddedVersion = data.version || 'unversioned';
    const draftKey = `${draftBaseKey}:${embeddedVersion}`;
    const draftLoad = loadDraft();
    const loadedDraft = draftLoad.data;
    let draftNotice = draftLoad.notice;
    if (loadedDraft?.nodes?.length) {
      Object.keys(data).forEach(key => delete data[key]);
      Object.assign(data, loadedDraft);
    }
    data.editor = data.editor || {};
    data.editor.positions = data.editor.positions || {};
    let layerLabels = data.mapLayers || ['Outcome', 'Ruler', 'Capability', 'Evidence / Interface', 'Sub-capability', 'Detail'];
    const svgNS = 'http://www.w3.org/2000/svg';
    const map = document.getElementById('map');
    const viewport = document.getElementById('viewport');
    const bandsEl = document.getElementById('bands');
    const linksEl = document.getElementById('links');
    const nodesEl = document.getElementById('nodes');
    const mini = document.getElementById('mini');
    const rawNodes = data.nodes || [];
    const byId = new Map();
    const children = new Map();
    let root = null;
    const nodeW = 238;
    const nodeH = 78;
    const xGap = 330;
    const yGap = 128;
    const margin = 92;
    let activeId = null;
    let transform = { x: 0, y: 0, k: 1 };
    let bounds = { x: 0, y: 0, width: 1000, height: 700, maxDepth: 1 };
    let isDragging = false;
    let dragStart = null;
    let nodeDrag = null;
    let editMode = false;
    let saveTimer = null;
    let fileHandle = null;
    let visibleNodeIds = new Set(rawNodes.map(node => node.id));

    function loadDraft() {
      try {
        const raw = localStorage.getItem(draftKey);
        if (raw) {
          const parsed = JSON.parse(raw);
          return { data: parsed, notice: '已载入本版本草稿' };
        }
        const legacyRaw = localStorage.getItem(draftBaseKey);
        if (legacyRaw) {
          const legacy = JSON.parse(legacyRaw);
          if ((legacy.version || 'unversioned') === embeddedVersion) {
            localStorage.setItem(draftKey, legacyRaw);
            localStorage.removeItem(draftBaseKey);
            return { data: legacy, notice: '已迁移本版本草稿' };
          }
          return { data: null, notice: '已忽略旧版本草稿' };
        }
        return { data: null, notice: '只读' };
      } catch (error) {
        console.warn('Could not load local draft', error);
        return { data: null, notice: '草稿读取失败' };
      }
    }

    function rebuildIndexes() {
      byId.clear();
      children.clear();
      rawNodes.forEach(node => {
        byId.set(node.id, node);
        const parentId = node.parentId || '__root__';
        if (!children.has(parentId)) children.set(parentId, []);
        children.get(parentId).push(node);
      });
      children.forEach(items => items.sort((a, b) => {
        const pa = priorityRank[a.priority] ?? 9;
        const pb = priorityRank[b.priority] ?? 9;
        if (pa !== pb) return pa - pb;
        const sa = statusRank[a.status || 'partial'] ?? 9;
        const sb = statusRank[b.status || 'partial'] ?? 9;
        if (sa !== sb) return sa - sb;
        return String(a.title || a.id).localeCompare(String(b.title || b.id), 'zh-CN');
      }));
      root = (children.get('__root__') || [])[0] || rawNodes[0] || null;
      if (!activeId || !byId.has(activeId)) activeId = root ? root.id : null;
    }

    rebuildIndexes();

    function layoutTree() {
      let cursor = 0;
      let maxDepth = 0;
      rawNodes.forEach(node => {
        delete node._depth;
        delete node._x;
        delete node._y;
      });
      function place(node, depth) {
        if (!node || node._depth !== undefined) return;
        node._depth = depth;
        maxDepth = Math.max(maxDepth, depth);
        const kids = children.get(node.id) || [];
        if (!kids.length) {
          node._y = margin + cursor * yGap;
          cursor += 1;
        } else {
          kids.forEach(child => place(child, depth + 1));
          node._y = kids.reduce((sum, child) => sum + child._y, 0) / kids.length;
        }
        node._x = margin + depth * xGap;
      }
      if (root) place(root, 0);
      rawNodes.forEach(node => {
        if (node._depth === undefined) {
          node._depth = 0;
          node._x = margin;
          node._y = margin + cursor * yGap;
          cursor += 1;
        }
        const saved = data.editor?.positions?.[node.id];
        if (saved && Number.isFinite(saved.x) && Number.isFinite(saved.y)) {
          node._x = saved.x;
          node._y = saved.y;
        }
      });
      const leaves = Math.max(1, cursor);
      const maxX = Math.max(...rawNodes.map(node => node._x || 0), margin);
      const maxY = Math.max(...rawNodes.map(node => node._y || 0), margin);
      bounds = {
        x: 0,
        y: 0,
        width: Math.max(margin * 2 + maxDepth * xGap + nodeW, maxX + nodeW + margin),
        height: Math.max(margin * 2 + Math.max(1, leaves - 1) * yGap + nodeH, maxY + nodeH + margin),
        maxDepth
      };
    }

    function textIndex(node) {
      return [
        node.title, node.summary, node.status, node.priority, node.ownerLens,
        node.workStatus, node.workNote, node.completedAt, node.proofGate, node.missingProof, node.nextSubtask,
        ...(node.existingSupport || []),
        ...(node.gaps || []),
        ...(node.evidence || []),
        ...(node.risks || [])
      ].filter(Boolean).join(' ').toLowerCase();
    }

    function directMatch(node) {
      const q = document.getElementById('search').value.trim().toLowerCase();
      const status = document.getElementById('status-filter').value;
      const workStatus = document.getElementById('work-filter').value;
      const priority = document.getElementById('priority-filter').value;
      if (status !== 'all' && (node.status || 'partial') !== status) return false;
      if (workStatus !== 'all' && (node.workStatus || 'pending') !== workStatus) return false;
      if (priority !== 'all' && node.priority !== priority) return false;
      if (q && !textIndex(node).includes(q)) return false;
      return true;
    }

    function updateVisibility() {
      visibleNodeIds = new Set();
      rawNodes.forEach(node => {
        if (directMatch(node)) visibleNodeIds.add(node.id);
      });
      if (visibleNodeIds.size === rawNodes.length) return;
      const addRelatives = id => {
        let current = byId.get(id);
        while (current) {
          visibleNodeIds.add(current.id);
          current = byId.get(current.parentId);
        }
        (children.get(id) || []).forEach(child => visibleNodeIds.add(child.id));
      };
      [...visibleNodeIds].forEach(addRelatives);
    }

    function renderMap() {
      layoutTree();
      updateVisibility();
      clear(bandsEl);
      clear(linksEl);
      clear(nodesEl);
      renderBands();
      renderLinks();
      renderNodes();
      updateSelection();
      renderMiniMap();
      applyTransform();
    }

    function renderBands() {
      for (let depth = 0; depth <= bounds.maxDepth; depth += 1) {
        const x = margin - 38 + depth * xGap;
        const rect = el('rect', {
          x,
          y: 34,
          width: xGap - 42,
          height: Math.max(420, bounds.height - 68),
          rx: 8,
          class: 'band'
        });
        const label = el('text', {
          x: x + 12,
          y: 58,
          class: 'band-label'
        });
        label.textContent = layerLabels[depth] || `Layer ${depth}`;
        bandsEl.append(rect, label);
      }
    }

    function renderLinks() {
      rawNodes.filter(node => node.parentId).forEach(node => {
        const parent = byId.get(node.parentId);
        if (!parent) return;
        const path = el('path', {
          d: linkPath(parent, node),
          class: ['link', String(node.priority || '').toLowerCase()].filter(Boolean).join(' '),
          'data-source': parent.id,
          'data-target': node.id
        });
        linksEl.append(path);
      });
    }

    function renderNodes() {
      rawNodes.forEach(node => {
        const workStatus = node.workStatus || 'pending';
        const group = el('g', {
          class: `map-node status-${node.status || 'partial'} work-${workStatus}`,
          transform: `translate(${node._x}, ${node._y})`,
          'data-node-id': node.id
        });
        const rect = el('rect', { class: 'node-card', width: nodeW, height: nodeH, rx: 8 });
        const strip = el('rect', {
          class: `status-strip status-${node.status || 'partial'}`,
          width: 8,
          height: nodeH,
          rx: 4
        });
        group.append(rect, strip);
        appendWrappedText(group, node.title || node.id, 18, 22, 18, 2, 'node-title');
        appendWrappedText(group, node.summary || '', 18, 52, 28, 1, 'node-summary');
        drawPill(group, labels[node.status] || node.status || 'partial', 16, nodeH - 20, 58);
        if (node.priority) drawPill(group, node.priority, 82, nodeH - 20, 34);
        if (node.workStatus) {
          group.append(el('circle', {
            cx: nodeW - 17,
            cy: nodeH - 14,
            r: 6,
            class: `work-dot work-${workStatus}-fill`
          }));
        }
        if (node.score !== undefined && node.score !== null) {
          const cx = nodeW - 25;
          group.append(el('circle', { cx, cy: 23, r: 17, class: 'score-ring' }));
          const score = el('text', { x: cx, y: 23, class: 'score-text' });
          score.textContent = node.score;
          group.append(score);
        }
        group.addEventListener('click', event => {
          event.stopPropagation();
          activeId = node.id;
          updateSelection();
          renderDetails();
          showInspectorPanel('details');
        });
        group.addEventListener('mousedown', event => {
          if (!editMode) return;
          event.preventDefault();
          event.stopPropagation();
          activeId = node.id;
          const point = screenToWorld(event.clientX, event.clientY);
          nodeDrag = {
            id: node.id,
            startX: point.x,
            startY: point.y,
            nodeX: node._x,
            nodeY: node._y
          };
          updateSelection();
          renderDetails();
          showInspectorPanel('details');
        });
        nodesEl.append(group);
      });
    }

    function linkPath(source, target) {
      const x1 = source._x + nodeW;
      const y1 = source._y + nodeH / 2;
      const x2 = target._x;
      const y2 = target._y + nodeH / 2;
      const bend = Math.max(90, (x2 - x1) * 0.46);
      return `M ${x1} ${y1} C ${x1 + bend} ${y1}, ${x2 - bend} ${y2}, ${x2} ${y2}`;
    }

    function appendWrappedText(parent, text, x, y, maxChars, maxLines, className) {
      const lines = wrapText(String(text || ''), maxChars, maxLines);
      lines.forEach((line, index) => {
        const t = el('text', { x, y: y + index * 14, class: className });
        t.textContent = line;
        parent.append(t);
      });
    }

    function wrapText(text, maxChars, maxLines) {
      if (!text) return [];
      const chars = [...text.replace(/\\s+/g, ' ').trim()];
      const lines = [];
      let current = '';
      chars.forEach(ch => {
        if (visualLength(current + ch) > maxChars) {
          lines.push(current);
          current = ch;
        } else {
          current += ch;
        }
      });
      if (current) lines.push(current);
      if (lines.length > maxLines) {
        const kept = lines.slice(0, maxLines);
        kept[maxLines - 1] = kept[maxLines - 1].replace(/[，。；、,. ]+$/g, '') + '...';
        return kept;
      }
      return lines;
    }

    function visualLength(text) {
      return [...text].reduce((sum, ch) => sum + (/[\u4e00-\u9fff]/.test(ch) ? 1.8 : 1), 0);
    }

    function drawPill(parent, text, x, y, width) {
      parent.append(el('rect', { x, y, width, height: 17, rx: 8, class: 'pill-bg' }));
      const t = el('text', { x: x + 8, y: y + 12, class: 'pill-text' });
      t.textContent = text;
      parent.append(t);
    }

    function updateSelection() {
      const active = byId.get(activeId);
      const related = new Set();
      let cursor = active;
      while (cursor) {
        related.add(cursor.id);
        cursor = byId.get(cursor.parentId);
      }
      function addDesc(id) {
        related.add(id);
        (children.get(id) || []).forEach(child => addDesc(child.id));
      }
      if (active) addDesc(active.id);
      document.querySelectorAll('.map-node').forEach(group => {
        const id = group.dataset.nodeId;
        group.classList.toggle('selected', id === activeId);
        group.classList.toggle('dimmed', !visibleNodeIds.has(id) || (active && !related.has(id)));
      });
      document.querySelectorAll('.link').forEach(link => {
        const source = link.dataset.source;
        const target = link.dataset.target;
        const inVisibleSet = visibleNodeIds.has(source) && visibleNodeIds.has(target);
        const selectedLink = active && related.has(source) && related.has(target);
        link.classList.toggle('dimmed', !inVisibleSet || (active && !selectedLink));
        link.classList.toggle('highlight', selectedLink);
      });
      updateMiniViewport();
    }

    function renderDetails() {
      const node = byId.get(activeId) || root;
      const details = document.getElementById('details');
      if (!node) {
        details.innerHTML = '<h2>节点详情</h2><p>没有节点。</p>';
        return;
      }
      details.innerHTML = `
        <h2>${escapeHtml(node.title || node.id)}</h2>
        <p>${escapeHtml(node.summary || '')}</p>
        <div class="badges">
          ${badge(labels[node.status] || node.status || '部分可用')}
          ${badge(node.priority, String(node.priority || '').toLowerCase())}
          ${badge(workLabels[node.workStatus] || node.workStatus, `work-${node.workStatus}-badge`)}
          ${badge(node.ownerLens)}
          ${node.score === undefined ? '' : badge('score ' + node.score)}
        </div>
        ${sectionText('施工状态', node.workNote)}
        ${sectionText('完成时间', node.completedAt)}
        ${sectionText('本节点作为结果', node.localResult)}
        ${sectionText('模拟达成样例', node.targetShape)}
        ${sectionText('父结果为什么需要它', node.directCauseForParent)}
        ${sectionText('需要类型', node.needType || node.causeType)}
        ${sectionText('父子关系证明', node.edgeProof)}
        ${sectionText('证明门槛', node.proofGate)}
        ${sectionText('缺失证明', node.missingProof)}
        ${sectionList('现有可用', node.existingSupport)}
        ${sectionList('缺口', node.gaps)}
        ${sectionList('证据', node.evidence)}
        ${sectionList('风险/边界', node.risks)}
        ${sectionText('下一步', node.nextSubtask)}
        ${editMode ? renderEditPanel(node) : ''}
      `;
      if (editMode) bindEditPanel(details, node);
    }

    function renderEditPanel(node) {
      const canChangeParent = node.id !== root?.id;
      const parentOptions = rawNodes
        .filter(candidate => candidate.id !== node.id && !isDescendant(candidate.id, node.id))
        .map(candidate => `<option value="${escapeHtml(candidate.id)}" ${node.parentId === candidate.id ? 'selected' : ''}>${escapeHtml(candidate.title || candidate.id)}</option>`)
        .join('');
      return `
        <div class="editor-form" data-editor-node="${escapeHtml(node.id)}">
          <h3>手动编辑</h3>
          <label>父节点连接
            <select data-edit-field="parentId" ${canChangeParent ? '' : 'disabled'}>
              ${canChangeParent ? parentOptions : `<option value="">root</option>`}
            </select>
          </label>
          <label>标题
            <input data-edit-field="title" value="${escapeHtml(node.title || '')}">
          </label>
          <label>摘要
            <textarea data-edit-field="summary">${escapeHtml(node.summary || '')}</textarea>
          </label>
          <div class="editor-row">
            <label>状态
              <select data-edit-field="status">${selectOptions(labels, node.status || 'partial')}</select>
            </label>
            <label>优先级
              <select data-edit-field="priority">${['P0','P1','P2','P3'].map(p => `<option value="${p}" ${node.priority === p ? 'selected' : ''}>${p}</option>`).join('')}</select>
            </label>
            <label>分数
              <input data-edit-field="score" type="number" min="0" max="100" value="${escapeHtml(node.score ?? '')}">
            </label>
          </div>
          <div class="editor-row">
            <label>施工
              <select data-edit-field="workStatus"><option value="">无</option>${selectOptions(workLabels, node.workStatus || '')}</select>
            </label>
            <label>需要类型
              <input data-edit-field="needType" value="${escapeHtml(node.needType || '')}">
            </label>
            <label>Owner lens
              <input data-edit-field="ownerLens" value="${escapeHtml(node.ownerLens || '')}">
            </label>
          </div>
          <label>本节点作为结果
            <textarea data-edit-field="localResult">${escapeHtml(node.localResult || '')}</textarea>
          </label>
          <label>模拟达成样例
            <textarea data-edit-field="targetShape">${escapeHtml(node.targetShape || '')}</textarea>
          </label>
          <label>父结果为什么需要它
            <textarea data-edit-field="directCauseForParent">${escapeHtml(node.directCauseForParent || '')}</textarea>
          </label>
          <label>父子关系证明
            <textarea data-edit-field="edgeProof">${escapeHtml(node.edgeProof || '')}</textarea>
          </label>
          <label>证明门槛
            <textarea data-edit-field="proofGate">${escapeHtml(node.proofGate || '')}</textarea>
          </label>
        </div>
      `;
    }

    function selectOptions(options, current) {
      return Object.entries(options).map(([value, label]) => (
        `<option value="${escapeHtml(value)}" ${value === current ? 'selected' : ''}>${escapeHtml(label)}</option>`
      )).join('');
    }

    function bindEditPanel(container, node) {
      container.querySelectorAll('[data-edit-field]').forEach(field => {
        field.addEventListener('input', () => applyFieldEdit(node, field));
        field.addEventListener('change', () => applyFieldEdit(node, field));
      });
    }

    function applyFieldEdit(node, field) {
      const key = field.dataset.editField;
      let value = field.value;
      if (key === 'parentId') {
        updateParent(node, value || null);
        return;
      }
      if (key === 'score') {
        value = value === '' ? undefined : clamp(Number(value), 0, 100);
      }
      if (value === undefined || value === '') {
        delete node[key];
      } else {
        node[key] = value;
      }
      recomputeMetrics();
      renderStats();
      renderMap();
      scheduleSave('已自动保存草稿');
    }

    function updateParent(node, nextParentId) {
      if (!nextParentId || nextParentId === node.id || isDescendant(nextParentId, node.id)) return;
      node.parentId = nextParentId;
      delete data.editor.positions[node.id];
      rebuildIndexes();
      recomputeMetrics();
      renderStats();
      renderMap();
      renderDetails();
      scheduleSave('已自动保存连接');
    }

    function isDescendant(candidateId, ancestorId) {
      let cursor = byId.get(candidateId);
      while (cursor?.parentId) {
        if (cursor.parentId === ancestorId) return true;
        cursor = byId.get(cursor.parentId);
      }
      return false;
    }

    function renderQueue() {
      const tasks = [...(data.subtasks || [])].sort((a, b) => {
        const pa = priorityRank[a.priority] ?? 9;
        const pb = priorityRank[b.priority] ?? 9;
        return pa - pb;
      });
        const queue = document.getElementById('queue');
      if (!tasks.length) {
        queue.innerHTML = '<p>没有子任务。</p>';
        return;
      }
      queue.innerHTML = tasks.map(task => `
        <div class="queue-item">
          ${badge(task.priority, String(task.priority || '').toLowerCase())}
          ${badge(workLabels[task.workStatus] || task.workStatus, `work-${task.workStatus}-badge`)}
          <b>${escapeHtml(task.title || '')}</b>
          <span class="queue-note">${escapeHtml(task.acceptance || task.why || '')}</span>
        </div>
      `).join('');
    }

    function renderCoverage() {
      const items = data.coverageReview || [];
      const coverage = document.getElementById('coverage');
      if (!items.length) {
        coverage.innerHTML = '<p>这份图还没有记录二轮覆盖审查。</p>';
        return;
      }
      coverage.innerHTML = items.map(item => `
        <div class="queue-item">
          ${badge(item.lens || 'lens')}
          <b>${escapeHtml(item.finding || '')}</b>
          <span class="queue-note">${escapeHtml(item.treeChange || '')}</span>
          ${item.residualRisk ? `<span class="queue-note">${escapeHtml('Residual risk: ' + item.residualRisk)}</span>` : ''}
        </div>
      `).join('');
    }

    function renderLegend() {
      document.getElementById('legend').innerHTML = Object.entries(labels).map(([key, value]) => `
        <div class="legend-item"><span class="swatch status-${key}"></span>${escapeHtml(value)}</div>
      `).join('') + Object.entries(workLabels).map(([key, value]) => `
        <div class="legend-item"><span class="swatch work-${key}-fill"></span>${escapeHtml(value)}</div>
      `).join('');
      const statusFilter = document.getElementById('status-filter');
      Object.entries(labels).forEach(([key, value]) => {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = value;
        statusFilter.append(option);
      });
      const workFilter = document.getElementById('work-filter');
      Object.entries(workLabels).forEach(([key, value]) => {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = value;
        workFilter.append(option);
      });
    }

    function renderStats() {
      const m = data.metrics || {};
      const sc = m.statusCounts || {};
      const wc = m.workCounts || {};
      const weakCount = (sc.weak || 0) + (sc.missing || 0) + (sc.risk || 0);
      const items = [
        ['节点', m.nodeCount ?? rawNodes.length],
        ['平均分', m.averageScore ?? '--'],
        ['施工中', wc.active || 0],
        ['已修复', wc.done || 0],
        ['薄弱/缺口/风险', weakCount],
        ['P0', (m.priorityCounts || {}).P0 || 0]
      ];
      document.getElementById('stats').innerHTML = items.map(([label, value]) => `
        <div class="stat"><b>${escapeHtml(String(value))}</b><span>${escapeHtml(label)}</span></div>
      `).join('');
    }

    function renderWorkBoard() {
      const board = document.getElementById('work-board');
      const active = rawNodes
        .filter(node => node.workStatus === 'active')
        .sort((a, b) => (priorityRank[a.priority] ?? 9) - (priorityRank[b.priority] ?? 9));
      const done = rawNodes
        .filter(node => node.workStatus === 'done')
        .sort((a, b) => String(b.completedAt || '').localeCompare(String(a.completedAt || '')));
      const next = rawNodes
        .filter(node => node.workStatus === 'next')
        .sort((a, b) => (priorityRank[a.priority] ?? 9) - (priorityRank[b.priority] ?? 9));
      board.innerHTML = `
        <h2>施工进度</h2>
        ${workGroup('正在修', active)}
        ${workGroup('已修复', done.slice(0, 5))}
        ${workGroup('下一步', next)}
      `;
    }

    function showInspectorPanel(panelName) {
      const name = panelName || 'details';
      document.querySelectorAll('.inspector-panel').forEach(panel => {
        panel.hidden = panel.dataset.panel !== name;
      });
      document.querySelectorAll('.inspector-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.panelTab === name);
      });
      const body = document.querySelector('.inspector-body');
      if (body) body.scrollTop = 0;
    }

    function workGroup(title, nodes) {
      if (!nodes.length) return `<h3>${escapeHtml(title)}</h3><p>暂无。</p>`;
      return `
        <h3>${escapeHtml(title)}</h3>
        ${nodes.map(node => `
          <div class="queue-item">
            ${badge(node.priority, String(node.priority || '').toLowerCase())}
            ${badge(workLabels[node.workStatus] || node.workStatus, `work-${node.workStatus}-badge`)}
            <b><button type="button" data-focus-node="${escapeHtml(node.id)}">${escapeHtml(node.title || node.id)}</button></b>
            <span class="queue-note">${escapeHtml(node.workNote || node.nextSubtask || node.summary || '')}</span>
          </div>
        `).join('')}
      `;
    }

    function sectionText(title, value) {
      if (!value) return '';
      return `<h3>${escapeHtml(title)}</h3><p>${escapeHtml(value)}</p>`;
    }

    function sectionList(title, values) {
      if (!values || !values.length) return '';
      return `<h3>${escapeHtml(title)}</h3><ul>${values.map(v => `<li>${escapeHtml(v)}</li>`).join('')}</ul>`;
    }

    function badge(value, cls = '') {
      if (!value) return '';
      return `<span class="badge ${escapeHtml(cls)}">${escapeHtml(value)}</span>`;
    }

    function serializableData() {
      const clone = JSON.parse(JSON.stringify(data));
      (clone.nodes || []).forEach(node => {
        Object.keys(node).forEach(key => {
          if (key.startsWith('_')) delete node[key];
        });
      });
      clone.project = clone.project || {};
      clone.project.editedAt = new Date().toISOString();
      clone.metrics = computeMetrics();
      return clone;
    }

    function scheduleSave(message = '已自动保存草稿') {
      updateSaveStatus('保存中...');
      window.clearTimeout(saveTimer);
      saveTimer = window.setTimeout(async () => {
        const payload = serializableData();
        try {
          localStorage.setItem(draftKey, JSON.stringify(payload));
          if (fileHandle) await writeBoundFile(payload);
          updateSaveStatus(fileHandle ? '已自动保存到 JSON' : message);
        } catch (error) {
          console.error(error);
          updateSaveStatus('保存失败');
        }
      }, 240);
    }

    async function writeBoundFile(payload = serializableData()) {
      if (!fileHandle) return;
      const writable = await fileHandle.createWritable();
      await writable.write(JSON.stringify(payload, null, 2));
      await writable.close();
    }

    function updateSaveStatus(text) {
      const status = document.getElementById('save-status');
      if (status) status.textContent = text;
    }

    function computeMetrics() {
      const statusCounts = {};
      const workCounts = {};
      const priorityCounts = {};
      const scores = [];
      rawNodes.forEach(node => {
        const status = node.status || 'partial';
        statusCounts[status] = (statusCounts[status] || 0) + 1;
        if (node.workStatus) workCounts[node.workStatus] = (workCounts[node.workStatus] || 0) + 1;
        if (node.priority) priorityCounts[node.priority] = (priorityCounts[node.priority] || 0) + 1;
        if (typeof node.score === 'number' && Number.isFinite(node.score)) scores.push(node.score);
      });
      return {
        nodeCount: rawNodes.length,
        statusCounts,
        workCounts,
        priorityCounts,
        averageScore: scores.length ? Math.round((scores.reduce((a, b) => a + b, 0) / scores.length) * 10) / 10 : null
      };
    }

    function recomputeMetrics() {
      data.metrics = computeMetrics();
    }

    function addChildNode() {
      if (!editMode) return;
      const parent = byId.get(activeId) || root;
      const id = uniqueNodeId('node');
      const node = {
        id,
        parentId: parent?.id,
        title: '新节点',
        summary: '填写这个父结果直接需要的子结果。',
        status: 'partial',
        priority: 'P0',
        score: 0,
        needType: 'capability',
        localResult: '这个节点作为局部结果成立时是什么。',
        targetShape: '模拟：<clean_placeholder_output>。',
        directCauseForParent: '说明父结果为什么直接需要这个子结果。',
        edgeProof: '如果缺少这个子结果，父结果哪里不成立。'
      };
      rawNodes.push(node);
      rebuildIndexes();
      activeId = id;
      recomputeMetrics();
      renderStats();
      renderMap();
      renderDetails();
      scheduleSave('已自动保存新节点');
    }

    function uniqueNodeId(prefix) {
      let base = `${prefix}:${Date.now().toString(36)}`;
      let id = base;
      let index = 1;
      while (byId.has(id)) {
        id = `${base}-${index}`;
        index += 1;
      }
      return id;
    }

    function clearManualLayout() {
      data.editor.positions = {};
      renderMap();
      scheduleSave('已自动保存自动布局');
    }

    function exportJson() {
      const payload = JSON.stringify(serializableData(), null, 2);
      const blob = new Blob([payload], { type: 'application/json;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'outcome-tree.edited.json';
      document.body.append(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      updateSaveStatus('已导出 JSON');
    }

    async function bindJsonFile() {
      if (!window.showOpenFilePicker) {
        updateSaveStatus('当前浏览器不支持绑定文件');
        return;
      }
      try {
        const [handle] = await window.showOpenFilePicker({
          multiple: false,
          types: [{ description: 'Outcome tree JSON', accept: { 'application/json': ['.json'] } }]
        });
        fileHandle = handle;
        await writeBoundFile();
        updateSaveStatus('已绑定并写回 JSON');
      } catch (error) {
        if (error?.name !== 'AbortError') {
          console.error(error);
          updateSaveStatus('绑定失败');
        }
      }
    }

    function discardDraft() {
      localStorage.removeItem(draftKey);
      localStorage.removeItem(draftBaseKey);
      Object.keys(data).forEach(key => delete data[key]);
      Object.assign(data, JSON.parse(JSON.stringify(embeddedData)));
      data.editor = data.editor || {};
      data.editor.positions = data.editor.positions || {};
      layerLabels = data.mapLayers || layerLabels;
      rawNodes.splice(0, rawNodes.length, ...(data.nodes || []));
      data.nodes = rawNodes;
      rebuildIndexes();
      activeId = root ? root.id : null;
      recomputeMetrics();
      renderStats();
      renderMap();
      renderDetails();
      updateSaveStatus('已丢弃本地草稿');
      draftNotice = '只读';
    }

    function screenToWorld(clientX, clientY) {
      const rect = map.getBoundingClientRect();
      return {
        x: (clientX - rect.left - transform.x) / transform.k,
        y: (clientY - rect.top - transform.y) / transform.k
      };
    }

    function zoomAt(clientX, clientY, factor) {
      const rect = map.getBoundingClientRect();
      const px = clientX - rect.left;
      const py = clientY - rect.top;
      const oldK = transform.k;
      const nextK = clamp(oldK * factor, 0.18, 2.6);
      const worldX = (px - transform.x) / oldK;
      const worldY = (py - transform.y) / oldK;
      transform.x = px - worldX * nextK;
      transform.y = py - worldY * nextK;
      transform.k = nextK;
      applyTransform();
    }

    function fitMap() {
      const rect = map.getBoundingClientRect();
      const pad = 82;
      const scale = Math.min(
        (rect.width - pad) / Math.max(bounds.width, 1),
        (rect.height - pad) / Math.max(bounds.height, 1),
        1.18
      );
      transform.k = Math.max(0.18, scale);
      transform.x = (rect.width - bounds.width * transform.k) / 2;
      transform.y = (rect.height - bounds.height * transform.k) / 2;
      applyTransform();
    }

    function applyTransform() {
      viewport.setAttribute('transform', `translate(${transform.x},${transform.y}) scale(${transform.k})`);
      updateMiniViewport();
    }

    function renderMiniMap() {
      clear(mini);
      const miniW = 220;
      const miniH = 142;
      mini.setAttribute('viewBox', `0 0 ${miniW} ${miniH}`);
      const scale = Math.min((miniW - 18) / bounds.width, (miniH - 24) / bounds.height);
      const ox = 9;
      const oy = 19;
      rawNodes.forEach(node => {
        mini.append(el('rect', {
          x: ox + node._x * scale,
          y: oy + node._y * scale,
          width: Math.max(3, nodeW * scale),
          height: Math.max(2, nodeH * scale),
          rx: 1.4,
          fill: statusColor(node.status),
          opacity: node.id === activeId ? 1 : 0.62
        }));
      });
      mini.append(el('rect', {
        id: 'mini-viewport',
        x: 0,
        y: 0,
        width: 1,
        height: 1,
        fill: 'none',
        stroke: '#111827',
        'stroke-width': 1.4
      }));
      mini.dataset.scale = scale;
      mini.dataset.ox = ox;
      mini.dataset.oy = oy;
      updateMiniViewport();
    }

    function updateMiniViewport() {
      const box = document.getElementById('mini-viewport');
      if (!box) return;
      const scale = Number(mini.dataset.scale || 1);
      const ox = Number(mini.dataset.ox || 0);
      const oy = Number(mini.dataset.oy || 0);
      const rect = map.getBoundingClientRect();
      const wx = -transform.x / transform.k;
      const wy = -transform.y / transform.k;
      const ww = rect.width / transform.k;
      const wh = rect.height / transform.k;
      box.setAttribute('x', ox + wx * scale);
      box.setAttribute('y', oy + wy * scale);
      box.setAttribute('width', Math.max(6, ww * scale));
      box.setAttribute('height', Math.max(6, wh * scale));
    }

    function statusColor(status) {
      return ({
        target: '#0f766e',
        ruler: '#2f63b7',
        exists: '#2f7d32',
        partial: '#b45f06',
        weak: '#b42318',
        missing: '#7a3db8',
        risk: '#bd1550',
        done: '#59667a'
      })[status || 'partial'] || '#b45f06';
    }

    function el(name, attrs = {}) {
      const node = document.createElementNS(svgNS, name);
      Object.entries(attrs).forEach(([key, value]) => {
        if (value !== undefined && value !== null) node.setAttribute(key, value);
      });
      return node;
    }

    function clear(node) {
      while (node.firstChild) node.removeChild(node.firstChild);
    }

    function clamp(value, min, max) {
      return Math.max(min, Math.min(max, value));
    }

    function escapeHtml(value) {
      return String(value ?? '').replace(/[&<>"']/g, ch => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
      }[ch]));
    }

    map.addEventListener('wheel', event => {
      event.preventDefault();
      zoomAt(event.clientX, event.clientY, event.deltaY < 0 ? 1.12 : 0.89);
    }, { passive: false });
    map.addEventListener('mousedown', event => {
      if (event.target.closest && event.target.closest('.map-node')) return;
      isDragging = true;
      dragStart = { x: event.clientX, y: event.clientY, tx: transform.x, ty: transform.y };
      map.classList.add('dragging');
    });
    window.addEventListener('mousemove', event => {
      if (nodeDrag) {
        const point = screenToWorld(event.clientX, event.clientY);
        const node = byId.get(nodeDrag.id);
        if (!node) return;
        const x = Math.round(nodeDrag.nodeX + point.x - nodeDrag.startX);
        const y = Math.round(nodeDrag.nodeY + point.y - nodeDrag.startY);
        data.editor.positions[node.id] = { x, y };
        node._x = x;
        node._y = y;
        renderMap();
        return;
      }
      if (!isDragging || !dragStart) return;
      transform.x = dragStart.tx + event.clientX - dragStart.x;
      transform.y = dragStart.ty + event.clientY - dragStart.y;
      applyTransform();
    });
    window.addEventListener('mouseup', () => {
      if (nodeDrag) {
        nodeDrag = null;
        scheduleSave('已自动保存布局');
      }
      isDragging = false;
      dragStart = null;
      map.classList.remove('dragging');
    });
    document.getElementById('zoom-in').addEventListener('click', () => {
      const rect = map.getBoundingClientRect();
      zoomAt(rect.left + rect.width / 2, rect.top + rect.height / 2, 1.18);
    });
    document.getElementById('zoom-out').addEventListener('click', () => {
      const rect = map.getBoundingClientRect();
      zoomAt(rect.left + rect.width / 2, rect.top + rect.height / 2, 0.84);
    });
    document.getElementById('fit').addEventListener('click', fitMap);
    document.getElementById('reset').addEventListener('click', () => {
      document.getElementById('search').value = '';
      document.getElementById('status-filter').value = 'all';
      document.getElementById('work-filter').value = 'all';
      document.getElementById('priority-filter').value = 'all';
      activeId = root ? root.id : null;
      renderMap();
      renderDetails();
      showInspectorPanel('details');
      fitMap();
    });
    document.getElementById('edit-toggle').addEventListener('click', () => {
      editMode = !editMode;
      document.body.classList.toggle('edit-mode', editMode);
      document.getElementById('edit-toggle').textContent = editMode ? '退出编辑' : '编辑';
      updateSaveStatus(editMode ? '编辑中，本地自动保存' : '只读');
      renderDetails();
      renderMap();
    });
    document.getElementById('add-child').addEventListener('click', addChildNode);
    document.getElementById('auto-layout').addEventListener('click', clearManualLayout);
    document.getElementById('bind-json').addEventListener('click', bindJsonFile);
    document.getElementById('export-json').addEventListener('click', exportJson);
    document.getElementById('discard-draft').addEventListener('click', discardDraft);
    document.getElementById('search').addEventListener('input', () => {
      updateVisibility();
      updateSelection();
    });
    document.getElementById('status-filter').addEventListener('change', () => {
      updateVisibility();
      updateSelection();
    });
    document.getElementById('work-filter').addEventListener('change', () => {
      updateVisibility();
      updateSelection();
    });
    document.getElementById('priority-filter').addEventListener('change', () => {
      updateVisibility();
      updateSelection();
    });
    document.getElementById('work-board').addEventListener('click', event => {
      const button = event.target.closest && event.target.closest('button[data-focus-node]');
      if (!button) return;
      activeId = button.dataset.focusNode;
      updateSelection();
      renderDetails();
      showInspectorPanel('details');
    });
    document.querySelectorAll('.inspector-tab').forEach(tab => {
      tab.addEventListener('click', () => showInspectorPanel(tab.dataset.panelTab));
    });
    window.addEventListener('resize', () => {
      fitMap();
      renderMiniMap();
    });

    document.getElementById('page-title').textContent = data.goal?.title || data.project?.name || 'Outcome Map';
    document.getElementById('page-subtitle').textContent = data.goal?.summary || data.project?.description || '';
    recomputeMetrics();
    renderStats();
    renderLegend();
    renderWorkBoard();
    renderQueue();
    renderCoverage();
    renderMap();
    renderDetails();
    showInspectorPanel('details');
    updateSaveStatus(draftNotice || (loadedDraft ? '已载入本版本草稿' : '只读'));
    requestAnimationFrame(fitMap);
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an outcome tree JSON file to static map HTML.")
    parser.add_argument("input", type=Path, help="Path to outcome-tree JSON.")
    parser.add_argument("--out", type=Path, default=None, help="Output HTML path.")
    args = parser.parse_args()

    data = _load_json(args.input)
    _validate(data)
    output_path = args.out or args.input.with_suffix(".html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_render_html(data, args.input), encoding="utf-8")
    print(f"Rendered outcome map: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
