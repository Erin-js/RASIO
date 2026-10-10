# RASIO Project Files

Folder ini sudah dipisahkan berdasarkan fungsi agar data sumber, notebook, grafik, dan dokumen tidak tercampur.

## Mulai dari sini

Notebook utama: [`01_notebooks/RASIO_Master_Analysis.ipynb`](01_notebooks/RASIO_Master_Analysis.ipynb)

Notebook tersebut menggabungkan seluruh alur analisis penting dan sudah diuji dengan **Run All** tanpa error. Urutannya:

1. clustering ketahanan pangan ASEAN;
2. konsentrasi pemasok beras 2024;
3. sensitivitas hasil padi terhadap El Nino;
4. eksposur pasokan negara defisit;
5. ekspor data baseline untuk dashboard.

## Struktur folder

| Folder | Isi |
|---|---|
| `00_data/raw` | Data sumber asli: RONI, hasil padi, dan perdagangan beras |
| `00_data/geospatial` | Shapefile Natural Earth untuk peta ASEAN |
| `00_data/processed` | Tabel hasil olahan yang dibuat notebook |
| `01_notebooks` | Notebook utama |
| `01_notebooks/modules` | Notebook penting per topik untuk analisis terpisah |
| `01_notebooks/archive` | Notebook duplikat atau eksperimen lama, dipertahankan sebagai arsip |
| `02_visualizations/final` | Grafik final yang layak dipakai di infografis/presentasi |
| `02_visualizations/archive` | Grafik kosong atau versi lama yang tidak disarankan dipakai |
| `03_documents/competition` | Pedoman, deskripsi infografis, dan pernyataan orisinalitas |
| `03_documents/presentation` | Naskah presentasi |
| `04_previews/infographic` | Preview dan potongan infografis |
| `04_previews/analysis` | Preview opsi analisis |
| `scripts` | Skrip pembentuk dan penguji notebook utama |

## Status notebook

### Notebook utama

- `RASIO_Master_Analysis.ipynb`: versi terpadu dan menjadi file kerja utama.

### Modul penting

- `01_clustering_asean.ipynb`: membentuk master data, validasi cluster, profil, dan peta.
- `02_supplier_concentration_2024.ipynb`: menghitung pangsa pemasok, HHI, dan stacked bar.
- `03_el_nino_yield_heatmap.ipynb`: mendeteksi episode El Nino dan menghitung sensitivitas hasil padi.
- `04_supply_exposure_bubble.ipynb`: menggabungkan kekurangan produksi, HHI, dan volume impor.
- `05_build_dashboard_baseline.ipynb`: helper ekspor data untuk dashboard, bukan analisis inti.

### Arsip

- `ASEAN_Rice_Clustering_Analysis_added_DUPLICATE.ipynb`: duplikat hampir identik dari notebook clustering.
- `Data_RASIO_LEGACY_EXPERIMENT.ipynb`: eksperimen awal; beberapa sel memakai file yang tidak tersedia dan data simulasi.

## Visualisasi final

- `Diverging_Bar_SSR_2026.svg`
- `Heatmap_Timing_Sensitivity.svg`
- `ASEAN_Rice_Clusters.svg`
- `rice_import_supplier_concentration_2024.png/.svg`
- `rice_supply_exposure_bubble_2024_2026.png/.svg`

Versi kosong atau versi lama tidak dihapus, tetapi dipindahkan ke `02_visualizations/archive` agar tidak tertukar dengan grafik final.

## Menjalankan ulang

Jalankan notebook dari folder proyek ini. Jalur input dan output sudah dibuat relatif terhadap akar proyek, sehingga tidak lagi bergantung pada lokasi absolut komputer.

Untuk membentuk ulang notebook utama dan menguji eksekusinya:

```powershell
python scripts/build_master_notebook.py
python scripts/validate_master_notebook.py
```
