---
categories:
- Bash
- Linux
- Mac
- notes
date: 2015-08-15 06:12:05+00:00
dir: rtl
lang: fa
layout: post
source_hash: sha256:5f6bf26003af3e6a52bcad99fa5a4869d91d0f263eacd28e712e74315c760783
source_id: 2015-08-15-bash临时取消alias的办法
source_lang: zh
source_path: _posts/2015-08-15-bash临时取消alias的办法.md
title: روش غیرفعال‌کردن موقت alias در bash
translated_by: llm
translation_model: gpt-5.4-nano
translation_updated_at: '2026-05-29T09:33:28.957007+00:00'
---

به‌طور معمول، داخل `~/.bash_profile` چند alias تعریف می‌شود (`alias`). گاهی هم وقتی در خط فرمان کار می‌کنید، لازم است موقتاً فقط همان alias مشخص را کنار بگذارید؛ در چنین حالتی می‌توانید از دستور `unalias` استفاده کنید.

```bash
unalias
 <要暂时禁用的别名>
```