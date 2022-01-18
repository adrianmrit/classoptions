# classoptions
## Description
Implement namespaced and inheritable metadata at the class level.

Inspired on Meta classes from Django and Django Rest Framework.

## Quick Start
### Installation
`pip install classoptions`

### Simple inheritance
In the example, `DefaultInfo` holds metadata that is inherited by subclasses, while `Info` holds
class specific metadata.
```python
from classoptions import get_options_metaclass
EmployeesInfoMetaclass = get_options_metaclass("EmployeesInfoMetaclass", "Info", "DefaultInfo")

class Pizza(metaclass=EmployeesInfoMetaclass):
    class DefaultInfo:
        client_can_modify = True
        notes = None

    cooking_temp = 400
    cooking_time = 1    

class HawaiianPizza(Pizza):
    ingredients = ["cheese", "ham", "pineapple"]
    
    class Info:
        notes = "Do not judge the costumer."
        private_note = "If planning a party, ask first if people like it."
        
print("Hawaiian Pizza:")
print("Ingredients:", ", ".join(HawaiianPizza.ingredients))
print("Cooking Temperature (F):", HawaiianPizza.cooking_temp)
print("Cooking Time (hours):", HawaiianPizza.cooking_time)
print("Client can modify:", HawaiianPizza.Info.client_can_modify)
print("Notes:")
print(HawaiianPizza.Info.notes)
print("Private Note:")
print(HawaiianPizza.Info.private_note)
```
#### Output:
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
from classoptions import get_options_metaclass
OptionsMetaclass = get_options_metaclass("OptionsMetaclass", "Options", "DefaultOptions")

class A(metaclass=OptionsMetaclass):
    class DefaultOptions:
        color = "red"
        size = 2
        hello = "world"
        i_like_pizza = True

class B(A):
    class DefaultOptions:
        color = "blue"
        size = 3

class C(B):
    class Options:
        size = 4  # Specific to C only

class D(A):
    class DefaultOptions:
        color = "black"
        hello = "country"

class E(D, C):
    class Options:
        i_like_hawaiian_pizza = "maybe"

print("E custom options")
print("i_like_hawaiian_pizza:", E.Options.i_like_hawaiian_pizza)

print("\nInherited from B")
print("size:", E.Options.size)

print("\nInherited from D")
print("color:", E.Options.color)
print("hello:", E.Options.hello)

print("\nInherited from A")
print("i_like_pizza:", E.Options.i_like_pizza)
```

#### Output:
```text
E custom options
i_like_hawaiian_pizza: maybe

Inherited from B
size: 3

Inherited from D
color: black
hello: country

Inherited from A
i_like_pizza: True
```

## License
MIT License.