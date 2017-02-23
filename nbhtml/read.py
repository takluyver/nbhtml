import json
from lxml.html import parse, tostring
import sys

from nbformat import NotebookNode, write, from_dict
from nbformat.v4 import (new_notebook, new_code_cell, new_markdown_cell,
    new_output)

def load_output(elt):
    stream = elt.xpath('.//div[contains(@class, "output_stream")]')
    if stream:
        name = 'stdout'
        if 'output_stderr' in stream[0].classes:
            name = 'stderr'
        pre = stream[0].xpath('pre')[0]
        return new_output('stream', name=name, text=pre.text_content())

    subarea = elt.xpath('.//div[contains(@class, "output_subarea")]')[0]

    if 'output_error' in subarea.classes:
        err_json = elt.xpath('.//pre[contains(@class, "error_json")]')[0]
        d = json.loads(err_json.text_content())
        return new_output('error', **d)

    # If we've got here, output must be display_data or execute_result
    op_json = elt.xpath('.//pre[contains(@class, "other_output_fmts")]')[0]
    out = from_dict(json.loads(op_json.text_content()))

    if 'output_html' in subarea.classes:
        out.data['text/html'] = ''.join(tostring(el, encoding='unicode') for el in subarea).strip()
    elif 'output_text' in subarea.classes:
        pre = subarea.xpath('pre')[0]
        out.data['text/plain'] = pre.text_content()
    elif 'output_png' in subarea.classes:
        src = subarea.xpath('img')[0].get('src')
        assert src.startswith('data:image/png;base64,'), src[:30]
        out.data['image/png'] = src[len('data:image/png;base64,'):]
    return out

def load_cell(cell_elt):
    if 'text_cell' in cell_elt.classes:
        md_elt = cell_elt.xpath('.//pre[contains(@class, "markdown_raw")]')[0]
        cell = new_markdown_cell(md_elt.text_content())
    elif 'code_cell' in cell_elt.classes:
        cell = load_code_cell(cell_elt)
    else:
        raise ValueError("Unhandled cell type", cell_elt.get('class'))

    metadata_elt = cell_elt.getprevious()
    cell.metadata = from_dict(json.loads(metadata_elt.text_content()))
    return cell

def load_code_cell(cell_elt):
    code_elt = cell_elt.xpath('.//div[@class="input_area"]//pre')[0]
    code = code_elt.text_content()
    if code.endswith('\n'):
        code = code[:-1]
    if code == ' ':  # Empty cell gains a space in HTML conversion
        code = ''
    cell = new_code_cell(code)
    for output in cell_elt.xpath('.//div[@class="output_area"]'):
        cell.outputs.append(load_output(output))

    ec = cell_elt.getnext().get('data-execution-count')
    cell.execution_count = json.loads(ec)

    return cell

def load_notebook(fp):
    tree = parse(fp)
    nb = new_notebook()
    metadata_elt = tree.xpath('//script[@id="notebook_metadata_json"]')[0]
    nb.metadata = from_dict(json.loads(metadata_elt.text_content()))
    for cell_elt in tree.xpath('//div[starts-with(@class, "cell ")]'):
        nb.cells.append(load_cell(cell_elt))
    
    return nb

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        nb = load_notebook(f)

    write(nb, 'from_html.ipynb')
    print('Saved from_html.ipynb')
        
