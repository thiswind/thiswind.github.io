---
categories:
- blog
date: 2024-12-23 19:46:00 +0800
dialect: damascus_levantine
dir: rtl
lang: ar
layout: post
source_hash: sha256:f5881bd6504553598f74a81fe9bb3b43c4810662128763cd0f7659c680c7b3e2
source_id: 2024-12-23-peach-and-pit-puzzle
source_lang: zh
source_path: _posts/2024-12-23-peach-and-pit-puzzle.md
tags:
- 编程
- 数学
- 趣味题
- 桃子
title: 'مسألة برمجة حلوة: خوخ و نواة الخوخ

  '
translated_by: llm
translation_model: gpt-5.4-nano
translation_updated_at: '2026-05-29T08:11:32.134191+00:00'
---

هيدي مسألة برمجة حلوة وشيّقة عن الخوخ ونواة الخوخ. القواعد هيك:
- من البداية في عندك عدد معيّن من الفلوس وعدد معيّن من النوى.
- كل مرة فيك تشتري خوخة واحدة بفلوس 1، أو تِبدّل 3 نوى على خوخة واحدة.
- كل ما تاكل خوخة وحدة، بصير تربح 1 نواة.

الهدف النهائي: تاكل أكبر عدد ممكن من الخوخ. يليها بتلاقي الفكرة الكاملة للحل والبرنامج كامل.

## فكرة الحل

السر هون إنك تستفيد بأقصى شكل من قيمة النوى وتمنع الهدر. خطوات العمل:
1. بكل خطوة، حوِّل قيمة النوى على فلوس، حتى تكون الفلوس هي الأكبر.
2. إذا الفلوس بتكفي، اشترِ خوخة واحدة وخليها تنأكل.
3. لما تجرّب تشتري وما بقى فيك تكمل، راجع إذا فيك “تبدّل مرة زيادة” حتى تستغل الموارد بأقصى قدر.

## كود البرنامج

يلي أدناه الكود كامل باستخدام Python:

```python
money = 10
peach_pits = 0
peaches_eaten = 0

while True:
    money += peach_pits / 3
    peach_pits = 0
    
    if money < 1:
        if money + 1/3 >= 1:
            money += 1/3
            peach_pits -= 1
        else:
            break
    
    money -= 1
    peaches_eaten += 1
    peach_pits += 1

print(f"总共吃了 {peaches_eaten} 个桃子")
```