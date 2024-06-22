import os
from flask import Flask, jsonify, request, json
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
import jwt
import datetime
import re

app = Flask(__name__)
CORS(app)

# .env
# KEY=''
# DATABASE=''
load_dotenv()
url_db = os.getenv("DATABASE")
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
    for i in x[0]:
        del i["pubkey"],i["privkey"]
    return x[0]
    
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

def select_c_conf(table,login,user):
    c.execute(f"""
             SELECT "clients" FROM {table} WHERE id_acc = (SELECT id_acc FROM accounts WHERE login = ('{login}'))
        """)
    tmp=c.fetchone()
    x = json.dumps(tmp)
    x = json.loads(x)
    return x[0]

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


# @app.route('/api', methods=['GET'])
# def cookies_test():
#     token = request.cookies.get('t')
#     if token:
#         data = jwt.decode(token, app.config['secret_key'], algorithms="HS256")
#         response = jsonify({ 
#             "name": data['user'],          
#             "auth": True
#             })
#         # response.set_cookie("t", token, max_age=0)
#         # token = jwt.encode({
#         #             'user': data['user'] , 
#         #             'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)
#         #             }, app.config['secret_key'])
#         # response.set_cookie("t", value=token, secure=False, httponly=True, max_age=86400)
#         return response
#     else:
#         return jsonify({
#             "name": "no auth",
#             "auth": False
#         })


@app.route('/api/login',methods=['POST','OPTIONS'])
def login():
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
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=86400)
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

@app.route("/api/getconf/<string:server>/<string:user>", endpoint="getconf", methods=['GET'])
@token_required
def getWGconf(server,user):
    if server == "ru.darksurf.ru":  # заменить
        server = "server_ru"        #
    elif server == "fi.darksurf.ru":#
        server = "server_fi"        #

    token = request.cookies.get('t') 
    data = jwt.decode(token, app.config['secret_key'], algorithms=['HS256'])
    x = select_s_conf(server,data["user"])
    y = select_c_conf(server,data["user"],user)
    for i in y:
        if i["name"] == user:
                wg_conf = (f"""
### DarkSurf.ru v0.1
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
            
    print(wg_conf)
    return wg_conf

# @app.route("/api/logout",endpoint="logout", methods=['GET'])
# @token_required
# def logout():
#     token = request.cookies.get('t')
#     response = jsonify({ 
#             "msg": "ok"         
#             })
#     response.set_cookie("t", token, max_age=0)
#     return response    
    



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
