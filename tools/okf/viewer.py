"""Generate a self-contained viz.html for the OKF bundle."""
from __future__ import annotations

import json
from pathlib import Path

from .index import iter_concepts
from .paths import bundle_root


_TEMPLATE = r'''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>OKF Graph</title>
  <style>
    html, body { height: 100%; margin: 0; padding: 0; font-family: system-ui, sans-serif; }
    #graph { width: 100%; height: 100%; background: #f8f9fa; }
    #panel { position: absolute; top: 10px; right: 10px; width: 320px; max-height: 80vh; overflow: auto; background: white; border: 1px solid #ddd; padding: 12px; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    #panel h2 { margin: 0 0 8px; font-size: 16px; }
    #panel p { margin: 4px 0; font-size: 13px; color: #333; }
    #panel a { color: #0066cc; }
    #controls { position: absolute; top: 10px; left: 10px; background: white; border: 1px solid #ddd; padding: 10px; border-radius: 6px; }
    #controls label { display: block; font-size: 13px; margin: 4px 0; }
    #search { width: 200px; padding: 4px; }
  </style>
  <script src="https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
</head>
<body>
  <div id="controls">
    <input id="search" type="text" placeholder="Search nodes...">
    <div id="filters"></div>
  </div>
  <div id="panel">
    <h2>OKF Bundle</h2>
    <p>Click a node to see details. Drag to pan, scroll to zoom.</p>
  </div>
  <div id="graph"></div>
  <script>
    const data = /*DATA*/;
    const colors = { Concept: '#4a90d9', Decision: '#d94a4a', System: '#4ad98f', Dataset: '#d9a84a', Table: '#a84ad9', Pipeline: '#4ad9d9', Playbook: '#d94ad9', default: '#999' };

    const cy = cytoscape({
      container: document.getElementById('graph'),
      elements: data.elements,
      style: [
        { selector: 'node', style: { label: 'data(label)', width: 16, height: 16, 'background-color': 'data(color)', 'font-size': 10, 'text-valign': 'bottom', 'text-halign': 'center', 'text-wrap': 'wrap', 'text-max-width': 80 } },
        { selector: 'edge', style: { width: 1, 'line-color': '#ccc', 'target-arrow-color': '#ccc', 'target-arrow-shape': 'triangle', 'curve-style': 'bezier' } }
      ],
      layout: { name: 'cose', padding: 20, animate: false }
    });

    const panel = document.getElementById('panel');
    cy.on('tap', 'node', function(evt){
      const n = evt.target.data();
      panel.innerHTML = `<h2>${n.label}</h2><p><b>Type:</b> ${n.type}</p><p><b>Description:</b> ${n.description || ''}</p><p><a href="${n.path}" target="_blank">Open file</a></p>`;
    });

    document.getElementById('search').addEventListener('input', function(e){
      const term = e.target.value.toLowerCase();
      cy.nodes().forEach(n => n.style('opacity', term && n.data('label').toLowerCase().indexOf(term) === -1 ? 0.1 : 1));
    });

    const types = [...new Set(data.elements.filter(e => e.data.type).map(e => e.data.type))];
    const filters = document.getElementById('filters');
    types.forEach(t => {
      const label = document.createElement('label');
      label.innerHTML = `<input type="checkbox" checked value="${t}"> ${t}`;
      filters.appendChild(label);
    });
    filters.addEventListener('change', function(){
      const checked = [...filters.querySelectorAll('input:checked')].map(i => i.value);
      cy.nodes().forEach(n => n.style('display', checked.includes(n.data('type')) ? 'element' : 'none'));
    });
  </script>
</body>
</html>
'''


def generate(cwd: Path = Path("."), output: Path | None = None) -> Path:
    root = bundle_root(cwd)
    output = output or (root.parent / "viz.html")

    nodes = []
    edges = []
    for doc in iter_concepts(root):
        rel = doc.path.relative_to(root).as_posix()
        node_id = "/" + rel
        doc_type = doc.type() or "Concept"
        nodes.append({
            "data": {
                "id": node_id,
                "label": doc.title() or doc.path.stem,
                "type": doc_type,
                "description": doc.description() or "",
                "path": doc.path.as_posix(),
                "color": _color(doc_type),
            }
        })
        for link in doc.links():
            edges.append({"data": {"source": node_id, "target": link.split("#")[0]}})

    data = {"elements": nodes + edges}
    html = _TEMPLATE.replace("/*DATA*/;", json.dumps(data) + ";")
    output.write_text(html, encoding="utf-8")
    return output


def _color(doc_type: str) -> str:
    palette = {
        "Concept": "#4a90d9",
        "Decision": "#d94a4a",
        "System": "#4ad98f",
        "Dataset": "#d9a84a",
        "Table": "#a84ad9",
        "Pipeline": "#4ad9d9",
        "Playbook": "#d94ad9",
    }
    return palette.get(doc_type, "#999")
