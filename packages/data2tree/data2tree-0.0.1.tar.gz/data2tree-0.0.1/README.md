# Tree Builder

> Input

``` python
 lst = [
     {"id": 1, "pid": 0, "name": "Tree - 1"},
     {"id": 2, "pid": 1, "name": "Tree - 1 - 1"},
     {"id": 3, "pid": 1, "name": "Tree - 1 - 2"},
     {"id": 4, "pid": 2, "name": "Tree - 1 - 1- 1"},
     {"id": 5, "pid": 0, "name": "Tree - 2"}
 ]
```

> Usage

``` python
tree = BuildTree(record_key="id", parent_record_key="pid").build_tree(lst)
print(tree)
```

> Notes

| Parameter         | Type   | required | Description      |
| ----------------- | ------ | -------- | ---------------- |
| record_key        | String | True     | record id        |
| parent_record_key | String | True     | parent_record id |

> Output
>

```python
[
    {
        "id": 1,
        "pid": 0,
        "name": "Tree - 1",
        "child": [
            {
                "id": 2,
                "pid": 1,
                "name": "Tree - 1 - 1",
                "child": [
                    {
                        "id": 4,
                        "pid": 2,
                        "name": "Tree - 1 - 1- 1"
                    }]
            },
            {
                "id": 3,
                "pid": 1,
                "name": "Tree - 1 - 2"
            }
        ]
    },
    {
        "id": 5,
        "pid": 0,
        "name": "Tree - 2"
    }
]
```


