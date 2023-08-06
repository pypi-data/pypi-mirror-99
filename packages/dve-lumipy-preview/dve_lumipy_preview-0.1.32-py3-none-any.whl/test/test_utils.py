from lumipy.navigation.atlas import Atlas
import pandas as pd
import os

from lumipy.navigation.field_definition import FieldDefinition
from lumipy.navigation.provider_definition import ProviderDefinition


def get_table_field_test_data():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = file_dir + '/data/'
    return pd.read_csv(
        test_data_dir + 'table_field_catalog.csv',
        index_col=0
    )


def get_entitlement_res_test_data():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_dir = file_dir + '/data/'
    return pd.read_csv(
        test_data_dir + 'entitlement_resources_catalog.csv',
        keep_default_na=False,
        index_col=0
    )


def make_test_atlas():
    table_field = get_table_field_test_data()
    table_field = table_field[~table_field.FieldName.isna()]
    entitlement_resources = get_entitlement_res_test_data()

    providers_df = entitlement_resources[
        entitlement_resources.Type.apply(
            lambda x: x in ['DataProvider']
        )
    ]

    dummy_client = "dummy client"

    provider_descriptions = []
    for _, p_row in providers_df.iterrows():
        fields_df = table_field[table_field['TableName'] == p_row.Name]
        fields = [FieldDefinition.from_row(row) for _, row in fields_df.iterrows()]

        if len(fields) == 0:
            continue

        provider = ProviderDefinition(
                table_name=p_row.Name,
                description=p_row.Description,
                provider_type=p_row.Type,
                category=p_row.Category,
                last_ping_at=p_row.LastPingAt,
                documentation=p_row.DocumentationLink,
                fields=fields,
                client=dummy_client
            )

        provider_descriptions.append(provider)

    return Atlas(
        provider_descriptions
    )


def assert_locked_lockable(test_case, instance):

    from lumipy.common.lockable import Lockable
    test_case.assertTrue(issubclass(type(instance), Lockable))

    with test_case.assertRaises(TypeError) as ar:
        instance.new_attribute = 'some new attribute'
    e = str(ar.exception)

    str1 = "Can't change attributes on "
    str2 = "they are immutable."
    test_case.assertTrue(str1 in e)
    test_case.assertTrue(str2 in e)

    test_case.assertFalse(hasattr(instance, 'new_attribute'))


def standardise_sql_string(sql_str):
    return " ".join(sql_str.split())
