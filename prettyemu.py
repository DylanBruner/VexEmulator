def prettyPrint(*args):
    text = ""
    for arg in args:
        text += str(arg) + " "
    print(f"[VexEmulator(Brain)] {text}")