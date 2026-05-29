---
layout: post
title: "DNSMasq and DNSCrypt in one Docker"
date: 2015-08-24T13:26:22.000Z
lang: zh
dir: ltr
source_id: "2015-08-24-dnsmasq-and-dnscrypt-in-one-docker"
categories:
  - "DNSCrypt"
  - "DNSMasq"
  - "Docker"
  - "notes"
legacy_source:
  repository: thiswind/thiswind.github.io.old
  url: "http://thiswind.info/2015/08/24/DNSMasq-and-DNSCrypt-in-one-Docker/"
---
# SOURCE CODE

[https://github.com/thiswind/dnscrypt_dnsmasq](https://github.com/thiswind/dnscrypt_dnsmasq)

# DNSMasq and DNSCrypt all in one, with OpenDNS

# PRE-REQUIREMENT

***Docker-Compose***1

For ubuntu & Mac OSX

```bash
sudo pip -H install --upgrade docker-compose
```

# INSTALL

```bash
git clone
 https://github.com/thiswind/dnscrypt_dnsmasq.git
cd
 dnscrypt_dnsmasq
docker-compose up
```

---
1.

Docker-Compse：https://docs.docker.com/compose/↩
