from utils import Color 

def red(text:str, bg:bool=False) -> str:
    if bg:
        return f"""{Color.RED_BACKGROUND.value}{text}{Color.RESET.value}"""
    else:
        return f"""{Color.RED.value}{text}{Color.RESET.value}"""

def green(text:str, bg:bool=False) -> str:
    if bg:
        return f"""{Color.GREEN_BACKGROUND.value}{text}{Color.RESET.value}"""
    else:
        return f"""{Color.GREEN.value}{text}{Color.RESET.value}"""

def yellow(text:str, bg:bool=False) -> str:
    if bg:
        return f"""{Color.YELLOW_BACKGROUND.value}{text}{Color.RESET.value}"""
    else:
        return f"""{Color.YELLOW.value}{text}{Color.RESET.value}"""

def blue(text:str, bg:bool=False) -> str:
    if bg:
        return f"""{Color.BLUE_BACKGROUND.value}{text}{Color.RESET.value}"""
    else:
        return f"""{Color.BLUE.value}{text}{Color.RESET.value}"""

def magenta(text:str, bg:bool=False) -> str:
    if bg:
        return f"""{Color.MAGENTA_BACKGROUND.value}{text}{Color.RESET.value}"""
    else:
        return f"""{Color.MAGENTA.value}{text}{Color.RESET.value}"""

def cyan(text:str, bg:bool=False) -> str:
    if bg:
        return f"""{Color.CYAN_BACKGROUND.value}{text}{Color.RESET.value}"""
    else:
        return f"""{Color.CYAN.value}{text}{Color.RESET.value}"""

def white(text:str, bg:bool=False) -> str:
    if bg:
        return f"""{Color.WHITE_BACKGROUND.value}{text}{Color.RESET.value}"""
    else:
        return f"""{Color.WHITE.value}{text}{Color.RESET.value}"""



