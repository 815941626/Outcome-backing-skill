# Outcome Tree Renderer

This folder is the visual ledger for the `outcome-backward-working` skill.

It turns an outcome-led analysis JSON file into a standalone map-style HTML
page. The page is meant to be created before large implementation work, so the
assistant keeps the root outcome, proof gates, existing support, gaps, and
P0/P1/P2/P3 subtasks visible instead of drifting into a loose backlog.

The rendered page is intentionally closer to a large navigation map than a
document outline: pan, zoom, fit-to-screen, search, status/priority filtering,
a minimap, and a click-through detail panel are all built into the generated
HTML.

The page also has an optional edit mode. Click `编辑` to drag nodes, edit node
text in the right inspector, change a node's parent connection, and add child
nodes. Edits auto-save to browser local storage as a draft. In Chromium-style
browsers that support the File System Access API, `绑定JSON` lets the user pick
a JSON file and then auto-save the edited tree back to that file during the
current browser session. `导出JSON` is the fallback when direct file writing is
not available.

The right inspector uses separate tabs for node details, construction progress,
subtask queue, coverage review, and legend. Clicking a graph node always returns
the inspector to the node-detail tab, so global construction progress does not
look like selected-node content.

Use `status` for capability maturity and `workStatus` for implementation
progress. This keeps "能力还只是 partial" separate from "本轮补丁已经 done".
Supported `workStatus` values are `active`, `done`, `next`, `pending`,
`blocked`, and `deferred`.

After the first causal tree is built, run a coverage audit and store the result
in `coverageReview`. The renderer will show this as a separate panel, so
missing branches and residual risks do not get lost in chat history.

## Files

- `render_outcome_tree.py` renders a JSON outcome tree to a static SVG map.
- `examples/aiqt-overview-advice.json` is a concrete first-pass tree for the
  AI Quant Trader goal: "系统在总览页有有效建议".

## Optional JSON Fields

```json
{
  "coverageReview": [
    {
      "lens": "Causal chain",
      "finding": "A related capability was attached to the wrong parent.",
      "treeChange": "Moved it under the contract it actually supports.",
      "residualRisk": "The exact field mapping still needs code inspection."
    }
  ],
  "nodes": [
    {
      "id": "capability:example",
      "status": "partial",
      "workStatus": "active",
      "localResult": "Treat this node as the result when deriving its children.",
      "targetShape": "A concrete simulated example of what this node looks like when achieved.",
      "directCauseForParent": "Explain why the parent result needs this node.",
      "needType": "capability",
      "edgeProof": "Short proof that this child is required at this layer.",
      "workNote": "当前正在修这个节点对应的 P0 链路。"
    }
  ]
}
```

## Basic Use

```powershell
python C:\Users\At\.codex\skills\outcome-backward-working\outcome-tree\render_outcome_tree.py `
  C:\Users\At\.codex\skills\outcome-backward-working\outcome-tree\examples\aiqt-overview-advice.json `
  --out C:\Users\At\.codex\skills\outcome-backward-working\outcome-tree\examples\aiqt-overview-advice.html
```

The output HTML has no external runtime dependency. Open it directly in a
browser.
