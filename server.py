from flask import Flask
import sys, json

porto        = int(sys.argv[1])
netfile      = sys.argv[2]
ixfile       = sys.argv[3]
netixlanfile = sys.argv[4]

app = Flask(__name__)

@app.route('/api/ix')
def ixis():
    with open(ixfile) as ixs:
        ixs_json = json.load(ixs)
        ixs_data = ixs_json['data']

        saida_ixs_json = {
            'data': ixs_data
        }

        return json.dumps(saida_ixs_json)

@app.route('/api/ixnets/<ix_id>')
def ixnets(ix_id):
    with open(netixlanfile) as net_ixs:
        net_ixs_json = json.load(net_ixs)
        numeros_net_ids = set()
        
        for net in net_ixs_json['data']:
            if net['ix_id'] == int(ix_id):
                numeros_net_ids.add(net['net_id'])
        
        saida_net_ixs_json = {
            'data': list(numeros_net_ids)
        }

        return json.dumps(saida_net_ixs_json)

@app.route('/api/netname/<net_id>')
def netname(net_id):
    with open(netfile) as arquivo_netfile:
        netfile_file = json.load(arquivo_netfile)
        
        for net in netfile_file['data']:
            if net['id'] == int(net_id):
                
                saida_netfile = {
                    'data': net['name'] 
                }

                return json.dumps(saida_netfile)

app.run(host='0.0.0.0', port=porto)
