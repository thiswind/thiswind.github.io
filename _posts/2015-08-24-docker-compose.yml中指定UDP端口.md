---
layout: post
title: "docker-compose.yml中指定UDP端口"
date: 2015-08-24T12:52:00.000Z
lang: zh
dir: ltr
source_id: "2015-08-24-docker-compose.yml中指定udp端口"
categories:
  - "Docker"
  - "UDP"
  - "notes"
legacy_source:
  repository: thiswind/thiswind.github.io.old
  url: "http://thiswind.info/2015/08/24/docker-compose-yml%E4%B8%AD%E6%8C%87%E5%AE%9AUDP%E7%AB%AF%E5%8F%A3/"
---
这样：

```bash
....:
  build: ...
  ...
  ports:
    - "53:53/udp"
```
