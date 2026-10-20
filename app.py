import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Graph Coloring Simulator", page_icon="🎨", layout="wide")
st.title("Graph Coloring Simulator")
st.write("Enter a graph and color its vertices using a greedy algorithm.")

with st.expander("Instructions", expanded=True):
    st.markdown("- Vertices: comma-separated labels, e.g. `A, B, C`.\n- Edges: one per line, e.g. `A-B`.\n- Both endpoints must be in the vertex list.")

left, right = st.columns(2)
with left:
    vertex_text = st.text_input("Vertices (comma-separated)", "A, B, C, D, E")
    edge_text = st.text_area("Edges (one per line, format A-B)",
                             "A-B\nA-C\nB-C\nB-D\nC-D\nD-E", height=190)
with right:
    st.markdown("**Example: triangle graph**")
    st.code("Vertices: A, B, C\nEdges:\nA-B\nB-C\nA-C")
    st.caption("A triangle needs three different colors.")

def greedy_coloring(graph):
    """Return a valid greedy coloring as zero-based color indices."""
    assigned = {}
    for vertex in graph.nodes():
        used = {assigned[n] for n in graph.neighbors(vertex) if n in assigned}
        color = 0
        while color in used:
            color += 1
        assigned[vertex] = color
    return assigned

if st.button("Color Graph", type="primary"):
    try:
        vertices = [v.strip() for v in vertex_text.split(",") if v.strip()]
        if not vertices:
            raise ValueError("Please enter at least one vertex.")
        if len(vertices) != len(set(vertices)):
            raise ValueError("Vertex labels must be unique.")
        graph = nx.Graph()
        graph.add_nodes_from(vertices)
        for line_no, raw_line in enumerate(edge_text.splitlines(), start=1):
            line = raw_line.strip()
            if not line:
                continue
            parts = line.split("-")
            if len(parts) != 2:
                raise ValueError(f"Line {line_no}: use edge format A-B.")
            a, b = (part.strip() for part in parts)
            if not a or not b:
                raise ValueError(f"Line {line_no}: both edge endpoints are required.")
            if a not in graph or b not in graph:
                raise ValueError(f"Line {line_no}: '{a}' or '{b}' is not in the vertex list.")
            if a == b:
                raise ValueError("Self-loops are not supported.")
            graph.add_edge(a, b)

        coloring = greedy_coloring(graph)
        palette = ["#4C78A8", "#F58518", "#54A24B", "#E45756",
                   "#B279A2", "#FF9DA6", "#9D755D", "#72B7B2",
                   "#BAB0AC", "#EECA3B"]
        node_colors = [palette[coloring[v] % len(palette)] for v in graph.nodes()]
        positions = nx.spring_layout(graph, seed=7)
        fig, ax = plt.subplots(figsize=(8, 5))
        nx.draw_networkx(graph, pos=positions, ax=ax, with_labels=True,
                         node_color=node_colors, node_size=1500, font_size=12,
                         font_weight="bold", edge_color="#666666", width=1.6)
        ax.set_title("Greedy Vertex Coloring")
        ax.axis("off")
        st.pyplot(fig)
        plt.close(fig)

        st.success(f"Valid coloring generated using {len(set(coloring.values()))} color(s).")
        st.subheader("Color assignments")
        st.table([{"Vertex": v, "Color number": coloring[v] + 1} for v in graph.nodes()])
        conflicts = [(u, v) for u, v in graph.edges() if coloring[u] == coloring[v]]
        if conflicts:
            st.error(f"Color conflicts found: {conflicts}")
        else:
            st.info("Verification passed: every connected pair has different colors.")
        st.warning("Greedy coloring produces a valid coloring, but does not guarantee the minimum number of colors.")
    except ValueError as exc:
        st.error(str(exc))
