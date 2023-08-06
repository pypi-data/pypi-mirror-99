import unittest

import pandas as pd

from lumipy.common.string_utils import handle_available_string
from lumipy.navigation.field_definition import FieldDefinition
from lumipy.navigation.provider_definition import ProviderDefinition
from test.test_utils import get_table_field_test_data, get_entitlement_res_test_data


class TestProviderDescription(unittest.TestCase):

    def setUp(self) -> None:
        self.table_field_df = get_table_field_test_data()
        self.table_field_df = self.table_field_df[
            ~self.table_field_df.FieldName.isna()
        ].where(pd.notnull(self.table_field_df), None)

        self.entitlement_res_df = get_entitlement_res_test_data()
        self.providers_df = self.entitlement_res_df[
            self.entitlement_res_df.Type.apply(
                lambda x: x in ['DataProvider']
            )
        ]

    def test_provider_description_construction(self):

        for _, p_row in self.providers_df.iterrows():

            fields_df = self.table_field_df[self.table_field_df.TableName == p_row.Name]
            fields = [FieldDefinition.from_row(row) for _, row in fields_df.iterrows()]

            provider = ProviderDefinition(
                table_name=p_row.Name,
                description=p_row.Description,
                provider_type=p_row.Type,
                category=p_row.Category,
                last_ping_at=p_row.LastPingAt,
                documentation=p_row.DocumentationLink,
                fields=fields,
                client="dummy client value"
            )

            self.assertEqual(len(provider.list_fields()), len(fields))
            self.assertEqual(len(provider.list_columns()), len([f for f in fields if f.field_type == 'Column']))
            self.assertEqual(len(provider.list_parameters()), len([f for f in fields if f.field_type == 'Parameter']))

            self.assertEqual(provider.get_name(), p_row.Name.replace('.', '_').lower())
            self.assertEqual(provider._client, "dummy client value")
            self.assertEqual(provider.get_table_name(), p_row.Name)
            self.assertEqual(provider._description, handle_available_string(p_row.Description))
            self.assertEqual(provider._provider_type, p_row.Type)
            self.assertEqual(provider._category, p_row.Category)
            self.assertEqual(provider._last_ping_at, p_row.LastPingAt)
            self.assertEqual(provider._documentation, handle_available_string(p_row.DocumentationLink))

            provider_str = str(provider)
            for field in fields:
                self.assertIn(field.get_name(), provider_str)
                self.assertTrue(hasattr(provider, field.get_name()))
