import sys
# sys.path.insert(0, "D:/UC/cloudofficeprint-python")
sys.path.insert(0, "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python")
import cloudofficeprint as cop


def test_for_each():
    """Also serves as the tests for Labels, ForEachSlide, ForEachInline, ForEachHorizontal and ForEachTableRow. """
    element1 = cop.elements.ElementCollection.from_mapping(
        {
            'a': 1,
            'b': 2,
            'c': 3
        }
    )
    element2 = cop.elements.ElementCollection.from_mapping(
        {
            'a': 4,
            'b': 5,
            'c': 6
        }
    )
    loop = cop.elements.ForEach(
        name='loop_name',
        content=(element1, element2)
    )
    loop_expected = {
        'loop_name': [
            {
                'a': 1,
                'b': 2,
                'c': 3
            },
            {
                'a': 4,
                'b': 5,
                'c': 6
            },
        ]
    }
    assert loop.as_dict == loop_expected


def test_for_each_sheet():
    element1 = cop.elements.ElementCollection.from_mapping(
        {
            "sheet_name": "John Dulles",
            "sheet_dynamic_print_area": True,
            "cust_first_name": "John",
            "cust_last_name": "Dulles",
            "cust_city": "Sterling",
            "orders": [
                {
                    "order_total": 2380,
                    "order_name": "Order 1",
                    "product": [
                        {
                            "product_name": "Business Shirt",
                            "quantity": 3,
                            "unit_price": 50
                        },
                        {
                            "product_name": "Trousers",
                            "quantity": 3,
                            "unit_price": 80
                        },
                        {
                            "product_name": "Jacket",
                            "quantity": 3,
                            "unit_price": 150
                        }
                    ]
                }
            ]
        }
    )
    element2 = cop.elements.ElementCollection.from_mapping(
        {
            "sheet_name": "William Hartsfield",
            "cust_first_name": "William",
            "cust_last_name": "Hartsfield",
            "cust_city": "Atlanta",
            "orders": [
                {
                    "order_total": 1640,
                    "order_name": "Order 1",
                    "product": [
                        {
                            "product_name": "Blouse",
                            "quantity": 4,
                            "unit_price": 60
                        },
                        {
                            "product_name": "Skirt",
                            "quantity": 4,
                            "unit_price": 80
                        }
                    ]
                },
                {
                    "order_total": 730,
                    "order_name": "Order 2",
                    "product": [
                        {
                            "product_name": "Blouse",
                            "quantity": 4,
                            "unit_price": 60
                        }
                    ]
                }
            ]
        }
    )
    loop1 = cop.elements.ForEachSheet(
        name='customers',
        content=(element1, element2)
    )

    element1 = cop.elements.ElementCollection.from_mapping(
        {
            "sheet_dynamic_print_area": True,
            "cust_first_name": "John",
            "cust_last_name": "Dulles",
            "cust_city": "Sterling",
            "orders": [
                {
                    "order_total": 2380,
                    "order_name": "Order 1",
                    "product": [
                        {
                            "product_name": "Business Shirt",
                            "quantity": 3,
                            "unit_price": 50
                        },
                        {
                            "product_name": "Trousers",
                            "quantity": 3,
                            "unit_price": 80
                        },
                        {
                            "product_name": "Jacket",
                            "quantity": 3,
                            "unit_price": 150
                        }
                    ]
                }
            ]
        }
    )
    element2 = cop.elements.ElementCollection.from_mapping(
        {
            "cust_first_name": "William",
            "cust_last_name": "Hartsfield",
            "cust_city": "Atlanta",
            "orders": [
                {
                    "order_total": 1640,
                    "order_name": "Order 1",
                    "product": [
                        {
                            "product_name": "Blouse",
                            "quantity": 4,
                            "unit_price": 60
                        },
                        {
                            "product_name": "Skirt",
                            "quantity": 4,
                            "unit_price": 80
                        }
                    ]
                },
                {
                    "order_total": 730,
                    "order_name": "Order 2",
                    "product": [
                        {
                            "product_name": "Blouse",
                            "quantity": 4,
                            "unit_price": 60
                        }
                    ]
                }
            ]
        }
    )
    loop2 = cop.elements.ForEachSheet(
        name='customers',
        content={
            'John Dulles': element1,
            'William Hartsfield': element2
        }
    )

    loop_expected = {
        "customers": [
            {
                "sheet_name": "John Dulles",
                "sheet_dynamic_print_area": True,
                "cust_first_name": "John",
                "cust_last_name": "Dulles",
                "cust_city": "Sterling",
                "orders": [
                    {
                        "order_total": 2380,
                        "order_name": "Order 1",
                        "product": [
                            {
                                "product_name": "Business Shirt",
                                "quantity": 3,
                                "unit_price": 50
                            },
                            {
                                "product_name": "Trousers",
                                "quantity": 3,
                                "unit_price": 80
                            },
                            {
                                "product_name": "Jacket",
                                "quantity": 3,
                                "unit_price": 150
                            }
                        ]
                    }
                ]
            },
            {
                "sheet_name": "William Hartsfield",
                "cust_first_name": "William",
                "cust_last_name": "Hartsfield",
                "cust_city": "Atlanta",
                "orders": [
                    {
                        "order_total": 1640,
                        "order_name": "Order 1",
                        "product": [
                            {
                                "product_name": "Blouse",
                                "quantity": 4,
                                "unit_price": 60
                            },
                            {
                                "product_name": "Skirt",
                                "quantity": 4,
                                "unit_price": 80
                            }
                        ]
                    },
                    {
                        "order_total": 730,
                        "order_name": "Order 2",
                        "product": [
                            {
                                "product_name": "Blouse",
                                "quantity": 4,
                                "unit_price": 60
                            }
                        ]
                    }
                ]
            }
        ]
    }
    assert loop1.as_dict == loop_expected
    assert loop2.as_dict == loop_expected


def test_for_each_merge_cells():
    element1 = cop.elements.ElementCollection.from_mapping(
        {
            "department": "Engineering",
            "employees": [
                {
                    "name": "John Smith",
                    "project": "Website Redesign",
                    "status": "In Progress"
                },
                {
                    "name": "Emily Johnson",
                    "project": "API Development",
                    "status": "Completed"
                },
                {
                    "name": "Michael Brown",
                    "project": "Mobile App",
                    "status": "Planning"
                }
            ]
        }
    )
    element2 = cop.elements.ElementCollection.from_mapping(
        {
            "department": "Marketing",
            "employees": [
                {
                    "name": "Sarah Wilson",
                    "project": "Brand Campaign",
                    "status": "In Progress"
                },
                {
                    "name": "David Thompson",
                    "project": "Market Research",
                    "status": "Not Started"
                }
            ]
        }
    )
    loop = cop.elements.ForEachMergeCells(
        name='departments',
        content=(element1, element2)
    )

    expected = {
        "departments": [
            {
                "department": "Engineering",
                "employees": [
                    {
                        "name": "John Smith",
                        "project": "Website Redesign",
                        "status": "In Progress"
                    },
                    {
                        "name": "Emily Johnson",
                        "project": "API Development",
                        "status": "Completed"
                    },
                    {
                        "name": "Michael Brown",
                        "project": "Mobile App",
                        "status": "Planning"
                    }
                ]
            },
            {
                "department": "Marketing",
                "employees": [
                    {
                        "name": "Sarah Wilson",
                        "project": "Brand Campaign",
                        "status": "In Progress"
                    },
                    {
                        "name": "David Thompson",
                        "project": "Market Research",
                        "status": "Not Started"
                    }
                ]
            }
        ]
    }

    assert loop.as_dict == expected

def run():
    test_for_each()
    test_for_each_sheet()
    test_for_each_merge_cells()


if __name__ == '__main__':
    run()
