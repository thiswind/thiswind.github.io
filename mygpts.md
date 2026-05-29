---
layout: base
title: My GPTs
permalink: /mygpts/
lang: zh
dir: ltr
---

<section class="gpt-registry cyber-frame" augmented-ui="tl-2-clip-x tr-clip br-2-clip-y bl-clip border">
  <header class="section-header compact">
    <span class="section-kicker">AI TOOL REGISTRY</span>
    <h1>Translation Nodes</h1>
    <p>这些是我构建和使用的翻译型 GPT 节点。它们关注语言之间的自然表达，而不是机械替换词语。</p>
  </header>
  <div class="gpt-grid">
    {% for gpt in site.data.gpts %}
      {% include gpt-card.html gpt=gpt %}
    {% endfor %}
  </div>
</section>
