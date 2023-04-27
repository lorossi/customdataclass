# Customdataclass Examples

## Basic Dataclass Example

```python
from customdataclass import Dataclass

# define a dataclass
class Person(Dataclass):
    name: str
    age: int

# create an instance
person = Person(name="John", age=42)
# access attributes 
print(person.name, person.age)
# convert to dict
print(person.to_dict)
# convert to string
print(str(person), person, sep="\n")
# convert to json
print(person.to_json)
# convert to json pretty printed
print(person.to_json_pretty)
# convert to yaml (requires PyYAML installed)
print(person.to_yaml)
# convert to toml (requires toml installed)
print(person.to_toml)

# create an instance from a dict
person = Person.from_dict({"name": "John", "age": 42})
# create an instance from a json string
person = Person.from_json('{"name": "John", "age": 42}')
# create an instance from a yaml string (requires PyYAML installed)
person = Person.from_yaml('name: John\nage: 42')
# create an instance from a toml string (requires toml installed)
person = Person.from_toml('name = "John"\nage = 42')
```

## Mutable Dataclass Example

```python
from customdataclass import Dataclass

# define a mutable dataclass
class Employee(Dataclass, mutable=True):
    name: str
    age: int
    salary: float

# create an instance
employee = Employee(name="John", age=42, salary=1000.0)
# access attributes
print(employee.name, employee.age, employee.salary)
```

## Dataclass with no type checking

A Dataclass with no type checking will not raise an exception whenever a passed value does not match the type annotation.

```python
from customdataclass import Dataclass

# define a dataclass with no type checking
class Person(Dataclass, type_checking=False):
    name: str
    age: int

# create an instance
person = Person(name="John", age="42") # age is passed as string
# access attributes
print(person.name, person.age)
```
