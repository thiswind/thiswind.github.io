---
layout: post
title: "Circle CI 中docker-compose 版本问题"
date: 2015-08-17T15:04:26.000Z
lang: zh
dir: ltr
source_id: "2015-08-17-circle-ci-中docker-compose-版本问题"
categories:
  - "CircleCI"
  - "Docker"
  - "notes"
legacy_source:
  repository: thiswind/thiswind.github.io.old
  url: "http://thiswind.info/2015/08/17/Circle-CI-%E4%B8%ADdocker-compose-%E7%89%88%E6%9C%AC%E9%97%AE%E9%A2%98/"
---
错误代码：

```vbscript
client and
 server don't have same version (client : 1.19
, server: 1.18) docker-compose up -d returned exit
 code 1
```

错误原因：

```bash
$ docker version

Client version: 1.6
.2-circleciClient API version: 1.18
Go version (client): go1.4.2
Git commit (client): 2
f3236dOS/Arch (client): linux/amd64
Server version: 1.6
.2-circleciServer API version: 1.18
Go version (server): go1.4.2
Git commit (server): 2
f3236dOS/Arch (server): linux/amd64
```

解决办法：`requirements.txt`

```bash
docker-compose<=1.3
```

解说

因为目前docker-compose版本已经升级到1.3.3+，并且采用的docker remote api 版本是1.19＋，而CircleCI的Docker版本仍然是1.6.2，支持的docker remote api版本只到1.18，造成客户端和服务端版本不一致。

解决办法，就是明确要求docker-compse的版本不能超过1.3
