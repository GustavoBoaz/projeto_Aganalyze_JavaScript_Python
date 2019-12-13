import os
import time
import pandas as pd
from glob import glob
import plotly.express as px


def compilar_dados_lineares_filial(dataframe):
    """
    Compila os dados necessários de um dado dataframe
    para a visualização de dados lienares
    
    Parameters:
    -----------
    dataframe : pandas.DataFrame
        dataframe com os dados puros de chamados executados
    
    Returns
    -------
    dados_compilados: pandas.DataFrame/None
        dataframe com as informações de contagem compiladas por filial/ano/mês;
        em caso de falha retorna objeto do tipo None
        
    execucao_bem_sucedida: bool
        bandeira de sobre o sucesso ou a falha da execução;
        retorna True em caso de sucesso e False em caso de falha

    """
    try:
        # Variável de início do cálculo de tempo
        inicio = time.time()

        # Descoberta das Colunas com Valores NAN
        dataframe.columns[dataframe.isna().any()].tolist()

        # Escolha = Completude com a moda dos valores (Somente em arquivos regionais!)
        for column in dataframe.columns[dataframe.isna().any()].tolist():
            dataframe[column] = dataframe[column].fillna(dataframe[column].mode()[0])

        # Separação dos elementos da data de abertura
        dataframe['MES'] = [int(data[-7:-5].replace('/', '')) for data in dataframe['DT ABERTURA']]
        dataframe['ANO'] = [int(data[-4:]) for data in dataframe['DT ABERTURA']]

        # Fomação da lista que se tornará o dataframe de resultados
        lista_dados = [
            [
                filial,
                ano,
                mes,
                int(dataframe[
                    (dataframe.REGIONAL == filial) &
                    (dataframe.ANO == ano) &
                    (dataframe.MES == mes)
                ].count().mean()),
                int(dataframe[
                    (dataframe.REGIONAL == filial) &
                    (dataframe.ANO == ano) &
                    (dataframe.MES == mes) &
                    (dataframe['SITUAÇÃO SLA SOLUÇÃO (TOTAL)'] == 'dentro do prazo')
                ].count().mean()),
                int(dataframe[
                    (dataframe.REGIONAL == filial) &
                    (dataframe.ANO == ano) &
                    (dataframe.MES == mes) &
                    (dataframe['SITUAÇÃO SLA SOLUÇÃO (TOTAL)'] == 'fora do prazo')
                ].count().mean())
            ]
            for filial in sorted(dataframe.REGIONAL.unique())
            for ano in sorted(dataframe.ANO.unique())
            for mes in sorted(dataframe.MES.unique())
        ]

        # Transporte dos Nomes das Colunas
        nomes_colunas = [
            'REGIONAL',
            'ANO',
            'MES',
            'QUANTIDADE DE CHAMADOS',
            'SLA DENTRO DO PRAZO',
            'SLA FORA DO PRAZO'
        ]

        # Criação do dataframe final
        dados_compilados = pd.DataFrame(data=lista_dados, columns=nomes_colunas)

        # Inserção da porcentagem de chamados dentro do prazo
        porcentagem_dentro_prazo = []

        for total_chamados, dentro_do_prazo in zip(
            dados_compilados['QUANTIDADE DE CHAMADOS'],
            dados_compilados['SLA DENTRO DO PRAZO']
        ):
            if total_chamados > 0:
                porcentagem_dentro_prazo.append((dentro_do_prazo / total_chamados) * 100)
            else:
                porcentagem_dentro_prazo.append(0)

        dados_compilados['PORCENTAGEM SLA DENTRO DO PRAZO'] = porcentagem_dentro_prazo

        # Inserção da porcentagem de chamados fora do prazo
        porcentagem_fora_prazo = []

        for total_chamados, fora_do_prazo in zip(
            dados_compilados['QUANTIDADE DE CHAMADOS'],
            dados_compilados['SLA FORA DO PRAZO']
        ):
            if total_chamados > 0:
                porcentagem_fora_prazo.append((fora_do_prazo / total_chamados) * 100)
            else:
                porcentagem_fora_prazo.append(0)

        dados_compilados['PORCENTAGEM SLA FORA DO PRAZO'] = porcentagem_fora_prazo

        # Arredondamento das casas decimais das porcentagens
        dados_compilados = dados_compilados.round({
            'PORCENTAGEM SLA DENTRO DO PRAZO': 2,
            'PORCENTAGEM SLA FORA DO PRAZO': 2
        })
        
        # Variável de fim da contagem do tempo
        fim = time.time()

        # Impressão no console para controle humano
        print('Finalizado!', end='\n\n')
        print(f'Tempo de Execução: {int(fim - inicio)} segundos', end='\n\n')
        
        # Flag de informação de sucesso na execução
        execucao_bem_sucedida = True
    
    except Exception as ex:
        
        # Impressão no console para controle humano
        print("Não Concluído!", end='\n\n')
        print("Erro durante a compilação dos dados lineares parciais.", end='\n\n')
        print(f"Mensagem de Erro: {type(ex).__name__} -> {str(ex)}")
        
        # Flag de informação de falha na execução
        execucao_bem_sucedida = False
        
        # Criação da variável final para bom funcionamento
        dados_compilados = None

    # Retorno dos dados compilados e da flag de status
    return dados_compilados, execucao_bem_sucedida


def main():
    folder_path = '../Data/Grafico_PolarStack_Raw/'
    
    # listagem de arquivos
    all_filenames = list(glob(f'{folder_path}*'))

    # Compilação de dataframes considerados
    lista_de_dataframes = []
    for filename in sorted(all_filenames):
        
        print(f"Arquivo de {filename.split('/')[-1].split('.')[0]}", end='...')
        dataframe = pd.read_csv(filename, encoding='utf-8-sig')
        
        bem_sucedido = True
        considerado, bem_sucedido = compilar_dados_lineares_filial(dataframe)
        
        if bem_sucedido:
            print('Bem Sucedido!')
            lista_de_dataframes.append(considerado)
        else:
            print("Falhou!")
            break
        
    # Junção dos dataframes
    print('\tJunção dos dataframes', end='...')
    considerado_mor = pd.concat(lista_de_dataframes, ignore_index=True)
    print('Pronto!')

    # Gravação do arquivo final
    print('\tGravação do arquivo final', end='...')
    considerado_mor.to_csv(
        f'{folder_path}regional_quantidades_ano_mes.csv',
        encoding='utf-8-sig',
        index=False
    )
    print('Pronto!', end='\n\n')


if __name__ == '__main__':
    main()