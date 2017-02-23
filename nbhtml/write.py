from copy import deepcopy
import json
import os.path
import sys

from nbconvert.exporters import HTMLExporter

def tojson(d):
    return json.dumps(d, sort_keys=True, indent=2)

def error_data(output):
    output = output.copy()
    del output['output_type']
    return json.dumps(output, sort_keys=True)

class SavingHTMLExporter(HTMLExporter):
    """Export HTML with enough information to reconstruct the notebook.
    """
    def __init__(self, **kw):
        super().__init__(**kw)
        self.template_path = [os.path.dirname(__file__)]
        self.template_file = 'saving.tpl'

    def json_non_shown_output(self, output):
        """Serialise a copy of outputs other than the one shown.
        """
        output = deepcopy(output)
        for fmt in self.config.NbConvertBase.display_data_priority:
            if fmt in output.data:
                del output.data[fmt]
                break

        return json.dumps(output, sort_keys=True)

    def default_filters(self):
        yield from super().default_filters()
        yield ('json_non_shown_output', self.json_non_shown_output)
        yield ('json_error_data', error_data)
        yield ('json', tojson)

def convert(ipynb_file):
    exp = SavingHTMLExporter()
    output, resource = exp.from_filename(ipynb_file)
    output_file = ipynb_file + '.html'
    with open(output_file, 'w') as f:
        f.write(output)
    return output_file

if __name__ == '__main__':
    output_file = convert(sys.argv[1])
    print('Saved', output_file)
