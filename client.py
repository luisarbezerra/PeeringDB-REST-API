# encoding=utf8
import sys, os
import json
import socket
import sys

ip_porto   = sys.argv[1]
analise    = int(sys.argv[2])
tcp        = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = ip_porto[:ip_porto.find(':')]
PORT = int(ip_porto[ip_porto.find(':')+1:])

def recebendo_fragmentos(SOCK):
    resposta_json = ''
    while True:
        resposta_atual = SOCK.recv(10000)
        if resposta_atual == '':
            break
        resposta_json = resposta_json + resposta_atual
    return resposta_json 

def get_dados(servico, HOST, PORT):
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((HOST, PORT))
    tcp.sendall('GET ' + servico + ' HTTP/1.1\nHost: ' + HOST + '\n\n')
    
    frags = recebendo_fragmentos(tcp).split('\n')
    try:
        pacote_json = json.loads(frags[-1])
    except: 
        pacote_json = None

    tcp.close()
    return pacote_json

### ANALISES ###

def main():
    if analise == 0:
        ixs = get_dados('/api/ix', HOST, PORT)
        contagem_ixs_por_net = {}

        # iterar em todos ixs
        for ix in ixs['data']:
            ix_nets = get_dados('/api/ixnets/' + str(ix['id']), HOST, PORT)
            
            for ix_net in ix_nets['data']:
                if ix_net in contagem_ixs_por_net:
                    contagem_ixs_por_net[ix_net] = contagem_ixs_por_net[ix_net] + 1
                else:
                    contagem_ixs_por_net[ix_net] = 1
        
        # pegando nome das nets
        for net in contagem_ixs_por_net:
            nome_rede = get_dados('/api/netname/' + str(net), HOST, PORT)
            
            print(str(net) + '\t' + nome_rede['data'] + '\t' + str(contagem_ixs_por_net[net]))

    elif analise == 1:
        ixs = get_dados('/api/ix', HOST, PORT)
        for ix in ixs['data']:
            ix_nets = get_dados('/api/ixnets/' + str(ix['id']), HOST, PORT)
            numero_nets_ix = len(ix_nets['data'])

            print(str(ix['id']) + '\t' + ix['name'] + '\t' + str(numero_nets_ix))

    else:
        print("Analise numero " + analise + " nao existente")

main()
