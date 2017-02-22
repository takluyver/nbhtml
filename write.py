from copy import deepcopy
import json
import os.path

from nbconvert.exporters import HTMLExporter

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

if __name__ == '__main__':
    exp = SavingHTMLExporter()
    output, resource = exp.from_filename('Sample.ipynb')
    output_file = 'Sample.html'
    with open(output_file, 'w') as f:
        f.write(output)
    print('Saved', output_file)
