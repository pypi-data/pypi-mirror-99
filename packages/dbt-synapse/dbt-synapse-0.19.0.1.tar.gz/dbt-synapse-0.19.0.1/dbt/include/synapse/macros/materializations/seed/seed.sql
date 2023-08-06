{% macro synapse__basic_load_csv_rows(model, batch_size, agate_table) %}

    {# Synapse does not support the TSQL's normal Table Value Constructor of #}
    {# INSERT INTO Dest_Table (cols) SELECT cols FROM Ref_Table #}

    {% set cols_sql = get_seed_column_quoted_csv(model, agate_table.column_names) %}
    {% set bindings = [] %}

    {% set statements = [] %}

    {% for chunk in agate_table.rows | batch(batch_size) %}
        {% set bindings = [] %}

        {% for row in chunk %}
            {% do bindings.extend(row) %}
        {% endfor %}

        {% set sql %}
            insert into {{ this.render() }} ({{ cols_sql }})
            {% for row in chunk -%}
                {{'SELECT'+' '}}
                {%- for column in agate_table.column_names -%}
                    {# TSQL catch 22: #}
                        {# strings must be single-quoted & #}
                        {# single-quotes inside of strings must be doubled #}
                    
                    {% set col_type = agate_table.columns[column].data_type | string %}
                    {%- if "text.Text" in col_type -%}
                      '{{str_replace(row[column]) if row[column]}}'
                    {% else %}
                      '{{ row[column] if row[column] }}'
                    {%- endif -%}
                    {%- if not loop.last%}, {%- endif -%}
                {%- endfor -%}
                {%- if not loop.last-%} {{' '+'UNION ALL'+'\n'}} {%- endif -%}
            {%- endfor -%}
        {% endset %}

        {% do adapter.add_query(sql, abridge_sql_log=True) %}

        {% if loop.index0 == 0 %}
            {% do statements.append(sql) %}
        {% endif %}
    {% endfor %}

    {# Return SQL so we can render it out into the compiled files #}
    {{ return(statements[0]) }}
{% endmacro %}

{% macro synapse__load_csv_rows(model, agate_table) %}
  {{ return(synapse__basic_load_csv_rows(model, 200, agate_table) )}}
{% endmacro %}