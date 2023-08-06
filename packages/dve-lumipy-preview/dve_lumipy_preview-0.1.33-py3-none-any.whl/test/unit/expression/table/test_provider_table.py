import unittest

from lumipy.query.expression.column.source_column import SourceColumn
from lumipy.query.expression.sql_value_type import SqlValType
from lumipy.query.expression.table.provider_class_factory import ProviderClassFactory
from test.test_utils import make_test_atlas, assert_locked_lockable
from lumipy.query.expression.column.column_literal import LiteralColumn
from lumipy.query.expression.table.table_alias import AliasedTable

from datetime import datetime
from decimal import Decimal


class TestProviderClasses(unittest.TestCase):

    def setUp(self) -> None:

        self.atlas = make_test_atlas()

    def test_provider_instance_ctor(self):

        def generate_params_input(p_descr):

            params = p_descr.list_parameters()
            out_dict = {}
            for p in params:
                if p.get_type() == SqlValType.Int:
                    out_dict[p.name] = 123
                elif p.get_type() == SqlValType.Double:
                    out_dict[p.name] = 123.456
                elif p.get_type() == SqlValType.Date or p.get_type() == SqlValType.DateTime:
                    out_dict[p.name] = datetime(2020, 1, 1)
                elif p.get_type() == SqlValType.Boolean:
                    out_dict[p.name] = True
                elif p.get_type() == SqlValType.Text:
                    out_dict[p.name] = 'TESTING'
                elif p.get_type() == SqlValType.Decimal:
                    out_dict[p.name] = Decimal(10000)
                else:
                    raise ValueError(f"{p.name}: {p.get_type()}")
            return out_dict

        for provider_description in self.atlas.list_providers():

            cls = ProviderClassFactory(provider_description)

            if any(p.get_type() == SqlValType.Table for p in provider_description.list_parameters()):
                # Just test ctors that take scalar values
                continue

            param_input = generate_params_input(provider_description)

            inst = cls(**param_input)
            for k, v in param_input.items():
                # Assert that the value is contained inside the param assignment

                # In this case it's in a Literal expression object so it's further down the lineage
                param_val = inst._param_assignments[k]._lineage[1]
                literal_v = LiteralColumn(v)
                self.assertEqual(
                    param_val.get_sql(),
                    literal_v.get_sql(),
                    msg=f"Value for parameter {k} not found in {cls.__name__} test instance."
                )

            # Instances of the class should be immutable
            assert_locked_lockable(self, cls())

    def test_provider_instance_columns(self):

        for provider_description in self.atlas.list_providers():
            # When we make an instance (provider class) of the metaclass
            cls = ProviderClassFactory(provider_description)
            # When make an instance of the provider class
            inst = cls()

            # There should be the full set of columns on the instance
            self.assertEqual(len(inst.get_columns()), len(provider_description.list_columns()))

            # The columns should be available on the instance as class attributes of type SourceColumn
            for col in provider_description.list_columns():
                self.assertTrue(
                    hasattr(inst, col.name),
                    msg=f"Column {col.name} not found as field on {cls.__name__} test instance."
                )
                # They should be column types
                col_attr = getattr(inst, col.name)
                self.assertTrue(
                    isinstance(col_attr, SourceColumn),
                    msg=f'Column attached to test instance of {cls.__name__} was '
                        f'not a Column but was {type(col_attr).__name__}.'
                )

                # Column belonging to source table should have a source_table_hash that matches the source table
                self.assertEqual(hash(inst), col_attr.source_table_hash())

    def test_provider_with_alias(self):

        for provider_description in self.atlas.list_providers():
            # When we make an instance (provider class) of the metaclass
            cls = ProviderClassFactory(provider_description)
            # When make an instance of the provider class
            inst = cls()
            lhs_inst = inst.with_alias("LHS")

            # Should be an alias table type and have 'as LHS' in its from argument
            self.assertTrue(isinstance(lhs_inst, AliasedTable))
            self.assertEqual(lhs_inst.get_from_arg_string(), f"{inst.get_from_arg_string()} as LHS")

    def test_provider_wrong_params_failure(self):
        p_description = self.atlas.lusid_logs_apprequest
        cls = p_description.get_class()

        with self.assertRaises(ValueError) as ve:
            cls(planet='Arrakis')

        msg = str(ve.exception)

        self.assertIn("'planet' is not a parameter", msg)
        self.assertIn(p_description.get_table_name().replace('.', ''), msg)
        for param in p_description.list_parameters():
            self.assertIn(param.get_name(), msg)

    def test_provider_table_valued_parameter(self):

        branch_def = self.atlas.dev_gitlab_branch
        branch_commit_def = self.atlas.dev_gitlab_branchcommit

        # Create table var for input parameter
        branches = branch_def.get_class()()
        l_branches = branches.select(
            branches.project_id,
            branches.project_name,
            BranchName=branches.name
        ).where(
            branches.project_name.like('lusid-p%') &
            (branches.name != 'master')
        ).order_by(branches.name.ascending()).limit(3).to_table_var('branches')

        # Try to use it in a provider class
        BranchCommit = branch_commit_def.get_class()
        commits = BranchCommit(projects_and_branches=l_branches)

        qry_sql = commits.select('*').get_sql()
        # Table var should be set
        self.assertIn('@branches = ', qry_sql)
        # Table var should show up in where to set the ProjectsAndBranches parameter
        self.assertIn('[ProjectsAndBranches] = @branches', qry_sql)
