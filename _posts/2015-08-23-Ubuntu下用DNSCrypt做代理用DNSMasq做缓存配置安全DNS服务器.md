---
layout: post
title: "Ubuntu下用DNSCrypt做代理用DNSMasq做缓存配置安全DNS服务器"
date: 2015-08-23T13:53:29.000Z
lang: zh
dir: ltr
source_id: "2015-08-23-ubuntu下用dnscrypt做代理用dnsmasq做缓存配置安全dns服务器"
categories:
  - "DNS"
  - "OpenDNS"
  - "Ubuntu"
  - "notes"
legacy_source:
  repository: thiswind/thiswind.github.io.old
  url: "http://thiswind.info/2015/08/23/Ubuntu%E4%B8%8B%E7%94%A8DNSCrypt%E5%81%9A%E4%BB%A3%E7%90%86%E7%94%A8DNSMasq%E5%81%9A%E7%BC%93%E5%AD%98%E9%85%8D%E7%BD%AE%E5%AE%89%E5%85%A8DNS%E6%9C%8D%E5%8A%A1%E5%99%A8/"
---
# OS：Ubuntu 12.04 64位

# 零、介绍

## DNS污染：

域名服务器缓存污染（DNS cache pollution），又称域名服务器缓存投毒（DNS cache poisoning），是指一些刻意制造或无意中制造出来的域名服务器封包，把域名指往不正确的IP地址。一般来说，在互联网上都有可信赖的域名服务器，但为减低网络上的流量压力，一般的域名服务器都会把从上游的域名服务器获得的解析记录暂存起来，待下次有其他机器要求解析域名时，可以立即提供服务。一旦有关域名的局域域名服务器的缓存受到污染，就会把域名内的电脑导引往错误的服务器或服务器的网址。1

## OpenDNS:

OpenDNS为个人和商业提供DNS方案，用户可以自行选择使用OpenDNS的服务或者使用当地ISP提供的DNS服务。将服务器组放置在具有战略意义的地方和使用大量的域名缓存可以使DNS查询进度可以更快得多地完成，从而加快页面的检索速度。DNS的查询结果有时被本地的操作系统或应用程序缓存下来，所以速度的增加也许不能在每次查询中体现出来，但本地缓存里没有的结果其查询速度的增加则显而易见。 其他特征包括一个反钓鱼过滤器和输入纠正（type correction）〔举例说明，你输入wikipedia.og会被自动替换成wikipedia.org〕。通过收集恶意网站列表，当用户通过他们的服务来访问这些恶意网站时，OpenDNS将封锁这些恶意网站。OpenDNS最近启动了反钓鱼服务（PhishTank），这样全球的用户就可以报告和察看不可信的钓鱼网站。

OpenDNS并不是像它的名字那样，它不是一款开源软件。2

## DNSCrypt为什么能防止DNS污染

用简单好理解的话说吧

传统DNS是明文的，就像一张明信片，明信片上在指定的位置，你写上了你是谁，发给谁，想询问什么信息。 这样一来，负责传递明信片的人可以看到你写的东西，只要他不高兴，就可以直接把你的明信片拿来，伪造一份改过内容的发过去骗你（或者干脆给你拦截下来，只要他想怎样都行） 反过来，DNS服务器发给你的回答，也是同理

而DNSCrypt将DNS信息进行加密处理，写在明信片上的，是另一种你和DNS服务器能看懂，但是邮递员以及其他人看不懂的语言，他会以为你发的只是一封正常的邮件，就把这个邮件当作普通的邮件处理（邮递员：看不懂呢…算了感觉没什么可疑的嘛不管了），于是原封不动地送到目的地。

当然了，也许有一天，邮递员们觉得，诶这个DNS服务器的东西似乎不太健康呢，于是他们也可以把目的地为某个服务器的所有信件全部瞎改或者扔掉，只是他们目前还没这么做。。。

上边有人说到使用TCP，这不是根本，因为DNS Crypt是可以使用UDP的。TCP的选项算是提供了一个额外的功能吧，因为在丢包率较高的网络环境下UDP用起来很坑爹的。3

## Dnsmasq

Dnsmasq是一个开源的轻量级DNS转发和DHCP、TFTP服务器，使用C语言编写。Dnsmasq针对家庭局域网等小型局域网设计，资源占用低，易于配置。支持的平台包括Debian、Fedora、 Smoothwall、IP-Cop、floppyfw、Firebox、LEAF、Freesco, fli4l、CoyoteLinux及 Android等，并且在dd-wrt、 openwrt路由器系统中也有使用。4

## Ubuntu

Ubuntu（国际音标：英语发音：/ʊˈbʊntuː/，uu-buun-too）是一个以桌面应用为主的GNU/Linux操作系统，其名称来自非洲南部祖鲁语或科萨语的“ubuntu”一词（译为乌班图），意思是“人性”、“我的存在是因为大家的存在”，是非洲传统的一种价值观。

Ubuntu由马克·舍特尔沃斯创立，其首个版本—4.10发布于2004年10月20日，它以Debian为开发蓝本。与Debian稳健的升级策略不同，Ubuntu每六个月便会发布一个新版，以便人们实时地获取和使用新软件。Ubuntu的开发目的是为了使个人电脑变得简单易用，同时也提供针对企业应用的服务器版本。Ubuntu的每个新版本均会包含当时最新的GNOME桌面环境，通常在GNOME发布新版本后一个月内发布。与其它基于Debian的Linux发布版，如MEPIS、Xandros、Linspire、Progeny和Libranet等相比，Ubuntu更接近Debian的开发理念，它主要使用自由、开源的软件，而其它发布版往往会附带很多闭源的软件。

Ubuntu建基于Debian的不稳定分支：不论其软件格式（deb）还是软件管理与安装系统（Debian Apt）。Ubuntu的开发者会把对软件的修改实时反馈给Debian社区，而不是在发布新版时才宣布这些修改。事实上，很多Ubuntu的开发者同时也是Debian主要软件的维护者。不过，Debian与Ubuntu的软件并不一定完全兼容，也就是说，将Debian的包安装在Ubuntu上可能会出现兼容性问题，反之亦然。

Ubuntu的运作主要依赖Canonical有限公司的支持，同时亦有来自Linux社区的热心人士提供协助。Ubuntu的开发人员多称马克·舍特尔沃斯为SABDFL（是self-appointed benevolent dictator for life的缩写，即自封终生开源码大佬）。在2005年7月8日，马克·舍特尔沃斯与Canonical有限公司宣布成立Ubuntu基金会，并提供1千万美元作为启始营运资金。成立基金会的目的是为了确保将来Ubuntu得以持续开发与获得支持，但直至2006年，此基金会仍未投入运作。马克·舍特尔沃斯形容此基金会是在Canonical有限公司出现财务危机时的紧急营运资金。

在过去的版本用户可以通过船运服务（shipit）来获得免费的安装光盘。Ubuntu 6.06版有提供免费船运服务，然而其后的Ubuntu 6.10版却没有提供免费的船运邮寄光盘服务，用户只可由网站上下载光盘映像文件刻录并安装。。Ubuntu 6.06发布当时，曾有消息指出往后不会再对非长期支持版提供船运服务，但在Ubuntu7.04版推出时，船运服务再度启动，而此版并非长期支持版。在Ubuntu11.04发布前夕，船运服务被停止。

目前Ubuntu共有五个长期支持版本（Long Term Support，LTS）：Ubuntu 6.06、8.04、10.04、12.04与14.04。Ubuntu 12.04和14.04桌面版与服务器版都有5年支持周期。而之前的长期支持版本为桌面版3年，服务器版5年。5

Ubuntu 发行版列表：6

Ubuntu 发行版列表

版本号
代号
中文意思

Ubuntu 4.10
Warty Warthog
多疣的疣猪

Ubuntu 5.04
Hoary Hedgehog
白发的刺猬

Ubuntu 5.10
Breezy Badger
活泼的獾

Ubuntu 6.06
LTS Dapper Drake
整洁的公鸭

Ubuntu 6.10
Edgy Eft
尖利的小蜥蜴

Ubuntu 7.04
Feisty Fawn
烦躁不安的小鹿

Ubuntu 7.10
Gutsy Gibbon
胆大的长臂猿

Ubuntu 8.04
LTS Hardy Heron
坚强的苍鹭

Ubuntu 8.10
Intrepid Ibex
勇敢的野山羊

Ubuntu 9.04
Jaunty Jackalope
得意洋洋的怀俄明野兔

Ubuntu 9.10
Karmic Koala
幸运的考拉

Ubuntu 10.04
LTS Lucid Lynx
清醒的猞猁

Ubuntu 10.10
Maverick Meerkat
标新立异的的狐獴

Ubuntu 11.04
Natty Narwhal
敏捷的独角鲸

Ubuntu 11.10
Oneiric Ocelot
有梦的虎猫

Ubuntu 12.04
LTS Precise Pangolin
精准的穿山甲

Ubuntu 12.10
Quantal Quetzal
量子的格查尔鸟

Ubuntu 13.04
Raring Ringtail
铆足了劲的环尾猫熊

Ubuntu 13.10
Saucy Salamander
活泼的蝾螈

Ubuntu 14.04
LTS Trusty Tahr
可靠的塔尔羊

Ubuntu 14.10
Utopic Unicorn
乌托邦的独角兽

# 一、配置PPA

```bash
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:shnatsel/dnscrypt
```

# 二、安装DNSCrypt Proxy

## 安装：

```bash
sudo apt-get update
sudo apt-get install dnscrypt-proxy
```

## 配置：

因为DNSCrypt默认端口时53，将会与DNSMasq发生端口冲突，所以我们要把端口改成其他，比如改成40

修改 `/etc/default/dnscrypt-proxy` 7， 找到这一行，并修改端口为40，当然你也可以改成其他，只要不和系统其他端口冲突即可：

```bash
# What local IP the daemon will listen to, with an optional port. The default port is 53.
local
-address=127.0.0.2:40
```

## 测试：

```bash
$ sudo service dnscrypt-proxy restart
dnscrypt-proxy stop/waiting
dnscrypt-proxy start/running, process 1561

$ dig g.cn @127.0
.0.2 -p 40
; > DiG 9.8
.1-P1 <<>> g.cn @127.0.0.2 -p 40;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 30656
;; flags: qr rd ra; QUERY: 1
, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1
;; OPT PSEUDOSECTION:
; EDNS: version: 0
, flags:; udp: 4096;; QUESTION SECTION:
;g.cn.				IN	A

;; ANSWER SECTION:
g.cn.			227
	IN	A	203.208.48.148g.cn.			227
	IN	A	203.208.48.144g.cn.			227
	IN	A	203.208.48.145g.cn.			227
	IN	A	203.208.48.146g.cn.			227
	IN	A	203.208.48.147
;; Query time: 113
 msec;; SERVER: 127.0
.0.2#40(127.0.0.2);; WHEN: Sun Aug 23
 22:28:37 2015;; MSG SIZE  rcvd: 113
```

## 讲解：

DNSCrypt有三种运行模式：

### 命令行模式: 直接在命令行用参数来设置启动命令 8

支持的命令如下：

```bash
$ dnscrypt-proxy --help
dnscrypt-proxy 1.4
.0
Options:

  -a
	--local-address=...			# 监听的地址，例如: 127.0.0.1:53  -d
	--Daemonize模式				# 守护进程模式  -e
	--edns-payload-size=...		# 后面略，详情见官方文档[^2]  -h	--help
  -L	--resolvers-list=...
  -R	--resolver-name=...
  -l
	--logfile=...  -m	--loglevel=...
  -n	--max-active-requests=...
  -p	--pidfile=...
  -X	--plugin=...
  -N	--provider-name=...
  -k	--provider-key=...
  -r	--resolver-address=...
  -u	--user=...
  -t	--test=...
  -T	--tcp-only
  -V	--version

Please consult the dnscrypt-proxy(8
) man page for details.
```

### Daemonize模式: 后台进程运行。

直接通过`sudo dnscrypt-proxy -d` 即可启动。不需要配置任何命令行参数，所有参数均从`/etc/default/dnscrypt-proxy`配置文件读取

### 系统服务模式：默认的运行模式

安装完成，或者系统启动就会自动启动。与Daemonize模式一样，启动参数从`/etc/default/dnscrypt-proxy`配置文件读取
- 停止：`sudo service dnscrypt stop`
- 启动：`sudo service dnscrypt start`
- 重启：`sudo service dnscrypt restart`

# 二、安装DNSMasq

## 安装：

```bash
sudo apt-get update
sudo apt-get -y install dnsmasq
```

## 配置：

修改 `/etc/dnsmasq.conf` 配置文件。配置文件内容可以根据需要酌情修改，这里就不详细介绍每个选项的功能和注意事项了，详情请google9，此处只需要修改一行，将DNSMasq的上行服务器设置为刚刚配置好的DNSCrypt-Proxy，找到，并改称这样：

```bash
# You can control how dnsmasq talks to a server: this forces
# queries to 10.1.2.3 to be routed via eth1
# server=10.1.2.3@eth1
server=127.0
.0.2#40
```

## 测试

注意，此处端口是 `-p 53`，不同于去前面讲到的 dnscrpyt-proxy 的 `-p 40`

```bash
$ sudo service dnsmasq restart
Stopped Name Service Cache Daemon: nscd.
 * Starting Name Service Cache Daemon nscd                               [ OK ]
 * Restarting DNS forwarder and DHCP server dnsmasq                      [ OK ]
Stopped Name Service Cache Daemon: nscd.
 * Starting Name Service Cache Daemon nscd                               [ OK ]

$ dig g.cn @127.0
.0.1 -p 53
; > DiG 9.8
.1-P1 <<>> g.cn @127.0.0.1 -p 53;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52188
;; flags: qr rd ra; QUERY: 1
, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1
;; OPT PSEUDOSECTION:
; EDNS: version: 0
, flags:; udp: 4096;; QUESTION SECTION:
;g.cn.				IN	A

;; ANSWER SECTION:
g.cn.			295
	IN	A	203.208.48.144g.cn.			295
	IN	A	203.208.48.146g.cn.			295
	IN	A	203.208.48.148g.cn.			295
	IN	A	203.208.48.145g.cn.			295
	IN	A	203.208.48.147
;; Query time: 113
 msec;; SERVER: 127.0
.0.1#53(127.0.0.1);; WHEN: Sun Aug 23
 22:41:00 2015;; MSG SIZE  rcvd: 113
```

## 讲解：

dnsmasq 也可以采用其他的上行服务器，例如著名的 `8.8.8.8` 和 `114.114.114.114`, dnsmasq 默认是监听外部端口的，所以不需要专门对监听的IP进行配置，你可以直接访问外部IP进行测试，例如

```bash
nslookup g.cn 192.168
.31.139
```

# 三、OpenDNS有效性测试

访问[OpenDNS的测试页面](https://www.opendns.com/welcome/)，如果你看到打勾，说明配置成功。如果有问题，请留言：）

---
1.

域名服务器缓存污染，维基百科：https://zh.wikipedia.org/wiki/域名服务器缓存污染↩
2.

OpenDNS，维基百科：https://zh.wikipedia.org/wiki/OpenDNS↩
3.

DNSCrypt的工作原理是什么？为什么能防止DNS污染？，知乎：http://www.zhihu.com/question/24253866/answer/29272628↩
4.

Dnsmasq，维基百科：https://zh.wikipedia.org/wiki/Dnsmasq↩
5.

Ubuntu，维基百科：https://zh.wikipedia.org/wiki/Ubuntu↩
6.

Ubuntu发行版列表，维基百科：https://zh.wikipedia.org/wiki/Ubuntu发行版列表↩
7.

这个文件是安装DNSCrypt的时候自动生成的↩
8.

这是文档上的标准启动方式，详见官方文档：https://github.com/jedisct1/dnscrypt-proxy#usage↩
9.

DNSMasq 配置：https://www.google.com/search?q=dnsmasq.conf%20%E7%9A%84#newwindow=1&safe=active&q=dnsmasq.conf+%E9%85%8D%E7%BD%AE↩
