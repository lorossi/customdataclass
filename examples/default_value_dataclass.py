from customdataclass import Dataclass


class DefaultValueDataclass(Dataclass):
    str_var: str = "default value"
    int_var: int = 42


def main():
    d = DefaultValueDataclass()
    print(d)


if __name__ == "__main__":
    main()
