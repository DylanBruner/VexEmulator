<h1>VEX v5 Brain Emulator</h1>
<br>
<br>
<h2>Note: Vex, if you see this and want me to remove the assets for some reason create a issue and i'll remove them</h2>
<br>
<h2>This is still very much in development if you find a issue, report it and i'll try to get around to fixing it asap</h2>
<br>
<h2>What it is and isn't</h2>

 - It's not, a virtual machine that can run C++ programs
    - It is, a pygame powered interface that's capable of running VEX v5python programs

 - It's not, (at least not yet) a full simulation, the devices dont talk to each other to figure out location data and such
    - It is, a way to test programs without a brain, the web interface can be used to simulate the devices actually being there

 - It's not, a professional grade emulator
    - It is, a hobby project, I've created this as a side project so bugs are to be expected

 - It's not, a seemless replacment for a physical brain
    - It is, a emulator that supports most devices (eventually will support all)

<br>
<h2>Currently Supported Devices</h2>

- Controller
- Motor
- Motor Group
- Drivetrain
- Bumper
- Electro Magnet
- Gyroscope
- Optical Sensor (not tested)
- Distance Sensor
- Rotation Sensor
- Inertial Sensor
- Vision Sensor
- Gps

<br>
<h2>List of Features</h2>

 - "Virtual" SDCard, supports writing to files stored in `data/emulatedstorage/SDCard`
 - Can select/view up to 18 programs on the brain
 - You can check if running on the real brain or the emulated one by checking if any devices have the _attributes attributes, for example
   -  ```python
      hasattr(brain, '_attributes')
 - The attributes of all devices can be controlled from the [web server](http://localhost:8080)
 - Emulates/Redirects functions like 'Thread' and 'wait' to their respective external libraries
 - Test Competitions can be ran using the webserver as a competition switch 

<br><br>
<h2>Planned ToDos</h2>

 - For the brain
    - Clean up code
    - Legacy mode
        - Add support for functions VEX changed or removed
    - Drivetrain w Inertial support!
    - Make all devices able to be emulated
    - Maybe use physical controller on the emulated brain not sure about the practicality of this
    - Register the brain's battery as a emulated device that way the web UI can control it's attributes
    - Maybe fix the emulator dragging (stop it from snapping)
    - A CLI interface to start the emulator at a certain point or to start a program without interaction
    - Ability to take screenshots of the emulator easily
    - Try to dump assets from the offical brain that way it will look 1000x better
    - Show which ports are ocupied when a program is running
    - Maybe a ability to limit the Clock Speed of the emulator along with the max amount of memory it can use
    - Maybe make all the devices work together, like if the drivetrain is told to move, update the location were supposed to be at and
        tell all the other devices to update their attributes (Would probably require a fairly exstensive rewrite)
    <br><br>
    - Interesting Possible Features
        - Try to inject code into VEX Code that will launch the emulator when the run button is clicked without a brain connected
            - Or possibly use a virtual serial device and pretend to be a real brain (not sure how hard this would be to do)
 <br><br><br>   
 - For the webserver
    - Make the UI look a lot nicer (pictures!!)
        - Nicer Input themeing
    - Use sliders when possible
    - Make device attributes collapseable
    - Group / order devices by type
        - Controller is at top when loaded
    - Check the brain for variable changes and update them on the site without reloading
    - Add support for the competition function
    - Possibly a mobile mode in which it only displays the controller and you can use it like a normal controller

<br>
<h2>Vex Mod</h2>
 
 - Vex mod is a "mod" for VEXcode V5 text (not pro!)

 - Vex mod currently overlays a yellow run button when a physical brain is not connected, it grabs the current project (must be saved in the emulator's project emulatedstorage folder) by taking a screenshot and extracting the text from it
 - Currently it must be ran seperatly from emulator.py if they are ran togehter the pygame windows get messy
 - If i find a way to use injected javascript to do the click events, project name getting and button color changing i will but i haven't found a way at this time

<br>
<h2>Some things worth mentioning</h2>
 
 - It is possible to create custom devices at the moment but in the future i will be providing a better system for this along with documentation
 - It is possible to run VEX projects without using the emulator but it's way harder and some functionality might not be there
 - The emulator can be used in your own projects as long as the brains main loop can be called periodically, for example

```python 
from os import listdir
from vexbrain import Brain
from virtualdeviceserver import VirtualInterface
from program import ProgramFile


brain = Brain()
vds   = VirtualInterface(('localhost', 8080), brain)

"""
Programs are stored in brain.ProgramsLoaded,
by default (in emulator.py) they are loaded from a folder like shown below
"""

for programFile in listdir('data/emulatedstorage/Internal/programs'):
    brain.ProgramsLoaded.append(ProgramFile(f'data/emulatedstorage/Internal/programs/{programFile}'))

while True:
    brain.tickmainloop()
    #Updates the screen and does all the other logic, must be called every so often
    #Unfortunately it can't be ran in it's own thread due to pygame limitations
```
