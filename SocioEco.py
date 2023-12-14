import pandas as pd
import numpy as np
import spacy
from datetime import date
from difflib import SequenceMatcher
from spacy.matcher import Matcher 
from collections import Counter
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import fpdf
from fpdf import FPDF
import os
from os.path import expanduser
import pt_core_news_sm
import string

home = expanduser("~")
caminho = os.path.join(home, "SocioEcoGraphs")
caminhoImagens = os.path.join(caminho, "Images")


def CriaPDF():
    pdf = FPDF()
    caminhoPdf = os.path.join(caminho, "PerfilSocioEco.pdf")


    pdf.add_page()
    pdf.image(CursosCaminho, 10, 8, 100)

    pdf.output(caminhoPdf, 'F')

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        return file_path
    else:
        return None

def CriaGrafico(df, Nome):
    data = df
    data = [x for x in data if x != "nan"]
    Contador = Counter(data)
    Nomes = list(Contador.keys())
    Frequencias = list(Contador.values())
    y = np.array(Frequencias)
    global CursosCaminho
    caminho1 = str(Nome) + ".png"
    CursosCaminho = os.path.join(caminhoImagens, caminho1)
    porcent = 100.*y/y.sum()

    patches, texts = plt.pie(Frequencias, startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(Nomes, porcent)]

    sort_legend = True
    if sort_legend:
        patches, labels, dummy =  zip(*sorted(zip(patches, labels, Contador),
                                          key=lambda x: x[2],
                                          reverse=True))

    plt.legend(patches, labels, loc='best', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)

    plt.savefig(CursosCaminho, bbox_inches='tight')
    plt.clf() 

def CriaGraficoSonhos(df, Nome):
    data = df
    Contador = Counter(data)
    Nomes, Frequencias = zip(*data)
    y = np.array(Frequencias)
    global CursosCaminho
    caminho1 = str(Nome) + ".png"
    CursosCaminho = os.path.join(caminhoImagens, caminho1)
    porcent = 100.*y/y.sum()

    patches, texts = plt.pie(Frequencias, startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(Nomes, porcent)]

    sort_legend = True
    if sort_legend:
        patches, labels, dummy =  zip(*sorted(zip(patches, labels, Contador),
                                          key=lambda x: x[2],
                                          reverse=True))

    plt.legend(patches, labels, loc='best', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)

    plt.savefig(CursosCaminho, bbox_inches='tight')
    plt.clf() 

def GraficoPessoasCasa(df):
    data = df
    Contador = Counter(data)
    Nomes = list(Contador.keys())
    Frequencias = list(Contador.values())
    caminho1 = "PessoasCasa.png"
    CursosCaminho = os.path.join(caminhoImagens, caminho1)


    total = sum(Frequencias)
    percents = [(value / total) * 100 for value in Frequencias]
    patches, texts = plt.pie(percents, startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(Nomes, percents)]

    sort_legend = True
    if sort_legend:
        patches, labels, dummy =  zip(*sorted(zip(patches, labels, Contador),
                                          key=lambda x: x[2],
                                          reverse=True))

    plt.legend(patches, labels, loc='best', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)

    plt.savefig(CursosCaminho, bbox_inches='tight')
    plt.clf() 

def GraficoAnosMoradia(df):
    data = df
    Contador = Counter(data)
    Nomes = list(Contador.keys())
    Frequencias = list(Contador.values())
    caminho1 = "AnosMoradia.png"
    CursosCaminho = os.path.join(caminhoImagens, caminho1)


    total = sum(Frequencias)
    percents = [(value / total) * 100 for value in Frequencias]
    patches, texts = plt.pie(percents, startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(Nomes, percents)]

    sort_legend = True
    if sort_legend:
        patches, labels, dummy =  zip(*sorted(zip(patches, labels, Contador),
                                          key=lambda x: x[2],
                                          reverse=True))

    plt.legend(patches, labels, loc='best', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)

    plt.savefig(CursosCaminho, bbox_inches='tight')
    plt.clf() 


def main():
    root = tk.Tk()
    root.title("Excel File Browser")
    root.geometry("300x250")

    def get_file_path():
        selected_path = browse_file()
        global CaminhoArquivo
        CaminhoArquivo = selected_path
        root.destroy()

    # Create a browse button
    browse_button = tk.Button(root, text="Pesquisar Planilha", command=get_file_path)
    browse_button.place(relx=0.5, rely=0.5, anchor='center')

    # Start the main event loop
    root.mainloop()
    
    #Carrega modelo de ML para analise das questões abertas
    nlp = pt_core_news_sm.load()
    print(nlp._path)
    nlp.Defaults.stop_words.add("trabalho")
    nlp.Defaults.stop_words.remove("nenhuma")

    #Le o arquivo excel
    df = pd.read_excel(CaminhoArquivo)

    #Exclui colunas que não serão utilizdas
    df = df.drop(columns=['Hora de início','Hora de conclusão', 'Hora da última modificação'])

    #Junta as 3 colunas dos meses em uma só
    df[['Mês de nascimento2', 'Mês de nascimento:', 'Mês de nascimento']] = df[['Mês de nascimento2', 'Mês de nascimento:', 'Mês de nascimento']].replace(np.nan, '')
    df['Holder'] = df['Mês de nascimento2'].astype(str) + df['Mês de nascimento:'].astype(str) + df['Mês de nascimento'].astype(str)
    df = df.drop(columns=['Mês de nascimento', 'Mês de nascimento2', 'Mês de nascimento:'])
    df.insert(9, 'Mês de nascimento', df['Holder'])
    df = df.drop(columns=['Holder'])

    #deixa a data de nascimento no formato dia-mes-ano
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Janeiro', '01')
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Fevereiro', '02')
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Março', '03')
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Abril', '04')
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Maio', '05')
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Junho', '06')
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Julho', '07')
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Agosto', '08')
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Setembro', '09')
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Outubro', '10')
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Novembro', '11')
    df['Mês de nascimento'] = df['Mês de nascimento'].replace('Dezembro', '12')
    df['Holder'] = df['Dia do nascimento:'].astype(str) + '-' + df['Mês de nascimento'].astype(str) + '-' + df['Ano de nascimento'].astype(str)
    df = df.drop(columns=['Mês de nascimento'])
    df.insert(10, 'Data de nascimento', df['Holder'])
    df = df.drop(columns=['Holder', 'Dia do nascimento:', 'Ano de nascimento'])

    #transforma a coluna Data que tinha o tipo string no tipo datetime
    df['Data de nascimento'] = pd.to_datetime(df['Data de nascimento'], dayfirst=True)
    DiaAtual = pd.Timestamp('now')
    for i in range(len(df['Data de nascimento'])):
        if DiaAtual < df['Data de nascimento'][i]:
            df.loc[[i], ['Data de nascimento']] = np.na
    
    idades = (DiaAtual - df['Data de nascimento']).astype('timedelta64[Y]') 
    idades = idades.astype(int)

    #Deixa o nome da empresa igual outras ocorrencias(ele considera a primeira ocorrencia como a correta, ent talvez seja 
    #necessario uma analise manual)
    df['Qual empresa que você está contratado agora?'] = df['Qual empresa que você está contratado agora?'].str.lower()
    df['Qual empresa que você está contratado agora?'] = df['Qual empresa que você está contratado agora?'].str.normalize('NFKD').str.encode('ascii', 'ignore').str.decode('ascii')
    df['Qual empresa que você está contratado agora?'] = df['Qual empresa que você está contratado agora?'].str.replace('[^a-zA-Z0-9]', ' ')
    df['Qual empresa que você está contratado agora?'] = df['Qual empresa que você está contratado agora?'].str.replace('  ', ' ')
    df['Qual empresa que você está contratado agora?'] = df['Qual empresa que você está contratado agora?'].fillna("")
    df['Qual empresa que você está contratado agora?'] = df['Qual empresa que você está contratado agora?'].str.strip(" ")

    for i in range(len(df['Qual empresa que você está contratado agora?'])):
        if df['Qual empresa que você está contratado agora?'][i] != None:
            df['NomesEmpresas'] = df['Qual empresa que você está contratado agora?'].copy()
            NomesEmpresas = df['NomesEmpresas'].copy()

    def RemoveStopWords(sentence):
        doc = nlp(sentence)
        filtered_tokens = [token for token in doc if not token.is_stop]
        return ' '.join([token.text for token in filtered_tokens])


    for i in range(len(NomesEmpresas)):
        NomesEmpresas[i] = RemoveStopWords(NomesEmpresas[i])
        
    for i in range(len(df['NomesEmpresas'])):
        df.at[i, 'NomesEmpresas'] = NomesEmpresas[i]

    df['NomesEmpresas'] = df['NomesEmpresas'].astype(str)

    thereshold = 0.80
    for i, Nome1 in enumerate(NomesEmpresas[:-1]):
        for Nome2 in NomesEmpresas[i+1:]:
            if Nome1 != '' and Nome2 != '':
                Similaridade = SequenceMatcher(None, Nome1, Nome2).ratio()
                if Similaridade > thereshold:
                    df['NomesEmpresas'] = df['NomesEmpresas'].str.replace(Nome1, Nome2)
                
    df['Qual empresa que você está contratado agora?'] = df['NomesEmpresas']
    df = df.drop(columns=['NomesEmpresas'])

    #Junta as colunas como TV e TV2 em uma só
    df[['TV', 'TV2']] = df[['TV', 'TV2']].replace(np.nan, "")
    df['Holder'] = df['TV'].astype(str) + df['TV2'].astype(str)
    df = df.drop(columns=['TV', 'TV2'])
    df.insert(69, 'TV', df['Holder'])
    df = df.drop(columns=['Holder'])

    df[['Internet', 'Internet2']] = df[['Internet', 'Internet2']].replace(np.nan, "")
    df['Holder'] = df['Internet'].astype(str) + df['Internet2'].astype(str)
    df = df.drop(columns=['Internet', 'Internet2'])
    df.insert(70, 'Internet', df['Holder'])
    df = df.drop(columns=['Holder'])

    df[['Revistas', 'Revistas2']] = df[['Revistas', 'Revistas2']].replace(np.nan, "")
    df['Holder'] = df['Revistas'].astype(str) + df['Revistas2'].astype(str)
    df = df.drop(columns=['Revistas', 'Revistas2'])
    df.insert(71, 'Revistas', df['Holder'])
    df = df.drop(columns=['Holder'])

    df[['Rádio2', 'Rádio3']] = df[['Rádio2', 'Rádio3']].replace(np.nan, "")
    df['Holder'] = df['Rádio2'].astype(str) + df['Rádio3'].astype(str)
    df = df.drop(columns=['Rádio2', 'Rádio3'])
    df.insert(71, 'Rádio2', df['Holder'])
    df = df.drop(columns=['Holder'])

    df[['Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).', 'Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).2']] = df[['Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).', 'Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).2']].replace(np.nan, "")
    df['Holder'] = df['Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).'].astype(str) + df['Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).2'].astype(str)
    df = df.drop(columns=['Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).', 'Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).2'])
    df.insert(73, 'Feed das Redes Sociais (Instagram, Youtube, TikTok, Twitter).', df['Holder'])
    df = df.drop(columns=['Holder'])

    df[['Conversas informais com amigos', 'Conversas informais com amigos2']] = df[['Conversas informais com amigos', 'Conversas informais com amigos2']].replace(np.nan, "")
    df['Holder'] = df['Conversas informais com amigos'].astype(str) + df['Conversas informais com amigos2'].astype(str)
    df = df.drop(columns=['Conversas informais com amigos', 'Conversas informais com amigos2'])
    df.insert(74, 'Conversas informais com amigos', df['Holder'])
    df = df.drop(columns=['Holder'])

    df[['Você tem plano de saúde privado?', 'Você tem plano de saúde privado?2']] = df[['Você tem plano de saúde privado?', 'Você tem plano de saúde privado?2']].replace(np.nan, "")
    df['Holder'] = df['Você tem plano de saúde privado?'].astype(str) + df['Você tem plano de saúde privado?2'].astype(str)
    df = df.drop(columns=['Você tem plano de saúde privado?2', 'Você tem plano de saúde privado?'])
    df.insert(39, 'Você tem plano de saúde privado?', df['Holder'])
    df = df.drop(columns=['Holder'])

    #Transforma a coluna de fontes de entretenimento em varias
    df2 = df['Quais fontes de ENTRETENIMENTO CULTURAL você usa?*'].str.get_dummies(sep=';')
    df.insert(83, 'Filmes', df2['Filmes'])
    df.insert(84, 'Música', df2['Música'])
    df.insert(85, 'Cinema', df2['Cinema'])
    df.insert(86, 'Documentários', df2['Documentários'])
    df.insert(87, 'Literatura', df2['Literatura'])
    df.insert(88, 'TV2', df2['TV'])
    df.insert(89, 'Teatro', df2['Teatro'])
    df = df.drop(columns=['Quais fontes de ENTRETENIMENTO CULTURAL você usa?*'])

    #Transforma a coluna de escolha do curso em varias
    df2 = df['Por que escolheu este curso?'].str.get_dummies(sep=';')
    df.insert(91, 'Este curso termina rápido (média duração)', df2['Este curso termina rápido (média duração)'])
    df.insert(92, 'Este curso é gratuito', df2['Este curso é gratuito'])
    df.insert(93, 'Facilidade de ser absorvido no mercado', df2['Facilidade de ser absorvido no mercado'])
    df.insert(94, 'Já trabalho na área', df2['Já trabalho na área'])
    df.insert(95, 'Não é o que eu queria, mas tenho talento pra isso', df2['Não é o que eu queria, mas tenho talento pra isso'])
    df.insert(96, 'Porque é uma profissão bem conceituada', df2['Porque é uma profissão bem conceituada'])
    df.insert(97, 'Profissão bem-remunerada', df2['Profissão bem-remunerada'])
    df.insert(98, 'Sugestão ou vontade familiar', df2['Sugestão ou vontade familiar'])
    df.insert(99, 'É minha verdadeira vocação', df2['É minha verdadeira vocação'])
    df = df.drop(columns=['Por que escolheu este curso?'])

    df['Qual/Quais? (Pode selecionar mais de uma, se for o caso)'] = df['Qual/Quais? (Pode selecionar mais de uma, se for o caso)'].dropna()
    df['Qual/Quais? (Pode selecionar mais de uma, se for o caso)'] = df['Qual/Quais? (Pode selecionar mais de uma, se for o caso)'].astype(str)

    df['Quantas pessoas (incluindo você) moram no seu domicílio ?'][df['Quantas pessoas (incluindo você) moram no seu domicílio ?'] > 5] = "Mais que 5"
    df['Quantas pessoas (incluindo você) moram no seu domicílio ?'] = df['Quantas pessoas (incluindo você) moram no seu domicílio ?'].astype(str)
    df['Quantas pessoas (incluindo você) moram no seu domicílio ?'] = df['Quantas pessoas (incluindo você) moram no seu domicílio ?'].replace("2", "2 - 3")
    df['Quantas pessoas (incluindo você) moram no seu domicílio ?'] = df['Quantas pessoas (incluindo você) moram no seu domicílio ?'].replace("3", "2 - 3")
    df['Quantas pessoas (incluindo você) moram no seu domicílio ?'] = df['Quantas pessoas (incluindo você) moram no seu domicílio ?'].replace("4", "4 - 5")
    df['Quantas pessoas (incluindo você) moram no seu domicílio ?'] = df['Quantas pessoas (incluindo você) moram no seu domicílio ?'].replace("5", "4 - 5")

    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].astype(float)
    df['Quanto tempo de moradia nesse domícilio?'] = df.apply(lambda x: x['Quanto tempo de moradia nesse domícilio?'] / 12, axis= 1)
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].round()
    df['Quanto tempo de moradia nesse domícilio?'][df['Quanto tempo de moradia nesse domícilio?'] > 10] = "Mais que 10"
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].astype(str)
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].replace("0.0", "Menos que 1")
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].replace("1.0", "1 - 5")
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].replace("2.0", "1 - 5")
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].replace("3.0", "1 - 5")
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].replace("4.0", "1 - 5")
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].replace("5.0", "1 - 5")
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].replace("6.0", "6 - 10")
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].replace("7.0", "6 - 10")
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].replace("8.0", "6 - 10")
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].replace("9.0", "6 - 10")
    df['Quanto tempo de moradia nesse domícilio?'] = df['Quanto tempo de moradia nesse domícilio?'].replace("10.0", "6 - 10")

    idadesFinal = []
    for idade in idades:
        if idade < 18:
            idadesFinal.append("Menor que 18")
        elif idade >= 18 and idade < 25:
            idadesFinal.append("18-25")
        elif idade >= 25 and idade < 30:
            idadesFinal.append("25-30")
        elif idade >= 30 and idade < 40:
            idadesFinal.append("30-40")
        elif idade >= 40 and idade <= 50:
            idadesFinal.append("30-40")
        else:
            idadesFinal.append("Maior que 50")

    df['Qual empresa que você está contratado agora?'] = df['Qual empresa que você está contratado agora?'].replace("", np.nan)
    df['Qual empresa que você está contratado agora?'] = df['Qual empresa que você está contratado agora?'].dropna()
    df['Qual empresa que você está contratado agora?'] = df['Qual empresa que você está contratado agora?'].astype(str)

    columns_to_dropna = [35,36,38,39,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,29,60,61,65,74,75,76]

    for columns_index in columns_to_dropna:
        column_name = df.columns[columns_index]
        df[column_name] = df[column_name].dropna()
        df[column_name] = df[column_name].astype(str)

    indexes = [82,83,84,85,86,87,88,90,91,92,93,94,95,96,97,98]

    for columns_index in indexes:
        column_name = df.columns[columns_index]
        df[column_name] = df[column_name].astype(str)
        df[column_name] = df[column_name].replace("1", "Sim")
        df[column_name] = df[column_name].replace("0", "Não")

    #transforma o sonho em uma megastring para ser analizada pelo spacy
    df['Escreva algumas linhas sobre sua história e seus sonhos de vida.'].astype(str)
    df['Escreva algumas linhas sobre sua história e seus sonhos de vida.'] = np.where(df['Escreva algumas linhas sobre sua história e seus sonhos de vida.'].str.len()< 19, '', df['Escreva algumas linhas sobre sua história e seus sonhos de vida.'])
    MegaString = df['Escreva algumas linhas sobre sua história e seus sonhos de vida.'].str.cat(sep = ' ')
    doc = nlp(MegaString, disable = ['ner'])

    matcher = Matcher(nlp.vocab) 
    pattern = [{'POS':'ADJ'}, {'POS':'NOUN'}] 
    matcher.add('ADJ_PHRASE', [pattern]) 
    matches = matcher(doc, as_spans=True) 
    frases = [] 
    for span in matches:
        frases.append(span.text.lower())
        FrequenciaFrases = Counter(frases)
    sonhos = FrequenciaFrases.most_common(30)
    deletar = ["presente momento", "maior objetivo", "pras pessoas", "melhor atraves", "forte vontade"]
    sonhos = [(label, value) for label, value in sonhos if label not in deletar]

    columns_to_loop = [3,4,6,7,8,9,11,12,13,14,16,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,29,60,61,62,
                       63,64,65,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102]

    for columns_index in columns_to_loop:
        column_name = df.columns[columns_index]
        Translator = str.maketrans('','', string.punctuation)
        nomearquivo = column_name.translate(Translator)
        CriaGrafico(df[column_name], nomearquivo)
        
    
    GraficoPessoasCasa(df['Quantas pessoas (incluindo você) moram no seu domicílio ?'])
    GraficoAnosMoradia(df['Quanto tempo de moradia nesse domícilio?'])
    CriaGraficoSonhos(sonhos, "sonhos")
    CriaGrafico(idadesFinal, "idades")

    CriaPDF()

if __name__ == "__main__":
    main()