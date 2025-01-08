<template>
<div class="wrapper" v-if="wg">
      <dialog :open="dialog" @click="closeQR()">
                  <img class="displayed" :src="qrcode" width=50% @click="closeQR()" border="0">
      </dialog>
      <div class="header">
            <span> 
                  <i>DarkSurf.ru</i>
            </span>
            <span>
                  <a @click="getlogout()">
                        <img src="./img/exit.png" width="35px">
                  </a>
            </span>
      </div>
      <div class="content">
            <div class="wg">
                  <div>
                        <img src="./img/fin.png" width="35px">
                        &#160WireGuard Хельсинки&#160 
                  </div>
                  <div>
                        <button class="btn" @click="setWGconf(wg[0].w_host)">Создать</button>
                  </div>
            </div>
            <div class="clients"  v-for="(key,index) in wg[0].clients" :key="index">
                  <div>
                        &#160&#160<img :src="onLineIMG(stats[0].clients_fi[index].last)" width="16px">
                        &#160 {{ key.name }} &#160:&#160 {{ key.ip }} 
                  </div>      
                  <div>
                        <a @click="getQR(wg[0].w_host,key.name)"><img src="./img/qr.png" width="18px"></a>&#160
                        <a @click="getWGconf(wg[0].w_host,key.name)"><img src="./img/down.png" width="16px"></a>&#160
                        <a @click="delWGconf(wg[0].w_host,key.name)"><img src="./img/del.png" width="20px"></a>&#160&#160
                  </div>
            </div>

            <div class="wg">
                  <div>
                        <img src="./img/rus.png" width="35px">
                        &#160WireGuard Москва&#160
                        <font style="vertical-align:middle; color: red; font-size: 10px">*obfs</font>
                  </div>
                  <div>
                        <button class="btn" @click="setWGconf(wg[1].w_host)">Создать</button>
                  </div>
            </div>
            <div class="clients"  v-for="(key,index) in wg[1].clients" :key="index">
                  <div> 
                        &#160&#160<img :src="onLineIMG(stats[1].clients_ru[index].last)" width="16px">
                        &#160 {{ key.name }} &#160:&#160 {{ key.ip }}  
                  </div>      
                  <div>
                        <a @click="getQR(wg[1].w_host,key.name)"><img src="./img/qr.png" width="18px"></a>&#160
                        <a @click="getWGconf(wg[1].w_host,key.name)"><img src="./img/down.png" width="16px"></a>&#160
                        <a @click="delWGconf(wg[1].w_host,key.name)"><img src="./img/del.png" width="20px"></a>&#160&#160
                  </div>
            </div>
            <div class="wg">
                  <div>
                        <img style="vertical-align:middle" src="./img/ss.png" width="26px">
                        <span style="vertical-align:middle">&#160ShadowSocks</span>
                  </div>
            </div>      
            <div class="clients">&#160&#160
                  <div>
                        <img src="./img/fin.png" width="20px">
                  </div>&#160&#160
                  <div class="ss">
                        <span id="ss_fi">ss://{{ ss.ss_fi }}#DarkSurf[Fi]</span>
                  </div>
                  <div>
                        <a @click="copySS('ss_fi')"><img src="./img/cp.png"></a>
                  </div>&#160
            </div>
            <div class="clients">&#160&#160
                  <div>
                        <img src="./img/rus.png" width="20px"> 
                  </div>&#160&#160
                  <div class="ss">
                        <span id="ss_ru">ss://{{ ss.ss_ru }}#DarkSurf[Ru]</span>
                  </div>
                  <div>
                        <a @click="copySS('ss_ru')"><img src="./img/cp.png"></a>
                  </div>&#160
            </div>
            <div class="wg">
                  <div>
                        <img style="vertical-align:middle" src="./img/obfs.png" width="28px">
                        <span style="vertical-align:middle">&#160*obfs</span>
                  </div>
            </div>
            <div class="clients obfs">&#160&#160
                  <div>
                        РКН перестал блокировать трафик.
                        <s>РКН блокирует wireguard-Москва. Для обхода блокировки необходимо обфусцировать(маскировать) трафик wireguard.</s>
                  </div>&#160
            </div>      
      </div>
      <div class="footer">
            <span>&copy; 2025 ebosh-product</span>
      </div>
</div>

<div class="wrapper" v-else>
      <div class="main">
            <div class="logo">
                  <span><i>DarkSurf.ru</i></span>
            </div>
            <div>      
                  <img src="./img/logozbs.png" width="165px" style="border-radius: 10px;">
            </div>
            <div>
                  <font style="font-family:sber;font-size: 16px"><b>МАНДУЛЯТОР 3000</b></font>
            </div>
            <div>
                  <p>&#160 {{ error }}</p>
            </div>
            <div>
                  <form @submit.prevent="setPost()">
                        <input class="txt" type="text"  id="user" placeholder="Логин" v-model.trim="user">
                        <input class="txt" type="password" id="password"  placeholder="Пароль" v-model.trim="password" autocomplete="no">
                        <br>
                        <center>
                              <button class="btn inter">Вход</button>
                        </center>
                  </form>
            </div>
      </div>
      <div class="footer">
            <span>&copy; 2025 ebosh-product</span>
      </div>
</div>
</template>
<script>
import VueCookies from 'vue-cookies'

export default {
created() {
      document.title = "DarkSurf.ru" 
      this.getCook()
},
data() {
  return {
      postAcc: {
          user: '',
          password: '',
      },
      dialog: false,
      qrcode: null,
      error: null,
      auth: {},
      cook: null,
      wg: null,
      wgconf: {},
      stats: null,
      ss : null,
      imgConn: "./img/conn2.png",
      };
},
methods: {
  async setPost(){
    if (this.user == null || this.password == '' ) {
      this.error = "Поля ввода не должны быть пустыми"
    } else {
    const response = await fetch('/api/login',{
      mode: 'cors',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "usr": this.user,
        "passwd": this.password })
      })
      const data = await response.json()
      this.auth = data
      if (data.auth == true) {
          VueCookies.set('t' ,data.t, "1h")
          this.getSocks()
      } 
        else {
           this.error = "Пользователь не найден"
      }
   }
  },
  getCook() {
     this.cook =  VueCookies.get('t')
     if (this.cook) {
        this.auth.auth = true
        this.getSocks()
      }
  },
  closeQR() {
      this.dialog = false
  },
  getlogout() {
      VueCookies.remove("t")
      window.location.reload()
  },
  copySS(x) {
      const range = document.createRange();
      range.selectNode(document.getElementById(x));
      window.getSelection().removeAllRanges(); 
      const txt = window.getSelection().addRange(range)
      document.execCommand("copy");
      window.getSelection().removeAllRanges();
      alert("скопировано в буфер")
  },
  async getWG() {
      const response = await fetch("/api/home")
      const data = await response.json()
      this.wg = data
      this.getStats()
  },
  async getQR(server,user) {
      this.dialog = true
      this.qrcode = "/api/getconf/" + server + "/" + user
  },
  async getWGconf(server,user) {
      const response = await fetch("/api/getconf/"+server+"/"+user, { method: 'PATCH'})
      const data = await response.text()
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(new Blob([data]))
      link.setAttribute('download', user + '.conf')
      document.body.appendChild(link)
      link.click()
  },
  async setWGconf(server) {
      const user =  prompt("Введите имя пользователя")
      if (user !== null) {
            const response = await fetch("/api/getconf/"+server+"/"+user,{
                  mode: 'cors',
                  method: 'POST',
            })
            const data = await response.json()
            this.getWG()
     }
  },
  async delWGconf(server,user) {
      const response = await fetch("/api/getconf/"+server+"/"+user,{
            mode: 'cors',
            method: 'DELETE'
      })
      const data = await response.json()
      this.getWG()
  },
  async getSocks() {
      const response = await fetch("/api/getsocks")
      const data = await response.json()
      this.ss = data
      this.getWG()
  },
  async getStats() {
      while(true) {
            const response = await fetch("/api/stats")
            if (response.status == 200) {
                  const data = await response.json()
                  this.stats = data
                  await new Promise(resolve => setTimeout(resolve, 30000));
            } else {
                  this.wg = false
                  //return 0
            }
      }
 },
 onLineIMG(x) {
      const time = Math.floor(Date.now() /1000 - x)
      if (time < 120 ) {
            return "/src/img/conn1.png"
      } else {
            return "/src/img/conn2.png"
      }
 }
},
}
</script>

<style scoped>
@font-face {
      font-family: 'sber';
       src: url('./fonts/sber.ttf') format('truetype');
}
@font-face {
      font-family: 'HH';
      src: url('./fonts/HH2.ttf') format('truetype');
}
@font-face {
      font-family: 'HHCyr';
      src: url('./fonts/HH_Cyr.ttf') format('truetype');
}
:global(html) {
      width: 100%;
      height: 100%; 
}
:global(body) {
      width: 100%;
      height: 100%;
      background-image: url(./img/fon2.png);
      font-family: "sber";
      font-size: 14px;
      color: #313131;
      margin: 0;
}

dialog {
      visibility: visible;
      transform: scale(1);
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.4);
      border-radius: 6px;
      border: 0px ;
}
img.displayed {
      position: absolute;               
      top: 50%;                         
      transform: translate(60%, -60%);
      width: 40%;
}
.wrapper {
	display: flex;
      flex-direction: column;
	align-items: center;
      min-height: 100vh;
      width: 100%;
}
.header {
      display: flex;
      justify-content: space-between;
      font-family: HH;
      font-size: 50px;
      width: 80%;
}
.content {
	flex: 1 0 auto;
      width: 70%;
}
.wg {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      vertical-align: middle;
      font-size: 24px;
      font-weight: 700;
      margin-top: 20px;
      margin-bottom: 4px;
}
.clients {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items:center;
      background: rgba(0,0,0,0.1);
      border-radius: 6px;
      height:  45px;
}
.obfs {
      background: rgba(0, 255, 17, 0);
      border: #000000 solid 1px;
      height:  50px;
}
.main {
	flex: 1 0 auto;
      width: 70%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items:center;
}
.logo {
      font-family: HH;
      font-size: 50px;
}
.footer {
	flex: 0 0 auto;
      display: flex;
      justify-content: center;
      width: 100%;
}
.btn {
      display: inline-block;
      outline: none;
      border: 1px solid #313131;
      border-radius: 6px;
      font-family: sber;
      align-items: center;
      vertical-align: middle;
      line-height: 28px;
      font-size: 14px;
      text-decoration: none;
      color: #313131;
      background-color: #ffffff;
      cursor: pointer;
      user-select: none;
      appearance: none;
}
.ss {
      white-space: normal;
      overflow: hidden;
      text-overflow: ellipsis;
 }
 .cp {
      width: 55px;
 }
.inter {
      color: #ffffff;
      background-color: #313131;
}
.txt {
      display: block;
      width: 160px;
      height: 20px;
      padding: 0.375rem 0.75rem;
      font-family: sber;
      font-size: 14px;
      font-weight: 10;
      line-height: 1.5;
      color: #212529;
      background-color: #ffffff;
      background-clip: padding-box;
      border: 1px solid #bdbdbd;
      border-radius: 0.25rem;
      transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}
.txt::placeholder {
      color: #212529;
      opacity: 0.4;
}
@media (min-width: 929px) {
  .header {
      width: 743px;
  }
  .content {
      width: 650px;
  }
}
@media (max-width: 675px) {
  .header {
      width: 99%;
  }
  .wg {
      padding-left: 2px;
      padding-right: 2px; 
  } 
  .content {
      width: 100%;
  }
  .clients {
      border-radius: 0;
  }
  img.displayed {
      top:20%;
      transform: translate(10%, -10%);
      width: 70%;
  }
}
@media (max-width: 420px) {
  .header {
      font-size: 40px;
  }
  .wg {
      font-size: 16px;
  }
  .obfs {
      border: #313131 solid 0px;
      height: 90px;
 }
}
</style>
