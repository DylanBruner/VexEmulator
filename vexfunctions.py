def competition(user_control, autonomous):
    print("[VexEmulator(Loader)] Warning competition mode will not work!! but might work in the future")
    print("[VexEmulator(Loader)] User control:", user_control)
    print("[VexEmulator(Loader)] Autonomous:", autonomous)

new_globals = {
    'Competition': competition,
}