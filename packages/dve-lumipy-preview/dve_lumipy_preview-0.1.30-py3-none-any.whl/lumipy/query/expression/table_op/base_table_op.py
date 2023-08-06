from abc import abstractmethod

from pandas import DataFrame

from IPython.core.display import clear_output

from lumipy.query.expression.base_expression import BaseExpression
from lumipy.query.expression.column.column_base import BaseColumnExpression
from lumipy.query.expression.table.base_table import BaseTable
from lumipy.common.ipython_utils import live_status_in_cell
from lumipy.common.string_utils import pretty_sql
from lumipy.client import Client

import networkx as nx

from typing import List, Union

from lumipy.query.expression.variable.base_variable import BaseVariable


class BaseTableExpression(BaseTable):
    """Base class for all expression that represent an operation on a whole table that resolves to another table
    such as 'select' or 'where' and resolves to valid SQL that can be sent off to Luminesce using the .go() method.

    Each table expression will manifest the columns it contains as public members as it inherits from BaseTable.

    All table expressions are built to support building up SQL table ops via method chaining. The design is that one
    starts with a source table (inheritor of BaseSourceTable class) and then chains table operation expressions
    (BaseTableExpression) of it and later child table operation expressions.
    Each table expression needs to pass along the source table it relates back to, the web client, the select type of
    the initial select statement (distinct or not) and it's immediate table expression ancestor (parent).

    Inheritors must implement the following methods:
        get_table_sql(self) -> str: function that builds the SQL string that the table expression resolves to
        (but not the @/@@ var assignment SQL)
        make_copy_with_auto_alias_cols(self) -> type(self): function that creates a version of the table expression
        where the columns that are functions of columns are automatically aliased. This is for when the expression is
        converted to an @ var (table variable).

    """

    @abstractmethod
    def __init__(
            self,
            columns: List[BaseColumnExpression],
            client: Client,
            table_op_name: str,
            select_type: Union[str, None],
            source_table: 'BaseSourceTable',
            parent_arg: BaseExpression,
            *args: BaseExpression
    ):
        """__init__ method of the BaseTableExpression class.
        
        Args:
            columns (List[BaseColumnExpression]): list of columns that are members of the table expression
            client (Client): web api client for sending query requests off to.
            table_op_name (str): name labelling the table op this class represents.
            select_type (str): the select type of the expression (whether select/select distinct is in the lineage)
            source_table (BaseSourceTable): source table of the table expression chain.
            parent_arg (BaseExpression): main parent expression of this table expresion (e.g. select passed into a where
            expression: source_table.select('*').where(...))
            *args (BaseExpression): other expression arguments for the table expression.
        """
        self._source_table = source_table
        self._parent = parent_arg
        self._select_type = select_type

        super().__init__(
            self._source_table.validate_source_columns(columns),
            client,
            table_op_name,
            parent_arg,
            *args
        )

    def get_select_type(self) -> str:
        """Get the select type string ('select' or 'select distinct')

        Returns:
            str: the select type
        """
        return self._select_type

    @abstractmethod
    def get_table_sql(self) -> str:
        """Get the SQL string for the table expression only. Not including the @/@@ var assignments.

        Returns:
            str: the table SQL string.
        """
        raise NotImplementedError

    def variable_sql(self) -> str:
        """Construct the SQL string that does the assignment of Luminesce @/@@ variables.

        Returns:
            str: the assignment SQL string for all of the @/@@ vars this expression depends on.
        """
        if self.get_at_var_dependencies() is not None and len(self.get_at_var_dependencies()) > 0:
            # Sort the dependencies by whether they depend on another
            dependencies = self._resolve_at_var_dependency_order()
            return '\n\n'.join(s.get_assignment_sql() for s in dependencies) + '\n\n'
        else:
            return ''

    def get_sql(self) -> str:
        """Return the SQL string that this expression resolves to.

        Returns:
            str: the SQL string.
        """
        return pretty_sql(f"{self.variable_sql()}{self.get_table_sql()}")

    def print_sql(self):
        """Print the SQL that this expression resolves to.

        """
        print(self.get_sql())

    def _resolve_at_var_dependency_order(self) -> List[BaseVariable]:
        """Resolve the dependency order of the @/@@ variables that this table expression requires.

        Table expressions can depend on @/@@ variables that in turn depend on @/@@ variables and so on. An @ variable
        that depends on another can't be above the one it depends on in the final SQL query string to Luminesce. This
        method constructs a directed acyclic graph in networkx (a graph analytics package) that represents these
        dependencies. Functionality in networkx is then used to count how many descendents each @/@@ var has and
        then the vars are returned as a list ordered by this number. The ones with most descendents are the ones with
        the most dependencies and they can be put at the top, and so on.

        Returns:
            List[BaseVariable]: list of @/@@ variable expressions ordered by dependency.
        """

        # Construct the DAG
        at_var_to_label = {at_var: i for i, at_var in enumerate(self.get_at_var_dependencies())}
        dag = nx.DiGraph()
        for at_var, i in at_var_to_label.items():
            dag.add_node(i, at_var=at_var)

        for at_var in at_var_to_label.keys():
            for dep in at_var.get_at_var_dependencies():
                u = at_var_to_label[dep]
                v = at_var_to_label[at_var]
                dag.add_edge(u, v)

        dag = nx.relabel.relabel_nodes(dag, {i: at_var.get_sql() for at_var, i in at_var_to_label.items()})

        # Count descendents and create sorted list
        def count_dependencies(n):
            return len(nx.algorithms.dag.descendants(dag, n))

        n_descendants = {n: count_dependencies(n) for n in dag.nodes}
        dependencies = []
        for k in sorted(n_descendants, key=n_descendants.get, reverse=True):
            dependencies.append(dag.nodes[k]['at_var'])

        return dependencies

    def to_scalar_var(self, var_name: str) -> 'ScalarVariable':
        """Build a scalar variable (@@variable) expression from this table expression.

        Args:
            var_name (str): name to give to the scalar variable. Names that conflict with SQL keywords are not allowed
            and will raise an error.

        Returns:
            ScalarVariable: the scalar variable expression built from this table expression.
        """
        from lumipy.query.expression.variable.scalar_variable import ScalarVariable
        # No need to alias this col. Scalar var is effectively doing the same job.
        return ScalarVariable(var_name, self)

    def to_table_var(self, var_name: str) -> 'TableVariable':
        """Build a table variable (@variable) expression from this table expression.

        Args:
            var_name: name to give to the table variable. Names that conflict with SQL keywords are not allowed
            and will raise an error.

        Returns:
            TableVariable: the table variable expression built from this table expression.

        """
        from lumipy.query.expression.variable.table_variable import TableVariable
        return TableVariable(var_name, self)

    def get_source_table(self) -> 'BaseSourceTable':
        """Get the source table expression object that this table expression depends on.

        Returns:
            BaseSourceTable: the source table of this table expression.
        """
        return self._source_table

    def go(self) -> DataFrame:
        """Send query off to Luminesce, monitor progress and then get the result back as a pandas dataframe.

        Returns:
            DataFrame: the result of the query as a pandas dataframe.
        """
        ex_id = 'N/A'
        try:
            ex_id = self._client.start_query(self.get_sql())
            live_status_in_cell(self._client, ex_id)
            df = self._client.get_result(ex_id)
            clear_output(wait=True)
            return df
        except KeyboardInterrupt as ki:
            print("Cancelling query... 💥")
            self._client.delete_query(ex_id)
            raise ki
        except Exception as e:
            raise e

    def go_async(self) -> str:
        """Just send the query to luminesce. Don't monitor progress or fetch result.

        Returns:
            str: the execution ID of the query.
        """
        ex_id = self._client.start_query(self.get_sql())
        print(f"Query running as {ex_id}")
        return ex_id

    def to_drive(self, file_path):
        """Add an expression to the query that saves the result to drive.

        Args:
            file_path: the file path to the save location including the file format. File format is inferred from the
            file_path string (i.e. /A/B/C/file.csv will save as a csv at directory /A/B/C)

        Returns:
            DriveSave: DriveSave instance representing the save to drive expression.
        """

        drive_path = "/".join(file_path.split('/')[:-1]) + '/'
        name = file_path.split('/')[-1].split('.')[0]
        file_type = file_path.split('.')[-1]
        input_tv = self.to_table_var(f'tv_{str(hash(self))[1:]}')

        from lumipy.navigation.drive.save import DriveSave
        return DriveSave(
            drive_path=drive_path,
            client=self.get_client(),
            drive_file_type=file_type,
            **{name: input_tv}
        )

    def to_view(self, view_path: str, commit_message: str):
        """Register this query as a view (like a virtual data provider). Once the query is run it will be
        available as a data provider in the atlas.

        Args:
            view_path (str): string that defines the view path. Must be just alphanumerics and '/'. For example
            A/B/C/MyView will become a view called A.B.C.MyView.
            commit_message (str): commit message describing the creation/update of the view.

        Returns:
            CreateView: CreateView instance representing the query with create view pragma lines at the top.
        """

        from lumipy.query.expression.pragma.view import CreateView
        return CreateView(view_path, commit_message, self)
