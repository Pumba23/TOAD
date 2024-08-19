from cx_Freeze import setup, Executable

setup(
    name="TOAD",
    version="0.1",
    description="Decomposition analysis",
    executables=[Executable("main.py")],
)
