---
categories:
- Bash
- Linux
- Mac
- notes
date: 2015-08-15 06:12:05+00:00
dir: ltr
lang: my
layout: post
source_hash: sha256:5f6bf26003af3e6a52bcad99fa5a4869d91d0f263eacd28e712e74315c760783
source_id: 2015-08-15-bash临时取消alias的办法
source_lang: zh
source_path: _posts/2015-08-15-bash临时取消alias的办法.md
title: bash တွင် alias ကို ယာယီ ပိတ်နည်း
translated_by: llm
translation_model: gpt-5.4-nano
translation_updated_at: '2026-05-29T09:33:28.948101+00:00'
---

အများအားဖြင့် `~/.bash_profile` ထဲမှာ alias တချို့ကို သတ်မှတ်ထားတတ်ပါတယ် (`alias`)။ တခါတရံ command line ထဲမှာ alias တစ်ခုခုကို ယာယီသာ သုံးချင်ရင် `unalias` ဆိုတဲ့ command ကို အသုံးပြုနိုင်ပါတယ်။

```bash
unalias
 <要暂时禁用的别名>
```