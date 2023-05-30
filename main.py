from operator import itemgetter
import copy
from pythonds.basic.stack import Stack

def FCFO(matriz, processos):
    tempo_espera = 0
    tempo_retorno = 0
    tempo_resposta = 0
    count = 0    
    linhas = processos
    sum = 0
    matriz_2 = copy.deepcopy(matriz)
    historico = []
    time = 0
    initial_time = [0]*processos
    count = 0
    

    for i in range(0, linhas):
        if(time < matriz_2[i][0]):
            for k in range(time, matriz_2[i][0]):  # tempo ocioso
                historico.append(-1)
            time = matriz_2[i][0]

        while(matriz_2[i][1]):  # enquanto o processo ainda for valido
            if (count == 0):
                initial_time[i] = time
            time += 1
            matriz_2[i][1] -= 1  # decrementa
            historico.append(i)
            count = 1
        count = 0
      
    rev = copy.deepcopy(historico)
    rev.reverse()
    sum = 0
   
    for i in range(0, processos):
        sum += initial_time[i]-matriz_2[i][0]
    tempo_espera = sum/processos
   
    tempo_resposta = tempo_espera
   
    sum = 0
  
    for k in range(0, processos):
        sum += initial_time[k]+historico.count(k)-matriz_2[k][0]
    tempo_retorno = sum/processos

    return tempo_retorno, tempo_resposta, tempo_espera

# insere os processos de acordo com o prox tempo
def insert_pilha(matriz_2, processos, pilha, referencia):
    #print('referencia', referencia)
    for i in range(0, processos):
        
        if(matriz_2[i][0] == referencia):
            pilha.append(i)             

def RR(matriz, processos, quantum):
    matriz_2 = copy.deepcopy(matriz)
    matriz_2.sort(key=itemgetter(0))

    tempo_espera = [0]*processos
    tempo_retorno = 0
    tempo_resposta = 0
    time = 0
    end_time = [0]*processos
    initial_time = [0]*processos
    last = [0]*processos
    count = 0
    pilha = []
    rev = []
    historico = []
    #print('\n\n|------------------- RR --------------------|')
    #print('| Dados:',matriz_2,'|')
    time = matriz[0][0]
    # Aloca todos os processos de tempo inicial [0][0]
    insert_pilha(matriz_2, processos, pilha, matriz_2[0][0])
    #print('\npilha inicial:',pilha)
    
    if(time != 0):
        for i in range(0, time):
            historico.append(-1)

    while(pilha != []):
        id = pilha[0]  # Salva o indice do processo da pilha
        #print('id:', id)
        for i in range(0, quantum):
            if((matriz_2[id][1])):
                matriz_2[id][1] -= 1
                time += 1
                #print('executou processo:', id)
                historico.append(id)
                #print('time',time,' -- matriz',matriz_2)
        if(pilha != []):
            maior = max(pilha)
        # print('maior',maior)
        pilha.remove(pilha[0])
        #print('processo removido:', pilha)
        # print('pilha',pilha,'\n')
        if(maior != processos-1):
            #print('matriz[maior][0]:',matriz_2[maior][0],'!= matriz[maior+1][0]:',matriz_2[maior+1][0])
            if(matriz_2[maior][0] != matriz_2[maior+1][0]):
                #print('time',time,'>= matriz[maior+1][0]',matriz_2[maior+1][0])
                if(time >= matriz_2[maior+1][0]):
                    #print('houve inserção na lista\n')
                    #print('referncia', matriz_2[maior+1][0])
                    insert_pilha(matriz_2, processos, pilha,
                                 matriz_2[maior+1][0])
                    # print('pilha',pilha,'\n')
        #print('IF matriz[',id,'[',1,'] = ',matriz_2[id][1])
        if (matriz_2[id][1]):  # Se o processo ainda existir, volta a lista
            #print('add o processo q n foi concluido- id', id)
            pilha.append(id)
        # print(pilha)
        if(pilha == []):  # diferenca de duas unidades no tempo de enrtada
            #print('pilha vaziaaaaaaaaaaa')
            # print(matriz_2)
            for k in range(0, processos):
                if(matriz_2[k][1] != 0):
                    #print('time antes:', time)
                    for l in range(time, matriz_2[k][0]):
                        # Sinaliza que tem uma lacuna no escalonador
                        historico.append(-1)
                    time = matriz_2[k][0]
                    #print('time now', time)
                    pilha.append(k)
                    # print(pilha)
                    count = 1
                if(count == 1):
                    break
            count = 0

    # print('historico',historico) #Ordem de execução dos processos

# Calcula-se os tempos analisando a ultima vez q foi executado e a primeira
    rev = copy.deepcopy(historico)
    rev.reverse()  # facilita o momento de finalização dos processos
    #print('reverso  ', rev)
    width = len(historico)
    #print('len do historico', width)
    k = 0
    count = 0
    aux = 1

    for k in range(0, processos):
        #print('processo', k)
        for i in range(0, width):
            if(k == rev[i]):
                end_time[k] += aux
                count = 1
                aux = 1
            elif((k != rev[i]) & (count == 0)):
                aux += 1
            else:
                break
        aux = 1
        count = 0
        # print('end time no reverso', end_time) #Salva o isntate que o processo executou pela ultima x

    # Subtrai o tamanho do historico das ultimas repetiçoes p saber o tempo de exec da ultima vez
    for k in range(0, processos):
        end_time[k] = width-end_time[k]
    # print('end_time',end_time)
    # O endtime tem o instante t da ultima de execucao dos processos

    for k in range(0, processos):
        for i in range(0, width):
            #print('busca ', k,'no historico', historico[i])
            if(k == historico[i]):
                #print('tempo inicial[',k,']:',initial_time[k],'=',i)
                initial_time[k] = i
                break

        for i in range(0, width):
            if(k == rev[i]):
                # Cria uma lista com a ultima ocorrencia do tempo p calcular o tempo de retorno
                last[k] = i
                break
    aux = 0
    repeticoes = 0
    sum = 0
    count = 0
    for k in range(0, processos):
        #print('\nprocesso',k,'--endtime',end_time[k],'initial time--',initial_time[k])
        #print('zerando rept', repeticoes)
        aux = end_time[k]-initial_time[k]
        # conta os processos que nao sao igais ao k
        for i in range(initial_time[k], end_time[k]):
            '''if((initial_time[k]>matriz_2[k][0])&(count==0)): #Não lembro o motivo de colocar isso
                repeticoes=initial_time[k]-matriz_2[k][0]
                count=1'''
            # print(historico)
            if(historico[i] != k):
                if(historico[i] != -1):
                    repeticoes += 1
                    #print('repeticoes:', repeticoes)
        #print('processo [',k,'] repetido', repeticoes)
        sum += repeticoes+(initial_time[k]-matriz_2[k][0])
        # print('sum',sum)
        repeticoes = 0
        count = 0
    tempo_espera = sum/processos
    # print('espera:',tempo_espera)
    sum = 0

    # Calculo do tempo de resposta
    # print(initial_time)
    for k in range(0, processos):
        sum += initial_time[k]-matriz_2[k][0]
    tempo_resposta = sum/processos

    sum = 0
    # Calculo do tempo de retorno
    # print(last)
    for i in range(0, processos):
        last[i] = width-last[i]-matriz_2[i][0]
        sum += last[i]
    # print(last)
    tempo_retorno = sum/processos
    # print('historico',historico)
    # print('|-------------------------------------------|\n')
    return(tempo_retorno, tempo_resposta, tempo_espera)


def SJF(matriz, processos):
    
    time = 0
    
    tempo_espera = 0
    tempo_resposta = 0
    tempo_retorno = 0
    s = Stack()
    i = 0

    matriz_2 = copy.deepcopy(matriz)
    matriz_2.sort()
    count2 = 1000
    # print(matriz_2)
    time = 0
    historico = []
    
    initial_time = [0]*processos

    #print('\n\n|------------------- SJF --------------------|')
    #print('| Dados:', matriz_2, '|')

    if(time != matriz_2[0][0]):
        for i in range(time, matriz_2[0][0]):
            historico.append(-1)
        time = matriz_2[0][0]
    #print('historico inicial', historico)
    #print('tempo de inicio', time)

    end_time = [0]*processos
    count = 0
    
    for i in range(0, processos):
        s.push(i)
    initial_time[0] = matriz_2[0][0]

    while(not(s.isEmpty())):
        #print('executa o for')
        i = 0
        count2 = 1000
        # for i in range(0,processos):
        while(i < processos):
            # print('PROCESSO:',i)
            #print('tempo',time,'---',matriz_2[i][1], 'é valido?')
            count2 = 1000
            # print('count2',count2)
            if(matriz_2[i][1]):
                if(count == 0):
                    #print('processo',i,'iniciado em ', initial_time[i])
                    #print('enqanto existir processo ele vai diminuir')
                    while (matriz_2[i][1]):
                        historico.append(i)
                        matriz_2[i][1] -= 1
                        time += 1
                        #print('time --', time, '--matriz', matriz_2)
                    if (matriz_2[i][1] == 0):
                        end_time[i] = time
                        #print('processo', i, 'encerrado em ', end_time[i])
                    # Ordena de acordo com a duracao
                    matriz_2.sort(key=itemgetter(1))

                else:
                    #print('matriz', matriz_2)
                    #print(matriz_2[i][1], 'é valido?')
                    if (matriz_2[i][1]):
                        #print(time,'>=', matriz_2[i][0])
                        if(time >= matriz_2[i][0]):
                            initial_time[i] = time
                            #print('processo iniciado em',initial_time[i])
                            #print('enqanto existir processo ele vai diminuir')
                            while(matriz_2[i][1]):
                                historico.append(i)
                                matriz_2[i][1] -= 1
                                time += 1
                                #print('time --',time,'--matriz', matriz_2)

                if(matriz_2[i][1] == 0):
                    end_time[i] = time
                    #print('processo',i,'encerrado em ', end_time[i])
                    # print('ennnd',end_time)
                    s.pop()
                    # print('\n')
                    # matriz_2.sort(key=itemgetter(1))
                    #print('reorganiza', matriz_2)
                    i = processos + 1
                    # print(historico)
            count = 1
           
            i += 1
            #print('valor de i', i)
        for k in range(0, processos):
            if(matriz_2[k][1] != 0):  # Salva o menor tempo de entrada dos processos n executados
                #print('processo[',k, 'nao vazio')
                if(matriz_2[k][0] < count2):
                    # print(count2)
                    count2 = matriz_2[k][0]
        #print('menor tempo de inicializaçao', count2)
        if(not(s.isEmpty())):
            #print('a lista nao esta vazia')
            for k in range(time, count2):
                time += 1
                #print('tempo ocioso, add -1')
                #print('time', time)
                historico.append(-1)
                # print(historico)
        # if(s.isEmpty()):
            #print('lista VAZIAAAAAAAAAAAAAAAAAAAAAA')

    # print('hitorico',historico)
    #print('tempo de inicio',initial_time)
    #print('tempo final',end_time)

    aux = [0]*processos
    sum = 0

    for i in range(0, processos):
        aux[i] = initial_time[i]-matriz_2[i][0]
        sum += aux[i]
    tempo_espera = sum/processos
    #print('tempo de espera', tempo_espera)
    tempo_resposta = tempo_espera
    #print('tempo de resposta', tempo_resposta)

    sum = 0
    for i in range(0, processos):
        aux[i] = 0
        aux[i] = end_time[i]-matriz_2[i][0]
        sum += aux[i]
    tempo_retorno = sum/processos
    #print('tempo de retorno', tempo_retorno)

    return(tempo_retorno, tempo_resposta, tempo_espera)

# ------------------------------------------------------------------------------------------------------------

def main():
    texto = []
    with open('entrada.txt') as arq:
        texto = arq.read()

    texto = texto.split()  # quebra os dados de acordo com os espaços
    # print(texto)
    # Converte os numeros de string para inteiro
    texto_num = list(map(int, texto))
    # print(texto_num)

    linhas = int(len(texto) / 2)  # calcula o numero de processos|linhas
    count = 0
    quantum = 2
    matriz = []
    flag = 1

    for i in range(0, linhas):
        linha = []
        for j in range(0, 2):
            if(j == 1):
                if(texto_num[count] == 0):  # Verifica se existe processo com duração 0
                    #print('O processo com duracao nula foi removido do escalonador')
                    flag = 0
                    linhas -= 1
            linha.append(texto_num[count])
            count = count+1
        if(flag == 1):
            # matriz desordenada pelo tempo de entrada do processo
            matriz.append(linha)
        flag = 1

    # Organiza a matriz de acordo com o tempo de entrada ->coluna(0)
    matriz.sort(key=itemgetter(0))
    #print("Dados lidos do arquivo:", matriz)

    # copia da matriz original para poder alterar os valores do tempo de duração
    
    SJF_v = 0

    FCFO_v = (FCFO(matriz, linhas))
    RR_v = (RR(matriz, linhas, quantum))
    SJF_v = (SJF(matriz, linhas))

    # desempactamento de tuplas
    a, b, c = FCFO_v
    d, e, f = SJF_v
    g, h, i = RR_v

   
    text1 = "\nFCFS "+ str(round(a, 1))+" "+ str(round(b, 1)) +" " + str(round(c, 1))
    print(text1.replace(".",","))
    text2 = "SJF "+ str(round(d, 1))+" "+ str(round(e, 1)) +" " + str(round(f, 1))
    print(text2.replace(".",","))
    text3 = "RR "+ str(round(g, 1))+" "+ str(round(h, 1)) +" " + str(round(i, 1))
    print(text3.replace(".",","))
    
    with open('saida.txt', 'w') as arquivo:
        arquivo.write(str(text1).replace(".",",") + "\n")
        arquivo.write(str(text2).replace(".",",") + "\n")
        arquivo.write(str(text3).replace(".",",") + "\n")
main()