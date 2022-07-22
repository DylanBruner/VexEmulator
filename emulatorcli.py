import click, vexbrain, virtualdeviceserver, os, program

@click.group()
def cli(): pass

@click.command()
@click.option('-f','--file',required=False,help='(Full path required!) File to launch upon brain boot')
@click.option('-d','--disable-vds',required=False,help='Disable the virtual device server',is_flag=True)
@click.option('-p','--port',required=False,help='Port to use for the virtual device server',default=8080)
@click.option('-s','--host',required=False,help='Host to use for the virtual device server',default='localhost')
@click.option('-D','--disable-prgm-scan',required=False,help='Dont scan data/emulatedstorage/Internal/programs',is_flag=True)
def start(file, disable_vds, port, host, disable_prgm_scan):
    brain = vexbrain.Brain()
    if not disable_vds: vds = virtualdeviceserver.VirtualInterface((host, port), brain)
    if not disable_prgm_scan:
        for programFile in os.listdir('data/emulatedstorage/Internal/programs'):
            brain.ProgramsLoaded.append(program.ProgramFile(f'data/emulatedstorage/Internal/programs/{programFile}'))
    

    if brain.CodeEnviorment != None: brain.teardownProgram()
    prgm = program.ProgramFile(file)
    brain.ProgramsLoaded.append(prgm)

    #Get the brain ready to run the program
    brain.onProgramFolderScreen = False; brain.BrainScreen._drawProgramBar = True
    brain.onProgramScreen       = True;  brain.onHomeScreen = False
    brain.onDeviceScreen        = False; brain.BrainScreen.clear_screen()

    #Run the program
    brain.CodeEnviorment = prgm.loadContainer(brain)
    brain.CodeEnviorment.threadedExecute()

    while True:
        brain.tickmainloop()


cli.add_command(start)
cli()