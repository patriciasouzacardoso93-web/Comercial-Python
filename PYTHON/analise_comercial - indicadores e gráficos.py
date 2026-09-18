import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def gerar_portfolio_comercial():
  print('=== 1. EXTRAÇÃO E CARREGAMENTO ===')
  cal = pd.read_excel('calendario.xlsx', sheet_name='Calendario')
  filiais = pd.read_excel('Filiais.xlsx', sheet_name='Estrutura')
  vendas = pd.read_excel('Vendas.xlsx')
  vendedores = pd.read_excel('Vendedores.xlsx')
  visitas = pd.read_excel('Visitas.xlsx')
  print('-> Ficheiros carregados com sucesso.')

  print('\n=== 2. TRANSFORMAÇÃO E LIMPEZA (ETL) ===')
  # Padronização de datas
  vendas['DATA VENDA'] = pd.to_datetime(
      vendas['DATA VENDA'], format='%d/%m/%Y', errors='coerce'
  )
  visitas['DATA VISITA'] = pd.to_datetime(
      visitas['DATA VISITA'], format='%d/%m/%Y', errors='coerce'
  )

  # Mapear a Filial através da tabela de vendedores
  vend_map = (
      vendedores[['Matricula Especialista', 'Filial']]
      .drop_duplicates()
      .set_index('Matricula Especialista')['Filial']
      .to_dict()
  )
  vendas['Filial'] = vendas['MATRÍCULA'].map(vend_map)
  visitas['Filial'] = visitas['MATRÍCULA'].map(vend_map)
  print('-> Limpeza e cruzamento de filiais concluídos.')

  print('\n=== 3. ANÁLISE DE TENDÊNCIAS E PERCENTAGENS ===')

  # 3.1. Percentagem de Vendas por Tipo de Estabelecimento
  estab_perc = (
      vendas['TIPO_ESTABELECIMENTO']
      .value_counts(normalize=True)
      .reset_index()
  )
  estab_perc.columns = ['Tipo_Estabelecimento', 'Percentagem']
  estab_perc['Percentagem'] = (
      estab_perc['Percentagem'] * 100
  ).round(2)
  print('\n--- Distribuição Percentual por Tipo de Estabelecimento ---')
  print(estab_perc.to_string(index=False))

  # 3.2. Tendência Temporal de Vendas (por Mês)
  vendas['Ano_Mes'] = vendas['DATA VENDA'].dt.to_period('M').astype(str)
  tendencia_mensal = (
      vendas.groupby('Ano_Mes').size().reset_index(name='Total_Vendas')
  )
  print('\n--- Tendência de Vendas por Mês ---')
  print(tendencia_mensal.to_string(index=False))

  print('\n=== 4. GERAÇÃO DE GRÁFICOS PARA O GITHUB ===')

  # Estilo visual moderno para os gráficos
  plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

  # Gráfico 1: Tendência Mensal de Vendas (Linha)
  plt.figure(figsize=(10, 5))
  plt.plot(
      tendencia_mensal['Ano_Mes'],
      tendencia_mensal['Total_Vendas'],
      marker='o',
      color='#1f77b4',
      linewidth=2.5,
      markersize=6,
  )
  plt.title(
      'Tendência Temporal - Volume de Vendas Mensal',
      fontsize=14,
      fontweight='bold',
  )
  plt.xlabel('Mês/Ano', fontsize=11)
  plt.ylabel('Total de Vendas', fontsize=11)
  plt.xticks(rotation=45)
  plt.tight_layout()
  plt.savefig('tendencia_vendas_mensal.png', dpi=300)
  plt.close()

  # Gráfico 2: Distribuição Percentual por Tipo de Estabelecimento (Barras)
  plt.figure(figsize=(9, 5))
  bars = plt.bar(
      estab_perc['Tipo_Estabelecimento'],
      estab_perc['Percentagem'],
      color='#2ca02c',
  )
  plt.title(
      'Percentagem de Vendas por Tipo de Estabelecimento',
      fontsize=14,
      fontweight='bold',
  )
  plt.xlabel('Tipo de Estabelecimento', fontsize=11)
  plt.ylabel('Percentagem (%)', fontsize=11)
  plt.xticks(rotation=15)

  # Adicionar os valores percentuais em cima de cada barra
  for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0,
        yval + 0.5,
        f'{yval}%',
        ha='center',
        va='bottom',
        fontsize=10,
    )

  plt.tight_layout()
  plt.savefig('percentagem_estabelecimentos.png', dpi=300)
  plt.close()

  print(
      '-> Gráficos gerados e salvos com sucesso na pasta ("tendencia_vendas_mensal.png"'
      ' e "percentagem_estabelecimentos.png")!'
  )
  print(
      '\n=== Processo Concluído com Sucesso! Pronto para o GitHub ==='
  )


if __name__ == '__main__':
  gerar_portfolio_comercial()
  