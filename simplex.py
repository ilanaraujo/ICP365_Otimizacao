# Trabalho final de Otimização
# Aluno: Ilan de Sousa Rocha de Araujo
# DRE: 115.169.959

# Bibliotecas utilizadas
import numpy as np
import pandas as pd
from datetime import datetime

# Função auxiliar que define os nomes das colunas 
# do Tableau para imprimir na tela
def define_colunas(quant_variaveis):
    colunas = ['z'] # Primeira coluna representa z

    # Insere as variáveis x
    for i in range(quant_variaveis):
        colunas.append(f'x{i+1}')
    
    colunas.append('b') # Última coluna é o vetor b
    return colunas

# Função que implementa o Simplex
def simplex(tabela : np.array):
    # Nomes das colunas do Tableau
    colunas = define_colunas(tabela.shape[1] - 2)
    df_tableau = pd.DataFrame(tabela, columns=colunas)

    print(f'Início da resolução com o Simplex\n')
    print('Tableau inicial:')
    print(f'{df_tableau}\n')
    ultima_linha = tabela[-1,:]
    iteracao = 1 # Armazena o número da iteração atual

    # Variáveis utilizadas para imprimir os resultados no final
    pares_pivo = [] # Pares linahe  coluna de cada pivô nas iterações
    constantes_x = [] # Constantes do problema inicial (Z = C1*X1 + C2*X2 +...+ Cn*Xn)
    
    # Remove constantes das variáveis de folga (iguais a zero)
    for valor in tabela[-1][1:-1] * (-1):
        if valor > 0:
            constantes_x.append(int(valor))

    # Início da execução
    inicio = datetime.now()

    # Executa o código enquanto houverem valores negativos na última linha do Tableau
    while ultima_linha.min() < 0:
        print(f'--- Início da iteração {iteracao} ---')
        print('Tableau antes da iteração:')
        print(f'{df_tableau}\n')
        col_p = ultima_linha.argmin() # Coluna pivô
        lin_p = np.argmin(tabela[:-1,-1]/tabela[:-1,col_p]) # Linha pivô
        pivo = tabela[lin_p, col_p] # Número Pivô

        print(f'Linha pivô: {lin_p}')
        print(f'Coluna pivô: {col_p}')
        print(f'Elemento pivô: {pivo}\n')

        # Linha e COluna do pivô atual
        pares_pivo.append([int(lin_p),int(col_p)])

        # Divide toda a linha pivô pelo número pivô e atualiza
        # o valor da variável com a linha pivô
        tabela[lin_p,:] = tabela[lin_p,:]*(1/pivo)
        linha_pivo = tabela[lin_p]

        # Subtrai das outras linhas a linah pivô multiplicada
        # pelo elemento da linha respectiva que está na coluna pivô
        for i in range(tabela.shape[0]):
            # Pula a execução se a linha a ser subtraída for a linha pivô
            if i == lin_p:
                continue
            # Executa a subtração da linha
            else:
                aux = tabela[i,col_p]
                tabela[i] += (-aux) * linha_pivo
        # Atualiza a variável que armazena a última linha do Tableau
        ultima_linha = tabela[-1]

        # Data Frame utilizado para imprimir de forma melhor o Tableau na tela
        df_tableau = pd.DataFrame(tabela, columns=colunas)
        print('Tableau após a Iteração:')
        print(df_tableau)
        print(f'--- Fim da iteração {iteracao} ---')
        iteracao += 1 # Incrementa o número da iteração
        print('')

    fim = datetime.now() # FIm da execução
    print(f'Tempo de execução: {fim - inicio}\n')

    problema = 'z = ' # String com o problema inicial (sem as restrições)
    for i in range(len(constantes_x)):
        problema += f'{constantes_x[i]}x{i+1} + '

    # Imprime a solução ótima
    print(f'Equação a ser maximizada: {problema[:-2]}\n')
    print('Solução ótima:')
    print(f'z = {tabela[-1,-1]}')
    for i in range(len(constantes_x)):
        # Define o valor da variável se for diferente de zero
        try:
            par_pivo = pares_pivo[i]
            valor_var = tabela[par_pivo[0],-1]
            print(f'x{i+1} = {valor_var}')

        # Valor da variável é igual a zero
        except:
            print(f'x{i+1} = 0')

    return tabela

# Tabela utilizada para exemplo
tabela_ex = np.array([[0, 3, 3, 2, 1, 0, 30],[0, 6, 3, 0, 0, 1, 48], [1, -10, -8, -1, 0, 0, 0]], dtype='float')

simplex(tabela_ex)
