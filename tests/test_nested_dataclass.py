import unittest

from src.customdataclass import Dataclass


class SubDataclass1(Dataclass):
    """Test class."""

    int_var: int
    float_var: float


class SubDataclass2(Dataclass):
    """Test class."""

    str_var: str
    list_var: list


class ContainerDataClass(Dataclass):
    """Test class."""

    number_dataclass: SubDataclass1
    string_dataclass: SubDataclass2


class DataclassLevel1(Dataclass):
    """Test class."""

    int_var: int


class DataclassLevel2(Dataclass):
    """Test class."""

    level1: DataclassLevel1


class DataclassLevel3(Dataclass):
    """Test class."""

    level2: DataclassLevel2


class DataclassLevel4(Dataclass):
    """Test class."""

    level3: DataclassLevel3


class TestNestedDataclass(unittest.TestCase):
    def _createNestedDataclass(self) -> ContainerDataClass:
        s1 = SubDataclass1(int_var=1, float_var=1.0)
        s2 = SubDataclass2(str_var="123", list_var=[1, 2, 3])
        return ContainerDataClass(number_dataclass=s1, string_dataclass=s2)

    def _reprDataclass(self) -> str:
        return (
            "ContainerDataClass(number_dataclass=SubDataclass1(int_var=1, "
            'float_var=1.0), string_dataclass=SubDataclass2(str_var="123", '
            "list_var=[1, 2, 3]))"
        )

    def testCreation(self):
        s = self._createNestedDataclass()
        self.assertEqual(s.number_dataclass.int_var, 1)
        self.assertEqual(s.number_dataclass.float_var, 1.0)
        self.assertEqual(s.string_dataclass.str_var, "123")
        self.assertEqual(s.string_dataclass.list_var, [1, 2, 3])

        self.assertIsInstance(s.number_dataclass.int_var, int)
        self.assertIsInstance(s.number_dataclass.float_var, float)
        self.assertIsInstance(s.string_dataclass.str_var, str)
        self.assertIsInstance(s.string_dataclass.list_var, list)

    def testEquality(self):
        s1 = self._createNestedDataclass()
        s2 = self._createNestedDataclass()
        self.assertEqual(s1, s2)

        s3 = ContainerDataClass(
            number_dataclass=SubDataclass1(int_var=1, float_var=1.0),
            string_dataclass=SubDataclass2(str_var="123", list_var=[1, 2, 3]),
        )
        s4 = ContainerDataClass(
            number_dataclass=SubDataclass1(int_var=1, float_var=1.0),
            string_dataclass=SubDataclass2(str_var="456", list_var=[1, 2, 3]),
        )
        self.assertNotEqual(s3, s4)

    def testRepr(self):
        s = self._createNestedDataclass()
        self.assertEqual(repr(s), self._reprDataclass())
        self.assertEqual(str(s), self._reprDataclass())

    def testSerializeDeserialize(self):
        c1 = self._createNestedDataclass()
        c2 = ContainerDataClass.from_dict(c1.to_dict)
        self.assertEqual(c1, c2)

        c3 = ContainerDataClass.from_json(c1.to_json)
        self.assertEqual(c1, c3)

        c4 = ContainerDataClass.from_toml(c1.to_toml)
        self.assertEqual(c1, c4)

        c5 = ContainerDataClass.from_yaml(c1.to_yaml)
        self.assertEqual(c1, c5)


class TestNestedDataclassLevel4(unittest.TestCase):
    def testCreation(self):
        d = DataclassLevel4(
            level3=DataclassLevel3(
                level2=DataclassLevel2(level1=DataclassLevel1(int_var=1))
            )
        )
        self.assertEqual(d.level3.level2.level1.int_var, 1)

    def testSerializeDeserialize(self):
        d = DataclassLevel4(
            level3=DataclassLevel3(
                level2=DataclassLevel2(level1=DataclassLevel1(int_var=1))
            )
        )
        d2 = DataclassLevel4.from_dict(d.to_dict)
        self.assertEqual(d, d2)

        d3 = DataclassLevel4.from_json(d.to_json)
        self.assertEqual(d, d3)

        d4 = DataclassLevel4.from_toml(d.to_toml)
        self.assertEqual(d, d4)

        d5 = DataclassLevel4.from_yaml(d.to_yaml)
        self.assertEqual(d, d5)
