import datetime

items = [
    {"id": 1, "name": "Apple", "created_on": datetime.datetime.utcnow,
        "description": """
            the round fruit of a tree of the rose family,
             which typically has thin red or green skin and crisp flesh.
             Many varieties have been developed as dessert or
             cooking fruit or for making c"id"er.
        """, "user_id": 1, "category_id": 1},
    {"id": 2, "name": "Banana", "created_on": datetime.datetime.utcnow,
        "description": """
            the tropical and subtropical treelike plant that bears this fruit.
             It has very large leaves and resembles a palm, but lacks a woody
             trunk.
        """, "user_id": 2, "category_id": 1}
]

item = {
    "id": 3, "name": "Coconut", "created_on": datetime.datetime.utcnow,
    "description": """
        the large, oval, brown seed of a tropical palm, consisting of a hard
         shell lined with edible white flesh and containing a clear liqu"id".
         It grows ins"id"e a woody husk, surrounded by fiber.
    """, "user_id": 3, "category_id": 1
}

categories = [
    {"id": 1, "name": "Fruits", "created_on": datetime.datetime.utcnow,
        "description": """
            the sweet and fleshy product of a tree or other plant that contains
             seed and can be eaten as food.
        """, "user_id": 1},
    {"id": 2, "name": "Seafood", "created_on": datetime.datetime.utcnow,
        "description": """
            shellfish and sea fish, served as food.
        """, "user_id": 2},
    {"id": 3, "name": "Dairy", "created_on": datetime.datetime.utcnow,
        "description": """
            containing or made from milk.
        """, "user_id": 3}
]

category = {
    "id": 4, "name": "Appliances", "created_on": datetime.datetime.utcnow,
    "description": """
        devices or equipment designed to perform a specific task,
         typically a domestic one.
    """, "user_id": 4
}
