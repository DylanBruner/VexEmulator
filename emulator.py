import program, vexbrain, vexcontroller

print("[VexEmulator(Loader)] Booting emulator")

controllerServer = vexcontroller.ControllerServer('localhost', 8080)
brain            = vexbrain.Brain()


#Fix text drawing, (kinda done)
#load devices cleaner,
#be able to kill running programs/threads
#make the rest of the menus
#  - Program selector
print("[VexEmulator(Loader)] Code started")
while True:
    brain.tickmainloop()