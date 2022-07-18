import program, vexbrain, vexcontroller, os

print("[VexEmulator(Loader)] Booting emulator")

controllerServer = vexcontroller.ControllerServer('localhost', 8080)
brain            = vexbrain.Brain()
brain.controllerServer = controllerServer

for programFile in os.listdir('data/emulatedstorage/Internal/programs'):
    brain.ProgramsLoaded.append(program.ProgramFile(f'data/emulatedstorage/Internal/programs/{programFile}'))

#Fix text drawing, (kinda done)
#make the rest of the menus
#  - Program selector
print("[VexEmulator(Loader)] Code started")
while True:
    brain.tickmainloop()