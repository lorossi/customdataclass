from customdataclass import Dataclass


class PartialValueDataclass(Dataclass, partial=True):
    """Test class."""

    list_var: list
    tuple_var: tuple
    set_var: set
    dict_var: dict


def main():
    p = PartialValueDataclass(list_var=[1, 2, 3])
    print(p)
    print(p.to_dict)


if __name__ == "__main__":
    main()
