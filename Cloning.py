import git
import traceback
import logging
import pydriller
import shutil
import os,stat
import time

fileNameList=[]
for i in repo_list:
    progress(count, len(repo_list))
    
    projectName=i[:-4].split('/')[-1:]
    fileNameList.append(projectName[0])
    
    local_path = "G:\\NewCloneRepository\\"+projectName[0]
    remote = f"https://"+Git_access_token+":@"+i[8:]
    
    #Cloning each repository and also checking if there are any exceptions
    try:
        git.Repo.clone_from(remote, local_path)
    except git.GitCommandError as e:
        
        #Checking if there are any Git LFS files to download. if present then just ignoring the LFS files
        if("smudge filter lfs failed" in e.stderr):
            print("Git LFS Error, Not downloading the LFS files")
            pass
        elif("Repository not found" in e.stderr): #Ignoring the project if the repo is not found in github
            print("Repository not found in GitHUb,",i)
            continue
    
    #For each clone, getting the clone message and clone hash id and writing it into a text file
    with open("G:\\NewDataRepository\\"+c[0]+'.txt', 'w') as f:
        for commit in pydriller.Repository(local_path).traverse_commits():
                    lines=[]
                    b=commit.hash
                    c=commit.msg.replace("\n"," ")
                    d=""
                    #Changing the unreadable charaters into a special character for better processing
                    for character in c:
                        if 0<=ord(character)<=127 :
                            d+=character
                        else:
                            d+='#'
                    lines.append(b+";dlt;"+d+";dlt;") #";dlt; is a delimiter to use it to split the data in future processing"
                    f.writelines(lines)
                    f.write('\n')
                    commit=None
    #Deleting the clone repository in local pc once all the commit messages are collected
    shutil.rmtree(local_path, onerror=remove_readonly)
