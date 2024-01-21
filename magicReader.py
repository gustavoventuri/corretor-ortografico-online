import language_tool_python as corretor

import nltk
from nltk.util import ngrams
from collections import Counter
#nltk.download('punkt')

tool = corretor.LanguageTool('pt-BR')

# Aponta erros no texto
def corrigir_texto(texto):    
    matches = tool.check(texto)
    return matches

"""
def criar_modelo_ngramas(texto, n):
    # Tokenização do texto
    palavras = nltk.word_tokenize(texto, language='portuguese')

    # n-gramas
    ngramas = list(ngrams(palavras, n))

    # modelo de n-gramas (frequências dos n-gramas)
    modelo = Counter(ngramas)

    return modelo

def validar_texto(texto, modelo, n):
    # Tokenização do texto
    palavras = nltk.word_tokenize(texto, language='portuguese')

    # n-gramas
    ngramas = list(ngrams(palavras, n))

    # Verificação cada n-grama no modelo
    for ngrama in ngramas:
        if ngrama not in modelo:
            print(f"Erro encontrado: {' '.join(ngrama)}")


# base de textos para treino do n-grama
with open('textos_treino.txt','r', encoding='utf-8') as treino:
    texto_treino = treino.read()

"""
# testes
texto = input("Digite o texto: ")
erros = corrigir_texto(texto)

for erro in erros:
    print(erro)
    
    

#modelo = criar_modelo_ngramas(texto_treino, 2)

#texto_validacao = texto
#validar_texto(texto_validacao, modelo, 2)





