from lxml.html import parse, tostring
from nbformat import NotebookNode, write
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
    op_type = 'display_data'
    kwargs = {}
    if 'output_execute_result' in subarea.classes:
        op_type = 'execute_result'
        ec = elt.xpath('.//div[@data-execution-count]')[0].get('data-execution-count')
        kwargs['execution_count'] = int(ec)
    data = {}
    if 'output_html' in subarea.classes:
        data['text/html'] = ''.join(tostring(el) for el in subarea)
    if 'output_text' in subarea.classes:
        pre = subarea.xpath('pre')[0]
        data['text/plain'] = pre.text_content()
    return new_output(op_type, data=data, **kwargs)

def load_code_cell(cell_elt):
    code_elt = cell_elt.xpath('.//div[@class="input_area"]//pre')[0]
    cell = new_code_cell(code_elt.text_content())
    for output in cell_elt.xpath('.//div[@class="output_area"]'):
        cell.outputs.append(load_output(output))
    return cell

def load_notebook(fp):
    tree = parse(fp)
    nb = new_notebook()
    for cell_elt in tree.xpath('//div[starts-with(@class, "cell ")]'):
        if 'text_cell' in cell_elt.get('class'):
            md_elt = cell_elt.xpath('.//pre[contains(@class, "markdown_raw")]')[0]
            nb.cells.append(new_markdown_cell(md_elt.text_content()))
        elif 'code_cell' in cell_elt.classes:
            nb.cells.append(load_code_cell(cell_elt))
    
    return nb

if __name__ == '__main__':
    with open('Sample.html') as f:
        nb = load_notebook(f)

    write(nb, 'test-loaded.ipynb')
        
