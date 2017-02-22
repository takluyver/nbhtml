{%- extends 'full.tpl' -%}

{%- block html_head -%}
{{ super() }}
<style type="text/css">
.hidden {
  display: none;
}
</style>
{%- endblock html_head -%}

{% block markdowncell scoped %}
<div class="cell border-box-sizing text_cell rendered">
<pre class="hidden markdown_raw">{{ cell.source }}</pre>
{{ self.empty_in_prompt() }}
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
{{ cell.source  | markdown2html | strip_files_prefix }}
</div>
</div>
</div>
{%- endblock markdowncell %}


{% block execute_result -%}
<div class="hidden" data-execution-count="{{ output.execution_count }}"/>
{{ super() }}
{%- endblock execute_result %}
