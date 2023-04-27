from customdataclass import Dataclass


# define a dataclass
class Person(Dataclass):
    name: str
    surname: str
    age: int


def main():
    # create an instance of the dataclass
    person = Person(name="John", surname="Doe", age=42)
    # access the fields
    print(person.name, person.surname, person.age)
    # convert to string
    print(person)
    # get a dictionary
    print(person.to_dict)
    # get a json string
    print(person.to_json)
    # get a yaml string
    print(person.to_yaml)
    # get a toml string
    print(person.to_toml)

    # create an instance of the dataclass from a dictionary
    person_d = Person.from_dict({"name": "John", "surname": "Doe", "age": 42})
    # create an instance of the dataclass from a json string
    person_j = Person.from_json('{"name": "John", "surname": "Doe", "age": 42}')
    # create an instance of the dataclass from a yaml string
    person_y = Person.from_yaml("name: John\nsurname: Doe\nage: 42")
    # create an instance of the dataclass from a toml string
    person_t = Person.from_toml('name = "John"\nsurname = "Doe"\nage = 42')

    # compare the instances
    print(person == person_d == person_j == person_y == person_t)


if __name__ == "__main__":
    main()
