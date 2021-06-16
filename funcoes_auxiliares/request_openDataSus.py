import requests
import pandas as pd
import io

from funcoes_auxiliares.otimizacao import *
from funcoes_auxiliares.crawler import *

def del_col(dfAtual):
    colunas = ['paciente_id', 'paciente_idade', 'paciente_enumsexobiologico', 'paciente_racacor_valor', 'vacina_grupoatendimento_nome', 
                'vacina_dataaplicacao', 'vacina_nome', 'vacina_descricao_dose']
    for i in dfAtual.columns.to_list():
        if i not in colunas:
            dfAtual.drop(columns=[i], inplace=True)
    return dfAtual

def filtrar_muni(dfAtual):
    filtro = dfAtual.paciente_endereco_nmmunicipio == 'FORTALEZA'
    dfAtual = dfAtual[filtro]
    dfAtual = dfAtual.drop(columns=['paciente_endereco_nmmunicipio'])
    return dfAtual

def pre_proces_vac(dfAtual):
    dfAtual = filtrar_muni(dfAtual)
    dfAtual = del_col(dfAtual)
    return dfAtual

def edit_dates(dfAtual):
    dfAtual['vacina_dataaplicacao'] = pd.to_datetime(dfAtual['vacina_dataaplicacao'])
    dfAtual['vacina_dataaplicacao'] = dfAtual['vacina_dataaplicacao'].mask(dfAtual['vacina_dataaplicacao'].dt.year == 2020, dfAtual['vacina_dataaplicacao'] + pd.offsets.DateOffset(year=2021))
    dfAtual['vacina_dataaplicacao'] = dfAtual['vacina_dataaplicacao'].dt.date
    return dfAtual

def corrigir_nome_vacina(dfAtual):
    dfAtual.vacina_nome.replace('Covid-19-Coronavac-Sinovac/Butantan', 'Coronavac', inplace=True)
    dfAtual.vacina_nome.replace('Vacina Covid-19 - Covishield', 'AstraZeneca', inplace=True)
    dfAtual.vacina_nome.replace('Vacina covid-19 - BNT162b2 - BioNTech/Fosun Pharma/Pfizer', 'Pfizer', inplace=True)
    dfAtual.vacina_nome.replace('Covid-19-AstraZeneca', 'AstraZeneca', inplace=True)
    return dfAtual

def fase_vac(dfAtual):
    dicFase = {'Outros': 'Outros',
                'Outros Grupos': 'Outros',
                'Pessoas de 80 anos ou mais': 'Fase 1',
                'Pessoas de 75 a 79 anos': 'Fase 1',
                'Médico': 'Fase 1',
                'Técnico de Enfermagem': 'Fase 1',
                'Enfermeiro(a)': 'Fase 1',
                'Odontologista': 'Fase 1',
                'Fisioterapeutas': 'Fase 1',
                'Auxiliar de Enfermagem': 'Fase 1',
                'Psicólogo': 'Fase 1',
                'Farmacêutico': 'Fase 1',
                'Técnico de Odontologia': 'Fase 1',
                'Pessoas de 60 nos ou mais Institucionalizadas': 'Fase 1',
                'Nutricionista': 'Fase 1',
                'Povos indígenas em terras indígenas': 'Fase 1',
                'Pessoas com Deficiência Institucionalizadas': 'Fase 1',
                'Biomédico': 'Fase 1',
                'Funcionário do Sistema Funerário c/ cadáveres potencialmente contaminados': 'Fase 1',
                'Acadêmicos/estudantes em estágio em estabelecimentos de saúde': 'Fase 1',
                'Pessoas de 60 a 64 anos': 'Fase 2',
                'Pessoas de 65 a 69 anos': 'Fase 2',
                'Pessoas de 70 a 74 anos': 'Fase 2',
                'Quilombola': 'Fase 2',
                'Hipertensão de difícil controle ou com complicações/lesão de órgão alvo': 'Fase 3',
                'Diabetes Mellitus': 'Fase 3',
                'Doenças Cardiovasculares e Cerebrovasculares': 'Fase 3',
                'Obesidade Grave (Imc>=40)': 'Fase 3',
                'Pneumopatias Crônicas Graves': 'Fase 3',
                'Pessoas com Deficiências Permanente Grave': 'Fase 3',
                'Doença Renal Crônica': 'Fase 3',
                'Neoplasias': 'Fase 3',
                'Síndrome de Down': 'Fase 3',
                'Outros Imunossuprimidos': 'Fase 3',
                'Anemia Falciforme': 'Fase 3',
                'Indivíduos Transplantados de Órgão Sólido': 'Fase 3',
                'Puérpera': 'Fase 3',
                'Doença Renal': 'Fase 3',
                'Cirrose hepática': 'Fase 3',
                'Câncer': 'Fase 3',
                'Doença Pulmonar Obstrutiva Crônica': 'Fase 3',
                'Gestante': 'Fase 3',
                'Ensino Básico': 'Fase 4',
                'Ensino Superior': 'Fase 4',
                'Policial Militar': 'Fase 4',
                'Pessoal da Limpeza': 'Fase 4',
                'Segurança': 'Fase 4',
                'Recepcionista': 'Fase 4',
                'Profissionais de Educação Física': 'Fase 4',
                'Assistente Social': 'Fase 4',
                'Guarda Municipal': 'Fase 4',
                'Fonoaudiólogo': 'Fase 4',
                'Policial Civil': 'Fase 4',
                'Terapeuta Ocupacional': 'Fase 4',
                'Motorista de Ambulância': 'Fase 4',
                'Pessoas de 18 a 64 anos': 'Fase 4',
                'Bombeiro Militar': 'Fase 4',
                'Funcionário do Sistema de Privação de Liberdade': 'Fase 4',
                'Cuidador de Idosos': 'Fase 4',
                'Cozinheiro e Auxiliares': 'Fase 4',
                'Estudante': 'Fase 4',
                'Profissionais e Auxiliares de limpeza': 'Fase 4',
                'Médico Veterinário': 'Fase 4',
                'Pessoas em Situação de Rua': 'Fase 4',
                'Trabalhadores Portuários': 'Fase 4',
                'Policial Rodoviário Federal': 'Fase 4',
                'Aéreo': 'Fase 4',
                'Policial Federal': 'Fase 4',
                'Exército Brasileiro - EB': 'Fase 4',
                'Biólogo': 'Fase 4',
                'Bombeiro Civil': 'Fase 4',
                'Força Aérea Brasileira - FAB': 'Fase 4',
                'Doula/Parteira': 'Fase 4',
                'Auxiliar de Veterinário': 'Fase 4',
                'Marinha do Brasil - MB': 'Fase 4',
                'Caminhoneiro': 'Fase 4',
                'Técnico de Veterinário': 'Fase 4',
                'Aquaviário': 'Fase 4',
                'População Privada de Liberdade': 'Fase 4',
                'Trabalhadores Industriais': 'Fase 4',
                'Trabalhadores de limpeza urbana e manejo de resíduos sólidos': 'Fase 4',
                'Coletivo Rodoviário Passageiros Urbano e de Longo Curso': 'Fase 4',
                'Ferroviário': 'Fase 4',
                'Metroviário': 'Fase 4',
                'Ribeirinha': 'Fase 4'
    }

    for i in range(len(list(dicFase))):
        dfAtual.loc[dfAtual.vacina_grupoatendimento_nome == list(dicFase)[i], 'faseDeVacinacao'] = dicFase[list(dicFase)[i]]
    return dfAtual

def request_vacinados():
    link = crawler()
    print('Solicitando dados')
    data = requests.get(link, stream=True).content
    data = pd.read_csv(io.StringIO(data.decode('utf-8')), sep=';')
    print('Tratando dados')
    optimize2(data, ['vacina_dataaplicacao'])
    data = pre_proces_vac(data)
    data.drop_duplicates(keep=False,inplace=True,ignore_index=True)
    data = edit_dates(data)
    data = corrigir_nome_vacina(data)
    data = fase_vac(data)
    data.to_csv('Base de dados/vacinados.csv', sep=';')
    print('######################################################################################################')