import requests, json
from v5mod import overlay

with open('data/config.json', 'r') as f:
    serverUrl = json.load(f)['serverUrl']

def loadAndRun(programName: str):
    return requests.get(f'{serverUrl}/api/program/loadandrun/{programName}').text


Overlay = overlay.VexCodeOverlay()

while True:
    Overlay.tick()

    if Overlay.pressed:
        if ProjectName := Overlay.getProjectName():
            ProjectName += '.v5python'
            print(f'Running {ProjectName}')
            print(loadAndRun(ProjectName))