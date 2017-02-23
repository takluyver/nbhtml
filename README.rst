This *experimental* project tries to save Jupyter notebooks as HTML and read them back.

To try it::

    python3 -m nbhtml.write Sample.ipynb
    python3 -m nbhtml.read Sample.ipynb.html

    diff from_html.ipynb Sample.ipynb

This could one day be combined with a project like `ipymd
<https://github.com/rossant/ipymd>`__ to save notebooks in two complementary
formats:

- 'Complete' HTML notebooks, including images and outputs, which can easily be
  shared with people who may not have the Notebook application installed.
- 'Clean' notebooks containing only the input (code and markdown) and metadata,
  convenient for version control (e.g. in git), making diffing and merging easy.
