class Meta(type):
    def __new__(mcs, name, bases, namespace):
        if '__annotate_func__' in namespace:
            ann = namespace['__annotate_func__'](1)
            print("evaluated:", ann)
        return super().__new__(mcs, name, bases, namespace)

class A(metaclass=Meta):
    a: int
    b: str = "hi"
