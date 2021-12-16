"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[348],{1478:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return s},contentTitle:function(){return p},metadata:function(){return l},toc:function(){return d},default:function(){return m}});var a=n(7462),i=n(3366),o=(n(7294),n(3905)),r=["components"],s={id:"networking",title:"Networking"},p=void 0,l={unversionedId:"RPI/networking",id:"RPI/networking",isDocsHomePage:!1,title:"Networking",description:"Specs",source:"@site/docs/01-RPI/03-networking.md",sourceDirName:"01-RPI",slug:"/RPI/networking",permalink:"/laundro/RPI/networking",editUrl:"https://github.com/usdevs/laundro/tree/docs/docs/01-RPI/03-networking.md",tags:[],version:"current",sidebarPosition:3,frontMatter:{id:"networking",title:"Networking"},sidebar:"tutorialSidebar",previous:{title:"Remote Access (SSH)",permalink:"/laundro/RPI/remote-access"},next:{title:"Hardware",permalink:"/laundro/Legacy/breakdown-hardware"}},d=[{value:"Specs",id:"specs",children:[],level:2},{value:"Connecting to a Wireless Network (Incomplete)",id:"connecting-to-a-wireless-network-incomplete",children:[],level:2},{value:"References",id:"references",children:[],level:2}],c={toc:d};function m(e){var t=e.components,n=(0,i.Z)(e,r);return(0,o.kt)("wrapper",(0,a.Z)({},c,n,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h2",{id:"specs"},"Specs"),(0,o.kt)("p",null,"Network card: ",(0,o.kt)("a",{parentName:"p",href:"https://www.raspberry-pi-geek.com/Archive/2016/17/Raspberry-Pi-3-Model-B-in-detail#:~:text=The%20Broadcom%20BCM43438%20WiFi%2FBluetooth,not%20enabled%20on%20the%20Pi."},(0,o.kt)("strong",{parentName:"a"},"BCM43438"))),(0,o.kt)("div",{className:"admonition admonition-caution alert alert--warning"},(0,o.kt)("div",{parentName:"div",className:"admonition-heading"},(0,o.kt)("h5",{parentName:"div"},(0,o.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,o.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",viewBox:"0 0 16 16"},(0,o.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M8.893 1.5c-.183-.31-.52-.5-.887-.5s-.703.19-.886.5L.138 13.499a.98.98 0 0 0 0 1.001c.193.31.53.501.886.501h13.964c.367 0 .704-.19.877-.5a1.03 1.03 0 0 0 .01-1.002L8.893 1.5zm.133 11.497H6.987v-2.003h2.039v2.003zm0-3.004H6.987V5.987h2.039v4.006z"}))),"caution")),(0,o.kt)("div",{parentName:"div",className:"admonition-content"},(0,o.kt)("p",{parentName:"div"},"It does ",(0,o.kt)("strong",{parentName:"p"},"not")," support 5GHz"))),(0,o.kt)("h2",{id:"connecting-to-a-wireless-network-incomplete"},"Connecting to a Wireless Network (Incomplete)"),(0,o.kt)("ol",null,(0,o.kt)("li",{parentName:"ol"},(0,o.kt)("p",{parentName:"li"},"Add credentials"),(0,o.kt)("pre",{parentName:"li"},(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"wpa_passphrase <ssid> <password> >> /etc/wpa_supplicant/wpa_supplicant.conf\n")),(0,o.kt)("div",{parentName:"li",className:"admonition admonition-warning alert alert--danger"},(0,o.kt)("div",{parentName:"div",className:"admonition-heading"},(0,o.kt)("h5",{parentName:"div"},(0,o.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,o.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"12",height:"16",viewBox:"0 0 12 16"},(0,o.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M5.05.31c.81 2.17.41 3.38-.52 4.31C3.55 5.67 1.98 6.45.9 7.98c-1.45 2.05-1.7 6.53 3.53 7.7-2.2-1.16-2.67-4.52-.3-6.61-.61 2.03.53 3.33 1.94 2.86 1.39-.47 2.3.53 2.27 1.67-.02.78-.31 1.44-1.13 1.81 3.42-.59 4.78-3.42 4.78-5.56 0-2.84-2.53-3.22-1.25-5.61-1.52.13-2.03 1.13-1.89 2.75.09 1.08-1.02 1.8-1.86 1.33-.67-.41-.66-1.19-.06-1.78C8.18 5.31 8.68 2.45 5.05.32L5.03.3l.02.01z"}))),"warning")),(0,o.kt)("div",{parentName:"div",className:"admonition-content"},(0,o.kt)("p",{parentName:"div"},"This will also add the raw passphrase into the ",(0,o.kt)("inlineCode",{parentName:"p"},".conf")," file as a comment. A good practice would be to remove that line of comment"))),(0,o.kt)("div",{parentName:"li",className:"admonition admonition-note alert alert--secondary"},(0,o.kt)("div",{parentName:"div",className:"admonition-heading"},(0,o.kt)("h5",{parentName:"div"},(0,o.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,o.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,o.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M6.3 5.69a.942.942 0 0 1-.28-.7c0-.28.09-.52.28-.7.19-.18.42-.28.7-.28.28 0 .52.09.7.28.18.19.28.42.28.7 0 .28-.09.52-.28.7a1 1 0 0 1-.7.3c-.28 0-.52-.11-.7-.3zM8 7.99c-.02-.25-.11-.48-.31-.69-.2-.19-.42-.3-.69-.31H6c-.27.02-.48.13-.69.31-.2.2-.3.44-.31.69h1v3c.02.27.11.5.31.69.2.2.42.31.69.31h1c.27 0 .48-.11.69-.31.2-.19.3-.42.31-.69H8V7.98v.01zM7 2.3c-3.14 0-5.7 2.54-5.7 5.68 0 3.14 2.56 5.7 5.7 5.7s5.7-2.55 5.7-5.7c0-3.15-2.56-5.69-5.7-5.69v.01zM7 .98c3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.12-7-7 3.14-7 7-7z"}))),"note")),(0,o.kt)("div",{parentName:"div",className:"admonition-content"},(0,o.kt)("p",{parentName:"div"},"This would only work for ",(0,o.kt)("strong",{parentName:"p"},"WPA")," networks and not ",(0,o.kt)("strong",{parentName:"p"},"WPA-Enterprise")," networks (e.g. ",(0,o.kt)("inlineCode",{parentName:"p"},"NUS_STU"),")")))),(0,o.kt)("li",{parentName:"ol"},(0,o.kt)("p",{parentName:"li"},"Reboot RPI"),(0,o.kt)("pre",{parentName:"li"},(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"sudo reboot\n")))),(0,o.kt)("h2",{id:"references"},"References"),(0,o.kt)("ul",null,(0,o.kt)("li",{parentName:"ul"},(0,o.kt)("a",{parentName:"li",href:"https://wiki.archlinux.org/title/wpa_supplicant"},"https://wiki.archlinux.org/title/wpa_supplicant"))))}m.isMDXComponent=!0}}]);