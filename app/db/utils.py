import re
from typing import Any

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

LOGICAL_OPERATORS = {"AND", "OR"}

ALLOWED_OPERATORS = {
    "=",
    "!=",
    "<>",
    "<",
    "<=",
    ">",
    ">=",
    "LIKE",
    "NOT LIKE",
    "IN",
    "NOT IN",
    "IS",
    "IS NOT",
}


def build_sql_values_clause_for_insert(columns_text: str) -> str:
    """
    Convert a comma-separated list of column names into a SQL VALUES clause with named placeholders.

    Input Example:
        columns_text = "(identifier, task_type, payload)"

    Output Example:
        "VALUES (:identifier, :task_type, :payload)"
    """
    values = columns_text.replace("(", "").replace(")", "")
    values = values.split(",")
    values = ", ".join([f":{value.strip()}" for value in values])
    return f"VALUES ({values})"


def build_sql_set_clause_for_update(data: dict) -> dict:
    """
    Construct a SQL SET clause string and corresponding values list from an update payload.

    Input Example:
        data = {
            "status": "COMPLETED",
            "attempts": {"value": "attempts + 1"}
        }

    Output Example:
        SqlSetClauseResult(
            query_str="SET status = :status, attempts = attempts + 1",
            values=["COMPLETED"]
        )
    """
    if not data:
        raise ValueError("data cannot be empty")

    data_len = len(data)

    query_str = ""
    values = {}

    # Building columns
    for index, (field, value) in enumerate(data.items()):
        if index == 0:
            query_str += "SET"

        if type(value) is dict:
            query_str += f" {field} = {value['value']}"
        elif isinstance(value, str) and value.upper() == "NOW":
            query_str += f" {field} = NOW()"
        else:
            query_str += f" {field} = :{field}"
            values[field] = value

        if index < data_len - 1:
            query_str += ", "

    result = {
        "column_str": query_str,
        "column_value": values
    }

    return result


def build_sql_where_clause(condition: dict) -> dict:
    """
    Convert a nested condition dictionary into a parametrized SQL WHERE clause.

    Returns:
        {
            "text": "id = :p0 AND (run_at IS NULL OR run_at <= NOW())",
            "values": {
                "p0": 1
            }
        }

    Example input:
        {
            "and": [
                {"id": 1},
                {
                    "or": [
                        {"run_at": None},
                        {"run_at": {"<=": "NOW"}}
                    ]
                }
            ]
        }

    Example output:
        {
            "text": "id = :p0 AND (run_at IS NULL OR run_at <= NOW())",
            "values": {
                "p0": 1
            }
        }

    Notes:
        - Values are parametrized.
        - Field/column names are validated because SQL parameters cannot
          be used for identifiers.
        - "NOW" is treated as the SQL function NOW().
    """

    values = {}
    parameter_counter = 0

    def validate_field(field: str) -> str:
        """Validate a SQL identifier such as 'id' or 'run_at'."""
        if not isinstance(field, str):
            raise TypeError(
                f"Field name must be a string, got {type(field).__name__}"
            )

        if not _IDENTIFIER_RE.fullmatch(field):
            raise ValueError(
                f"Invalid SQL field name: {field!r}"
            )

        return field

    def add_parameter(value: Any) -> str:
        """Add a value and return its named SQL placeholder."""
        nonlocal parameter_counter

        name = f"p{parameter_counter}"
        parameter_counter += 1

        values[name] = value

        return f":{name}"

    def format_value(value: Any) -> str:
        """
        Convert a Python value into a parametrized SQL value.

        Special case:
            "NOW" -> NOW()
        """
        if isinstance(value, str) and value.upper() == "NOW":
            return "NOW()"

        return add_parameter(value)

    def format_condition(field: str, value: Any) -> str:
        """Build SQL for a single field condition."""

        field = validate_field(field)

        # {"id": None}
        if value is None:
            return f"{field} IS NULL"

        # {"age": {">": 18, "<": 60}}
        if isinstance(value, dict):
            if not value:
                raise ValueError(
                    f"Condition for field '{field}' cannot be empty"
                )

            conditions = []

            for operator, operator_value in value.items():
                if not isinstance(operator, str):
                    raise TypeError(
                        f"SQL operator must be a string, "
                        f"got {type(operator).__name__}"
                    )

                operator = operator.upper().strip()

                if operator not in ALLOWED_OPERATORS:
                    raise ValueError(
                        f"Unsupported SQL operator: {operator}"
                    )

                # -------------------------------------------------
                # IS / IS NOT
                # -------------------------------------------------
                if operator in {"IS", "IS NOT"}:
                    if operator_value is None:
                        sql_value = "NULL"
                    else:
                        sql_value = format_value(operator_value)

                    conditions.append(
                        f"{field} {operator} {sql_value}"
                    )
                    continue

                # -------------------------------------------------
                # Handle = NULL and != NULL correctly
                # -------------------------------------------------
                if operator in {"=", "!=", "<>"} and operator_value is None:
                    if operator == "=":
                        conditions.append(f"{field} IS NULL")
                    else:
                        conditions.append(f"{field} IS NOT NULL")

                    continue

                # -------------------------------------------------
                # IN / NOT IN
                # -------------------------------------------------
                if operator in {"IN", "NOT IN"}:
                    if not isinstance(
                            operator_value,
                            (list, tuple, set)
                    ):
                        raise TypeError(
                            f"{operator} requires a list, tuple, or set"
                        )

                    if not operator_value:
                        raise ValueError(
                            f"{operator} cannot use an empty collection"
                        )

                    placeholders = [
                        format_value(item)
                        for item in operator_value
                    ]

                    conditions.append(
                        f"{field} {operator} "
                        f"({', '.join(placeholders)})"
                    )

                    continue

                # -------------------------------------------------
                # Normal comparison
                # -------------------------------------------------
                conditions.append(
                    f"{field} {operator} "
                    f"{format_value(operator_value)}"
                )

            return " AND ".join(conditions)

        # ---------------------------------------------------------
        # Normal equality
        # ---------------------------------------------------------
        return f"{field} = {format_value(value)}"

    def build(data: dict) -> str:
        """Recursively build the SQL expression."""

        if not isinstance(data, dict):
            raise TypeError(
                f"Expected dict, got {type(data).__name__}"
            )

        if not data:
            raise ValueError("Condition cannot be empty")

        expressions = []

        for key, value in data.items():

            if not isinstance(key, str):
                raise TypeError(
                    f"Condition key must be a string, "
                    f"got {type(key).__name__}"
                )

            operator = key.upper().strip()

            # =====================================================
            # AND / OR
            # =====================================================
            if operator in LOGICAL_OPERATORS:

                if not isinstance(value, list):
                    raise TypeError(
                        f"'{operator}' requires a list of conditions"
                    )

                if not value:
                    raise ValueError(
                        f"'{operator}' cannot have an empty condition list"
                    )

                children = [
                    build(item)
                    for item in value
                ]

                if not children:
                    raise ValueError(
                        f"'{operator}' contains no valid conditions"
                    )

                joined = f" {operator} ".join(children)

                if len(children) > 1:
                    joined = f"({joined})"

                expressions.append(joined)

            # =====================================================
            # FIELD CONDITION
            # =====================================================
            else:
                expressions.append(
                    format_condition(key, value)
                )

        if not expressions:
            raise ValueError("Condition cannot be empty")

        # Multiple top-level fields have implicit AND semantics.
        return " AND ".join(expressions)

    text = build(condition)

    return {
        "where_str": f" WHERE {text} ",
        "where_value": values,
    }


def rows_to_dict_list(rows: Any) -> dict | list | None:
    if not rows:
        return None

    if len(rows) == 1:
        return dict(rows[0]._mapping)

    return [dict(row._mapping) for row in rows]
