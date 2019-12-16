from weasyprint import HTML, CSS
import commonmark
import sys, os
import argparse

parser = argparse.ArgumentParser(description="Convert Markdown file to pdf")
parser.add_argument("input", help="Markdown file to convert in pdf.")
parser.add_argument("-o", "--output", dest="output", help="Output file.", type=str, default=None)
parser.add_argument("--double-column", dest="dc", help="Use double columns.", action="store_true")
args = parser.parse_args()

with open(args.input) as fp:
  text = fp.read()
  html = commonmark.commonmark(text)
  html = HTML(string=html, encoding='utf-8')
  css = CSS(string='@page { size: A4; margin: 1cm }')
  css_file = CSS('./style.css')
  css_file_dc = CSS('./style_doublecolumn.css')

  if args.output == None:
    out_file = os.path.splitext(args.input)[0] + '.pdf'
  else:
    out_file = args.output

  if args.dc:
    stylesheets = [css, css_file, css_file_dc]
  else:
    stylesheets = [css, css_file]

  html.write_pdf(out_file, stylesheets=stylesheets)
