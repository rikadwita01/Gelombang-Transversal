import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
import math

st.set_page_config(
    page_title="🌊 Simulasi Gelombang Transversal",
    page_icon="🌊",
    layout="wide"
)

st.markdown("""
<style>
h1 {color: #2c3e50; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.1)}
.metric {background: linear-gradient(135deg, #3498db, #2980b9); color: white}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def hitung_gelombang_transversal(A, f, lambda_, t_max=4, num_points=500):
    """Hitung snapshot gelombang transversal"""
    x = np.linspace(0, 3*lambda_, num_points)
    t = np.linspace(0, t_max, 50)
    
    # y(x,t) = A sin(2π(x/λ - ft))
    y_snapshots = []
    for ti in t:
        y = A * np.sin(2 * np.pi * (x / lambda_ - f * ti))
        y_snapshots.append(y)
    
    return x, t, y_snapshots

def animasi_gelombang(A, f, lambda_, phase=0):
    """Buat animasi gelombang"""
    x = np.linspace(0, 3*np.pi, 500)
    frames = []
    
    for i in range(100):
        t = i * 0.05
        y = A * np.sin(x - 2*np.pi*f*t + phase)
        
        frame = go.Frame(
            data=go.Scatter(x=x, y=y, mode='lines', line=dict(color='#e74c3c', width=4)),
            name=f'frame{i}'
        )
        frames.append(frame)
    
    fig = go.Figure(
        data=go.Scatter(x=x, y=A * np.sin(x + phase), mode='lines', line=dict(color='#e74c3c', width=4)),
        layout=go.Layout(
            title="🌊 Animasi Gelombang Transversal",
            xaxis=dict(title="Posisi (x)", range=[0, 3*np.pi]),
            yaxis=dict(title="Amplitudo (y)", range=[-A*1.2, A*1.2]),
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="▶️ Play", method="animate", args=[None])]
            )]
        ),
        frames=frames
    )
    return fig

# HEADER
st.title("🌊 Simulasi Gelombang Transversal")
st.markdown("### *y(x,t) = A sin(2π(x/λ - ft))*")

# SIDEBAR - PARAMETER
st.sidebar.header("⚙️ Pengaturan Gelombang")
A = st.sidebar.slider("Amplitudo A (m)", 0.5, 3.0, 1.0)
f = st.sidebar.slider("Frekuensi f (Hz)", 0.5, 3.0, 1.0)
lambda_ = st.sidebar.slider("Panjang Gelombang λ (m)", 0.5, 3.0, 1.0)
v = f * lambda_  # Kecepatan gelombang

# DISPLAY PARAMETER
col1, col2, col3, col4 = st.columns(4)
col1.metric("📏 Amplitudo", f"{A} m")
col2.metric("🔄 Frekuensi", f"{f} Hz")
col3.metric("📐 Panjang Gelombang", f"{lambda_} m")
col4.metric("🚀 Kecepatan Gelombang", f"{v:.2f} m/s")

# MAIN CONTENT
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("🎬 Animasi Real-time")
    
    # TOMTOM START BESAR!
    if st.button("▶️ **START ANIMASI GELOMBANG**", 
                type="primary", use_container_width=True, help="Klik untuk mulai!"):
        
        # Progress animasi
        progress = st.progress(0)
        status = st.empty()
        
        # Hitung data
        x, t, y_snapshots = hitung_gelombang_transversal(A, f, lambda_)
        
        for i in range(len(t)):
            # Update plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y_snapshots[i], 
                                   mode='lines', line=dict(color='#e74c3c', width=5),
                                   name=f't={t[i]:.2f}s'))
            
            # Tambah panah arah propagasi
            fig.add_annotation(x=0.1, y=A*0.8, text="← Propagasi", 
                             showarrow=True, arrowhead=2)
            
            fig.update_layout(
                title=f"🌊 Gelombang pada t={t[i]:.2f}s",
                xaxis_title="Posisi x (m)", yaxis_title="Amplitudo y (m)",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Update progress
            progress.progress((i+1)/len(t))
            status.text(f'Frame {i+1}/{len(t)} | Kecepatan: {v:.2f} m/s')
            time.sleep(0.1)
        
        status.success("✅ Animasi selesai!")
        st.balloons()

# SNAPSHOT BERBEDA WAKTU
with col_right:
    st.subheader("📸 Snapshot Berbeda Waktu")
    
    x, t, y_snapshots = hitung_gelombang_transversal(A, f, lambda_)
    
    # Pilih waktu
    waktu_idx = st.select_slider("Pilih waktu (s):", 
                                options=np.round(t, 1), value=2.0)
    
    idx = np.where(np.round(t, 1) == waktu_idx)[0][0]
    
    fig_snapshot = go.Figure()
    fig_snapshot.add_trace(go.Scatter(x=x, y=y_snapshots[idx], 
                                    mode='lines', line=dict(color='#9b59b6', width=4)))
    fig_snapshot.update_layout(
        title=f"Snapshots t={waktu_idx}s",
        xaxis_title="x (m)", yaxis_title="y (m)"
    )
    st.plotly_chart(fig_snapshot, use_container_width=True)

# TABEL DATA
st.markdown("---")
st.subheader("📊 Tabel Karakteristik Gelombang")

data = {
    "Parameter": ["Amplitudo (A)", "Frekuensi (f)", "Panjang Gelombang (λ)", 
                 "Periode (T)", "Kecepatan (v)", "Sudut Fasa"],
    "Nilai": [f"{A} m", f"{f} Hz", f"{lambda_} m", f"{1/f:.2f} s", 
             f"{v:.2f} m/s", "2π(x/λ - ft)"]
}

df = pd.DataFrame(data)
st.table(df)

# QUIZ
st.markdown("---")
st.subheader("❓ Cek Pemahaman")

col1, col2 = st.columns(2)
with col1:
    st.write("**Kecepatan gelombang v = ?**")
    jawab = st.radio("", ["A × f", "f × λ", "A / λ", "f / λ"], key="quiz")

with col2:
    if jawab == "f × λ":
        st.success("✅ BENAR! v = f × λ")
        st.latex(r"v = f \times \lambda")
    else:
        st.info("💡 Rumus: v = f × λ")

st.markdown("---")
st.markdown("*Simulasi Gelombang Transversal - Python + Streamlit*")
