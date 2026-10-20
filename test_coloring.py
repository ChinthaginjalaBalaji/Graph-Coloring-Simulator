import unittest
from coloring_core import greedy_coloring, parse_graph

class GraphColoringTests(unittest.TestCase):
    def assert_valid(self, graph, colors):
        for v, neighbors in graph.items():
            for n in neighbors:
                self.assertNotEqual(colors[v], colors[n])

    def test_path_graph(self):
        g = parse_graph("A, B, C", "A-B\nB-C")
        c = greedy_coloring(g)
        self.assert_valid(g, c)
        self.assertEqual(c["A"], c["C"])

    def test_triangle_uses_three_colors(self):
        g = parse_graph("A, B, C", "A-B\nB-C\nA-C")
        c = greedy_coloring(g)
        self.assert_valid(g, c)
        self.assertEqual(len(set(c.values())), 3)

    def test_disconnected_vertex(self):
        g = parse_graph("A, B, C", "A-B")
        c = greedy_coloring(g)
        self.assert_valid(g, c)
        self.assertIn("C", c)

    def test_invalid_endpoint(self):
        with self.assertRaises(ValueError):
            parse_graph("A, B", "A-C")

    def test_invalid_edge_format(self):
        with self.assertRaises(ValueError):
            parse_graph("A, B, C", "A-B-C")

    def test_empty_vertices(self):
        with self.assertRaises(ValueError):
            parse_graph("", "")

    def test_duplicate_vertices(self):
        with self.assertRaises(ValueError):
            parse_graph("A, A", "")

if __name__ == "__main__":
    unittest.main(verbosity=2)
