from weasyprint import HTML, CSS
import commonmark
import sys, os
import argparse
import re
import unicodedata
import tinycss2
import html.parser

def slugify(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def wrap_sections(html):
    return re.sub(
        r'(?s)(<h2>(.*?)</h2>.*?)(?=<h2>|</body>)',
        lambda m: f'<div id="{slugify(m.group(2))}">{m.group(1)}</div>',
        html
    )

def wrap_entries(html):
    return re.sub(
        r'(?s)(<h3>([^<]+)</h3>.*?)(?=<h3>|<h2>|</div>)',
        lambda m: f'<div id="{slugify(m.group(2))}">{m.group(1)}</div>',
        html
    )

def hidden_ids_from_css(css):
    ids = []
    for rule in tinycss2.parse_stylesheet(css):
        if rule.type != 'qualified-rule':
            continue
        declarations = tinycss2.parse_declaration_list(rule.content)
        is_hidden = any(
            d.type == 'declaration'
            and d.lower_name == 'display'
            and any(t.type == 'ident' and t.lower_value == 'none' for t in d.value)
            for d in declarations
        )
        if is_hidden:
            selector = ''.join(t.serialize() for t in rule.prelude)
            ids += re.findall(r'#([\w-]+)', selector)
    return ids

class _DivStripper(html.parser.HTMLParser):
    def __init__(self, hidden_ids):
        super().__init__(convert_charrefs=False)
        self.hidden_ids = hidden_ids
        self.output = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if self.skip_depth > 0:
            if tag == 'div':
                self.skip_depth += 1
            return
        if tag == 'div' and dict(attrs).get('id') in self.hidden_ids:
            self.skip_depth = 1
            return
        self.output.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if tag == 'div' and self.skip_depth > 0:
            self.skip_depth -= 1
            return
        if self.skip_depth == 0:
            self.output.append(f'</{tag}>')

    def handle_data(self, data):
        if self.skip_depth == 0:
            self.output.append(data)

    def handle_entityref(self, name):
        if self.skip_depth == 0:
            self.output.append(f'&{name};')

    def handle_charref(self, name):
        if self.skip_depth == 0:
            self.output.append(f'&#{name};')

    def handle_comment(self, data):
        if self.skip_depth == 0:
            self.output.append(f'<!--{data}-->')

def strip_hidden_divs(html_content, hidden_ids):
    stripper = _DivStripper(set(hidden_ids))
    stripper.feed(html_content)
    return ''.join(stripper.output)

def wrap_header(html):
    return re.sub(
        r'(?s)(<h1>.*?</h1>)((?:\s*<p>.*?</p>)*)',
        r'<div class="resume-header">\1\2</div>',
        html,
        count=1
    )

parser = argparse.ArgumentParser(description="Convert Markdown file to pdf")
parser.add_argument("input", help="Markdown file to convert in pdf.")
parser.add_argument("-o", "--output", dest="output", help="Output file.", type=str, default=None)
parser.add_argument("--html", dest="html", help="Generate HTML file.", action="store_true")
args = parser.parse_args()

with open(args.input, encoding='utf-8') as fp:
  text = fp.read()
  html = commonmark.commonmark(text)
  html = wrap_header(html)
  html = wrap_sections(html)
  html = wrap_entries(html)

  css = ""
  with open('./style.css', encoding='utf-8') as fr:
    css = fr.read()

  html = strip_hidden_divs(html, hidden_ids_from_css(css))
  html_full = "<!DOCTYPE html>\n<html>\n<head>\n<style>\n"
  html_full += '@page { size: A4; margin: 1cm }\n'
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
