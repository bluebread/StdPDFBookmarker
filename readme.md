# StdPDFBookmarker

## Install

Before you use, you must install PLY package first. The package has been contained in this project already.

```shell
$ git clone https://github.com/dabeaz/ply.git
$ cd ./ply
$ python install.py
```

## Example

```python
from bookmarker import AddBookmarksInPDF

if __name__ == '__main__':
    pdf_file = 'your_pdf_file.pdf'
    AddBookmarksInPDF(pdf_file, 'your_rule.txt')
```

## Note

Syntax of rule file is like some nested memo list.  
In your rule file, be careful that all of indents MUST be '\t' (not 4 or 2 spaces ' ') in every single line.