# BCNEventer

So, you have decided to put some effort into this thing, very good! Please read on to know how to get started. Following these steps will make collaboration easy and keep the git flow clean and consistent. Keep in mind that this is not everything there is to GitHub, but covers most of the basics. If you have any questions, ask Philippe. Feel free to add new content to the _README_, but before changing content, please notify Philippe.

Side note: you are all smart enough to understand this, but just to put it out there; if you encounter pieces of text/command between pointy brackets, e.g. `<branch>`, then this is a variable.

## Getting started
> NOTE: Make sure you don't have anything running on port 5000 (in the future, after adding mysql, probably we have to add port 3306 here)

#### 1. Get Docker
Check the [documentation](https://docs.docker.com/docker-for-mac/install/) to install docker.

#### 2. Fork the main repository
Make sure to fork the main repo (https://github.com/ADS2018UB/BCNEventer) to your own GitHub account. Forking will clone the main repo to your own GitHub account, from which you can safely work without disturbing the main repo. The button to fork can be found on the right top corner of the repo, saying `Fork`, the rest will explain itself.

#### 3. Clone your repo
Go to your GitHub account and clone the forked repo to your computer. You can do this with the following command:
```
git clone git@github.com:<account_name>/BCNEventer.git
```
Copy `.env.example` to `.env` and fill in the variables. Now setup the upstream remote (to easily pull changes from the main repo) by entering this command:
```
git remote add upstream git@github.com:ADS2018UB/BCNEventer.git
```
Now with the command `git pull upstream <branch>` you should be able to pull in a certain branch from the main repo into your current branch.<br>
When you do your first push to your own repo use the following command to 'track' the branch, so next time you just have to type `git push`:
```
git push -u origin <branch>
```

#### 4. Getting this thing to run
Go to your terminal, or whatever other means it may be on windows. Go to this directory and run the following command:
```
docker-compose up
```
This will fire up the containers and magically, the app should be reachable at `http://localhost:5000/`. If you want to daemonize the docker process, that is to make the process non-blocking for your terminal, use 
```
docker-compose up -d
```

#### 5. Develop
Go make something beautiful! :smile:


## Git workflow
> VERY IMPORTANT: DO NOT WORK ON THE `master` BRANCH UNLESS IT IS A HOTFIX! 

Please, please, please follow these guidelines.

For every new feature/user story make a new branch, called `features/<branch>`. For every patch/fix make a new branch, called `patches/<branch>`. 

#### General workflow
This is the workflow after you follows the _getting started_ section. 
1. Pull from the main repo (unless starting a new branch, see next section) `git pull upstream <branch>`
2. Make code
3. Commit: `git commit -m "<message>"` or `git commit` (last option is meant for longer commit messages)
4. Push: `git push`, now the changes are in your repo
5. Make a pull request to the main repo, not necessary every time, but do not wait too long to do this

#### Creating a new branch
1. On your computer type `git checkout -b <branch>`, e.g. `git checkout -b features/cool-new-feature`
2. Make code
3. Commit
4. Push: `git push -u origin <branch>`, this will automatically make a branch in your GitHub repo and track it
5. Pull request to main repo

#### Switching branches
```
git checkout <branch>
```

#### Working on a new branch that exists on the main repo
```
git checkout -b <branch> upstream/<branch>
```
Now follow the instructions from the section _general workflow_.
