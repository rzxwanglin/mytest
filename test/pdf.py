import markdown2
import pdfkit

# 读取 Markdown 文件内容
with open('api接口.md', 'r', encoding='utf-8') as md_file:
    md_content = md_file.read()

# 将 Markdown 内容转换为 HTML
html_content = markdown2.markdown(md_content)

# 将 HTML 内容转换为 PDF 并保存
pdfkit.from_string(html_content, 'output.pdf')
