import numpy as np
import pandas as pd
import datetime
import Levenshtein

from funcoes_auxiliares.otimizacao import *


def delete_wrong_dates(df_atual):
    print('Excluindo datas bsurdas')
    df_atual.idadeCaso = df_atual.idadeCaso.replace(range(101,1001), float("nan"))
    df_atual.loc[df_atual['idadeCaso'] == float("nan"), 'faixaEtaria'] = 'Sem Informacao'
    df_atual.faixaEtaria = df_atual.faixaEtaria.fillna('Sem Informacao')
    dates = ['dataResultadoExame', 'dataInicioSintomas', 'dataColetaExame']
    optimize2(df_atual, dates)
    return df_atual


def remove_columns(df_atual):
    print('Removendo colunas desnecessarias')
    df_atual = df_atual.drop(columns=['idRedcap', 'classificacaoEstadoRedcap', 'idEsus', 'idSivep',
                                'bairroCasoGeocoder', 'tipoObitoMaterno', 'codigoMunicipioCaso', 
                                'comorbidadeHiv', 'comorbidadeNeoplasias', 'paisCaso', 'estadoCaso',
                                'dataNascimento', 'requisicaoGal', 'laboratorioExame', 'cnesNotificacaoEsus',
                                'municipioNotificacaoEsus', 'localObito', 'comorbidadePuerperaSivep',
                                'comorbidadeHematologiaSivep', 'comorbidadeSindromeDownSivep',
                                'comorbidadeHepaticaSivep', 'comorbidadeNeurologiaSivep',
                                'comorbidadeImunodeficienciaSivep','comorbidadeRenalSivep', 
                                'comorbidadeObesidadeSivep', 'gestante', 'classificacaoEstadoEsus', 
                                'classificacaoFinalEsus', 'tipoTesteEsus', 'tipoLocalObito', 'classificacaoObito',
                                'evolucaoCasoEsus', 'evolucaoCasoSivep', 'tipoTesteExame',
                                'comorbidadeCardiovascularSivep',  'comorbidadeAsmaSivep', 'comorbidadeDiabetesSivep', 
                                'comorbidadePneumopatiaSivep', 'classificacaoEstadoSivep', 'dataNotificacao', 'dataSolicitacaoExame',
                                'dataInternacaoSivep', 'dataEntradaUTISivep', 'dataSaidaUTISivep', 'dataEvolucaoCasoSivep',
                                'dataNotificacaoObito', 'classificacaoFinalCasoSivep'])
    return df_atual

def correct_cboEsus(df_atual):
    print("Corrigindo profissões")
    for i in df_atual.cboEsus.value_counts().index.to_list():
        correcao = i.split('-')[1]
        if correcao[0] == ' ':
            correcao = correcao[1:]
        df_atual.cboEsus.replace(i, correcao, inplace=True)
    return df_atual

def filter_muni(df_atual):
    print('Filtrando dados para Fortaleza')
    correcoes = {}
    for i in df_atual.municipioCaso.value_counts().index:
        lev = Levenshtein.distance(i,'FORTALEZA')
        if lev < 4:
            correcoes[i] = 'FORTALEZA'
            dist = lev
    for i in range(len(list(correcoes))):
        df_atual.municipioCaso = df_atual.municipioCaso.replace(list(correcoes)[i], correcoes[list(correcoes)[i]])

    filtro = (df_atual.municipioCaso == 'FORTALEZA')
    df_atual = df_atual[filtro]
    df_atual = df_atual.drop(columns=['municipioCaso'])
    return df_atual


def date_correction(df_atual):
    print('Corrigindo datas')
    anoDeCont = []
    dataCaso = []
    result = df_atual.dataResultadoExame.to_list()
    sintomas = df_atual.dataInicioSintomas.to_list()
    exame = df_atual.dataColetaExame.to_list()

    for i in range(len(result)):
        if sintomas[i].year == 2020:
            anoDeCont.append('2020')
            dataCaso.append(sintomas[i])
        elif sintomas[i].year == 2021:
            anoDeCont.append('2021')
            dataCaso.append(sintomas[i])
        else:
            if exame[i].year == 2020:
                anoDeCont.append('2020')
                dataCaso.append(exame[i])
            elif exame[i].year == 2021:
                anoDeCont.append('2021')
                dataCaso.append(exame[i])
            else:
                if result[i].year == 2020:
                    anoDeCont.append('2020')
                    dataCaso.append(result[i])
                elif result[i].year == 2021:
                    anoDeCont.append('2021')
                    dataCaso.append(result[i])
                else:
                    anoDeCont.append('Excluir')
                    dataCaso.append('Excluir')
    df_atual['anoDeContagio'] = anoDeCont

    for i in df_atual.columns.to_list(): 
        if i[0]+i[1]+i[2]+i[3] == 'data':
            df_atual = df_atual.drop(columns=i)
    df_atual['dataCaso'] = dataCaso

    indexNames = df_atual[ (df_atual['dataCaso'] == 'Excluir') |
                            (df_atual['anoDeContagio'] == 'Excluir') ].index
    df_atual.drop(indexNames , inplace=True)

    return df_atual


def wrong_values(df_atual):
    print('Tratando valores errados')

    df_atual.bairroCaso.fillna('Indeterminado', inplace=True)

    df_atual.sexoCaso.replace('INDEFINIDO', df_atual.sexoCaso.value_counts().index[0], inplace=True)
    df_atual.sexoCaso.replace('I', df_atual.sexoCaso.value_counts().index[0], inplace=True)
    df_atual.sexoCaso.replace('N.I.', df_atual.sexoCaso.value_counts().index[0], inplace=True)
    df_atual.sexoCaso.fillna(df_atual.sexoCaso.value_counts().index[0], inplace=True)

    df_atual.resultadoFinalExame.replace('Provável', 'Caso suspeito', inplace=True)
    df_atual.resultadoFinalExame.replace('Inconclusivo', 'Caso suspeito', inplace=True)
    df_atual.resultadoFinalExame.replace('Em Análise', 'Caso suspeito', inplace=True)
    df_atual.resultadoFinalExame.fillna('Caso suspeito', inplace=True)
    # df_atual.resultadoFinalExame.replace('Negativo', 'Z Negativo', inplace=True)

    df_atual.racaCor.replace('Parda.0', 'Parda', inplace=True)
    df_atual.racaCor.replace('.0', 'Sem Informacao', inplace=True)
    df_atual.racaCor.fillna('Sem Informacao', inplace=True)
    df_atual.racaCor.replace('Branca.0', 'Branca', inplace=True)
    df_atual.racaCor.replace('Preta.0', 'Preta', inplace=True)
    df_atual.racaCor.replace('Amarela.0', 'Amarela', inplace=True)
    df_atual.racaCor.replace('Indígena.0', 'Indígena', inplace=True)

    df_atual.obitoConfirmado.replace(True, 'Verdadeiro', inplace=True)
    df_atual.obitoConfirmado.replace(False, 'Falso', inplace=True)
    df_atual.obitoConfirmado.fillna('Falso', inplace=True)

    return df_atual


def correction_bairro(df_atual, bairro_info):
    print('Corrigindo bairros')
    correcoes = {}
    bairros_cor = bairro_info.index
    for i in df_atual.bairroCaso.value_counts().index:
        dist = 20
        for j in bairros_cor:
            lev = Levenshtein.distance(i,j)
            if dist == 20 and lev < 3:
                correcoes[i] = j
                dist = lev
            elif dist < 20 and lev < dist:
                correcoes[i] = j
                dist = lev

    for i in range(len(list(correcoes))):
        df_atual.bairroCaso = df_atual.bairroCaso.replace(list(correcoes)[i], correcoes[list(correcoes)[i]])

    filtro = ~ df_atual.bairroCaso.isin(bairros_cor)
    df_atual.loc[filtro, 'bairroCaso'] = 'Indeterminado'

    return df_atual


def prof_group(df_atual):
    print('Criando grupos')
    dicGrupo = {'Técnicos e auxiliares de enfermagem' : 'Profissional da saude',
        'Enfermeiros e afins' : 'Profissional da saude',
        'Médico' : 'Profissional da saude',
        'Agente Comunitário de Saúde' : 'Profissional da saude',
        'Farmacêuticos' : 'Profissional da saude',
        'Fisioterapeutas' : 'Profissional da saude',
        'Cirurgião' : 'Profissional da saude',
        'Psicólogos e psicanalistas' : 'Profissional da saude',
        'Cuidador em Saúde' : 'Profissional da saude',
        'Médicos clínicos' : 'Profissional da saude',
        'Nutricionistas' : 'Profissional da saude',
        'Policiais' : 'Policial/Exercito/Bombeiros',
        'Outro tipo de agente de saúde ou visitador sanitário' : 'Profissional da saude',
        'Agente de Saúde Pública' : 'Profissional da saude',
        'Profissionais da educação física' : 'Profissionais da Educação',
        'Vigilantes e guardas de segurança' : 'Policial/Exercito/Bombeiros',
        'Médicos em medicina diagnóstica e terapêutica' : 'Profissional da saude',
        'Terapeutas ocupacionais' : 'Profissional da saude',
        'Condutor de Ambulância' : 'Profissional da saude',
        'Cabos e soldados da polícia militar' : 'Policial/Exercito/Bombeiros',
        'Oficiais generais das forças armadas' : 'Policial/Exercito/Bombeiros',
        'Técnicos de odontologia' : 'Profissional da saude',
        'Professor de Educação Infantil ou Ensino Fundamental' : 'Profissionais da Educação',
        'Socorrista não médico e não enfermeiro' : 'Profissional da saude',
        'Técnico em farmácia e em manipulação farmacêutica' : 'Profissional da saude',
        'Engenheiros civis e afins' : 'Profissionais da área de construção',
        'Inspetores de alunos e afins' : 'Profissionais da Educação',
        'Biomédico' : 'Profissional da saude',
        'Professor do Ensino Médio' : 'Profissionais da Educação',
        'Subtenentes e sargentos da policia militar' : 'Policial/Exercito/Bombeiros',
        'Cozinheiros' : 'Profissionais da área alimentícia',
        'Profissional da Biotecnologia' : 'Profissional da saude',
        'Técnicos em transportes aéreos' : 'Transporte',
        'Contadores e afins' : 'Finanças e Secretariado',
        'Operadores de máquinas para costura de peças do vestuário' : 'Industria textil',
        'Outros profissionais de ensino' : 'Profissionais da Educação',
        'Dirigentes do serviço público' : 'Finanças e Secretariado',
        'Motoristas de veículos de cargas em geral' : 'Transporte ',
        'Secretárias(os) executivas(os) e afins' : 'Finanças e Secretariado',
        'Auxiliares de serviços de documentação' : 'Finanças e Secretariado',
        'Lavadores e passadores de roupa' : 'Industria textil',
        'Professor de Ensino Superior' : 'Profissionais da Educação',
        'Trabalhadores no atendimento em estabelecimentos de serviços de alimentação' : 'Profissionais da área alimentícia',
        'Trabalhadores nos  serviços de manutenção de edificações' : 'Profissionais da área de construção',
        'Oficiais superiores da polícia militar' : 'Policial/Exercito/Bombeiros',
        'Arquitetos e urbanistas' : 'Profissionais da área de construção',
        'Assistentes sociais e economistas domésticos' : 'Finanças e Secretariado',
        'Motociclistas e ciclistas de entregas rápidas' : 'Profissionais da área alimentícia',
        'Trabalhadores auxiliares nos serviços de alimentação' : 'Profissionais da área alimentícia',
        'Delegados de polícia' : 'Policial/Exercito/Bombeiros',
        'Profissionais de administração ecônomico' : 'Finanças e Secretariado',
        'Técnicos em construção civil (edificações)' : 'Profissionais da área de construção',
        'Bombeiros' : 'Policial/Exercito/Bombeiros',
        'Diretores administrativos e financeiros' : 'Finanças e Secretariado',
        'Técnico em Eletroeletrônica e Fotônica atuando na área de saúde' : 'T.I., Tecnologias e mecanica',
        'Tenentes da polícia militar' : 'Policial/Exercito/Bombeiros',
        'Motoristas de ônibus urbanos' : 'Transporte',
        'Gerentes de tecnologia da informação' : 'T.I., Tecnologias e mecanica',
        'Auxiliares de contabilidade' : 'Finanças e Secretariado',
        'Capitães da  polícia militar' : 'Policial/Exercito/Bombeiros',
        'Ajudantes de obras civis' : 'Profissionais da área de construção',
        'Técnicos mecânicos (ferramentas)' : 'T.I., Tecnologias e mecanica',
        'Médicos em especialidades cirúrgicas' : 'Profissional da saude',
        'Profissionais polivalentes da confecção de roupas' : 'Industria textil',
        'Chefes de cozinha e afins' : 'Profissionais da área alimentícia',
        'Professores de nível superior na educação infantil' : 'Profissionais da Educação',
        'Eletricistas de manutenção eletroeletrônica' : 'T.I., Tecnologias e mecanica',
        'Técnicos em contabilidade' : 'Finanças e Secretariado',
        'Professores de nível médio na educação infantil' : 'Profissionais da Educação',
        'Diretores e gerentes de instituição de serviços educacionais' : 'Profissionais da Educação',
        'Técnicos em operações e serviços bancários' : 'Finanças e Secretariado',
        'Padeiros' : 'Profissionais da área alimentícia',
        'Profissionais da informação' : 'T.I., Tecnologias e mecanica',
        'Técnicos em construção civil (obras de infraestrutura)' : 'Profissionais da área de construção',
        'Trabalhadores em registros e informações em saúde' : 'T.I., Tecnologias e mecanica',
        'Cabos e soldados do corpo de bombeiros militar' : 'Policial/Exercito/Bombeiros',
        'Técnicos em eletrônica' : 'T.I., Tecnologias e mecanica',
        'Professores do ensino médio' : 'Profissionais da Educação',
        'Trabalhadores de segurança e atendimento aos usuários nos transportes' : 'Transporte',
        'Engenheiros eletricistas' : 'T.I., Tecnologias e mecanica',
        'Supervisores de serviços financeiros' : 'Finanças e Secretariado',
        'Operadores de máquinas de costurar e montar calçados' : 'Industria textil',
        'Supervisores de lavanderia' : 'Industria textil',
        'Pintores de obras e revestidores de interiores (revestimentos flexíveis)' : 'Profissionais da área de construção',
        'Administradores de tecnologia da informação' : 'T.I., Tecnologias e mecanica',
        'Professores de nível superior do ensino fundamental (primeira a quarta séries)' : 'Profissionais da Educação',
        'Profissionais de direitos autorais e de avaliacão de produtos dos meios de comunicação' : '',
        'Oficiais de máquinas da marinha mercante' : 'Policial/Exercito/Bombeiros',
        'Programadores' : 'T.I., Tecnologias e mecanica',
        'Professores na área de formação pedagógica do ensino superior' : 'Profissionais da Educação',
        'Professores de nível médio no ensino fundamental' : 'Profissionais da Educação',
        'Técnicos em secretariado' : 'Finanças e Secretariado',
        'Designers de interiores' : 'Profissionais da área de construção',
        'Engenheiro de Alimentos' : 'Profissionais da área alimentícia',
        'Economistas' : 'Finanças e Secretariado',
        'Técnicos em eletricidade e eletrotécnica' : 'T.I., Tecnologias e mecanica',
        'Engenheiros mecânicos e afins' : 'T.I., Tecnologias e mecanica',
        'Professor de Ensino Profissionalizante' : 'Profissionais da Educação',
        'Oficiais intermediários do corpo de bombeiros militar' : 'Policial/Exercito/Bombeiros',
        'Trabalhadores da preparação da confecção de roupas' : 'Industria textil',
        'Diretores de operações de serviços em instituição de intermediação financeira' : 'Finanças e Secretariado',
        'Supervisores da construção civil' : 'Profissionais da área de construção',
        'Gerentes de operações de serviços em empresa de transporte' : 'Transporte',
        'Professores de educação especial' : 'Profissionais da Educação',
        'Supervisores na confecção do vestuário' : 'Industria textil',
        'Supervisores dos serviços de transporte' : 'Transporte',
        'Mecânicos de manutenção de bombas' : 'T.I., Tecnologias e mecanica',
        'Trabalhadores de instalações elétricas' : 'Profissionais da área de construção',
        'Mecânicos de manutenção de veículos automotores' : 'T.I., Tecnologias e mecanica',
        'Técnicos de suporte e monitoração ao usuário de tecnologia da informação.' : 'T.I., Tecnologias e mecanica',
        'Subtenentes e sargentos do corpo de bombeiros militar' : 'Policial/Exercito/Bombeiros',
        'Professores leigos no ensino fundamental' : 'Profissionais da Educação',
        'Técnicos em manutenção e reparação de equipamentos biomédicos' : 'T.I., Tecnologias e mecanica',
        'Pesquisadores de engenharia e tecnologia' : 'T.I., Tecnologias e mecanica',
        'Trabalhadores artesanais da confecção de peças e tecidos' : 'Industria textil',
        'Instrutores e professores de cursos livres' : 'Profissionais da Educação',
        'Oficiais superiores do corpo de bombeiros militar' : 'Policial/Exercito/Bombeiros',
        'Trabalhadores da fabricação de cerâmica estrutural para construção' : 'Profissionais da área de construção',
        'Engenheiros em computação' : 'T.I., Tecnologias e mecanica',
        'Supervisores da fabricação de alimentos' : 'Profissionais da área alimentícia',
        'Técnicos em telecomunicações' : 'T.I., Tecnologias e mecanica',
        'Mecânicos de manutenção aeronáutica' : 'T.I., Tecnologias e mecanica',
        'Professores de nível superior no ensino fundamental de quinta a oitava série' : 'Profissionais da Educação',
        'Desenhistas projetistas de construção civil e arquitetura' : 'Profissionais da área de construção',
        'Supervisores da indústria têxtil' : 'Industria textil',
        'Trabalhadores de acabamento de calçados' : 'Industria textil',
        'Pilotos de aviação comercial' : 'Transporte',
        'Mecânicos de instrumentos de precisão' : 'T.I., Tecnologias e mecanica',
        'Trabalhadores agropecuários em geral' : 'Profissionais da área alimentícia',
        'Inspetores e revisores de produção têxtil' : 'Industria textil',
        'Instaladores e mantenedores de sistemas eletroeletrônicos de segurança' : 'T.I., Tecnologias e mecanica',
        'Operadores de tear e máquinas similares' : 'Industria textil',
        'Aplicadores de revestimentos cerâmicos' : 'Profissionais da área de construção',
        'Técnicos mecânicos na manutenção de máquinas' : 'T.I., Tecnologias e mecanica',
        'Professores de artes do ensino superior' : 'Profissionais da Educação',
        'Técnicos do vestuário' : 'Industria textil',
        'Supervisores de manutenção eletromecânica' : 'T.I., Tecnologias e mecanica',
        'Vidreiros e ceramistas (arte e decoração)' : 'Profissionais da área de construção',
        'Gerentes de obras em empresa de construção' : 'Profissionais da área de construção',
        'Trabalhadores de tecelagem manual' : 'Industria textil',
        'Professores do ensino profissional' : 'Profissionais da Educação',
        'Gerentes operacionais da aviação civil' : 'Transporte',
        'Trabalhadores polivalentes das indústrias têxteis' : 'Industria textil',
        'Gerentes de operações de serviços em instituição de intermediação financeira' : 'Finanças e Secretariado',
        'Tenentes do corpo de bombeiros militar' : 'Policial/Exercito/Bombeiros'}

    for i in range(len(list(dicGrupo))):
        df_atual.loc[df_atual.cboEsus == list(dicGrupo)[i], 'profissoes'] = dicGrupo[list(dicGrupo)[i]]

    df_atual.drop(columns=['cboEsus'], inplace=True)
    return df_atual


def processing_new_rows(df_atual):
    df_atual = remove_columns(df_atual)
    df_atual = delete_wrong_dates(df_atual)
    df_atual = correct_cboEsus(df_atual)
    df_atual = filter_muni(df_atual)
    df_atual = date_correction(df_atual)
    df_atual = wrong_values(df_atual)

    bairro_info = pd.read_csv(f'Base_de_dados/dados_bairros.csv', sep=',')
    bairro_info.Bairros	= bairro_info.Bairros.str.upper()
    bairro_info = bairro_info.set_index('Bairros')

    df_atual = correction_bairro(df_atual, bairro_info)
    df_atual = prof_group(df_atual)

    # df_atual.sort_values(by=['resultadoFinalExame'], inplace=True)  
    # df_atual.drop_duplicates(subset='identificadorCaso', keep='last', inplace=True)
    # df_atual = df_atual.drop(columns=['identificadorCaso'])


    df_atual.to_csv('Base_de_dados/dados_limpos.csv', sep=';')
    

    

