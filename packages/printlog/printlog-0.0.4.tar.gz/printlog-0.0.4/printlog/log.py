from utils import Color

def error(text:str, bg:bool=False) -> None:
    if bg:
        print(f"""{Color.RED_BACKGROUND_BRIGHT.value}{text}{Color.RESET.value} """)
    else:
        print(f"""{Color.RED_BOLD.value}{text}{Color.RESET.value}""")


def success(text:str, bg:bool=False) -> None:
    if bg:
        print(f"""{Color.GREEN_BACKGROUND.value}{text}{Color.RESET.value}""")
    else:
        print(f"""{Color.GREEN_BRIGHT.value}{text}{Color.RESET.value}""")

success("It is a success")
success("It is a success with background", bg=True)
error("It is an error")
error("It is an error with background", bg=True)

