import inquirer
import os
import subprocess

change = inquirer.list_input("type of change", choices=['major', 'minor', 'patch'])

bashCommand = "git tag --sort=committerdate | grep -E '[0-9]' | tail -1 | cut -b 2-7"
pro = subprocess.Popen(bashCommand, stdout= subprocess.PIPE, shell=True)
pro.wait()
result = pro.stdout.readlines()
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

    print(newTag)
    confirmation = inquirer.list_input(f"Are you sure to release tag v{newTag}", choices=['yes', 'no'])
    
    if confirmation == 'yes':
        # bashCommand = "git commit -m"$(echo -e "test\ntest")""
        print('release new tag  v', newTag)
        
    