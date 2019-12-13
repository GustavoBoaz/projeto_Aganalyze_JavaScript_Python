#!/usr/bin/env python
# coding: utf-8
import os
import time
import pandas as pd
import numpy as np
from glob import glob
from datetime import timedelta


def main():
    full_bg = time.time()
    # listagem de arquivos
    all_filenames = list(glob(f'../Data/Grafico_PolarStack_Raw/*'))

    # Compilação de dataframes considerados
    lista_de_dataframes = []
    for filename in sorted(all_filenames):

        print(f"Arquivo de {filename.split('/')[-1].split('.')[0]}", end='...')
        dataframe = pd.read_csv(filename, encoding='utf-8-sig')

        bg = time.time()
        considerado, bem_sucedido = compilar_dados_polares_filial(dataframe)
        end = time.time()

        if bem_sucedido:
            print('Bem Sucedido!')
            lista_de_dataframes.append(considerado)
        else:
            print("Falhou!")
            
        # Contagem final de tempo (Parcial da Regional)
        print(f'\tTempo Parcial: {timedelta(seconds=(end - bg))}')

    
    # Junção dos dataframes
    print('\tJunção dos dataframes', end='...')
    considerado_mor = pd.concat(lista_de_dataframes, ignore_index=True)
    print('Pronto!')

    # Gravação do arquivo final
    print('\tGravação do arquivo final', end='...')
    considerado_mor.to_csv(
        '../Data/Grafico_PolarStack_Final/cliente_regional_quantidades_ano_mes.csv',
        encoding='utf-8-sig',
        index=False
    )
    print('Pronto!', end='\n\n')
    
    full_end = time.time()
    print(f'Tempo Total: {timedelta(seconds=(full_end - full_bg))}', end="\n\n")


def compilar_dados_polares_filial(dataframe):
    try:
        # Escolha = Completude com a moda dos valores (Somente em arquivos regionais!)
        for column in dataframe.columns[dataframe.isna().any()].tolist():
            dataframe[column] = dataframe[column].fillna(dataframe[column].mode()[0])

        # Criação das colunas de ano e mês
        dataframe['ANO'] = [int(data.split('/')[-1]) for data in dataframe['DT ABERTURA']]
        dataframe['MES'] = [int(data.split('/')[-2]) for data in dataframe['DT ABERTURA']]

        # Criação de Lista com todas as possibilidades das colunas escolhidas
        possibilidades = [
            [cliente, regional, ano, mes]
            for cliente in dataframe.CLIENTE.unique()
            for regional in dataframe.REGIONAL.unique()
            for ano in dataframe.ANO.unique()
            for mes in dataframe.MES.unique()
        ]

        # Contagem dos chamados dentro e fora do prazo
        contagens = [
            [
                len(dataframe[
                    (dataframe.CLIENTE == possibilidade[0]) &
                    (dataframe.REGIONAL == possibilidade[1]) &
                    (dataframe.ANO == possibilidade[2]) &
                    (dataframe.MES == possibilidade[3]) &
                    (dataframe['SITUAÇÃO SLA SOLUÇÃO (TOTAL)'] == 'dentro do prazo')
                ]),
                len(dataframe[
                    (dataframe.CLIENTE == possibilidade[0]) &
                    (dataframe.REGIONAL == possibilidade[1]) &
                    (dataframe.ANO == possibilidade[2]) &
                    (dataframe.MES == possibilidade[3]) &
                    (dataframe['SITUAÇÃO SLA SOLUÇÃO (TOTAL)'] == 'fora do prazo')
                ])
            ]
            for possibilidade in possibilidades
        ]

        # Extensão da contagem para conter as porcentagem e o total
        contagem_estendida = [
            [
                contagem[0] + contagem[1],
                contagem[0],
                contagem[1],
                100 * (contagem[0] / (contagem[0] + contagem[1])) if (contagem[0] + contagem[1]) != 0 else 0,
                100 * (contagem[1] / (contagem[0] + contagem[1])) if (contagem[0] + contagem[1]) != 0 else 0
            ]
            for contagem in contagens
        ]

        # Compilação final dos dados para geração do dataframe
        dados_finais = [
            possibilidade + contagem
            for possibilidade, contagem in zip(possibilidades, contagem_estendida)
        ]


        # Criação do dataframe a ser gravado
        compilado_final = pd.DataFrame(
            data=dados_finais,
            columns=[
                'CLIENTE',
                'REGIONAL',
                'ANO',
                'MES',
                'QUANTIDADE DE CHAMADOS',
                'SLA DENTRO DO PRAZO',
                'SLA FORA DO PRAZO',
                'PORCENTAGEM SLA DENTRO DO PRAZO',
                'PORCENTAGEM SLA FORA DO PRAZO'
            ]
        )


        # Arredondamento das casas decimais das porcentagens
        compilado_final = compilado_final.round({
            'PORCENTAGEM SLA DENTRO DO PRAZO': 2,
            'PORCENTAGEM SLA FORA DO PRAZO': 2
        })

        # Retorno do Resultado Compilado
        return compilado_final, True
    
    except Exception:
        return None, False


if __name__ == '__main__':
    main()
