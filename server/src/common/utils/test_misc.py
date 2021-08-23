from .misc import filter_item_properties


items = [
    {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3',
        'key4': 'value4',
    }
]


def test_filter_item_properties() -> None:
    assert filter_item_properties(items, ['key1', 'key3']) == [
        {
            'key1': 'value1',
            'key3': 'value3',
        }
    ]
