"""Save and load notebooks in HTML files.

To work out:
- Metadata: script tags containing JSON?
- Markdown cells
"""
import json
from warnings import warn

from htmlgen import (
    Division as Div, Document, Element, html_attribute, Script,
)
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

class Style(Element):
    def __init__(self, contents):
        super(Style, self).__init__('style')
        self.type_ = 'text/css'
        self.append_raw(contents)

    type_ = html_attribute('type')

def _get_pygments_lexer(language):

    if language == 'ipython2':
        try:
            from IPython.lib.lexers import IPythonLexer
        except ImportError:
            warn("IPython lexer unavailable, falling back on Python")
            language = 'python'
        else:
            return IPythonLexer()
    elif language == 'ipython3':
        try:
            from IPython.lib.lexers import IPython3Lexer
        except ImportError:
            warn("IPython3 lexer unavailable, falling back on Python 3")
            language = 'python3'
        else:
            return IPython3Lexer()

    try:
        return get_lexer_by_name(language, stripall=True)
    except ClassNotFound:
        warn("No lexer found for language %r. Treating as plain text." % language)
        from pygments.lexers.special import TextLexer
        return TextLexer()

class NotebookElement(Div):
    def __init__(self, nb, lexer, formatter):
        super(NotebookElement, self).__init__()
        self.nb = nb
        self.lexer = lexer
        self.formatter = formatter

    def generate(self):
        yield '<div class="notebook">'
        for cell in self.nb.cells:
            if cell.cell_type == 'code':
                div = Div()
                div.append_raw(highlight(cell.source, self.lexer, self.formatter))
                div.add_css_classes('cell', 'code-cell')
                yield div

        yield '</div>'

def dump(nb, fp, nb_name):
    doc = Document(title=nb_name)
    langinfo = nb.metadata.get('language_info', {})
    lexer_name = langinfo.get('pygments_lexer', langinfo.get('name', None))
    lexer = _get_pygments_lexer(lexer_name)
    formatter = HtmlFormatter()
    pygments_styles = Style(formatter.get_style_defs())
    doc.append_head(pygments_styles)
    metadata_et = Script(script=json.dumps(nb.metadata))
    metadata_et.id = "nb_metadata"
    metadata_et.set_attribute('type', 'application/json')
    doc.append_head(metadata_et)
    doc.append_body(NotebookElement(nb, lexer, formatter))

    for fragment in doc:
        #print(repr(fragment))
        fp.write(fragment)


if __name__ == '__main__':
    from nbformat import read
    nb = read('Master-Project.ipynb', as_version=4)
    with open('test-output.html', 'wb') as f:
        dump(nb, f, 'test.ipynb')
