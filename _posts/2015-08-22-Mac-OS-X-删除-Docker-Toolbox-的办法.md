---
layout: post
title: "Mac OS X 删除 Docker Toolbox 的办法"
date: 2015-08-22T05:24:26.000Z
lang: zh
dir: ltr
source_id: "2015-08-22-mac-os-x-删除-docker-toolbox-的办法"
categories:
  - "Docker"
  - "Mac"
  - "notes"
legacy_source:
  repository: thiswind/thiswind.github.io.old
  url: "http://thiswind.info/2015/08/22/Mac-OS-X-%E5%88%A0%E9%99%A4-Docker-Toolbox-%E7%9A%84%E5%8A%9E%E6%B3%95/"
---
创建一个bash脚本：

```bash
vi toolbox_osx_uninstall.sh
```

填入如下代码：

```bash
#!/bin/bash

# Uninstall Script

if
 [ "${USER}" != "root" ]; then	echo
 "$0 must be run as root!"	exit
 2fi

while
 true; do  read
 -p "Remove all VMs? (Y/N): " yn  case
 $yn in    [Yy]* ) docker-machine rm -f
 $(docker-machine ls -q); break;;    [Nn]* ) break
;;    * ) echo
 "Please answer yes or no.";;  esac
done

echo
 "Removing Applications..."rm -rf /Applications/Docker

echo
 "Removing docker binaries..."rm -f
 /usr/local/bin/dockerrm -f
 /usr/local/bin/docker-machinerm -f
 /usr/local/bin/docker-compose
echo
 "Removing boot2docker.iso and socket files..."rm -rf ~/.docker
rm -rf /usr/local
/share/boot2docker
echo
 "All Done!"
```

增加可执行权限：

```bash
chmod a+x toolbox_osx_uninstall.sh
```

运行校本：

```bash
macbook:Scripts thiswind$ sudo ./toolbox_osx_uninstall.sh
Password:
Remove all VMs? (Y/N): y
./toolbox_osx_uninstall.sh: line 13
: docker-machine: command not found./toolbox_osx_uninstall.sh: line 13
: docker-machine: command not foundRemoving Applications...
Removing docker binaries...
Removing boot2docker.iso and socket files...
All Done!
macbook:Scripts thiswind$
```
