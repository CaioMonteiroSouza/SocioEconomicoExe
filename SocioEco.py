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

home = expanduser("~")
caminho = os.path.join(home, "SocioEcoGraphs")
caminhoImagens = os.path.join(caminho, "Images")
os.mkdir(caminho)
os.mkdir(caminhoImagens)

print(caminho)

TITLE = "Graficos Perfil Socio Economico"
WIDTH = 210
HEIGHT = 297

def CriaPDF():
    pdf = FPDF()
    caminhoPdf = os.path.join(caminho, "annual_performance_report.pdf")


    pdf.add_page()
    pdf.image(CursosCaminho, 10, 8, 100)

    pdf.output(caminhoPdf, 'F')

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        return file_path
    else:
        return None

def CriaGraficoCursos(df):
    cursos = df
    ContadorCursos = Counter(cursos)
    CursosNomes = list(ContadorCursos.keys())
    CursosFrequencias = list(ContadorCursos.values())
    global CursosCaminho
    CursosCaminho = os.path.join(caminhoImagens, "Cursos.png")
    print(CursosCaminho)

    plt.pie(CursosFrequencias, labels=CursosNomes, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')

    plt.title('Distribuição de cursos')

    plt.savefig(CursosCaminho)

def CriaGraficoPeriodo(df):
    periodos = df
    ContadorPeriodos = Counter(periodos)
    PeriodoNomes = list(ContadorPeriodos.keys())
    PeriodoFrequencias = list(ContadorPeriodos.values())

    plt.pie(PeriodoFrequencias, labels=PeriodoNomes, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')

    plt.title('Distribuição de periodos')

    plt.savefig("images/Periodos.png")

def CriaGraficoEstados(df):
    Estados = df
    ContadorEstados = Counter(Estados)
    PeriodoEstados = list(ContadorEstados.keys())
    EstadosFrequencias = list(ContadorEstados.values())

    plt.pie(EstadosFrequencias, labels=PeriodoEstados, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')

    plt.title('Estados de nascimento')

    plt.savefig("images/Estados.png")
    
def CriaGraficoCidades(df):
    Cidades = df
    ContadorCidades = Counter(Cidades)
    PeriodoCidades = list(ContadorCidades.keys())
    CidadesFrequencias = list(ContadorCidades.values())

    plt.pie(CidadesFrequencias, labels=PeriodoCidades, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')

    plt.title('Cidades de residência')

    plt.savefig("images/Cidades.png")    

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
    browse_button = tk.Button(root, text="Browse", command=get_file_path)
    browse_button.place(relx=0.5, rely=0.5, anchor='center')

    # Start the main event loop
    root.mainloop()
    
    #Carrega modelo de ML para analise das questões abertas
    nlp = spacy.load(r"C:/Users/caio/anaconda3/envs/envsocioeco/lib/site-packages/pt_core_news_sm/pt_core_news_sm-3.6.0")
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
    df['Data de nascimento'] = pd.to_datetime(df['Data de nascimento'], dayfirst=True).dt.date
    DiaAtual = pd.Timestamp(date.today())
    for i in range(len(df['Data de nascimento'])):
        if DiaAtual < df['Data de nascimento'][i]:
            df.loc[[i], ['Data de nascimento']] = np.na

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

    CriaGraficoCursos(df['Qual o seu curso ?'])
    #CriaGraficoPeriodo(df['Qual o Período que você cursa? '])
    #CriaGraficoEstados(df['Em qual estado do Brasil você nasceu ?'])
    #CriaGraficoCidades(df['Qual a sua cidade de Residência ? (Em qual cidade você mora?)'])

    CriaPDF()

if __name__ == "__main__":
    main()