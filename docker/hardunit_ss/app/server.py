import os
import psycopg2
from flask import Flask, jsonify, json
import ipaddress
from waitress import serve
import subprocess


app = Flask(__name__)
#CORS(app)

def select(rows,table,login):
    c.execute(f"""
          SELECT {rows} FROM {table} WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
          """)
    tmp=c.fetchone()
    x = json.dumps(tmp)
    x = json.loads(x)
    return x[0]

def update(rows,table,json,login):
    c.execute(f"""
          UPDATE {table} SET {rows} = '{json}'::jsonb WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
          """)
    conn.commit()
    return 0

def config():
    wg0_conf = (f"""### DarkSurf.ru (c)
[Interface]
PrivateKey = {s_privkey}
Address = {wg_gateway[1]}/24
ListenPort = 51820
PostUp = iptables -t nat -A POSTROUTING -s {wg_lan} -o eth0 -j MASQUERADE; iptables -P INPUT ACCEPT; iptables -P OUTPUT ACCEPT; iptables -P FORWARD ACCEPT""")
    for c_conf in select("clients",table,login):
        wg0_conf = wg0_conf + (f'\n\n[Peer] # Client = {c_conf["name"]}\nPublicKey = {c_conf["pubkey"]}\nAllowedIPs = {c_conf["ip"]}/32')

    with open("/etc/wireguard/wg0.conf","w") as file:
        file.write(wg0_conf) # ЧИИИК!!
    return 0

def ss_config():
    ss_conf = select("ss_serv",table, login)
    with open("/etc/config.json","w") as file:
        file.write(ss_conf) # ХУЯКС!
    return 0

# ifconfig eth0 | grep inet | awk -F: '{print $2}'| awk '{print $1}') 
ip = subprocess.run(["/app/c_ip.sh"],capture_output=True, text=True) # чииииик !!!
c_ip = ip.stdout
login = os.environ.get("LOGIN")
w_port = os.environ.get("W_PORT")
w_host = os.environ.get("W_HOST")
url_db = os.environ.get("DATABASE")
wg_lan = os.environ.get("WG_LAN")
table = os.environ.get("TABLE")

# url_db='postgresql://user:password@host:port/database_name'

try:
    conn = psycopg2.connect(url_db)
except:
    print('NO CONNECT DATABASE')

c = conn.cursor()
s_conf = select("server",table,login)
s_conf["c_ip"] = c_ip.strip() # перемменная.strip убрать \n
s_conf["w_port"] = w_port
s_conf["w_host"] = w_host
s_conf["wg_lan"] = wg_lan
s_privkey = s_conf["privkey"]
s_pubkey = s_conf["pubkey"]
s_tc = s_conf["tc"]
s_conf = json.dumps(s_conf)
wg_gateway = ipaddress.ip_network(wg_lan) # чиик !!!
update("server",table,s_conf,login) # ХОП !

config() # ЧИИИИИИИИИИИИИИИИККККК!
ss_config()

os.chmod("/etc/wireguard/wg0.conf",0o600) # чик
subprocess.run(["wg-quick", "up", "wg0"]) # ОПА!!!!!!!
subprocess.run(["ssserver","-c","/etc/config.json","-d"]) # запуск сервера shadowsocks-rust

###### 


@app.route('/punch',endpoint="punch" , methods=['GET'])
def punch():
    config()
    subprocess.run(["/app/wg_reload.sh"]) # wg syncconf wg0 <(wg-quick strip wg0) перечитать конфиг
    return jsonify({"msg":"ok"})


######### stat
@app.route('/stats',endpoint="stats" , methods=['GET'])
def stream():
    x = os.popen("/app/wg_stats.sh").readlines()[0].strip("\n")
    x = x.rstrip(',')
    x = "[" + x + "]"
    return x


######### стрим залупа
# @app.route('/stream',endpoint="stream" , methods=['GET'])
# def stream():
#     def gen():
#        while True:
#           time.sleep(2)
#           x = subprocess.run(["/app/wg_stats.sh"], shell=True, stdout=subprocess.PIPE, encoding='utf-8')
#           yield str(x.stdout)

#     return Response(gen(), mimetype='text/plain')
  

if __name__ == "__main__":
  serve(app, host='0.0.0.0', port=5000)
  #app.run(debug=True, host='0.0.0.0', port=5000) # dev mode
   
