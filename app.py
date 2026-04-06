import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="🌊 Gelombang Transversal", layout="wide")

st.title("🌊 **Simulasi Gelombang Transversal**")

# Sidebar kontrol
st.sidebar.header("⚙️ Parameter Gelombang")
amplitudo = st.sidebar.slider("Amplitudo (A)", 1.0, 5.0, 2.0)
frekuensi = st.sidebar.slider("Frekuensi (f)", 0.5, 2.0, 1.0)
lamda = st.sidebar.slider("Panjang Gelombang (λ)", 2.0, 10.0, 5.0)

# Hitung parameter
kecepatan = frekuensi * lamda
periode = 1 / frekuensi

# Data untuk plot
x = np.linspace(0, 4*lamda, 1000)
k = 2 * np.pi / lamda
w = 2 * np.pi * frekuensi

# Fungsi gelombang
def gelombang(x, t=0):
    return amplitudo * np.sin(k * x - w * t)

# Plot gelombang
fig = go.Figure()
y = gelombang(x)
fig.add_trace(go.Scatter(x=x, y=y, mode='lines',
                        line=dict(color='#1f77b4', width=4),
                        name='Gelombang Transversal'))

fig.update_layout(
    title=f"🌊 Gelombang: A={amplitudo}, f={frekuensi}Hz, λ={lamda}m",
    xaxis_title="Posisi x (meter)",
    yaxis_title="Amplitudo y (meter)",
    height=500,
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

# Info parameter
col1, col2, col3 = st.columns(3)
col1.metric("Kecepatan v", f"{kecepatan:.1f} m/s")
col2.metric("Periode T", f"{periode:.2f} s")
col3.metric("Pjg Gelombang λ", f"{lamda} m")

# Kuis sederhana
st.subheader("🧠 Test Pemahaman")
f_input = st.number_input("Frekuensi f (Hz)", 0.1, 5.0, 1.0)
l_input = st.number_input("Panjang gelombang λ (m)", 1.0, 20.0, 5.0)

if st.button("Hitung v = f × λ"):
    v_hasil = f_input * l_input
    st.success(f"✅ v = {v_hasil:.1f} m/s")
    st.balloons()

st.markdown("---")
st.caption("🎓 Simulasi untuk pelajaran fisika SMA - Gelombang Transversal")
