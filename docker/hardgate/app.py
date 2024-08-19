import os
from flask import Flask, jsonify, request, json ,send_file, Response
from flask_cors import CORS
import qrcode
import requests
from io import BytesIO
from dotenv import load_dotenv
import psycopg2
import jwt
#from flask_jwt import JWT
import datetime
import re
import subprocess
import ipaddress
from flask_parameter_validation import ValidateParameters, Json

app = Flask(__name__)
CORS(app)

# .env
# KEY=''
# DATABASE=''
load_dotenv()
url_db = os.getenv("DATABASE")
#app.config['secret_key'] = 'AafgHAehae5hbdrh'
app.config['secret_key'] = os.getenv("KEY")

try:
    conn = psycopg2.connect(url_db)
    c = conn.cursor()
except:
        print('NO CONNECT DATABASE')

def select(table,login):
    c.execute(f"""
             SELECT "clients" FROM {table} WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
        """)
    tmp=c.fetchone()
    x = json.dumps(tmp)
    x = json.loads(x)
    if x != {}:                                     #
        for i in x[0]:                              #
            del i["pubkey"],i["privkey"]            #
        return x[0]                                 #
    else:                                           #
        x = "nousers"                               #
        print(x)
        return x                                    #

def select_serv(table,login):
    c.execute(f"""
          select jsonb_build_object('w_host', server->'w_host','clients', '') from {table} WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
          """)
    tmp=c.fetchone()
    x = json.dumps(tmp)
    x = json.loads(x)
    return x[0]

def select_s_conf(table,login):
    c.execute(f"""
          select jsonb_build_object('w_host', server->'w_host','pubkey', server->'pubkey','w_port', server->'w_port') from {table} WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
          """)
    tmp=c.fetchone()
    x = json.dumps(tmp)
    x = json.loads(x)
    return x[0]

def select_s_lan(table,login):
    c.execute(f"""
          select jsonb_build_object('wg_lan', server->'wg_lan') from {table} WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
          """)
    tmp=c.fetchone()
    x = json.dumps(tmp)
    x = json.loads(x)
    return x[0]

def select_c_ip(table,login):
    c.execute(f"""
          select jsonb_build_object('c_ip', server->'c_ip') from {table} WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
          """)
    tmp=c.fetchone()
    x = json.dumps(tmp)
    x = json.loads(x)
    return x[0]

def select_c_conf(table,login,user):
    c.execute(f"""
             SELECT "clients" FROM {table} WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
        """)
    tmp=c.fetchone()
    x = json.dumps(tmp)
    x = json.loads(x)
    return x[0]

def select_c_ips(table,login):
    c.execute(f"""
             SELECT "clients" FROM {table} WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
        """)
    tmp=c.fetchone()
    x = json.dumps(tmp)
    x = json.loads(x)
    for i in x[0]:
        del i["pubkey"],i["privkey"],i["name"]
    return x[0]

def WGkeys():
    privkey = subprocess.check_output("wg genkey", shell=True).decode("utf-8").strip()
    pubkey = subprocess.check_output(f"echo '{privkey}' | wg pubkey", shell=True).decode("utf-8").strip()
    return (privkey, pubkey)

def add_client(table,c_json,login):
    c.execute(f"""
                UPDATE {table} SET clients = clients || '{c_json}'::jsonb WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
        """)
    conn.commit()
    return 0

def delete(table,index,login):
    c.execute(f"""
             update {table} set clients = clients - {index} WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
        """)
    conn.commit()
    return print("DELETE OK")

def token_required(f):
    def decorated(*args, **kwargs):
        #token = request.headers.get('token')
        #token = request.args.get('token')
        token = request.cookies.get('t')
        if not token:
            return jsonify({'error': 'NO ACCESS'}), 403
        try:
            jwt.decode(token, app.config['secret_key'], algorithms="HS256")
        except Exception as error:
            return jsonify({'error': 'BAD TOKEN'}),403
        return f(*args, **kwargs)
    return decorated

@app.route('/api/login',methods=['POST','OPTIONS'])
@ValidateParameters()
def login(
     usr: str = Json(
         min_str_length = 1,
        max_str_length = 10,
        pattern = r"" #regex
    ),
    passwd: str = Json(
        min_str_length = 1,
        max_str_length = 20,
        pattern = r"" #regex
    )
    ):
#def login():
    data = request.get_json()
    name = data["usr"]
    password = data["passwd"]
    CHECK_ACC = f"SELECT (login = '{name}') AND (password = crypt('{password}', password)) FROM accounts;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(CHECK_ACC)
            results = cursor.fetchall()
            res = re.search(r"True",str(results))
            if res:
                token = jwt.encode({
                    'user': name , 
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
                    }, app.config['secret_key'])
                response = jsonify({
                    "auth": True,
                    "t": token
                    })
                # response.set_cookie("t", value=token, secure=False, httponly=True, max_age=86400)
                return response               
            else:
                return jsonify({
                    "auth": False,
                    })

@app.route("/api/home",endpoint="home" , methods=['GET'])
@token_required
def home():
    # тут личный кабинет и параментры для конфигов клиентов
    token = request.cookies.get('t') 
    data = jwt.decode(token, app.config['secret_key'], algorithms=['HS256'])
    x=select_serv("server_fi",data["user"])
    x["clients"] = select("server_fi",data["user"])
    y=select_serv("server_ru",data["user"])
    y["clients"] = select("server_ru",data["user"])
    return [x,y]

@app.route("/api/getconf/<string:server>/<string:user>", endpoint="getconf", methods=['GET','POST','DELETE','PATCH'])
@token_required
def WGconf(server,user):
    token = request.cookies.get('t') 
    data = jwt.decode(token, app.config['secret_key'], algorithms=['HS256'])
    if server == "ru.darksurf.ru":  # заменить
        server = "server_ru"        # нахуй
    elif server == "fi.darksurf.ru":# REGEX
        server = "server_fi"        #
    
    if request.method == 'GET' or request.method == 'PATCH':    # если PATCH генерируем конфиг или GET то qrcode
        x = select_s_conf(server,data["user"])
        y = select_c_conf(server,data["user"],user)
        for i in y:
            if i["name"] == user:
                    wg_conf = (f"""
### DarkSurf.ru v0.1
### МАНДУЛЯТОР 3000
### ebosh-product                               
### user:{user} 
### 
                          
[Interface]
PrivateKey = {i["privkey"]}
Address = {i["ip"]}/24
DNS = 45.142.122.244,77.221.159.104 

[Peer]
PublicKey = {x["pubkey"]}
AllowedIPs = 0.0.0.0/0
Endpoint = {x["w_host"]}:{x["w_port"]}""") 
                    if request.method == 'PATCH':
                        return wg_conf
                    else:
                        buffer = BytesIO()
                        img = qrcode.make(wg_conf)
                        img.save(buffer)
                        buffer.seek(0)
                        response = send_file(buffer, mimetype='image/png')
                        return response

                            
    elif request.method == 'POST': # если POST добавляем пользователя в бд
        ip_lan = select_s_lan(server,data["user"])                 
        net_list = list(ipaddress.ip_network(ip_lan["wg_lan"]))    
        del net_list[1],net_list[0],net_list[253]
        ips = select_c_ips(server,data["user"])                      
        ip_list=[]
        for ip in ips:
           ip_list = ipaddress.ip_address(ip["ip"])
           net_list.remove(ip_list) 
        wgkey = WGkeys()
        dict = {"ip":str(net_list[0]),"name":str(user),"privkey":str(wgkey[0]),"pubkey":str(wgkey[1])}
        c_json = json.dumps(dict)
        add_client(server,c_json,data["user"])
        c_ip = select_c_ip(server,data["user"])
        subprocess.run(['curl','http://' + c_ip["c_ip"] + ':5000/punch'],stdout=subprocess.PIPE)
        return jsonify({"msg":"ok"})

    elif request.method == 'DELETE': # если DELETE
        resp = select(server,data["user"])
        for i,x in enumerate(resp):
            if x["name"] == user:
                    delete(server,i,data["user"])
                    c_ip = select_c_ip(server,data["user"])
                    subprocess.run(['curl','http://' + c_ip["c_ip"] + ':5000/punch'],stdout=subprocess.PIPE)
        return jsonify({"msg":"ok"})

@app.route("/api/stats",endpoint="stats" , methods=['GET'])
@token_required
def stats():
    token = request.cookies.get('t') 
    data = jwt.decode(token, app.config['secret_key'], algorithms=['HS256'])
    login = data["user"]
    ip_ru = select_c_ip("server_ru",login)
    ip_fi = select_c_ip("server_fi",login)
    ip_ru = ip_ru["c_ip"]
    ip_fi = ip_fi["c_ip"]
    url_ru = f"http://{ip_ru}:5000/stats"
    url_fi = f"http://{ip_fi}:5000/stats"
    res_fi = requests.get(url_fi)
    res_ru = requests.get(url_ru)
    res_fi = res_fi.json()
    res_ru = res_ru.json()
    res_fi = json.dumps({'clients_fi' : res_fi})
    res_ru = json.dumps({'clients_ru' : res_ru})
    line =f"""[{res_fi},{res_ru}]"""
    line = json.loads(line)
    return line

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
