import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(
    page_title="Simulasi Ekonomi Terapan",
    page_icon="🔹️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 👇 JUDUL & SUBJUDUL BARU
st.title("🔹️ Simulasi Ekonomi Terapan")
st.subheader("Informasi Asimetris & Adverse Selection")

st.markdown("""
Model ini mensimulasikan **The Market for Lemons** (George Akerlof, 1970). 
Pembeli tidak mengetahui kualitas individual barang, sehingga menawar berdasarkan **rata-rata kualitas yang ditawarkan**. 
Penjual mengetahui kualitas asli barangnya dan hanya mau menjual jika harga pasar ≥ harga reserve mereka.
""")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Parameter Simulasi")
n_sellers = st.sidebar.slider("Jumlah Penjual Awal", 50, 1000, 200, step=50)
buyer_mult = st.sidebar.slider("Multiplier Pembeli (Valuasi)", 0.5, 2.0, 1.4, step=0.05)
seller_mult = st.sidebar.slider("Multiplier Penjual (Harga Reserve)", 0.5, 1.5, 1.0, step=0.05)
max_rounds = st.sidebar.slider("Maks Ronde Simulasi", 5, 30, 15, step=1)
seed = st.sidebar.slider("Seed Random", 0, 100, 42, step=1)

# Validasi Parameter
if buyer_mult <= seller_mult:
    st.sidebar.error("⚠️ Multiplier Pembeli harus > Multiplier Penjual agar ada potensi surplus perdagangan.")

# ---------------- FUNGSI SIMULASI ----------------
@st.cache_data
def run_lemon_market(n, b_mult, s_mult, rounds, seed):
    np.random.seed(seed)
    qualities = np.random.uniform(0, 1, n)
    reserves = qualities * s_mult
    
    # Harga awal berdasarkan ekspektasi rata-rata populasi
    price = np.mean(qualities) * b_mult
    
    history = {'round': [], 'price': [], 'avg_offered': [], 'num_offered': [], 'status': []}
    
    for t in range(rounds):
        # Penjual yang bersedia menawarkan barang di harga saat ini
        willing = reserves <= price
        n_off = np.sum(willing)
        
        history['round'].append(t)
        history['price'].append(price)
        history['num_offered'].append(n_off)
        
        if n_off == 0:
            history['avg_offered'].append(0.0)
            history['status'].append('Kolaps Pasar')
            break
            
        # Pembeli hanya bisa mengamati kualitas barang yang DITAWARKAN
        avg_offered = np.mean(qualities[willing])
        history['avg_offered'].append(avg_offered)
        
        # Update harga untuk ronde berikutnya berdasarkan kualitas yang benar-benar tersedia
        price = avg_offered * b_mult
        
        # Cek kondisi pasar
        if price < 0.1:
            history['status'].append('Menyusut Drastis')
        else:
            history['status'].append('Aktif')
            
        # Simulasi Adverse Selection: Penjual berkualitas tinggi yang tidak mau jual 
        # secara bertahap keluar dari pasar (unraveling)
        reserves[~willing] = np.inf  # Mark sebagai exit
            
    return history, qualities

# Jalankan Simulasi
history, init_qual = run_lemon_market(n_sellers, buyer_mult, seller_mult, max_rounds, seed)
df_hist = pd.DataFrame(history)

# ---------------- VISUALISASI ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📉 Dinamika Harga & Kualitas")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_hist['round'], y=df_hist['price'], mode='lines+markers', name='Harga Pasar', line=dict(width=3)))
    fig1.add_trace(go.Scatter(x=df_hist['round'], y=df_hist['avg_offered'], mode='lines+markers', name='Rata-rata Kualitas Ditawarkan', line=dict(dash='dot', width=3)))
    fig1.add_hline(y=np.mean(init_qual), line_dash="dash", line_color="gray", annotation_text="Rata-rata Kualitas Awal")
    fig1.update_layout(xaxis_title="Ronde", yaxis_title="Nilai / Kualitas", template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📦 Volume Penawaran & Kondisi Pasar")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df_hist['round'], y=df_hist['num_offered'], name='Jumlah Barang Ditawarkan'))
    fig2.update_layout(xaxis_title="Ronde", yaxis_title="Unit", template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

# Tampilkan tabel ringkasan
with st.expander("📊 Lihat Data Historis Lengkap"):
    st.dataframe(df_hist.style.highlight_max(axis=0, subset=['price', 'avg_offered'], color='lightgreen')
                 .highlight_min(axis=0, subset=['price', 'avg_offered'], color='lightcoral'), use_container_width=True)

# ---------------- INTERPRETASI OTOMATIS ----------------
st.subheader("🧠 Interpretasi Ekonomi")
market_collapsed = df_hist['num_offered'].iloc[-1] == 0
final_price = df_hist['price'].iloc[-1]
init_avg = np.mean(init_qual)

st.info(f"""
**Status Pasar**: `{'KOLAPS' if market_collapsed else 'MENGALAMI ADVERSE SELECTION'}`  
**Harga Awal**: `{init_avg * buyer_mult:.3f}` → **Harga Terakhir**: `{final_price:.3f}`  
**Penawaran Awal**: `{n_sellers}` unit → **Penawaran Terakhir**: `{df_hist['num_offered'].iloc[-1]}` unit
""")

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("""
    ### 🔍 Mengapa Ini Terjadi?
    1. **Informasi Asimetris**: Penjual tahu kualitas, pembeli tidak.
    2. **Pembayaran Berdasarkan Rata-rata**: Pembeli hanya mau membayar sesuai ekspektasi kualitas yang ditawarkan.
    3. **Adverse Selection**: Pada harga awal, hanya penjual dengan barang berkualitas rendah/medium yang mau jual. Barang berkualitas tinggi menahan diri.
    4. **Spiral Penurunan (Unraveling)**: Rata-rata kualitas yang ditawarkan turun → pembeli menurunkan tawaran → lebih banyak penjual menengah/kualitas keluar → pasar menyusut hingga kolaps.
    """)

with col_b:
    st.markdown("""
    ### 🛡️ Solusi Kebijakan & Mekanisme Pasar
    | Masalah | Solusi Ekonomi |
    |---------|----------------|
    | Pembeli tidak tahu kualitas | **Signaling** (Sertifikasi, Garansi, Reputasi) |
    | Penjual berkualitas tinggi tersingkir | **Screening** (Kontrak diferensial, Asuransi tiered) |
    | Kegagalan pasar total | **Regulasi** (Standar mutu, Wajib disclosure, Lembaga pengawas) |
    | Ketidakpercayaan struktural | **Intermediasi** (Platform kurasi, Marketplace terverifikasi) |
    """)

# Footer
st.markdown("---")
st.caption("Simulasi berbasis model Akerlof (1970). Parameter dapat diubah di sidebar untuk menguji ketahanan pasar terhadap berbagai tingkat valuasi dan heterogenitas kualitas.")
st.caption ('copyleft @alamyin www.dataaksi.id')
