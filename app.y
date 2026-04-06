

Copy code
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Config page
st.set_page_config(
    page_title="🌊 Simulasi Gelombang Fisika",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌊 **Simulasi Gelombang Fisika Interaktif**")
st.markdown("---")

# Sidebar kontrol
st.sidebar.header("⚙️ **Kontrol Simulasi**")
amplitudo = st.sidebar.slider("Amplitudo (A)", 1.0, 10.0, 3.0, 0.1)
frekuensi = st.sidebar.slider("Frekuensi (f)", 0.1, 3.0, 1.0, 0.1)
panjang_gelombang = st.sidebar.slider("Panjang Gelombang (λ)", 1.0, 20.0, 5.0, 0.5)
kecepatan = st.sidebar.slider("Kecepatan Gelombang (v)", 1.0, 10.0, 2.0, 0.1)
fase = st.sidebar.slider("Fase Awal (φ)", 0.0, 2*np.pi, 0.0, 0.1)

# Tombol animasi
if st.sidebar.button("▶️ Mulai Animasi"):
    animasi = True
else:
    animasi = False

# Hitung parameter otomatis
periode = 1/frekuensi
v_hitung = frekuensi * panjang_gelombang

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Periode (T)", f"{periode:.2f} s", f"1/{frekuensi:.2f}")
with col2:
    st.metric("Kecepatan (v)", f"{v_hitung:.2f} m/s", f"{kecepatan:.2f}")
with col3:
    st.metric("Frekuensi (f)", f"{frekuensi:.2f} Hz")

st.markdown("---")

# Simulasi gelombang
t = np.linspace(0, 4*np.pi/frekuensi, 1000)
x = np.linspace(0, 4*panjang_gelombang, 1000)

# Fungsi gelombang sinusoida
def gelombang(x, t, A, k, omega, phi):
    k_wave = 2*np.pi/panjang_gelombang
    omega_wave = 2*np.pi*frekuensi
    return A * np.sin(k_wave*x - omega_wave*t + phi)

# Plot utama
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Gelombang Transversal', 'Snapshot 3D', 'Animasi Waktu', 'Spektrum Frekuensi'),
    specs=[[{"type": "scatter"}, {"type": "surface"}],
           [{"type": "scatter"}, {"type": "scatter"}]]
)

# 1. Gelombang statis
y1 = gelombang(x, 0, amplitudo, 0, 0, fase)
fig.add_trace(
    go.Scatter(x=x, y=y1, mode='lines', name='Gelombang', 
              line=dict(color='blue', width=3)),
    row=1, col=1
)

# 2. Surface 3D (x,t,y)
X, T = np.meshgrid(x, t)
Z = gelombang(X, T, amplitudo, 0, 0, fase)
fig.add_trace(
    go.Surface(x=X, y=T, z=Z, colorscale='Viridis', showscale=False),
    row=1, col=2
)

# 3. Animasi waktu (titik tertentu)
x0 = panjang_gelombang / 4
y_titik = gelombang(x0, t, amplitudo, 0, 0, fase)
fig.add_trace(
    go.Scatter(x=t, y=y_titik, mode='lines', name='Titik x=λ/4',
              line=dict(color='red', width=3)),
    row=2, col=1
)

# 4. Spektrum frekuensi (FFT)
fft_y = np.fft.fft(y1)
freqs = np.fft.fftfreq(len(fft_y), x[1]-x[0])
fig.add_trace(
    go.Scatter(x=freqs[:len(freqs)//2], y=np.abs(fft_y)[:len(freqs)//2],
              mode='lines', name='Spektrum', line=dict(color='purple')),
    row=2, col=2
)

fig.update_layout(height=800, showlegend=True, title_text="📊 Visualisasi Lengkap Gelombang")
st.plotly_chart(fig, use_container_width=True)

# Animasi real-time
if animasi:
    st.subheader("🎬 **Animasi Real-time**")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        t_anim = i * 0.1
        y_anim = gelombang(x, t_anim, amplitudo, 0, 0, fase)
        
        fig_anim = go.Figure()
        fig_anim.add_trace(go.Scatter(x=x, y=y_anim, mode='lines',
                                     line=dict(color='orange', width=4)))
        fig_anim.update_layout(title=f'Animasi t={t_anim:.2f}s', height=400)
        
        st.plotly_chart(fig_anim, use_container_width=True)
        
        progress_bar.progress(i + 1)
        status_text.text(f'Simulasi: {i+1}/100 frames')
        time.sleep(0.05)
    
    st.success("✅ Animasi selesai!")

# Info fisika
with st.expander("📚 **Rumus & Teori**"):
    st.latex(r"""
    **Gelombang Sinusoida:**
    $$
    y(x,t) = A \sin\left(\frac{2\pi}{\lambda}x - \frac{2\pi}{T}t + \phi\right)
    $$
    
    **Hubungan:**
    $$
    v = f \lambda = \frac{\lambda}{T}
    $$
    """)
    
    st.info("👆 Coba ubah parameter di sidebar untuk lihat efeknya!")

# Kuis interaktif
st.subheader("🧠 **Tes Pemahamanmu**")
col_a, col_b = st.columns(2)

with col_a:
    st.write("**Hitung kecepatan gelombang:**")
    f_input = st.number_input("Frekuensi (Hz)", 0.1, 5.0, 1.0)
    lambda_input = st.number_input("Panjang gelombang (m)", 1.0, 20.0, 5.0)
    v_user = st.number_input("Kecepatan v = ?", 0.0, 50.0)

with col_b:
    v_teori = f_input * lambda_input
    if st.button("✅ Cek Jawaban"):
        if abs(v_user - v_teori) < 0.1:
            st.success(f"🎉 Benar! v = fλ = {v_teori:.2f} m/s")
        else:
            st.error(f"❌ Salah. Jawaban benar: {v_teori:.2f} m/s")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    Made with ❤️ using Streamlit | Simulasi Fisika SMA/MA
</div>
""", unsafe_allow_html=True)
