def greedy_coloring(adjacency):
    colors = {}
    for vertex, neighbors in adjacency.items():
        used = {colors[n] for n in neighbors if n in colors}
        color = 0
        while color in used:
            color += 1
        colors[vertex] = color
    return colors

def parse_graph(vertex_text, edge_text):
    vertices = [v.strip() for v in vertex_text.split(",") if v.strip()]
    if not vertices:
        raise ValueError("Please enter at least one vertex.")
    if len(vertices) != len(set(vertices)):
        raise ValueError("Vertex labels must be unique.")
    adjacency = {v: set() for v in vertices}
    for line_no, raw in enumerate(edge_text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split("-")
        if len(parts) != 2:
            raise ValueError(f"Line {line_no}: use edge format A-B.")
        a, b = (p.strip() for p in parts)
        if not a or not b:
            raise ValueError(f"Line {line_no}: both edge endpoints are required.")
        if a not in adjacency or b not in adjacency:
            raise ValueError(f"Line {line_no}: endpoint not in vertex list.")
        if a == b:
            raise ValueError("Self-loops are not supported.")
        adjacency[a].add(b)
        adjacency[b].add(a)
    return adjacency
