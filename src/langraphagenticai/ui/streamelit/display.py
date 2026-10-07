from typing import Any

import streamlit as st


class GraphDisplay:
    """Render a compiled LangGraph in the Streamlit sidebar."""

    def __init__(self, graph: Any) -> None:
        self.graph = graph

    def graph_data(self) -> dict[str, list[Any]]:
        """Return a serializable view of the graph's nodes and edges."""
        drawable_graph = self.graph.get_graph()
        nodes = list(drawable_graph.nodes.keys())
        edges = [
            {"source": edge.source, "target": edge.target}
            for edge in drawable_graph.edges
        ]
        return {"nodes": nodes, "edges": edges}

    def render(self) -> None:
        """Show graph metadata and a Mermaid diagram."""
        data = self.graph_data()
        st.subheader("Graph")
        st.json(data)

        mermaid_lines = ["flowchart LR"]
        for edge in data["edges"]:
            mermaid_lines.append(f"    {edge['source']} --> {edge['target']}")
        st.code("\n".join(mermaid_lines), language="mermaid")
