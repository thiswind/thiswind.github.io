---
categories:
- Bash
- Linux
- Mac
- notes
date: 2015-08-15 06:12:05+00:00
dialect: damascus_levantine
dir: rtl
lang: ar
layout: post
source_hash: sha256:5f6bf26003af3e6a52bcad99fa5a4869d91d0f263eacd28e712e74315c760783
source_id: 2015-08-15-bash临时取消alias的办法
source_lang: zh
source_path: _posts/2015-08-15-bash临时取消alias的办法.md
title: كيف بتلغي alias مؤقتًا في bash
translated_by: llm
translation_model: gpt-5.4-nano
translation_updated_at: '2026-05-29T09:33:28.959154+00:00'
---

بشكل عام، جوا `~/.bash_profile` عم يتم تعريف شوية alias (مثل `alias`) . أحيانًا بعندك شغل على سطر الأوامر وبدّك تستخدم alias معيّن بشكل مؤقت فقط، ممكن تعمل هيك باستخدام الأمر `unalias`.

```bash
unalias
 <要暂时禁用的别名>
```