from cx_Freeze import setup, Executable

setup(
    name = "SPdf",
    version = "0.4",
    description = "search",
    executables = [Executable("search.py",  base = 'Win32GUI')]
)