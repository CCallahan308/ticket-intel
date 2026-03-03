class Meta(type):
    def __new__(mcs, name, bases, namespace):
        print("namespace keys:", list(namespace.keys()))
        return super().__new__(mcs, name, bases, namespace)

class A(metaclass=Meta):
    a: int
    b: str = "hi"
