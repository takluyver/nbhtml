{%- extends 'full.tpl' -%}

{%- block html_head -%}
{{ super() }}
<style type="text/css">
.hidden {
  display: none;
}
</style>

<script type="application/json" id="notebook_metadata_json">
{{ nb.metadata | json }}
</script>
{%- endblock html_head -%}

{% block any_cell %}
<pre class="hidden cell_metadata_json">{{cell.metadata | json | escape }}</pre>
{{ super() }}
{% endblock any_cell %}

{% block codecell %}
{{ super() }}
<div class="hidden" data-execution-count="{{ cell.execution_count | json }}"></div>
{%- endblock codecell %}

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

{% block output_area_prompt %}
{{ super() }}

{%- if output.output_type in ('execute_result', 'display_data') -%}
<pre class="hidden other_output_fmts">{{ output | json_non_shown_output | escape }}</pre>
{%- endif -%}
{% endblock output_area_prompt %}


{% block error -%}
<pre class="hidden error_json">{{output | json_error_data | escape }}</pre>
{{ super() }}
{%- endblock error %}
