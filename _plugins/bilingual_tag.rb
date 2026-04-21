# 双语段落标签插件
# 使用方法:
#
# {% bilingual %}
# 这里写中文内容，可以写多行，可以用 Markdown
# ---
# 这里写阿拉伯语内容，同样可以写多行
# {% endbilingual %}
#
# 设计理念: 作者只需要关心内容，不需要关心布局和 HTML 结构
# 用 --- 分隔两种语言，简单直观

module Jekyll
  class BilingualTag < Liquid::Block
    def initialize(tag_name, markup, tokens)
      super
    end

    def render(context)
      content = super.strip
      
      # 用 --- 分隔中文和阿拉伯语
      parts = content.split(/^---$/, 2).map(&:strip)
      
      zh_content = parts[0] || ''
      ar_content = parts[1] || ''
      
      # 渲染 Markdown
      site = context.registers[:site]
      converter = site.find_converter_instance(Jekyll::Converters::Markdown)
      
      zh_html = converter.convert(zh_content)
      ar_html = converter.convert(ar_content)
      
      # 生成最终 HTML 结构（使用新的 Tailwind 类名）
      <<~HTML
        <div class="bilingual-card">
          <div class="zh-section">
            #{zh_html}
          </div>
          #{'<div class="ar-section">' + ar_html + '</div>' if ar_content && !ar_content.empty?}
        </div>
      HTML
    end
  end
end

Liquid::Template.register_tag('bilingual', Jekyll::BilingualTag)
