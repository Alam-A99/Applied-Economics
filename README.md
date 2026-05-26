# 🍋 Simulasi Ekonomi Terapan: Informasi Asimetris & Adverse Selection

> Dashboard interaktif berbasis Streamlit untuk memodelkan dinamika pasar dengan informasi tidak sempurna, mengadaptasi teori klasik *The Market for Lemons* (George Akerlof, 1970).

---

## 📋 Daftar Isi
- [📖 Deskripsi](#-deskripsi)
- [✨ Fitur Utama](#-fitur-utama)
- [🚀 Instalasi](#-instalasi)
- [🎮 Cara Penggunaan](#-cara-penggunaan)
- [⚙️ Parameter Simulasi](#️-parameter-simulasi)
- [🧠 Dasar Teori](#-dasar-teori)
- [📁 Struktur Proyek](#-struktur-proyek)
- [🔬 Skenario Eksperimen](#-skenario-eksperimen)
- [🤝 Kontribusi](#-kontribusi)
- [📜 Lisensi](#-lisensi)
- [📚 Referensi](#-referensi)

---

## 📖 Deskripsi

Proyek ini merupakan implementasi komputasional dari model **informasi asimetris** dalam ekonomi. Simulasi ini menunjukkan bagaimana ketimpangan informasi antara pembeli dan penjual dapat menyebabkan:

- 📉 **Adverse Selection**: Barang berkualitas tinggi tersingkir dari pasar
- 🌀 **Unraveling Effect**: Spiral penurunan kualitas dan harga
- ⚠️ **Market Failure**: Kegagalan alokasi sumber daya secara efisien

Dashboard ini dirancang untuk:
- 🎓 **Pendidikan**: Alat bantu mengajar teori ekonomi informasi
- 🔬 **Riset**: Eksplorasi parameter kebijakan dan sensitivitas pasar
- 🏛️ **Kebijakan**: Simulasi dampak intervensi regulasi dan transparansi

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🎛️ **Parameter Interaktif** | Slider untuk menyesuaikan jumlah penjual, multiplier valuasi, intensitas konflik, dan tingkat transparansi |
| 📊 **Visualisasi Dinamis** | Grafik Plotly interaktif: harga vs kualitas, volume perdagangan, indeks ketidakpastian |
| 🧠 **Interpretasi Otomatis** | Analisis hasil simulasi dalam bahasa natural berdasarkan output model |
| 📋 **Ekspor Data** | Unduh hasil simulasi dalam format CSV untuk analisis lanjutan |
| 🌐 **Dua Mode Simulasi** | (1) Market for Lemons klasik, (2) Pasar minyak dengan shock geopolitik |
| 🎨 **UI Responsif** | Tampilan optimal di desktop maupun tablet dengan layout widescreen |

---

## 🚀 Instalasi

### Prasyarat
- Python ≥ 3.9
- pip (Python package manager)

### Langkah Instalasi

```bash
# 1. Clone atau download repository ini
git clone https://github.com/username/asymmetric-info-sim.git
cd asymmetric-info-sim

# 2. (Opsional) Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run app.py

# Skenario 1: Pasar normal (informasi simetris)
buyer_mult=1.5, seller_mult=1.0, transparency=1.0
# → Harga stabil, volume tinggi, tidak ada adverse selection

# Skenario 2: Informasi asimetris murni
buyer_mult=1.4, seller_mult=1.0, transparency=0.0
# → Spiral penurunan kualitas, unraveling dalam 5-8 ronde

# Skenario 3: Intervensi signaling
Tambahkan biaya sertifikasi untuk supplier berkualitas tinggi
# → Supplier bagus tetap masuk pasar, efisiensi meningkat

📚 Referensi Akademik
Akerlof, G. A. (1970). The Market for "Lemons": Quality Uncertainty and the Market Mechanism. Quarterly Journal of Economics, 84(3), 488–500.
🔗 DOI:10.2307/1879431
Spence, M. (1973). Job Market Signaling. Quarterly Journal of Economics, 87(3), 355–374.
(Model signaling sebagai solusi informasi asimetris)
Rothschild, M. & Stiglitz, J. E. (1976). Equilibrium in Competitive Insurance Markets. QJE, 90(4), 629–649.
(Screening contracts dalam pasar dengan adverse selection)
Stiglitz, J. E. (2000). The Contributions of the Economics of Information to Twentieth Century Economics. QJE, 115(4), 1441–1478.
(Nobel Lecture: Overview kontribusi ekonomi informasi)
IEA (2024). Oil Market Report: Geopolitical Risk Assessment. International Energy Agency.
(Data empiris pasar energi global)

copyleft @alamyin www.dataaksi.id
