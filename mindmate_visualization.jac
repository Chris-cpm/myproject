# ------------------------------
# streamlit_graph.py
# ------------------------------
import streamlit as st
import requests
from pyvis.network import Network
import tempfile
import os

JASECI_GRAPH_URL = st.secrets.get('JASECI_GRAPH_URL', 'http://localhost:11000/js/graph_viz/export_graph')

st.set_page_config(page_title='MindMate Graph', layout='wide')
st.title('MindMate Knowledge Graph Visualization')

if st.button('Load Graph'):
    with st.spinner('Fetching graph...'):
        resp = requests.post(JASECI_GRAPH_URL, json={})
        if resp.status_code != 200:
            st.error('Failed to fetch graph from Jaseci.')
        else:
            data = resp.json()
            nodes = data.get('nodes', [])
            edges = data.get('edges', [])

            net = Network(height='800px', width='100%', notebook=False)

            for n in nodes:
                net.add_node(n['id'], label=n.get('label', n['id']), title=n.get('label', ''), group=n.get('group', 'default'))

            for e in edges:
                net.add_edge(e['from'], e['to'])

            tmpdir = tempfile.gettempdir()
            path = os.path.join(tmpdir, 'mindmate_graph.html')
            net.show(path)

            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()

            st.components.v1.html(html, height=820)


# ------------------------------
# GraphViz.jsx (React Component)
# ------------------------------
# Save under: frontend/components/GraphViz.jsx
# Requires: npm install cytoscape

"""
import React, { useEffect, useRef, useState } from 'react';
import cytoscape from 'cytoscape';

export default function GraphViz({ apiUrl }) {
  const cyRef = useRef(null);
  const containerRef = useRef(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!containerRef.current) return;

    cyRef.current = cytoscape({
      container: containerRef.current,
      elements: [],
      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'text-valign': 'center',
            'color': '#fff',
            'font-size': '14px',
            'background-color': '#3b82f6'
          }
        },
        {
          selector: 'edge',
          style: {
            'line-color': '#aaa',
            'curve-style': 'bezier',
            'width': 2
          }
        }
      ]
    });

    async function loadGraph() {
      setLoading(true);
      try {
        const res = await fetch(apiUrl || '/js/graph_viz/export_graph', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });

        const data = await res.json();
        const nodes = data.nodes.map(n => ({ data: { id: n.id, label: n.label, group: n.group } }));
        const edges = data.edges.map(e => ({ data: { id: `${e.from}_${e.to}`, source: e.from, target: e.to } }));

        cyRef.current.add([...nodes, ...edges]);
        cyRef.current.layout({ name: 'cose', animate: true }).run();
      } catch (err) {
        console.error('Graph load error:', err);
      } finally {
        setLoading(false);
      }
    }

    loadGraph();

    return () => {
      if (cyRef.current) cyRef.current.destroy();
    };
  }, [containerRef]);

  return (
    <div className="w-full h-[700px] bg-gray-900 rounded-lg p-3">
      {loading && <div className="text-white mb-2">Loading graph...</div>}
      <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
    </div>
  );
}
"""


// --- USER INTERFACE ENTRY POINT (Streamlit + React Hooks) ---
walker ui_entrypoint {
    can: {
        "message": "MindMate Harmony Space UI Ready",
        "endpoints": {
            "streamlit": "/ui/streamlit",
            "react": "/ui/react",
            "submit_mood": "/api/submit_mood"
        }
    };
}

// Submit mood + classify + advise + connect to trigger node
walker submit_mood(user_input: dict) {
    root << mood_entry(text=user_input.text, trigger_type=user_input.trigger_type);
    take . classify_trigger;
    take . generate_advice;
    take . link_trigger_node;

    can: {
        "status": "mood processed",
        "classified_trigger": .trigger_final,
        "advice": .advice
    };
}
