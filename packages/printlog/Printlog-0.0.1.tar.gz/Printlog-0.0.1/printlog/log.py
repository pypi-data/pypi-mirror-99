def error(text:str) -> None:
    print(f"""\33[1;31;40m {text}""")


def succes(text:str) -> None:
    print(f"""\033[1;32;40m {text}""")

if __name__ = '__main__':
    error("This an error")
    succes("This is a succes")