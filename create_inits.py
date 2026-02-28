# Create necessary __init__.py files
import os

dirs = [
    "src",
    "src/api",
    "src/models",
    "src/data",
    "src/features",
    "src/ui",
    "src/utils",
]

for d in dirs:
    init_file = os.path.join(
        "c:/Users/Calla/OneDrive/Desktop/Project/Test/ticket-intel", d, "__init__.py"
    )
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            pass
