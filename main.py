import inquirer
import os
import subprocess
from git import Repo
import json
from pathlib import Path

change = inquirer.list_input("type of change", choices=['major', 'minor', 'patch'])
parentDirectory = Path(os.getcwd())

bashCommandForGitAdd = "git add ."
bashCommandForGitCommit = "git commit -m 'Add tag message to changelog'"
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

    confirmation = inquirer.list_input(f"Are you sure to release tag v{newTag}", choices=['yes', 'no'])
    if confirmation == 'yes':
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
                
            print('message',message)
        os.chdir(parentDirectory)
        with open("CHANGELOG.md", "r") as in_file:
            line = in_file.read()
            dn = line.replace("## [Unreleased]", f"## [Unreleased]\n\n### v{newTag}\n\n{message}")
            in_file.close()
        
        with open("CHANGELOG.md", "w") as out_file:
                out_file.write(dn)
                out_file.close()
        
        pro = subprocess.Popen(bashCommandForGitAdd, stdout= True, shell=True)
        pro.wait()
        pro = subprocess.Popen(bashCommandForGitCommit, stdout= True, shell=True)
        pro.wait()
        obj = Repo(parentDirectory)
        new_tag = obj.create_tag(f'v{newTag}', message=f'Version v{newTag}\n {message}')
        obj.remotes.origin.push(new_tag)

    

# pro = subprocess.Popen(bashCommand, stdout= subprocess.PIPE, shell=True)
# pro.wait()
# result = pro.stdout.readlines()
# for tag in result:
#     decodeTag = tag.decode("utf-8")
#     splitTag = decodeTag.split('.')

#     major = int(splitTag[0])
#     minor = int(splitTag[1])
#     patch = int(splitTag[2])

#     global newTag 

#     if change == 'major':
#         newTag = str(major+1)+"."+"0"+"."+"0"
  
#     if change == 'minor':
#         newTag = str(major)+"."+str(minor+1)+"."+"0"
       
#     if change == 'patch':
#         newTag = str(major)+"."+str(minor)+"."+str(patch+1)

#     print(newTag)
#     confirmation = inquirer.list_input(f"Are you sure to release tag v{newTag}", choices=['yes', 'no'])
    
#     if confirmation == 'yes':
#         tagCreateBashCommand = f"git tag -a v1.0.3 -m 'this is test'"
#         obj = Repo("/Users/devin/Documents/devin-apps/tag-create/tag-MVP")
#         new_tag = obj.create_tag(f'v{newTag}', message=f'Version v{newTag}\n shopping-cart-components: 1.0.0\n dealer-map: 1.0.2\n shopping-cart: 1.1.0\n common-components: 0.0.3'.format(f'v{newTag}'))
#         obj.remotes.origin.push(new_tag)
#         pro = subprocess.Popen("git tag --sort=-creatordate", stdout= subprocess.PIPE, shell=True)
#         pro.wait()
#         result=pro.stdout.readlines()
#         reversedResult = result[::-1]
#         for x in reversedResult:
#             p = x.decode()
#             tagg = p.removesuffix('\n')
#             prod = subprocess.Popen(f"git cat-file -p {tagg} | tail -n +6", stdout= subprocess.PIPE, shell=True)
#             prod.wait()
#             result2=prod.stdout.readlines()
#             msgdd = ''
#             for index, msg in enumerate(result2):
#                 decodeMsg = msg.decode("utf-8")
#                 if index != 0:
#                     msgdd = msgdd + decodeMsg

#             with open("CHANGELOG.md", "r") as in_file:
#                 line = in_file.read()
#                 dn = line.replace("## [Unreleased]", f"## [Unreleased]\n\n### {tagg}\n\n{msgdd}")
#                 in_file.close()
            
#             if tagg not in line:
#                 with open("CHANGELOG.md", "w") as out_file:
#                     out_file.write(dn)
#                     out_file.close()


#     else:
#         print('exit !!')
