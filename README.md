# resume-markdown

To create a pdf file :

```
python3 convert.py resume-en.md
```

The option `--html` also generates the HTML which will be converted into pdf :

```
python3 convert.py --html resume-en.md
```

The option `--double-column` creates files in double columns :

```
python3 convert.py --double-column resume-en.md
```

The Python application use the CSS files `style.css` and `style_doublecolumn.css` to render the resume nicely.

The application depends on CommonMark and WeasyPrint.

## Downloads

My resume : [pdf](https://github.com/jgurhem/resume-markdown/releases/latest/download/resume-en.pdf)
