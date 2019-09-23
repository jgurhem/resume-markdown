from weasyprint import HTML, CSS
import commonmark
import sys, os

if len(sys.argv) != 2:
  print("Usage : python3 " + sys.argv[0] + " resume.md")
  sys.exit(1)


with open(sys.argv[1]) as fp:
  text = fp.read()
  html = commonmark.commonmark(text)
  html = HTML(string=html, encoding='utf-8')
  css = CSS(string='@page { size: A4; margin: 1cm }')
  css_file = CSS('./style.css')
  out_file = os.path.splitext(sys.argv[1])[0] + '.pdf'
  html.write_pdf(out_file, stylesheets=[css, css_file])
