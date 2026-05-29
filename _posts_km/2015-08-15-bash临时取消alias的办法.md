---
categories:
- Bash
- Linux
- Mac
- notes
date: 2015-08-15 06:12:05+00:00
dir: ltr
lang: km
layout: post
source_hash: sha256:5f6bf26003af3e6a52bcad99fa5a4869d91d0f263eacd28e712e74315c760783
source_id: 2015-08-15-bash临时取消alias的办法
source_lang: zh
source_path: _posts/2015-08-15-bash临时取消alias的办法.md
title: វិធីបិទ alias ជាបណ្តោះអាសន្ននៅ bash
translated_by: llm
translation_model: gpt-5.4-nano
translation_updated_at: '2026-05-29T09:33:28.950419+00:00'
---

ជាទូទៅ នៅក្នុង `~/.bash_profile` ជាធម្មតាត្រូវបានកំណត់នូវ alias មួយចំនួន (`alias`)។ ពេលខ្លះ នៅពេលប្រើ command line អ្នកចង់ប្រើ alias តែមួយចំនួនជាបណ្តោះអាសន្ន អាចធ្វើបានដោយប្រើពាក្យបញ្ជា `unalias`។

```bash
unalias
 <要暂时禁用的别名>
```