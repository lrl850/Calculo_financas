import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Nubank · Dashboard Março 2026",
    page_icon="💜",
    layout="wide",
)

# ── CSS personalizado ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0f0f1a; }
    .block-container { padding: 2rem 2.5rem; }

    .kpi-card {
        background: #16162a;
        border-radius: 14px;
        padding: 18px 22px;
        text-align: center;
        border: 1px solid #2a2a4a;
    }
    .kpi-label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { font-size: 22px; font-weight: 900; margin-top: 4px; }

    h1 { font-weight: 900 !important; }
    .stMultiSelect > div { background: #16162a; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Dados ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Nubank_Mes_04.xlsx")
        df.columns = ["date", "title", "Valor", "Categoria"]
    except FileNotFoundError:
        # fallback com dados reais do arquivo
        data = [
            ("2026-03-06", "SILVIA MARIA RIBEIRO LIMA",  208.99, "Mercado"),
            ("2026-03-01", "Araujo Loja",                  9.99, "Saúde"),
            ("2026-03-01", "Jhonatan Rodrigues da",         4.51, "Sacolão"),
            ("2026-03-01", "Distribuidora Wallac",         16.77, "Lazer"),
            ("2026-03-01", "Supermercados Novo Hor",       32.99, "Mercado"),
            ("2026-03-01", "Supermercados Novo Hor",       28.98, "Mercado"),
            ("2026-02-28", "Vivo Easy",                    50.00, "Moradia"),
            ("2026-02-28", "Pag*Steam - Parcela 1/3",      46.32, "Gamer"),
            ("2026-02-28", "Espacolanches",                21.50, "Alimentação_IFMG"),
            ("2026-02-28", "Distribuidora Wallac",         14.97, "Lazer"),
            ("2026-02-27", "IFOOD Pedido",                 27.96, "IFOOD"),
            ("2026-02-27", "Transporte SP",                50.00, "Transporte"),
            ("2026-02-26", "Shopee Compra",               438.23, "Compras Online"),
            ("2026-02-25", "Empréstimo",                  370.21, "Agiota"),
            ("2026-02-24", "Loja de Roupas",              171.65, "Vestuario"),
            ("2026-02-23", "RU IFMG",                      28.00, "Alimentação_IFMG"),
            ("2026-02-22", "Bandejão IFMG",                21.00, "Alimentação_IFMG"),
            ("2026-02-21", "Cantina IFMG",                 42.50, "Alimentação_IFMG"),
            ("2026-02-20", "Drogaria Saúde",                5.59, "Saúde"),
        ]
        df = pd.DataFrame(data, columns=["date", "title", "Valor", "Categoria"])
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

PALETTE = [
    "#8B5CF6","#EC4899","#F59E0B","#10B981","#3B82F6",
    "#EF4444","#06B6D4","#84CC16","#F97316","#6366F1",
    "#14B8A6","#F43F5E",
]
categorias = df.groupby("Categoria")["Valor"].sum().sort_values(ascending=False).index.tolist()
color_map = {cat: PALETTE[i % len(PALETTE)] for i, cat in enumerate(categorias)}

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("## 💜 Nubank · Dashboard de Gastos — Março 2026")
st.markdown("---")

# ── Sidebar — Filtros ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Filtros")

    selecionadas = st.multiselect(
        "Categorias",
        options=categorias,
        default=categorias,
        help="Selecione uma ou mais categorias para filtrar os gráficos",
    )

    tipo_grafico = st.radio(
        "Tipo de gráfico",
        ["Barras", "Pizza", "Barras Horizontais", "Linha por Data"],
        index=0,
    )

    ordenar = st.selectbox(
        "Ordenar por",
        ["Valor (maior → menor)", "Valor (menor → maior)", "Nome A→Z"],
    )

    st.markdown("---")
    st.markdown("#### 📂 Carregar seu arquivo")
    upload = st.file_uploader("Substitua com novo .xlsx", type=["xlsx"])
    if upload:
        df = pd.read_excel(upload)
        df.columns = ["date", "title", "Valor", "Categoria"]
        df["date"] = pd.to_datetime(df["date"])
        st.success("Arquivo carregado!")

if not selecionadas:
    st.warning("Selecione ao menos uma categoria no painel lateral.")
    st.stop()

# ── Dados filtrados ────────────────────────────────────────────────────────────
df_filtrado = df[df["Categoria"].isin(selecionadas)]
totais = df_filtrado.groupby("Categoria")["Valor"].sum().reset_index()
totais.columns = ["Categoria", "Total"]

if ordenar == "Valor (maior → menor)":
    totais = totais.sort_values("Total", ascending=False)
elif ordenar == "Valor (menor → maior)":
    totais = totais.sort_values("Total", ascending=True)
else:
    totais = totais.sort_values("Categoria")

total_geral = df["Valor"].sum()
total_sel = totais["Total"].sum()
maior_cat = totais.iloc[totais["Total"].argmax()]["Categoria"] if len(totais) else "-"
ticket_medio = totais["Total"].mean() if len(totais) else 0

# ── KPIs ───────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("💰 Total Geral", f"R$ {total_geral:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
with c2:
    st.metric("🎯 Total Selecionado", f"R$ {total_sel:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
with c3:
    st.metric("🏆 Maior Gasto", maior_cat)
with c4:
    st.metric("📊 Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.markdown("---")

# ── Gráfico Principal ──────────────────────────────────────────────────────────
col_graf, col_tabela = st.columns([3, 2])

with col_graf:
    st.markdown(f"#### 📈 {tipo_grafico} — Gastos por Categoria")

    colors = [color_map.get(c, "#7c3aed") for c in totais["Categoria"]]

    if tipo_grafico == "Barras":
        fig = px.bar(
            totais, x="Categoria", y="Total",
            color="Categoria", color_discrete_map=color_map,
            text=totais["Total"].apply(lambda v: f"R$ {v:.2f}"),
            template="plotly_dark",
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, xaxis_tickangle=-35)

    elif tipo_grafico == "Pizza":
        fig = px.pie(
            totais, names="Categoria", values="Total",
            color="Categoria", color_discrete_map=color_map,
            hole=0.4, template="plotly_dark",
        )
        fig.update_traces(textinfo="label+percent", pull=[0.03]*len(totais))

    elif tipo_grafico == "Barras Horizontais":
        fig = px.bar(
            totais.sort_values("Total"), x="Total", y="Categoria",
            orientation="h", color="Categoria", color_discrete_map=color_map,
            text=totais.sort_values("Total")["Total"].apply(lambda v: f"R$ {v:.2f}"),
            template="plotly_dark",
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)

    else:  # Linha por Data
        df_time = df_filtrado.groupby(["date", "Categoria"])["Valor"].sum().reset_index()
        fig = px.line(
            df_time, x="date", y="Valor", color="Categoria",
            color_discrete_map=color_map, markers=True,
            template="plotly_dark",
        )

    fig.update_layout(
        paper_bgcolor="#16162a", plot_bgcolor="#16162a",
        font_color="#e5e7eb", height=420,
        margin=dict(t=30, b=60, l=10, r=10),
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Tabela ─────────────────────────────────────────────────────────────────────
with col_tabela:
    st.markdown("#### 📋 Detalhamento")

    tabela = totais.copy()
    tabela["% do Total"] = (tabela["Total"] / total_geral * 100).round(1).astype(str) + "%"
    tabela["% Selecionado"] = (tabela["Total"] / total_sel * 100).round(1).astype(str) + "%"
    tabela["Total"] = tabela["Total"].apply(lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.dataframe(
        tabela.reset_index(drop=True),
        use_container_width=True,
        height=380,
        hide_index=True,
    )

    st.markdown(f"""
    <div style='background:#16162a;border-radius:10px;padding:12px 16px;border:1px solid #7c3aed33;margin-top:8px;'>
        <span style='color:#a78bfa;font-size:12px;font-weight:700;'>TOTAL SELECIONADO</span><br>
        <span style='color:#ec4899;font-size:20px;font-weight:900;'>R$ {total_sel:,.2f}</span>
    </div>
    """.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

# ── Gráfico secundário — distribuição individual ───────────────────────────────
st.markdown("---")
st.markdown("#### 🧾 Transações Individuais")

df_detalhe = df_filtrado.sort_values("Valor", ascending=False).copy()
df_detalhe["date"] = df_detalhe["date"].dt.strftime("%d/%m/%Y")
df_detalhe["Valor_fmt"] = df_detalhe["Valor"].apply(lambda v: f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X","."))

fig2 = px.scatter(
    df_detalhe, x="date", y="Valor", color="Categoria",
    size="Valor", hover_name="title",
    color_discrete_map=color_map,
    template="plotly_dark", size_max=40,
)
fig2.update_layout(
    paper_bgcolor="#16162a", plot_bgcolor="#16162a",
    font_color="#e5e7eb", height=320,
    margin=dict(t=20, b=40, l=10, r=10),
)
st.plotly_chart(fig2, use_container_width=True)

st.dataframe(
    df_detalhe[["date","title","Categoria","Valor_fmt"]].rename(columns={
        "date":"Data","title":"Descrição","Valor_fmt":"Valor"
    }).reset_index(drop=True),
    use_container_width=True,
    hide_index=True,
)