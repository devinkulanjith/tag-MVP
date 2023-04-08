import inquirer
import os
import subprocess
from git import Repo
import json
from pathlib import Path

BASH_COMMAND_FOR_GIT_ADD = "git add CHANGELOG.md"
BASH_COMMAND_FOR_GIT_COMMIT_CHANGELOG = "git commit -m 'Add tag message to changelog'"
BASH_COMMAND_FOR_GIT_LATEST_TAG = "git tag --sort=committerdate | grep -E '[0-9]' | tail -1 | cut -b 2-7"

currentDirectory = Path(os.getcwd())
parentDirectory = currentDirectory.resolve().parents[0]

change = inquirer.list_input("type of change", choices=['major', 'minor', 'patch'])

cmd = subprocess.Popen(BASH_COMMAND_FOR_GIT_LATEST_TAG, stdout= subprocess.PIPE, shell=True)
cmd.wait()
result = cmd.stdout.readlines()
for tag in result:
    decodeTag = tag.decode("utf-8")
    splitTag = decodeTag.split('.')

    major = int(splitTag[0])
    minor = int(splitTag[1])
    patch = int(splitTag[2])

    global newTag 

    if change == 'major':
        newTag = str(major+1)+"."+"0"+"."+"0"
  
    if change == 'minor':
        newTag = str(major)+"."+str(minor+1)+"."+"0"
       
    if change == 'patch':
        newTag = str(major)+"."+str(minor)+"."+str(patch+1)

    confirmation = inquirer.list_input(f"Are you sure to release tag v{newTag}", choices=['yes', 'no'])
    if confirmation == 'yes':
        os.chdir(parentDirectory)
        message = ''
        with open("president_order.txt", "r") as in_file:
            lines = in_file.readlines()
            for x in lines:
                appName = x.removesuffix('\n')
                os.chdir(parentDirectory.joinpath(appName))
                with open('manifest.json', encoding="utf-8") as f:
                    data = json.load(f)
                    version = data['version']
                    message = message + ' >> ' + appName + ':' + " " + version + "\n"
                
        os.chdir(parentDirectory)
        with open("CHANGELOG.md", "r") as in_file:
            line = in_file.read()
            dn = line.replace("## [Unreleased]", f"## [Unreleased]\n\n### v{newTag}\n\n{message}")
            in_file.close()
        
        with open("CHANGELOG.md", "w") as out_file:
                out_file.write(dn)
                out_file.close()
        
        cmd = subprocess.Popen(BASH_COMMAND_FOR_GIT_ADD, stdout= False, shell=True)
        cmd.wait()
        cmd = subprocess.Popen(BASH_COMMAND_FOR_GIT_COMMIT_CHANGELOG, stdout= False, shell=True)
        cmd.wait()
        obj = Repo(parentDirectory)
        createdTag = obj.create_tag(f'v{newTag}', message=f'Version v{newTag}\n {message}')
        obj.remotes.origin.push(createdTag)
