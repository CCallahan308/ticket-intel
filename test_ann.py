import inspect
class A:
    a: int
    b: str = "hi"

print("annotate:", A.__dict__.get('__annotate__'))
print("annotations:", A.__dict__.get('__annotations__'))
print("inspect:", inspect.get_annotations(A))
