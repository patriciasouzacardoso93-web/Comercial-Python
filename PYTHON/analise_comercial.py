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

  # Mapear a Filial para cada venda e visita através da tabela de vendedores
  vend_map = (
      vendedores[['Matricula Especialista', 'Filial']]
      .drop_duplicates()
      .set_index('Matricula Especialista')['Filial']
      .to_dict()
  )
  vendas['Filial'] = vendas['MATRÍCULA'].map(vend_map)
  visitas['Filial'] = visitas['MATRÍCULA'].map(vend_map)
  print('-> Limpeza e cruzamento de filiais concluídos.')

  print('\n=== 3. ANÁLISE DE INDICADORES (KPIs) ===')

  # 3.1. Top 5 Vendedores
  top_vendedores = (
      vendas.groupby('MATRÍCULA').size().reset_index(name='Vendas_Totais')
  )
  top_vendedores = top_vendedores.sort_values(
      by='Vendas_Totais', ascending=False
  )
  print('\n--- Top 5 Vendedores por Volume de Vendas ---')
  print(top_vendedores.head(5).to_string(index=False))

  # 3.2. Taxa de Conversão por Filial (Vendas / Visitas)
  vendas_filial = (
      vendas.groupby('Filial').size().reset_index(name='Total_Vendas')
  )
  visitas_filial = (
      visitas.groupby('Filial').size().reset_index(name='Total_Visitas')
  )
  conversao_filial = pd.merge(vendas_filial, visitas_filial, on='Filial')
  conversao_filial['Taxa_Conversao_%'] = (
      conversao_filial['Total_Vendas']
      / conversao_filial['Total_Visitas']
      * 100
  )
  conversao_filial = conversao_filial.sort_values(
      by='Taxa_Conversao_%', ascending=False
  )
  print('\n--- Taxa de Conversão por Filial (Top 5 Melhores) ---')
  print(conversao_filial.head(5).to_string(index=False))

  # 3.3. Melhor Mês em Residências
  vendas['Mes_Ano'] = vendas['DATA VENDA'].dt.to_period('M')
  residencia_vendas = vendas[
      vendas['TIPO_ESTABELECIMENTO'].str.contains(
          'Residenc|Residencial', case=False, na=False
      )
  ]
  if not residencia_vendas.empty:
    melhor_mes_res = (
        residencia_vendas.groupby('Mes_Ano')
        .size()
        .reset_index(name='Vendas_Residenciais')
    )
    melhor_mes_res = melhor_mes_res.sort_values(
        by='Vendas_Residenciais', ascending=False
    )
    print('\n--- Melhor Mês em Residências ---')
    print(melhor_mes_res.head(1).to_string(index=False))
  else:
    print('\n--- Melhor Mês em Residências --- (Sem registos residenciais)')

  # 3.4. Projeção Linear de Outubro
  outubro_vendas = vendas[vendas['DATA VENDA'].dt.month == 10]
  if not outubro_vendas.empty:
    dias_comercializados = outubro_vendas['DATA VENDA'].dt.day.nunique()
    total_vendas_outubro = len(outubro_vendas)
    # Projeção baseada nos dias com atividade no mês vs 31 dias totais
    projecao = (
        total_vendas_outubro / max(dias_comercializados, 1)
    ) * 31
    print('\n--- Projeção Linear para o Mês de Outubro ---')
    print(f'Vendas registadas em Outubro: {total_vendas_outubro}')
    print(f'Projeção estimada de fechamento (linear): {projecao:.0f} vendas')
  else:
    print(
        '\n--- Projeção Linear para o Mês de Outubro --- (Sem dados para'
        ' outubro)'
    )

  print(
      '\n=== Processo Automatizado de ETL e Análise Completa Concluído com'
      ' Sucesso! ==='
  )


if __name__ == '__main__':
  executar_analise_completa()