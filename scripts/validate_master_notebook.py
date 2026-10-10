from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "01_notebooks" / "RASIO_Master_Analysis.ipynb"


notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
client = NotebookClient(
    notebook,
    timeout=900,
    kernel_name="python3",
    resources={"metadata": {"path": str(ROOT)}},
    allow_errors=False,
)
client.execute()
nbformat.write(notebook, NOTEBOOK_PATH)

code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
error_outputs = [
    output
    for cell in code_cells
    for output in cell.get("outputs", [])
    if output.get("output_type") == "error"
]
print(f"Executed code cells: {len(code_cells)}")
print(f"Error outputs: {len(error_outputs)}")
print(f"Saved executed notebook: {NOTEBOOK_PATH}")
