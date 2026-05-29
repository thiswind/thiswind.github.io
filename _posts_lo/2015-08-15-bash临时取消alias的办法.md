---
categories:
- Bash
- Linux
- Mac
- notes
date: 2015-08-15 06:12:05+00:00
dir: ltr
lang: lo
layout: post
source_hash: sha256:5f6bf26003af3e6a52bcad99fa5a4869d91d0f263eacd28e712e74315c760783
source_id: 2015-08-15-bash临时取消alias的办法
source_lang: zh
source_path: _posts/2015-08-15-bash临时取消alias的办法.md
title: วิธีปิด alias ชั่วคราวใน bash
translated_by: llm
translation_model: gpt-5.4-nano
translation_updated_at: '2026-05-29T09:33:28.952668+00:00'
---

โดยทั่วไปแล้ว ใน `~/.bash_profile` มักจะมีการกำหนด alias บางอย่างเอาไว้ (`alias`)។ บางครั้งเวลาที่ใช้งานในบรรทัดคำสั่ง จำเป็นต้องใช้คำสั่งโดยอาศัย alias เพียงชั่วคราว ก็สามารถใช้คำสั่ง `unalias` ได้

```bash
unalias
 <要暂时禁用的别名>
```