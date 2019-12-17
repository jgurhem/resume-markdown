from weasyprint import HTML, CSS
import commonmark
import sys, os
import argparse

parser = argparse.ArgumentParser(description="Convert Markdown file to pdf")
parser.add_argument("input", help="Markdown file to convert in pdf.")
parser.add_argument("-o", "--output", dest="output", help="Output file.", type=str, default=None)
parser.add_argument("--double-column", dest="dc", help="Use double columns.", action="store_true")
parser.add_argument("--html", dest="html", help="Generate HTML file.", action="store_true")
args = parser.parse_args()

with open(args.input, encoding='utf-8') as fp:
  text = fp.read()
  html = commonmark.commonmark(text)

  css = ""
  with open('./style.css', encoding='utf-8') as fr:
    css = fr.read()
  html_full = "<!DOCTYPE html>\n<html>\n<head>\n<style>\n"
  html_full += '@page { size: A4; margin: 1cm }\n'
  html_full += css
  if args.dc:
    with open('./style_doublecolumn.css', encoding='utf-8') as fr:
      css = fr.read()
    html_full += css
  html_full += "</style>\n</head>\n<body>\n"
  html_full += html
  html_full += "</body>\n</html>"

  html = HTML(string=html_full, encoding='utf-8')

  if args.output == None:
    out_file = os.path.splitext(args.input)[0] + '.pdf'
    html_file = os.path.splitext(args.input)[0] + '.html'
  else:
    out_file = os.path.splitext(args.output)[0] + '.pdf'
    html_file = os.path.splitext(args.output)[0] + '.html'

  if args.html:
    with open(html_file, "w", encoding='utf-8') as fw:
      fw.write(html_full)

  html.write_pdf(out_file)
