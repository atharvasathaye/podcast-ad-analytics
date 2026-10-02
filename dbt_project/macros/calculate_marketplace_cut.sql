{% macro calculate_marketplace_cut(amount_column, fee_percentage='0.30') %}
    round(cast({{ amount_column }} as numeric) * {{ fee_percentage }}, 2)
{% endmacro %}
