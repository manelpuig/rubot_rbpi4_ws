# rubot_rbpi4_ws

This is the workspace in the rUBot raspberrypi4 with all the needed packages

Be careful to syncronize the submodules in github:
https://gist.github.com/gitaarik/8735255

**1. Add a new package as a submodule**

When you need to use other third party packages, the best way is to add them as a submodules.

Open a terminal in src folder to add a package as a submodule:
```shell
git submodule add https://github.com/Slamtec/rplidar_ros.git
```

**2. Clone the repository with submodules to your raspberrypi4:**

In the destination folder of your raspberrypi4, type:
```shell
git clone --recurse-submodules https://github.com/manelpuig/rubot_rbpi4_ws.git
```
When finished your programs, syncronize the changes with your github.

Open a terminal in your local repository and type the first time:
```shell
git config --global user.email mail@alumnes.ub.edu
git config --global user.name 'your github username'
git config --global credential.helper store
```
for succesive times, you only need to do:
```shell
git add -A
git commit -a -m 'message'
git push
```
