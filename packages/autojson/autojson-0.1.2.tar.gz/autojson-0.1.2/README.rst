========
Overview
========

By defining a Python class, you can define a JSON format.
There is no need to define your own JSON parser.
You can convert JSON to Python classes with a short code and support the type hints available in vscode's Pylance extension.
Here's an example of it.


.. code-block:: python

    import json
    from autojson import Object, Array, Int, Float, Boolean, String

    # JSON file
    txt = """
    {
        "name": "config",
        "threshold": 0.5,
        "flag": true,
        "rectangles": [
            {
                "left": 0,
                "top": 0,
                "width": 100,
                "height": 200
            },
            {
                "left": 100,
                "top": 100,
                "width": 100,
                "height": 200
            }
        ],
        "area": [
            [0, 0],
            [1920, 0],
            [1920, 1080],
            [0, 1080]
        ]
    }
    """

    # define your JSON format
    class Rectangle(Object):
        left = Int()
        top = Int()
        width = Int()
        height = Int()
        right: int
        bottom: int

        def __autojson_init__(self):
            self.right = self.left + self.width
            self.bottom = self.top + self.height

        @property
        def ltwh(self):
            return self.left, self.top, self.width, self.height

        @property
        def ltrb(self):
            return self.left, self.top, self.right, self.bottom


    class Config(Object):
        name = String()
        threshold = Float()
        flag = Boolean()
        rectangles = Array(Rectangle())
        area = Array(Array(Int(), size=2))


    # load JSON to your class
    config = Config().parse_json(json.loads(txt))
    # To change parameter
    config.threshold = Float(0.7)
    # or
    config["threshold"] = Float(0.3)

    for rectangle in config.rectangles:
        print("ltrb", rectangle.ltrb)
        print("ltwh", rectangle.ltwh)

    # if you don't have json template, create the template
    print(json.dumps(Config().get_default_json()))
    # Object is subclass of dict
    # so you can save it as json


=======
Classes
=======

This module provides six classes: Object, Array, Int, Float, Boolean, and String.


Int
===

Int is a subclass of int, with additional methods for JSON, but it behaves the same as int.


Float
=====

Float is a subclass of float, with additional methods for JSON, but it behaves the same as float.


Boolean
=======

Boolean is NOT a subclass of bool, with additional methods for JSON, but it behaves the same as bool.
However, it will not work correctly for the is operator.
Also, if you assign a value to a variable annotated as a bool type, an error message will be displayed,
so please use bool() or Boolean.value when assigning.


String
======

String is a subclass of str, with additional methods for JSON, but it behaves the same as str.


Array
=====

Array is a subclass of list, with additional methods for JSON, but it behaves the same as list.
However, since `__init__` is overridden, the constructor behaves differently from list.
It is always generated as an empty list.


Object
======

Object is a subclass of dict, with additional methods for JSON, but it behaves the same as dict.
This class is assumed to be inherited. As shown in the sample above, you can use this class by specifying instances of these five classes in the class variables of the class that inherits from it.
The combination of these instances will be the definition of JSON.


=======
Methods
=======

All classes are defined as subclasses of the AutoJson class.
Any class that inherits from it will always have two instance methods defined.


get_default_json
================

It can be used to create a template for a JSON file when the JSON file is not trivial.
The return value is equivalent to json.loads, but int is replaced with Int, float with Float, str with String, list with Array, and dict with Object.


parse_json
==========

It takes the result of parsing with json.load and returns the defined class with the attributes properly defined.


===============
Special Methods
===============


`__autojson_init__`
===================

This is only valid for the Object class.
Initialization functions that can be added by the user.
It does not accept any arguments, but allows the user to add code that will be executed after being initialized by parse_json.
It is used to modify the information read from the file.
