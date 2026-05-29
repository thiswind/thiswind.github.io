---
categories:
- blog
date: 2024-12-23 19:46:00 +0800
dir: ltr
lang: tr
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
title: 'Eğlenceli Bir Programlama Problemi: Şeftali ve Şeftali Çekirdeği

  '
translated_by: llm
translation_model: gpt-5.4-nano
translation_updated_at: '2026-05-29T08:11:32.137403+00:00'
---

Bu, şeftali ve şeftali çekirdeğiyle ilgili eğlenceli bir programlama problemidir. Kurallar aşağıdaki gibidir:
- Başlangıçta belirli miktarda para ve çekirdek bulunur.
- Her seferinde 1 birim para ile 1 şeftali satın alabilir ya da 3 çekirdeği 1 şeftali ile takas edebilirsiniz.
- Her bir şeftaliyi yediğinizde 1 çekirdek kazanırsınız.

Nihai hedef: mümkün olduğunca çok şeftali yemek. Aşağıda bu problemi çözmek için eksiksiz düşünce yapısı ve kod yer almaktadır.

## Çözüm Fikri

Bu problemin ana noktası, çekirdeklerin değerini yeterince iyi kullanmak ve israfı önlemektir. İzlenecek adımlar şunlardır:
1. Her adımda, çekirdeklerin değerini paraya çevirerek fonları en üst düzeye çıkarın.
2. Yeterli para varsa, 1 şeftali satın alıp yiyin.
3. Artık satın almaya devam edemediğinizde, kaynak kullanımını maksimize etmek için “bir kere daha takas yapıp yapamayacağınıza” bakın.

## Program Kodu

Aşağıdaki kod, Python ile eksiksiz bir uygulamadır:

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