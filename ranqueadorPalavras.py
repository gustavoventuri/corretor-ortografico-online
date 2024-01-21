from collections import Counter
import re
import string


def tokenizar_e_ordenar(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        texto = f.read()

    # Tokeniza as palavras
    palavras = re.findall(r'\b\w+\b', texto.lower())
    
    # Conta a frequência de cada palavra
    frequencia = Counter(palavras)
    
    # Ordena as palavras pela frequência
    palavras_ordenadas = sorted(frequencia.items(), key=lambda x: x[1], reverse=True)
    
    return palavras_ordenadas

ranking = tokenizar_e_ordenar('textos_treino.txt')

#escreve arquivo com o ranking
with open('ranking_palavras.txt','w') as f:
    for palavra, frequencia in ranking:
        f.write(f'{palavra}: {frequencia}\n')
