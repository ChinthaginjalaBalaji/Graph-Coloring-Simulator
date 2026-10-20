# Graph Coloring Simulator

Beginner-friendly Python/Streamlit web application for greedy vertex coloring.

## Run
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run `python -m pip install -r requirements.txt`
4. Run `python -m streamlit run app.py`
5. Open the local URL printed by Streamlit (usually http://localhost:8501).

## Input
Vertices: `A, B, C`
Edges (one per line): `A-B`, `B-C`, `A-C`

## Notes
The greedy algorithm returns a valid coloring for a simple undirected graph, but may not return the minimum number of colors. Run the included tests with `python -m unittest -v test_coloring.py`.

Before submission, add your own student details and capture an actual screenshot after running the app.
