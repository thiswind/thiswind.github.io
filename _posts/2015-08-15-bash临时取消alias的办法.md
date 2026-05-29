---
layout: post
title: "bash临时取消alias的办法"
date: 2015-08-15T06:12:05.000Z
lang: zh
dir: ltr
source_id: "2015-08-15-bash临时取消alias的办法"
categories:
  - "Bash"
  - "Linux"
  - "Mac"
  - "notes"
legacy_source:
  repository: thiswind/thiswind.github.io.old
  url: "http://thiswind.info/2015/08/15/bash%E4%B8%B4%E6%97%B6%E5%8F%96%E6%B6%88alias%E7%9A%84%E5%8A%9E%E6%B3%95/"
---
一般来说，在`~/.bash_profile`里面一般都定义了一些别名(`alias`)。有时候在命令行当中要临时仅用某个别名，可以用`unalias`命令

```bash
unalias
 <要暂时禁用的别名>
```
