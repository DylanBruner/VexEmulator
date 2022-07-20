import vexbrain, virtualdeviceserver, os, program

print("[VexEmulator(Loader)] Booting emulator")

#Setup the emulator's core
brain = vexbrain.Brain()
vds   = virtualdeviceserver.VirtualInterface(('localhost', 8080), brain)

#load the emulator's programs
for programFile in os.listdir('data/emulatedstorage/Internal/programs'):
    brain.ProgramsLoaded.append(program.ProgramFile(f'data/emulatedstorage/Internal/programs/{programFile}'))

print("[VexEmulator(Loader)] Code started")

#main loop
while True:
    brain.tickmainloop()