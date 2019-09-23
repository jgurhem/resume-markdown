# resume-markdown

To create a pdf file :

```
python3 convert.py resume-en.md
```

To create an html file :

```
cmark resume-en.md > resume-en.html
```

The HTML file and the Python application use the CSS file `style.css` to render the resume nicely.

The applications depends on CommonMark and WeasyPrint.
