from copy import deepcopy
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
MODULE_DIR = ROOT / "01_notebooks" / "modules"
MASTER_PATH = ROOT / "01_notebooks" / "RASIO_Master_Analysis.ipynb"


PROJECT_ROOT_HELPER = '''def find_project_root():
    """Temukan akar proyek dari folder kerja notebook saat ini."""
    start = Path.cwd().resolve()
    for folder in (start, *start.parents):
        if (folder / "00_data").exists() and (folder / "01_notebooks").exists():
            return folder
    raise FileNotFoundError("Folder akar proyek RASIO tidak ditemukan.")


PROJECT_ROOT = find_project_root()
RAW_DATA_DIR = PROJECT_ROOT / "00_data" / "raw"
'''


def read_notebook(name):
    return nbformat.read(MODULE_DIR / name, as_version=4)


def write_notebook(notebook, path):
    nbformat.write(notebook, path)


def replace_cell(notebook, index, source):
    notebook.cells[index].source = source.strip() + "\n"


def clean_outputs(notebook):
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.execution_count = None
            cell.outputs = []
    return notebook


def update_clustering(notebook):
    old = '''# Ubah hanya baris ini jika folder proyekmu berbeda.
WINDOWS_PROJECT_DIR = Path(r"C:\\Users\\ACER\\OneDrive\\Dokumen\\COMPETITION\\RASIO")

CANDIDATE_DIRS = [
    WINDOWS_PROJECT_DIR,
    Path.cwd(),
    Path.cwd() / "upload",
    Path.cwd().parent,
]

def resolve_file(patterns, required=True):
    # Cari file pertama yang cocok pada seluruh kandidat folder.
    if isinstance(patterns, str):
        patterns = [patterns]
    for folder in CANDIDATE_DIRS:
        if not folder.exists():
            continue
        for pattern in patterns:
            matches = sorted(folder.glob(pattern))
            if matches:
                return matches[0]
    if required:
        raise FileNotFoundError(
            f"File tidak ditemukan. Pola: {patterns}. "
            "Letakkan file pada folder proyek atau folder yang sama dengan notebook."
        )
    return None

RONI_PATH = resolve_file(["RONI_3_Months*.csv", "RONI*.csv"])
TRADE_PATH = resolve_file(["TradeData*.csv", "*TradeData*.csv"])
YIELD_PATH = resolve_file(["rice-yields*.csv", "*rice*yield*.csv"])

SHP_CANDIDATES = [
    WINDOWS_PROJECT_DIR / "ne_10m_admin_0_countries" / "ne_10m_admin_0_countries.shp",
    Path.cwd() / "ne_10m_admin_0_countries" / "ne_10m_admin_0_countries.shp",
    Path.cwd() / "upload" / "ne_10m_admin_0_countries.shp",
    Path.cwd() / "ne_10m_admin_0_countries.shp",
]
SHP_PATH = next((p for p in SHP_CANDIDATES if p.exists()), SHP_CANDIDATES[0])'''
    new = PROJECT_ROOT_HELPER + '''
RONI_PATH = RAW_DATA_DIR / "RONI_3_Months.csv"
TRADE_PATH = RAW_DATA_DIR / "TradeData_8_27_2026_21_50_21.csv"
YIELD_PATH = RAW_DATA_DIR / "rice-yields.csv"
SHP_PATH = (
    PROJECT_ROOT
    / "00_data"
    / "geospatial"
    / "ne_10m_admin_0_countries"
    / "ne_10m_admin_0_countries.shp"
)'''
    notebook.cells[2].source = notebook.cells[2].source.replace(old, new)
    notebook.cells[35].source = notebook.cells[35].source.replace(
        'OUTPUT_DIR = Path.cwd() / "outputs_asean_clustering"',
        'OUTPUT_DIR = PROJECT_ROOT / "00_data" / "processed" / "clustering"',
    )
    return notebook


def update_supplier(notebook):
    old = '''DATA_FILENAME = "TradeData_8_27_2026_21_50_21.csv"

candidate_paths = [
    Path(DATA_FILENAME),
    Path("upload") / DATA_FILENAME,
    Path("/content") / DATA_FILENAME,
]

DATA_PATH = next((path for path in candidate_paths if path.exists()), None)
if DATA_PATH is None:
    raise FileNotFoundError(
        f"File {DATA_FILENAME!r} tidak ditemukan. Letakkan CSV di folder yang sama "
        "dengan notebook atau ubah variabel DATA_PATH."
    )

OUTPUT_DIR = Path("output_stacked_bar")
OUTPUT_DIR.mkdir(exist_ok=True)'''
    new = PROJECT_ROOT_HELPER + '''
DATA_PATH = RAW_DATA_DIR / "TradeData_8_27_2026_21_50_21.csv"
OUTPUT_DIR = PROJECT_ROOT / "00_data" / "processed" / "supplier_concentration"
FIGURE_DIR = PROJECT_ROOT / "02_visualizations" / "final"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)'''
    notebook.cells[4].source = notebook.cells[4].source.replace(old, new)
    notebook.cells[22].source = notebook.cells[22].source.replace(
        'png_path = OUTPUT_DIR / "rice_import_supplier_concentration_2024.png"\nsvg_path = OUTPUT_DIR / "rice_import_supplier_concentration_2024.svg"',
        'png_path = FIGURE_DIR / "rice_import_supplier_concentration_2024.png"\nsvg_path = FIGURE_DIR / "rice_import_supplier_concentration_2024.svg"',
    )
    return notebook


def update_heatmap(notebook):
    # Dua sel terakhir adalah salinan tidak sengaja dari analisis stacked bar.
    notebook.cells = notebook.cells[:24]
    marker = 'def resolve_input(filename):\n'
    source = notebook.cells[1].source
    helper = PROJECT_ROOT_HELPER + '''
def resolve_input(filename):
    candidate = RAW_DATA_DIR / filename
    if candidate.exists():
        return candidate.resolve()
    raise FileNotFoundError(f"{filename} tidak ditemukan di {RAW_DATA_DIR}")
'''
    before, _, _after = source.partition(marker)
    imports_and_config = before
    suffix_start = source.index('RONI_PATH = resolve_input("RONI_3_Months.csv")')
    suffix = source[suffix_start:]
    notebook.cells[1].source = imports_and_config + helper + "\n" + suffix
    return notebook


def update_bubble(notebook):
    new_config = '''MASTER_FILENAME = "asean_master_dataframe.csv"
HHI_FILENAME = "hhi_summary_2024.csv"

''' + PROJECT_ROOT_HELPER + '''
MASTER_PATH = PROJECT_ROOT / "00_data" / "processed" / "clustering" / MASTER_FILENAME
HHI_PATH = PROJECT_ROOT / "00_data" / "processed" / "supplier_concentration" / HHI_FILENAME
DATA_OUTPUT_DIR = PROJECT_ROOT / "00_data" / "processed" / "supply_exposure"
FIGURE_DIR = PROJECT_ROOT / "02_visualizations" / "final"
DATA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

DEFICIT_COUNTRIES = [
    "Brunei Darussalam",
    "Malaysia",
    "Philippines",
    "Singapore",
]

print("AFSIS master table:", MASTER_PATH.resolve())
print("UN Comtrade HHI table:", HHI_PATH.resolve())
print("Data output directory:", DATA_OUTPUT_DIR.resolve())
print("Figure directory:", FIGURE_DIR.resolve())'''
    replace_cell(notebook, 4, new_config)
    notebook.cells[12].source = notebook.cells[12].source.replace(
        "png_path = OUTPUT_DIR / 'rice_supply_exposure_bubble_2024_2026.png'\nsvg_path = OUTPUT_DIR / 'rice_supply_exposure_bubble_2024_2026.svg'",
        "png_path = FIGURE_DIR / 'rice_supply_exposure_bubble_2024_2026.png'\nsvg_path = FIGURE_DIR / 'rice_supply_exposure_bubble_2024_2026.svg'",
    ).replace("plt.savefig('rice_supply_exposure_bubble_2024_2026.svg', format='svg')\n", "")
    notebook.cells[14].source = notebook.cells[14].source.replace(
        "chart_data_path = OUTPUT_DIR / 'rice_supply_exposure_bubble_data_2024_2026.csv'",
        "chart_data_path = DATA_OUTPUT_DIR / 'rice_supply_exposure_bubble_data_2024_2026.csv'",
    )
    return notebook


def update_baseline(notebook):
    notebook.cells[0].source = (
        "# Build ASEAN Country Baseline for the Dashboard\n\n"
        "Sumber langsung: `00_data/processed/clustering/asean_master_dataframe.csv`. "
        "File ini merupakan keluaran modul clustering utama yang menggabungkan proyeksi "
        "neraca beras AFSIS 2026 dan hasil clustering terpilih `k = 3`."
    )
    new_config = '''from pathlib import Path
import pandas as pd

pd.set_option("display.max_columns", 30)
pd.set_option("display.width", 160)

''' + PROJECT_ROOT_HELPER + '''
SOURCE_PATH = PROJECT_ROOT / "00_data" / "processed" / "clustering" / "asean_master_dataframe.csv"
OUTPUT_PATH = PROJECT_ROOT / "00_data" / "processed" / "dashboard" / "asean-country-baseline.csv"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

print("Source:", SOURCE_PATH)
print("Output:", OUTPUT_PATH)'''
    replace_cell(notebook, 1, new_config)
    return notebook


MODULE_SPECS = [
    ("01_clustering_asean.ipynb", "1. Clustering ketahanan pangan ASEAN", update_clustering),
    ("02_supplier_concentration_2024.ipynb", "2. Konsentrasi pemasok beras 2024", update_supplier),
    ("03_el_nino_yield_heatmap.ipynb", "3. El Nino dan sensitivitas hasil padi", update_heatmap),
    ("04_supply_exposure_bubble.ipynb", "4. Eksposur pasokan negara defisit", update_bubble),
    ("05_build_dashboard_baseline.ipynb", "5. Ekspor baseline dashboard", update_baseline),
]


def main():
    modules = []
    for filename, title, updater in MODULE_SPECS:
        notebook = updater(read_notebook(filename))
        clean_outputs(notebook)
        write_notebook(notebook, MODULE_DIR / filename)
        modules.append((title, notebook))

    master = nbformat.v4.new_notebook()
    master.metadata = deepcopy(modules[0][1].metadata)
    master.cells = [
        nbformat.v4.new_markdown_cell(
            "# RASIO Master Analysis\n\n"
            "Notebook utama untuk menghasilkan analisis inti proyek RASIO secara berurutan. "
            "Jalankan dari atas ke bawah. Semua input dibaca dari `00_data/raw`, data olahan "
            "ditulis ke `00_data/processed`, dan grafik final disimpan di `02_visualizations/final`."
        )
    ]

    for title, notebook in modules:
        master.cells.append(nbformat.v4.new_markdown_cell(f"# {title}"))
        master.cells.extend(deepcopy(notebook.cells))

    clean_outputs(master)
    write_notebook(master, MASTER_PATH)
    print(f"Updated {len(modules)} module notebooks")
    print(f"Created master notebook: {MASTER_PATH}")
    print(f"Master cells: {len(master.cells)}")


if __name__ == "__main__":
    main()
