import unittest

from lumipy.query.expression.sql_value_type import SqlValType
from test.test_utils import get_table_field_test_data, assert_locked_lockable
from lumipy.navigation.field_definition import FieldDefinition
from lumipy.common.string_utils import sql_str_to_name
import pandas as pd


class TestFieldDescription(unittest.TestCase):

    def setUp(self) -> None:
        self.table_field_df = get_table_field_test_data()
        self.table_field_df = self.table_field_df[
            ~self.table_field_df.FieldName.isna()
        ].where(pd.notnull(self.table_field_df), None)

    def test_field_description_construction_from_df_rows(self):
        for _, row in self.table_field_df.iterrows():
            f_description = FieldDefinition.from_row(row)
            self.assertEqual(sql_str_to_name(row.FieldName), f_description.get_name())
            self.assertEqual(row.FieldName, f_description.field_name)
            self.assertEqual(row.DataType, f_description.data_type.name)
            self.assertEqual(row.DataType, f_description.get_type().name)
            self.assertEqual(row.FieldType, f_description.field_type)
            self.assertEqual(row.IsPrimaryKey, f_description.is_primary_key)
            self.assertEqual(row.IsMain, f_description.is_main)
            self.assertEqual(row.Description, f_description.description)
            self.assertEqual(row.ParamDefaultValue, f_description.param_default_value)
            self.assertEqual(row.TableParamColumns, f_description.table_param_columns)

    def test_field_description_construction_via_init(self):
        f_description = FieldDefinition(
            table_name="TableName",
            field_name="FieldName",
            data_type=SqlValType.Boolean,
            field_type='Column',
            is_primary_key=True,
            is_main=True,
            description="A description for the field.",
            param_default_value=None,
            table_param_columns=None
        )
        self.assertEqual(f_description.table_name, "TableName")
        self.assertEqual(f_description.field_name, "FieldName")
        self.assertEqual(f_description.data_type, SqlValType.Boolean)
        self.assertEqual(f_description.get_type(), SqlValType.Boolean)
        self.assertEqual(f_description.field_type, 'Column')
        self.assertEqual(f_description.is_primary_key, True)
        self.assertEqual(f_description.is_main, True)
        self.assertEqual(f_description.description, "A description for the field.")
        self.assertEqual(f_description.param_default_value, None)
        self.assertEqual(f_description.table_param_columns, None)
        self.assertEqual(f_description.get_name(), "field_name")

    def test_field_description_construction_via_init_name_override(self):
        f_description = FieldDefinition(
            table_name="TableName",
            field_name="FieldName",
            data_type=SqlValType.Boolean,
            field_type='Column',
            is_primary_key=True,
            is_main=True,
            description="A description for the field.",
            param_default_value=None,
            table_param_columns=None,
            name_override="another_field_name"
        )
        self.assertEqual(f_description.table_name, "TableName")
        self.assertEqual(f_description.field_name, "FieldName")
        self.assertEqual(f_description.data_type, SqlValType.Boolean)
        self.assertEqual(f_description.get_type(), SqlValType.Boolean)
        self.assertEqual(f_description.field_type, 'Column')
        self.assertEqual(f_description.is_primary_key, True)
        self.assertEqual(f_description.is_main, True)
        self.assertEqual(f_description.description, "A description for the field.")
        self.assertEqual(f_description.param_default_value, None)
        self.assertEqual(f_description.table_param_columns, None)
        self.assertEqual(f_description.get_name(), "another_field_name")

    def test_field_description_construction_via_init_name_override_validation(self):
        with self.assertRaises(ValueError):
            FieldDefinition(
                table_name="TableName",
                field_name="FieldName",
                data_type=SqlValType.Boolean,
                field_type='Column',
                is_primary_key=True,
                is_main=True,
                description="A description for the field.",
                param_default_value=None,
                table_param_columns=None,
                name_override="another-field-name"
            )
        with self.assertRaises(ValueError):
            FieldDefinition(
                table_name="TableName",
                field_name="FieldName",
                data_type=SqlValType.Boolean,
                field_type='Column',
                is_primary_key=True,
                is_main=True,
                description="A description for the field.",
                param_default_value=None,
                table_param_columns=None,
                name_override="0name"
            )
        with self.assertRaises(ValueError):
            FieldDefinition(
                table_name="TableName",
                field_name="FieldName",
                data_type=SqlValType.Boolean,
                field_type='Column',
                is_primary_key=True,
                is_main=True,
                description="A description for the field.",
                param_default_value=None,
                table_param_columns=None,
                name_override="_name"
            )

    def test_field_description_is_immutable(self):
        for _, row in self.table_field_df.iterrows():
            f_description = FieldDefinition.from_row(row)
            assert_locked_lockable(self, f_description)
