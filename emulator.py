import vexbrain, virtualdeviceserver, os, program, pygamepopup

print("[VexEmulator(Loader)] Booting emulator")

#Setup the emulator's core
brain = vexbrain.Brain()
vds   = virtualdeviceserver.VirtualInterface(('localhost', 8080), brain)

for programFile in os.listdir('data/emulatedstorage/Internal/programs'):
    brain.ProgramsLoaded.append(program.ProgramFile(f'data/emulatedstorage/Internal/programs/{programFile}'))

#make the rest of the menus (Done for now, maybe devices menu)
#Detect if the program fails and ask if they want to retry in legacy mode
#add set_font support
print("[VexEmulator(Loader)] Code started")

while True:
    brain.tickmainloop()