import program, vexbrain, codecontainer, threading, veximplementations, vexunits, vexcontroller, prettyemu, time, vexfunctions
from vexdevices import virtualmotor, virtualdrivetrain, virtualgyro

CurrentProgram = program.ProgramFile('EmulationTest.v5python')


ProgramCode = CurrentProgram.patchTextCode()
print("[VexEmulator(Loader)] Booting emulator")

controllerServer = vexcontroller.ControllerServer('localhost', 8080)

brainCore = vexbrain.Brain()
brainCore.BrainScreen.programName  = CurrentProgram.fileName.split('.v5python')[0]

#Setup the brain program execute container
NewContainer = codecontainer.Container(ProgramCode)
NewContainer.set_global('brain', vexbrain.BrainLinker(brainCore.BrainScreen, vexbrain.Battery(), vexbrain.Timer()))
NewContainer.set_global('print', prettyemu.prettyPrint)
NewContainer.merge_globals(vexunits.new_globals)
NewContainer.merge_globals(veximplementations.new_globals)
NewContainer.merge_globals(vexfunctions.new_globals)

for device in CurrentProgram.fileData['rconfig']:
    if device['deviceType'] == 'Controller':
        controllerCore = vexcontroller.Controller()
        controllerServer.set_controller(controllerCore)
        NewContainer.set_global(device['name'], controllerCore)
        print(f'[VexEmulator(Loader)] Found controller {device["name"]}')
    elif device['deviceType'] == 'Motor':
        brainCore.usedPorts.append(device['port'][0])
        motorName = device['name']
        NewContainer.set_global(motorName, virtualmotor.Motor())
        print(f'[VexEmulator(Loader)] Found motor {motorName}')
    elif device['deviceType'] == 'Drivetrain':
        brainCore.usedPorts.extend(device['port'])
        NewContainer.set_global(device['name'], virtualdrivetrain.Drivetrain())
        print(f'[VexEmulator(Loader)] Found drivetrain {device["name"]}')
    elif device['deviceType'] == 'Gyro':
        brainCore.usedPorts.append(device['port'][0])
        NewContainer.set_global(device['name'], virtualgyro.Gyro())
        print(f'[VexEmulator(Loader)] Found gyro {device["name"]}')

    else:
        print(f'[VexEmulator(Loader)] Unknown device type {device["deviceType"]}')

#Fix text drawing
threading.Thread(target=NewContainer.execute).start()
brainCore.BrainScreen.startTime = time.time()
print("[VexEmulator(Loader)] Code started")
while True:
    brainCore.tickmainloop()