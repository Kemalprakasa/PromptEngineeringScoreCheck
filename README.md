
# Prompt Engineering Checker — Supply Chain (Webbase, Streamlit)

Tool web untuk mengecek kualitas prompt peserta training berdasarkan kerangka **RTF-CO** dan guardrails anti-halusinasi.

## Cara Menjalankan (Lokal)
```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Akses di browser: http://localhost:8501

## Struktur
- `app.py` — UI Streamlit
- `validator.py` — logika penilaian
- `rubric.yaml` — bobot & aturan (bisa disesuaikan)
- `examples/` — contoh prompt baik/buruk

## Kustomisasi
- Ubah bobot/aturan di `rubric.yaml` agar sesuai SOP tim (mis. wajib sebut Q3 atau MOQ).
- Anda bisa menambah aturan `any_of` per komponen.

## Deployment Cepat
- **Railway / Render / Hugging Face Spaces**: push repo dan jalankan perintah `streamlit run app.py`.
  - Railway: set `Start Command` = `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
  - Pastikan `PORT` diambil dari environment platform.

## Opsional: Review LLM
- Template kode tersedia di UI (expand panel). Anda bisa hubungkan ke model lokal (Ollama) atau layanan cloud.

## Lisensi
MIT — gunakan bebas untuk keperluan training internal.
