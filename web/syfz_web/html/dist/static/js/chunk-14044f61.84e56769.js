(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-14044f61"],{"30c7":function(t,n,s){},"98a7":function(t,n,s){"use strict";s.r(n);var e=function(){var t=this,n=t.$createElement,s=t._self._c||n;return s("div",{staticClass:"agent-deploy"},[s("el-card",{staticClass:"agent-card"},[s("div",{staticClass:"agent-container"},[s("div",{staticClass:"agent-left"},[s("div",{staticClass:"agent-item-header"},[s("div",{staticClass:"agent-logo"},[s("SvgIcon",{staticStyle:{width:"100px",height:"100px"},attrs:{"icon-class":"linux"}})],1),t._v(" "),s("div",{staticClass:"agent-title"},[t._v("Linux主机取证流程")])]),t._v(" "),s("div",{staticClass:"agent-item-container"},[s("div",{staticClass:"agent-item-content"},[t._v("\n            方法一：在主机运行以下安装命令\n          ")]),t._v(" "),s("div",{staticClass:"agent-item-content agent-code"},[s("code",[t._v("\n              "+t._s(t.codes[0])+"\n            ")]),t._v(" "),s("div",{staticClass:"copy-btn",on:{click:function(n){return t.copy(0)}}},[t._v("复制")])]),t._v(" "),s("span",{staticClass:"agent-tips"},[t._v("或")]),t._v(" "),s("div",{staticClass:"agent-item-content agent-code"},[s("code",[t._v("\n              "+t._s(t.codes[1])+"\n            ")]),t._v(" "),s("div",{staticClass:"copy-btn",on:{click:function(n){return t.copy(1)}}},[t._v("复制")])]),t._v(" "),s("span",{staticClass:"agent-tips"},[t._v("注意：执行后，当前目录会生成以IP+时间命名的.log取证文件，同时会自动上传到境外服务器进行解析。若出现无法在线读取的情况请保存.log文件到本地并在本系统内手动上传。")])]),t._v(" "),s("el-divider"),t._v(" "),s("div",{staticClass:"agent-item-container"},[s("div",{staticClass:"agent-item-content"},[t._v("\n            方法二：下载相应版本轻代理并上传傀儡机执行\n          ")]),t._v(" "),s("div",{staticClass:"agent-item-content"},[s("el-button",{attrs:{type:"primary"},on:{click:t.downShellFile}},[t._v("\n              CentOS/Ubuntu/Debian\n            ")]),t._v(" "),s("el-button",{attrs:{type:"primary"},on:{click:t.downShellFile}},[t._v("\n              Linux ARM 64\n            ")])],1),t._v(" "),s("span",[t._v("执行以下命令")]),t._v(" "),s("div",{staticClass:"agent-item-content agent-code"},[s("code",[t._v("\n              "+t._s(t.codes[2])+"\n            ")]),t._v(" "),s("div",{staticClass:"copy-btn",on:{click:function(n){return t.copy(2)}}},[t._v("复制")])]),t._v(" "),s("span",{staticClass:"agent-tips"},[t._v("注意：执行后，当前目录会生成以IP+时间命名的.log取证文件，请保存.log文件到本地并在本系统内手动上传。")])])],1),t._v(" "),s("div",{staticClass:"divider"}),t._v(" "),s("div",{staticClass:"agent-right"},[s("div",{staticClass:"agent-item-header"},[s("div",{staticClass:"agent-logo"},[s("SvgIcon",{staticStyle:{width:"100px",height:"100px"},attrs:{"icon-class":"windows"}})],1),t._v(" "),s("div",{staticClass:"agent-item-title"},[t._v("Windows主机取证流程")])]),t._v(" "),s("div",{staticClass:"agent-item-container"},[s("div",{staticClass:"agent-item-content"},[t._v("\n            方法一：下载轻代理并以管理员权限进行安装\n          ")]),t._v(" "),s("div",{staticClass:"agent-item-content"},[s("el-button",{attrs:{type:"primary"},on:{click:t.downShellFile}},[t._v("\n              下载轻代理\n            ")])],1)]),t._v(" "),s("div",{staticClass:"agent-item-container"},[s("div",{staticClass:"agent-item-content"},[t._v("\n            方法二：在主机运行以下安装命令\n          ")]),t._v(" "),s("div",{staticClass:"agent-item-content agent-code"},[s("code",[t._v(" "+t._s(t.codes[3])+" ")]),t._v(" "),s("div",{staticClass:"copy-btn",on:{click:function(n){return t.copy(3)}}},[t._v("复制")])])])])])])],1)},a=[],c=s("c00a"),i={components:{SvgIcon:c["a"]},data:function(){return{downUrl:"http://192.161.164.168:82/zsscan.sh",codes:["wget http://192.161.164.168:82/zsscan.sh && chmod +x zsscan.sh && ./zsscan.sh","curl -O http://192.161.164.168:82/zsscan.sh && chmod +x zsscan.sh && ./zsscan.sh","chmod +x zsscan.sh && ./zsscan.sh","powershell.exe -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command $IP='172.19.212.146',$USER='cloud';$TYPE=NF-7400D'’,iex((New-Object System.Net.WebClient).DownloadString('http://'+$IP+'/safe/soft/sdserver-installer.ps1'))"]}},methods:{copy:function(t){var n=this.codes[t],s=document.createElement("input");s.value=n,document.body.appendChild(s),s.select(),document.execCommand("copy"),document.body.removeChild(s),this.$message.success("复制成功！")},downShellFile:function(){var t=document.createElement("a");t.href=this.downUrl,t.target="_blank",document.body.appendChild(t),t.click(),document.body.removeChild(t)}}},o=i,l=(s("d8c3"),s("2877")),d=Object(l["a"])(o,e,a,!1,null,null,null);n["default"]=d.exports},d8c3:function(t,n,s){"use strict";var e=s("30c7"),a=s.n(e);a.a}}]);