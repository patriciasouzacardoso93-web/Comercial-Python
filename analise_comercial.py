import numpy as np
import pandas as pd


def executar_analise_completa():
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

  # Mapear a Filial para cada venda através da tabela de vendedores
  vend_map = (
      vendedores[['Matricula Especialista', 'Filial']]
      .drop_duplicates()
      .set_index('Matricula Especialista')['Filial']
      .to_dict()
  )
  vendas['Filial'] = vendas['MATRÍCULA'].map(vend_map)
  visitas['Filial'] = visitas['MATRÍCULA'].map(vend_map)

  print('-> Limpeza e cruzamento de filiais concluídos.')

  print('\n=== 3. ANÁLISE DE DADOS (KPIs) ===')
  # Total de vendas por tipo de estabelecimento
  resumo_estab = (
      vendas.groupby('TIPO_ESTABELECIMENTO')
      .size()
      .reset_index(name='Total_Vendas')
  )
  print('\nDesempenho por Tipo de Estabelecimento:')
  print(resumo_estab.to_string(index=False))

  # Top 5 Vendedores com mais vendas
  top_vendedores = (
      vendas.groupby('MATRÍCULA').size().reset_index(name='Vendas_Totais')
  )
  top_vendedores = top_vendedores.sort_values(
      by='Vendas_Totais', ascending=False
  )
  print('\nTop 5 Vendedores (Matrícula) por Volume de Vendas:')
  print(top_vendedores.head(5).to_string(index=False))

  print(
      '\n=== Processo Automatizado de ETL e Análise Concluído com'
      ' Sucesso! ==='
  )


if __name__ == '__main__':
  executar_analise_completa()