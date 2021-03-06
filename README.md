## Description
Implement namespaced and inheritable metadata at the class level.

Inspired on Meta classes from Django models and Django Rest Framework model serializers.

## Quick Start
### Installation
`pip install classoptions`

### Simple inheritance
```python
from classoptions import ClassOptionsMetaclass
from typing import Any

class Pizza(metaclass=ClassOptionsMetaclass):
    _meta: Any
    
    class DefaultMeta:
        client_can_modify = True
        notes = None

    cooking_temp = 400
    cooking_time = 1    

class HawaiianPizza(Pizza):
    ingredients = ["cheese", "ham", "pineapple"]
    
    class Meta:
        notes = "Do not judge the costumer."
        private_note = "If planning a party, ask first if people like it."
        
print("Hawaiian Pizza:")
print("Ingredients:", ", ".join(HawaiianPizza.ingredients))
print("Cooking Temperature (F):", HawaiianPizza.cooking_temp)
print("Cooking Time (hours):", HawaiianPizza.cooking_time)
print("Client can modify:", HawaiianPizza._meta.client_can_modify)
print("Notes:")
print(HawaiianPizza._meta.notes)
print("Private Note:")
print(HawaiianPizza._meta.private_note)
```
Outputs:
```text
Hawaiian Pizza:
Ingredients: cheese, ham, pineapple
Cooking Temperature (F): 400
Cooking Time (hours): 1
Client can modify: True
Notes:
Do not judge the costumer.
Private Note:
If planning a party, ask first if people like it.
```

### Multiple Inheritance
Works similar to python inheritance, except we don't need to explicitly inherit from the parent class.

```python
from classoptions import ClassOptionsMetaclass
from typing import Any

class A(metaclass=ClassOptionsMetaclass):
    _meta: Any
    class DefaultMeta:
        color = "red"
        size = 2
        hello = "world"
        i_like_pizza = True

class B(A):
    class DefaultMeta:
        color = "blue"
        size = 3

class C(B):
    class Meta:
        size = 4  # Specific to C only

class D(A):
    class DefaultMeta:
        color = "black"
        hello = "country"

class E(D, C):
    class Meta:
        i_like_hawaiian_pizza = "maybe"

print("E custom meta")
print("i_like_hawaiian_pizza:", E._meta.i_like_hawaiian_pizza)

print("\nInherited from B")
print("size:", E._meta.size)

print("\nInherited from D")
print("color:", E._meta.color)
print("hello:", E._meta.hello)

print("\nInherited from A")
print("i_like_pizza:", E._meta.i_like_pizza)
```
Outputs:
```text
E custom meta
i_like_hawaiian_pizza: maybe

Inherited from B
size: 3

Inherited from D
color: black
hello: country

Inherited from A
i_like_pizza: True
```

### Using other class/attribute names
With ``ClassOptionsMetaclass.factory`` you can overwrite how you define default metadata, class specific metadata,
and how you access the result.

```python
from classoptions import ClassOptionsMetaclass
from typing import Any

class A(metaclass=ClassOptionsMetaclass.factory("Options", "DefaultOptions", "_options")):
    _options: Any
    
    class DefaultOptions:
        color = "red"
        size = 2

    cooking_temp = 400
    cooking_time = 1    

class B(A):
    class Options:
        color = "blue"
        
print("B color:", B._options.color)
print("B size:", B._options.size)
```
Outputs:
```text
B color: blue
B size: 2
```

## License
MIT License.