import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Nubank · Gastos",
    page_icon="💜",
    layout="centered",  # centered = melhor em mobile
    initial_sidebar_state="collapsed",  # sidebar fechada por padrão no celular
)

# ── CSS Mobile-First ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Padding responsivo */
    .block-container {
        padding: 1rem 1rem 3rem 1rem !important;
        max-width: 100% !important;
    }

    /* Fundo escuro */
    .stApp { background-color: #0f0f1a; }
    .main  { background-color: #0f0f1a; }

    /* Header compacto */
    .nubank-header {
        background: linear-gradient(135deg, #7c3aed22, #ec489922);
        border: 1px solid #7c3aed44;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        margin-bottom: 16px;
    }
    .nubank-header h1 {
        font-size: clamp(18px, 5vw, 28px) !important;
        font-weight: 900 !important;
        background: linear-gradient(90deg,#a78bfa,#f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 !important;
    }
    .nubank-header p {
        color: #6b7280;
        font-size: 12px;
        margin: 4px 0 0 0;
    }

    /* KPI cards responsivos - grid 2x2 */
    .kpi-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-bottom: 16px;
    }
    .kpi-card {
        background: #16162a;
        border-radius: 12px;
        padding: 12px 14px;
        border: 1px solid #2a2a4a;
        text-align: center;
    }
    .kpi-label {
        font-size: 10px;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        line-height: 1.2;
    }
    .kpi-value {
        font-size: clamp(14px, 3.5vw, 20px);
        font-weight: 900;
        margin-top: 4px;
        line-height: 1.2;
    }

    /* Radio horizontal compacto */
    .stRadio > div {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
    }
    .stRadio label {
        font-size: 12px !important;
        padding: 4px 10px !important;
        border-radius: 20px !important;
        background: #16162a !important;
        border: 1px solid #2a2a4a !important;
        cursor: pointer !important;
        white-space: nowrap;
    }

    /* Tabela compacta */
    .stDataFrame { font-size: 12px !important; }

    /* Multiselect compacto */
    .stMultiSelect span { font-size: 12px !important; }

    /* Total card */
    .total-card {
        background: linear-gradient(135deg,#7c3aed22,#ec489922);
        border: 1px solid #7c3aed55;
        border-radius: 12px;
        padding: 14px 16px;
        text-align: center;
        margin: 10px 0;
    }

    /* Expander estilizado */
    .streamlit-expanderHeader {
        background: #16162a !important;
        border-radius: 10px !important;
        font-size: 13px !important;
        color: #a78bfa !important;
    }

    /* Esconder elementos desnecessários */
    footer { display: none !important; }
    #MainMenu { display: none !important; }
    header { display: none !important; }

    /* Mobile extra pequeno */
    @media (max-width: 400px) {
        .kpi-value { font-size: 12px !important; }
        .block-container { padding: 0.4rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ── Dados ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file=None):
    if file is not None:
        df = pd.read_excel(file)
    else:
        try:
            df = pd.read_excel("Nubank_Mes_04.xlsx")
        except FileNotFoundError:
            dados = [
                ("2026-03-06","SILVIA MARIA RIBEIRO LIMA",208.99,"Mercado"),
                ("2026-03-01","Araujo Loja",9.99,"Saúde"),
                ("2026-03-01","Jhonatan Rodrigues da",4.51,"Sacolão"),
                ("2026-03-01","Distribuidora Wallac",16.77,"Lazer"),
                ("2026-03-01","Supermercados Novo Hor",32.99,"Mercado"),
                ("2026-03-01","Supermercados Novo Hor",28.98,"Mercado"),
                ("2026-02-28","Vivo Easy",50.00,"Moradia"),
                ("2026-02-28","Pag*Steam - Parcela 1/3",46.32,"Gamer"),
                ("2026-02-28","Espacolanches",21.50,"Alimentação_IFMG"),
                ("2026-02-28","Distribuidora Wallac",14.97,"Lazer"),
                ("2026-02-27","IFOOD Pedido",27.96,"IFOOD"),
                ("2026-02-27","Transporte SP",50.00,"Transporte"),
                ("2026-02-26","Shopee Compra",438.23,"Compras Online"),
                ("2026-02-25","Empréstimo",370.21,"Agiota"),
                ("2026-02-24","Loja de Roupas",171.65,"Vestuario"),
                ("2026-02-23","RU IFMG",28.00,"Alimentação_IFMG"),
                ("2026-02-22","Bandejão IFMG",21.00,"Alimentação_IFMG"),
                ("2026-02-21","Cantina IFMG",42.50,"Alimentação_IFMG"),
                ("2026-02-20","Drogaria Saúde",5.59,"Saúde"),
            ]
            df = pd.DataFrame(dados, columns=["date","title","Valor","Categoria"])
    df.columns = ["date","title","Valor","Categoria"]
    df["date"] = pd.to_datetime(df["date"])
    return df

PALETTE = ["#8B5CF6","#EC4899","#F59E0B","#10B981","#3B82F6",
           "#EF4444","#06B6D4","#84CC16","#F97316","#6366F1","#14B8A6","#F43F5E"]

def brl(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

# ── Upload e configurações na sidebar ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    upload = st.file_uploader("📂 Carregar novo .xlsx", type=["xlsx"])
    st.markdown("---")
    ordenar = st.selectbox("Ordenar categorias", ["Valor ↓","Valor ↑","Nome A→Z"])

df = load_data(upload)
categorias = df.groupby("Categoria")["Valor"].sum().sort_values(ascending=False).index.tolist()
color_map = {c: PALETTE[i % len(PALETTE)] for i, c in enumerate(categorias)}

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='nubank-header'>
    <h1>💜 Nubank · Gastos</h1>
    <p>Março 2026 · Dashboard interativo</p>
</div>
""", unsafe_allow_html=True)

# ── Tipo de gráfico (horizontal, sem sidebar) ──────────────────────────────────
tipo = st.radio(
    "Gráfico",
    ["📊 Barras", "🥧 Pizza", "↔️ Horizontal", "📈 Linha"],
    horizontal=True,
    label_visibility="collapsed",
)

# ── Filtro de categorias em expander (economiza espaço no mobile) ─────────────
with st.expander("🏷️ Filtrar categorias", expanded=False):
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("✅ Todas", use_container_width=True):
            st.session_state["cats"] = categorias
    with col_b:
        if st.button("❌ Limpar", use_container_width=True):
            st.session_state["cats"] = [categorias[0]]

    selecionadas = st.multiselect(
        "Categorias",
        options=categorias,
        default=st.session_state.get("cats", categorias),
        label_visibility="collapsed",
    )
    st.session_state["cats"] = selecionadas

if not selecionadas:
    st.warning("⚠️ Selecione ao menos uma categoria.")
    st.stop()

# ── Processamento ──────────────────────────────────────────────────────────────
df_f = df[df["Categoria"].isin(selecionadas)]
totais = df_f.groupby("Categoria")["Valor"].sum().reset_index()
totais.columns = ["Categoria","Total"]

if ordenar == "Valor ↓":    totais = totais.sort_values("Total", ascending=False)
elif ordenar == "Valor ↑":  totais = totais.sort_values("Total", ascending=True)
else:                        totais = totais.sort_values("Categoria")

total_geral = df["Valor"].sum()
total_sel   = totais["Total"].sum()
maior_cat   = totais.iloc[totais["Total"].argmax()]["Categoria"] if len(totais) else "-"
ticket_med  = totais["Total"].mean() if len(totais) else 0

# ── KPIs 2x2 ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='kpi-grid'>
    <div class='kpi-card'>
        <div class='kpi-label'>Total Geral</div>
        <div class='kpi-value' style='color:#8B5CF6'>{brl(total_geral)}</div>
    </div>
    <div class='kpi-card'>
        <div class='kpi-label'>Selecionado</div>
        <div class='kpi-value' style='color:#EC4899'>{brl(total_sel)}</div>
    </div>
    <div class='kpi-card'>
        <div class='kpi-label'>Maior Gasto</div>
        <div class='kpi-value' style='color:#F59E0B;font-size:12px'>{maior_cat}</div>
    </div>
    <div class='kpi-card'>
        <div class='kpi-label'>Ticket Médio</div>
        <div class='kpi-value' style='color:#10B981'>{brl(ticket_med)}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Gráfico principal ──────────────────────────────────────────────────────────
LAYOUT = dict(
    paper_bgcolor="#16162a", plot_bgcolor="#16162a",
    font=dict(color="#e5e7eb", size=10),
    margin=dict(t=20, b=50, l=4, r=4),
    height=300,
    legend=dict(font=dict(size=9), orientation="h", y=-0.3, x=0),
)

if "Barras" in tipo:
    fig = px.bar(totais, x="Categoria", y="Total",
                 color="Categoria", color_discrete_map=color_map,
                 text=totais["Total"].apply(lambda v: brl(v)),
                 template="plotly_dark")
    fig.update_traces(textposition="outside", textfont_size=8)
    fig.update_layout(**LAYOUT, showlegend=False,
                      xaxis=dict(tickangle=-40, tickfont_size=8))

elif "Pizza" in tipo:
    fig = px.pie(totais, names="Categoria", values="Total",
                 color="Categoria", color_discrete_map=color_map,
                 hole=0.45, template="plotly_dark")
    fig.update_traces(textinfo="percent", textfont_size=9,
                      pull=[0.03]*len(totais))
    fig.update_layout(**LAYOUT)

elif "Horizontal" in tipo:
    fig = px.bar(totais.sort_values("Total"), x="Total", y="Categoria",
                 orientation="h", color="Categoria", color_discrete_map=color_map,
                 text=totais.sort_values("Total")["Total"].apply(lambda v: brl(v)),
                 template="plotly_dark")
    fig.update_traces(textposition="outside", textfont_size=8)
    fig.update_layout(**LAYOUT, showlegend=False,
                      yaxis=dict(tickfont_size=9))

else:
    df_t = df_f.groupby(["date","Categoria"])["Valor"].sum().reset_index()
    fig = px.line(df_t, x="date", y="Valor", color="Categoria",
                  color_discrete_map=color_map, markers=True,
                  template="plotly_dark")
    fig.update_layout(**LAYOUT)

fig.update_layout(dragmode=False)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── Barras de progresso por categoria (nativo mobile) ─────────────────────────
st.markdown("#### 📋 Categorias")
for _, row in totais.iterrows():
    pct = row["Total"] / total_sel * 100
    cor = color_map.get(row["Categoria"], "#7c3aed")
    st.markdown(f"""
    <div style='margin-bottom:12px'>
        <div style='display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px'>
            <span style='color:#e5e7eb;font-weight:600'>{row['Categoria']}</span>
            <span style='color:{cor};font-weight:700'>{brl(row['Total'])}</span>
        </div>
        <div style='background:#2a2a4a;border-radius:6px;height:8px'>
            <div style='background:{cor};width:{pct:.1f}%;height:8px;border-radius:6px;
                        transition:width 0.4s ease'></div>
        </div>
        <div style='font-size:10px;color:#6b7280;margin-top:2px'>{pct:.1f}% do selecionado</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class='total-card'>
    <div style='color:#a78bfa;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px'>
        Total Selecionado
    </div>
    <div style='color:#ec4899;font-size:26px;font-weight:900;margin-top:4px'>{brl(total_sel)}</div>
</div>
""", unsafe_allow_html=True)

# ── Transações em expander (não poluem a tela principal) ──────────────────────
with st.expander("🧾 Ver todas as transações"):
    df_det = df_f.sort_values("Valor", ascending=False).copy()
    df_det["Data"] = df_det["date"].dt.strftime("%d/%m")
    df_det["Valor R$"] = df_det["Valor"].apply(brl)
    st.dataframe(
        df_det[["Data","title","Categoria","Valor R$"]].rename(
            columns={"title":"Descrição"}
        ).reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
        height=260,
    )