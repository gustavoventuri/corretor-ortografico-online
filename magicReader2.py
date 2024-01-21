from flask import Flask, request, render_template
import language_tool_python
from collections import Counter
import re

app = Flask(__name__)
tool = language_tool_python.LanguageTool('pt-BR')


def limpa_texto():
    with open('ranking_palavras.txt','r',encoding='latin1') as f:
        texto = f.read()
        texto_limpo = re.sub(r'[^a-zA-Z ]', '', texto)
        palavras_ranking = set(texto_limpo.split())
    return palavras_ranking

with open('ranking_palavras.txt','r',encoding='latin1') as f:
    palavras_ranking = set(f.read().split())


def correcao_texto(txt):
    with open('ranking_palavras.txt','r',encoding='latin1') as f:
        palavras_comuns = f.read()
        palavras_comuns = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚâêîôûÂÊÎÔÛãõÃÕçÇ ]', '', palavras_comuns)
        palavras_comuns = set(palavras_comuns.split())
        print(len(palavras_comuns))

    matches = tool.check(txt)

    while len(matches) != 0:
        corrigido = txt
        idx = matches[0].offset + matches[0].errorLength
        t = txt[:idx]
        t1 = txt[:matches[0].offset]        
        rep = next((r for r in matches[0].replacements if r.lower() in palavras_comuns),None)   

        print(f'rep - comuns: {rep}')
        if rep is None:
            rep = matches[0].replacements[0]
            print(f'rep - matches: {rep}')
        else:
            rep = rep
        corr = t1 + rep
        n_idx = len(corr)
        corrigido = corr + corrigido[idx:]
        print(corr)
        txt = corrigido
        matches = tool.check(txt)
    
    return txt


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text'] 
        texto_corrigido = correcao_texto(text) 
        corrected_text = text
        apontamento_erros = text     
        matches = tool.check(corrected_text)
        qt_erros = 0
        qt_palavras = len(text.split())
        lista_erros = []
        lista_sugestoes = []
        lista_sugestoes_texto = []
        for erro in matches:            
            i = erro.offset +(4*qt_erros)
            j = erro.errorLength 
            lista_erros.append(erro.message)
            lista_sugestoes.append(erro.replacements)
            apontamento_erros = apontamento_erros[:i]  +"||"+ apontamento_erros[i:i+j] +"¨¨"+ apontamento_erros[i+j:]
            qt_erros += 1

        apontamento_erros = apontamento_erros.replace("||","<u><b>")
        apontamento_erros = apontamento_erros.replace("¨¨","</u></b>")
        nota = str(round((1-(qt_erros/qt_palavras))*100,2)) + '%'

        return render_template('index.html', original_text=text, corrected_text=texto_corrigido, qt_erros=qt_erros, qt_palavras=qt_palavras, nota=nota, apontamento_erros=apontamento_erros,lista_erros=lista_erros, lista_sugestoes=lista_sugestoes)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
