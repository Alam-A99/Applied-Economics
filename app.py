import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

# =============================================================================
# KONFIGURASI HALAMAN
# =============================================================================
st.set_page_config(
    page_title="Simulasi Ekonomi Terapan",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tampilkan logo jika file tersedia
try:
    st.image("icon.png", width=50)
except:
    pass

# 👇 JUDUL & SUBJUDUL
st.title("Simulasi Ekonomi Terapan")
st.subheader("Informasi Asimetris & Adverse Selection")

st.markdown("""
Model ini mensimulasikan **The Market for Lemons** (George Akerlof). 
Pembeli tidak mengetahui kualitas individual barang, sehingga menawar berdasarkan **rata-rata kualitas yang ditawarkan**. 
Penjual mengetahui kualitas asli barangnya dan hanya mau menjual jika harga pasar ≥ harga reserve mereka.

> 💱 **Catatan**: Semua harga ditampilkan dalam **Rupiah (Rp)** dengan asumsi 1 unit valuasi = Rp 15.000.
""")

# =============================================================================
# HELPER FUNCTION: FORMAT RUPIAH
# =============================================================================
def format_rupiah(value, multiplier=15000):
    """
    Mengkonversi nilai simulasi ke format Rupiah yang rapi.
    Contoh: 0.85 → Rp 12.750
    """
    nominal = value * multiplier
    return f"Rp {nominal:,.0f}".replace(",", ".")

# =============================================================================
# SIDEBAR: PARAMETER SIMULASI
# =============================================================================
st.sidebar.header("⚙️ Parameter Simulasi")

# Parameter konversi mata uang
exchange_rate = st.sidebar.number_input(
    "💱 Faktor Konversi ke Rupiah", 
    min_value=1000, max_value=50000, value=15000, step=1000,
    help="1 unit valuasi dalam simulasi = berapa Rupiah?"
)

n_sellers = st.sidebar.slider("Jumlah Penjual Awal", 50, 1000, 200, step=50)
buyer_mult = st.sidebar.slider("Multiplier Pembeli (Valuasi)", 0.5, 2.0, 1.4, step=0.05)
seller_mult = st.sidebar.slider("Multiplier Penjual (Harga Reserve)", 0.5, 1.5, 1.0, step=0.05)
max_rounds = st.sidebar.slider("Maks Ronde Simulasi", 5, 30, 15, step=1)
seed = st.sidebar.slider("Seed Random", 0, 100, 42, step=1)

# Validasi Parameter
if buyer_mult <= seller_mult:
    st.sidebar.error("⚠️ Multiplier Pembeli harus > Multiplier Penjual agar ada potensi surplus perdagangan.")

# =============================================================================
# FUNGSI SIMULASI INTI
# =============================================================================
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

# =============================================================================
# JALANKAN SIMULASI
# =============================================================================
history, init_qual = run_lemon_market(n_sellers, buyer_mult, seller_mult, max_rounds, seed)
df_hist = pd.DataFrame(history)

# Tambahkan kolom harga dalam Rupiah ke dataframe untuk kemudahan display
df_hist['price_rupiah'] = df_hist['price'].apply(lambda x: x * exchange_rate)

# =============================================================================
# VISUALISASI INTERAKTIF
# =============================================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📉 Dinamika Harga & Kualitas")
    fig1 = go.Figure()
    
    # Harga Pasar dalam Rupiah
    fig1.add_trace(go.Scatter(
        x=df_hist['round'], 
        y=df_hist['price_rupiah'], 
        mode='lines+markers', 
        name='💰 Harga Pasar (Rp)', 
        line=dict(width=3, color='#E63946'),
        hovertemplate='<b>Ronde %{x}</b><br>Harga: Rp %{y:,.0f}<extra></extra>'
    ))
    
    # Rata-rata Kualitas Ditawarkan (tetap dalam skala 0-1)
    fig1.add_trace(go.Scatter(
        x=df_hist['round'], 
        y=df_hist['avg_offered'], 
        mode='lines+markers', 
        name='📊 Rata-rata Kualitas Ditawarkan', 
        line=dict(dash='dot', width=3, color='#2A9D8F'),
        yaxis='y2',
        hovertemplate='<b>Ronde %{x}</b><br>Kualitas: %{y:.2f}<extra></extra>'
    ))
    
    # Garis referensi: rata-rata kualitas awal
    fig1.add_hline(
        y=np.mean(init_qual), 
        line_dash="dash", 
        line_color="gray", 
        annotation_text="Rata-rata Kualitas Awal",
        annotation_position="top right"
    )
    
    fig1.update_layout(
        xaxis_title="Ronde",
        yaxis_title="Harga (Rupiah)",
        yaxis2=dict(title="Kualitas (0-1)", overlaying='y', side='right', range=[0, 1]),
        template="plotly_white",
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📦 Volume Penawaran & Kondisi Pasar")
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        x=df_hist['round'], 
        y=df_hist['num_offered'], 
        name='📦 Jumlah Barang Ditawarkan',
        marker_color='#457B9D',
        hovertemplate='<b>Ronde %{x}</b><br>Unit: %{y}<extra></extra>'
    ))
    
    fig2.update_layout(
        xaxis_title="Ronde", 
        yaxis_title="Unit", 
        template="plotly_white",
        hovermode='x unified'
    )
    st.plotly_chart(fig2, use_container_width=True)

# =============================================================================
# TABEL DATA HISTORIS
# =============================================================================
with st.expander("📊 Lihat Data Historis Lengkap"):
    # Siapkan dataframe untuk display dengan format Rupiah
    df_display = df_hist.copy()
    df_display['Harga (Rp)'] = df_display['price_rupiah'].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
    df_display['Kualitas Rata-rata'] = df_display['avg_offered'].apply(lambda x: f"{x:.3f}")
    df_display['Status'] = df_display['status']
    
    # Tampilkan hanya kolom yang relevan
    st.dataframe(
        df_display[['round', 'Harga (Rp)', 'Kualitas Rata-rata', 'num_offered', 'Status']]
        .rename(columns={'round': 'Ronde', 'num_offered': 'Unit Ditawarkan'})
        .style.set_properties(**{'text-align': 'center'}),
        use_container_width=True,
        hide_index=True
    )

# =============================================================================
# INTERPRETASI EKONOMI DINAMIS
# =============================================================================
st.subheader("🧠 Interpretasi Ekonomi")

market_collapsed = df_hist['num_offered'].iloc[-1] == 0
final_price = df_hist['price'].iloc[-1] * exchange_rate  # Konversi ke Rupiah
init_avg = np.mean(init_qual)
init_price_rupiah = init_avg * buyer_mult * exchange_rate

# Box status utama dengan format Rupiah
st.info(f"""
**Status Pasar**: `{'🔴 KOLAPS' if market_collapsed else '🟡 MENGALAMI ADVERSE SELECTION'}`  
**Harga Awal**: `{format_rupiah(init_avg * buyer_mult, exchange_rate)}` → **Harga Terakhir**: `{format_rupiah(final_price/exchange_rate, exchange_rate)}`  
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

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.caption("Simulasi berbasis model Akerlof (1970). Parameter dapat diubah di sidebar untuk menguji ketahanan pasar terhadap berbagai tingkat valuasi dan heterogenitas kualitas.")
st.caption("💱 1 unit valuasi = Rp {:,}".format(exchange_rate).replace(",", "."))
st.caption("copyleft @alamyin www.dataaksi.id")
