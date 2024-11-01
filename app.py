import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar os dados do Excel
file_path = "docsPGTWeb_SO_31out2024.xlsx"
df = pd.read_excel(file_path)

# Definir título do aplicativo
st.title("Dashboard de Documentos PGT")

# Filtros laterais
tipos_documento = ['Todos'] + sorted(list(df['Tipo de documento PGT'].unique()))
assentamentos = ['Todos'] + sorted(list(df['Assentamento'].unique()))
nomes_t1 = ['Todos'] + sorted(list(df['Nome T1'].unique()))

selected_tipo_documento = st.sidebar.selectbox("Selecione um tipo de documento:", tipos_documento, key="tipo_documento")
selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos, key="assentamento")
selected_nome_t1 = st.sidebar.selectbox("Selecione um nome T1:", nomes_t1, key="nome_t1")

# Filtrar por tipo de documento
if selected_tipo_documento != "Todos":
    df = df[df['Tipo de documento PGT'] == selected_tipo_documento]

# Filtrar por assentamento
if selected_assentamento != "Todos":
    df = df[df['Assentamento'] == selected_assentamento]

# Filtrar por nome T1
if selected_nome_t1 != "Todos":
    df = df[df['Nome T1'] == selected_nome_t1]

# Gráfico de pizza para tipos de documento
st.subheader("Distribuição por Tipo de Documento")
tipo_documento_data = df['Tipo de documento PGT'].value_counts()
fig_tipo_documento = px.pie(
    names=tipo_documento_data.index,
    values=tipo_documento_data.values,
    title='Distribuição dos Documentos por Tipo'
)
st.plotly_chart(fig_tipo_documento)

# Gráfico de barras para assentamentos
st.subheader("Distribuição por Assentamento")
assentamento_data = df['Assentamento'].value_counts()
st.bar_chart(assentamento_data)

# Exibir tabela interativa
st.subheader("Relação de Documentos")
st.write(df)

# Exibir quadro com os totais por tipo de documento e assentamento
total_por_tipo_assentamento = df.groupby(['Tipo de documento PGT', 'Assentamento']).size().reset_index(name='Quantidade de Documentos')
st.subheader("Quantidade de documentos por tipo e assentamento")
st.write(total_por_tipo_assentamento)

# Adicionar barra de progresso para Solicitação de Documentação Complementar
st.subheader("Progresso da Solicitação de Documentação Complementar")

# Calcular o total atual de solicitações
solicitacoes_atual = df[df['Tipo de documento PGT'] == 'Solicitação de documentação complementar'].shape[0]

# Definir o total a atingir
total_a_atingir = 674

# Criar gráfico de barras empilhadas para mostrar o progresso
fig_progress = go.Figure()

fig_progress.add_trace(go.Bar(
    name='Concluídos',
    x=['Solicitações'],
    y=[solicitacoes_atual],
    marker_color='green'
))

fig_progress.add_trace(go.Bar(
    name='Faltando',
    x=['Solicitações'],
    y=[max(0, total_a_atingir - solicitacoes_atual)],
    marker_color='lightgrey'
))

fig_progress.update_layout(
    barmode='stack',
    title='Progresso das Solicitações de Documentação Complementar',
    xaxis_title='Status',
    yaxis_title='Número de Documentos'
)

st.plotly_chart(fig_progress)
