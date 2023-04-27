from customdataclass import Dataclass


class MutableDataclass(Dataclass, mutable=True):
    """Test class."""

    int_var: int
    float_var: float


def main():
    m = MutableDataclass(int_var=1, float_var=2.0)
    print(m)
    m.int_var = 2
    m.float_var = 3.0
    print(m)


if __name__ == "__main__":
    main()
