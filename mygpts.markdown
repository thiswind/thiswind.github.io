---
layout: default
title: "My GPTs"
permalink: /mygpts/
---

# Welcome to My GPTs Page


- ## Zaina （Chinese、Arabic）

Fluent Chinese-Arabic translator for daily use.

<img src="/assets/images/Zaina-Chinese-Arabic.png" alt="Zaina (Chinese, Arabic)" style="width:40%;"/>

[Unlock the experience now!](https://chatgpt.com/g/g-6739c10a75e08191bcbc82d4686be4ac-zaina-chinese-arabic)

---

- ## Zaina (Arabic, English )

Zaina provides smooth, culturally aware English-Arabic translations for everyday conversations.

<img src="/assets/images/Zaina-Chinese-English.png" alt="Zaina (Arabic, English)" style="width:40%;"/>

[Unlock the experience now!](https://chatgpt.com/g/g-673b1f7347288191be080f68e585cd78-zaina-arabic-english)



---

<div id="gitalk-container"></div>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/gitalk@1/dist/gitalk.css">
<script src="https://cdn.jsdelivr.net/npm/gitalk@1/dist/gitalk.min.js"></script>
<script>
  const gitalk = new Gitalk({
    clientID: 'Ov23linCXcCwRNHz8v8I',
    clientSecret: '37d9884c3dc889dfa4c3106273aa3f178b4636f2',
    repo: 'thiswind.github.io',      // The repository of store comments,
    owner: 'thiswind',
    admin: ['thiswind'],
    // id: location.pathname,      // Ensure uniqueness and length less than 50
    id: location.pathname.replace(/[^a-zA-Z0-9_\-\/]/g, ""),  // 简化 id，移除中文和特殊字符
    distractionFreeMode: false  // Facebook-like distraction free mode
  })

  gitalk.render('gitalk-container')
</script>