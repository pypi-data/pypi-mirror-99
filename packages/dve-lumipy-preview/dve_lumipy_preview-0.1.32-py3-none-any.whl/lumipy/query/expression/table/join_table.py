from typing import List

from lumipy.common.string_utils import indent_str
from lumipy.query.expression.column.column_base import BaseColumnExpression
from lumipy.query.expression.column.column_prefix import PrefixedColumn
from lumipy.query.expression.column.source_column import SourceColumn
from lumipy.query.expression.sql_value_type import SqlValType
from lumipy.query.expression.table.base_source_table import BaseSourceTable
from lumipy.query.expression.table.table_alias import AliasedTable


def _check_for_alias_clashes(left_table, right_table):
    left_parts = set([node.get_alias() for node in left_table.get_decomposition() if isinstance(node, AliasedTable)])
    right_parts = set([node.get_alias() for node in right_table.get_decomposition() if isinstance(node, AliasedTable)])

    if len(left_parts.intersection(right_parts)) != 0:
        raise ValueError(
            "Detected duplicate aliases during join construction:\n"
            f"    Left table contains: {', '.join(left_parts)}\n"
            f"    Right table contains: {', '.join(right_parts)}\n"
            "Consider supplying right_alias or left_alias parameters to the join method if the defaults are clashing "
            "(lhs, rhs)."
        )


class JoinSourceTable(BaseSourceTable):
    """Class representing a source table that is the result of a source table join.

    """

    def __init__(
            self,
            join_op_name: str,
            left_table: BaseSourceTable,
            right_table: BaseSourceTable,
            on: BaseColumnExpression,
            left_alias: str,
            right_alias: str
    ):
        """__init__ method for JoinSourceTable class.

        Args:
            join_op_name (str): name labelling the join operation.
            left_table (BaseSourceTable): table on the left hand side of the join operation.
            right_table (BaseSourceTable): table on the right hand side of the join operation.
            on (BaseColumnExpression): column expression that defines the join condition between the parent tables.
            left_alias (str): alias to use for the left hand side parent table.
            right_alias (str): alias to use for the right hand side parent table.
        """
        if not issubclass(type(left_table), BaseSourceTable):
            raise TypeError(f"Left table must be a source table type. Was {type(left_table).__name__}.")
        if not issubclass(type(right_table), BaseSourceTable):
            raise TypeError(f"Left table must be a source table type. Was {type(right_table).__name__}.")
        if isinstance(right_table, JoinSourceTable):
            raise TypeError(
                "Right table can't be a join: either convert to a table variable and join that, or chain join methods "
                "together."
            )
        if hash(right_table) == hash(left_table):
            raise ValueError(
                f"Left and right sides of the join are identical - this is not allowed without aliasing.\n"
                f"To do a self join the sides of the join must be supplied as two aliases of the parent table of the "
                f"self join.\n"
                f"Try the following instead:\n"
                "  rhs = table.with_alias('RHS')\n"
                "  lhs = table.with_alias('LHS')\n"
                "  join = lhs.inner_join(rhs, on=<your join condition>)\n"
            )
        if not issubclass(type(on), BaseColumnExpression):
            raise TypeError(
                f"Join's on expression must be a type of column expression. Was {type(on).__name__}."
            )
        if on.get_type() != SqlValType.Boolean:
            raise TypeError(f"Join's on expression did not resolve to a boolean, but was {on.get_type().name}.")

        self._join_type = join_op_name

        if isinstance(left_table, AliasedTable):
            self._left_table = left_table
            left_hash = hash(left_table.get_original())
        elif isinstance(left_table, JoinSourceTable):
            self._left_table = left_table
            left_hash = hash(left_table)
        else:
            self._left_table = left_table.with_alias(left_alias)
            left_hash = hash(left_table)

        if isinstance(right_table, AliasedTable):
            self._right_table = right_table
            right_hash = hash(right_table.get_original())
        elif isinstance(right_table, JoinSourceTable):
            self._right_table = right_table
            right_hash = hash(right_table)
        else:
            self._right_table = right_table.with_alias(right_alias)
            right_hash = hash(right_table)

        self._is_self_join = left_hash == right_hash

        # Check for clashing aliases
        _check_for_alias_clashes(self._left_table, self._right_table)

        # store aliased duplicates against their hashes
        self._duplicates_aliases = {}
        union_of_cols = self._handle_duplicate_join_columns(
            self._left_table.get_columns()
            + self._right_table.get_columns()
        )
        union_of_params = {
            **self._left_table.get_parameters(),
            **self._right_table.get_parameters()
        }

        self._on = self.apply_prefix(on)

        from_arg_string = f'{self._left_table.get_from_arg_string()} {self._join_type}'
        from_arg_string += f' join {self._right_table.get_from_arg_string()}'
        from_arg_string += f' on {self._on.get_sql()}'

        super().__init__(
            from_arg_string,
            union_of_cols,
            left_table.get_client(),
            f"{join_op_name} join",
            union_of_params,
            self._left_table,
            self._right_table
        )

        self.validate_source_columns([on])

    def apply_prefix(self, expression: BaseColumnExpression) -> BaseColumnExpression:
        """Apply prefixes to source columns in a column expression. If the column belongs to this table it will be
        prefixed with the table alias otherwise it will be left alone.

        Args:
            expression (BaseColumnExpression): input expression

        Returns:
            BaseColumnExpression: expression with preixes applied
        """
        return self._left_table.apply_prefix(
            self._right_table.apply_prefix(expression)
        )

    def contains_column(self, column: BaseColumnExpression) -> bool:
        # Overload b/c we want to accept anything the parent tables do
        membership_tests = [
            lambda x: super(JoinSourceTable, self).contains_column(x),
            lambda x: self._left_table.contains_column(x),
            lambda x: self._right_table.contains_column(x),
        ]
        return any(mt(column) for mt in membership_tests)

    def _handle_duplicate_join_columns(self, cols):
        in_cols = []
        names = []
        for col in cols:
            if col.get_name() not in names:
                names.append(col.get_name())
                in_cols.append(col)
            else:
                # Column name is degenerate between lhs/rhs. Add an alias and warn user.
                original = col.get_without_prefix()
                name_str = original.get_sql().replace('[', '').replace(']', '')
                alias = f"{name_str}_{col.get_prefix()}"
                aliased = col.with_alias(alias)
                self._duplicates_aliases[hash(col)] = aliased
                in_cols.append(aliased)
        return in_cols

    @staticmethod
    def _extra_self_join_condition(col):
        decomp = col.get_decomposition()

        # Every source column node must have at least one associated prefixed col expression
        sources = [node for node in decomp.keys() if isinstance(node, SourceColumn)]
        prefixes = [node for node in decomp.keys() if isinstance(node, PrefixedColumn)]
        for s in sources:
            assoc_prefixed = [p for p in prefixes if p.get_without_prefix().hash_equals(s)]
            if len(assoc_prefixed) == 0:
                return False

        return True

    def validate_source_columns(self, columns: List[BaseColumnExpression]) -> List[BaseColumnExpression]:
        """Validate and preprocess columns.

        For each input column, check membership and handle cases such as python
        primitives -> LiteralColumn and the '*' and '^' inputs -> column object lists. Additionally, in this overload
        for the JoinSourceTable class there is automatic handling of aliasing for degenerate names between RHS/LHS
        table columns and auto prefixing of columns from the parent table. This allows the join source table to accept
        column expressions built from columns that belong to its parents.

        Args:
            columns (List[BaseColumnExpression, Union[str, int, bool, float, date, datetime]]): list of column inputs.

        Returns:
            List[BaseColumnExpression]: list of validated and processed columns.
        """

        cols = super().validate_source_columns(columns)

        if self._is_self_join and not all(self._extra_self_join_condition(c) for c in cols):
            problems = [c for c in cols if not self._extra_self_join_condition(c)]
            problems_repr = "\n\n".join(repr(p) for p in problems)
            raise ValueError(
                f"All columns must be prefixed in a self-join table op expression.\n"
                f"You should build table expressions from columns on the alias table objects supplied to the join.\n"
                f"There were {len(problems)} unprefixed columns/expressions that contain unprefixed columns:\n"
                + indent_str(problems_repr)
            )

        input_cols = []
        for i, col in enumerate(cols):
            processed = self.apply_prefix(col)
            col_hash = hash(processed)

            if col_hash in self._duplicates_aliases.keys():
                # If column corresponds to an aliased duplicate from when the table was built,
                # replace with the aliased column
                processed = self._duplicates_aliases[col_hash]
                input_cols.append(processed)
            else:
                # No duplicate yet, add column with the required prefix
                input_cols.append(processed)

        return input_cols

    def with_alias(self, alias: str) -> 'AliasedTable':
        raise ValueError("Can't alias a join. You may want to convert to a table variable instead.")
