
import streamlit as st
import yaml, json
from validator import evaluate_prompt, load_rubric
import matplotlib.pyplot as plt

st.set_page_config(page_title="Prompt Checker (Supply Chain)", layout="wide")

st.title("✅ Prompt Engineering Checker — Supply Chain")
st.caption("RTF-CO + guardrails • Fokus kasus: Demand, Inventory, PO, Routing")

col1, col2 = st.columns([2,1])

with col2:
    st.subheader("Rubrik & Pengaturan")
    rubric_file = "rubric.yaml"
    rubric = load_rubric(rubric_file)
    st.write("**Versi**:", rubric.get("version"))
    st.json(rubric["weights"])

with col1:
    st.subheader("Tulis/Tempel Prompt")
    default_prompt = ("Anda adalah Demand Planner.\n"
                      "Tugas: Susun forecast Y+1 untuk PCR Replacement Indonesia dengan 3 skenario.\n"
                      "Format: Tabel [Skenario, CAGR, Permintaan(Y+1), Musiman, Catatan].\n"
                      "Constraints: Gunakan CAGR dari data yang diberikan; jangan gunakan data di luar; Q3 ≤ +15% kapasitas.\n"
                      "Orientation: Beri contoh mini dan jelaskan langkah perhitungannya.\n"
                      "Verifikasi: Tulis 3 cek silang (histori vs asumsi vs kapasitas).")
    prompt = st.text_area("Prompt", height=260, value=default_prompt)

left, right = st.columns([1,1])
if left.button("🔍 Cek Sekarang"):
    result = evaluate_prompt(prompt, rubric)
    left.success(f"Skor: {result['total']} / {result['max_total']}  •  Status: {'LULUS' if result['passed'] else 'PERLU PERBAIKAN'}")
    with left.expander("Rincian Skor"):
        st.json(result["scores"])

    # Breakdown chart
    labels = list(result["scores"].keys())
    values = [result["scores"][k] for k in labels]
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title("Breakdown Skor per Komponen")
    ax.set_xticklabels(labels, rotation=30, ha='right')
    right.pyplot(fig, use_container_width=True)

    # Tips per komponen yang gagal
    bad = [k for k, v in result["scores"].items() if v == 0]
    if bad:
        st.warning("Komponen yang perlu ditingkatkan: " + ", ".join(bad))
        tips = rubric.get("tips", {})
        for b in bad:
            if b in tips:
                st.write(f"**{b}** → {tips[b]}")
else:
    right.info("Klik **Cek Sekarang** untuk menilai prompt.")

st.markdown("---")
st.subheader("Cara Pakai")
st.markdown("""
1. Tempel prompt peserta di kotak di atas.
2. Klik **Cek Sekarang** untuk melihat skor dan komponen yang kurang.
3. Gunakan tips per komponen untuk memperbaiki prompt.
4. (Opsional) Sesuaikan bobot & aturan di `rubric.yaml` agar sesuai SOP tim.
""")

with st.expander("🛠 Opsional: Integrasi LLM untuk Review Otomatis (template)"):
    st.code()