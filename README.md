### Requirements
* Ubuntu 20 LTS (could be WSL 2)
* Python 3.9.x
* requirements_py/common.txt
* requirements_py/master.txt

#### Scripts
##### Build local
The python script **build_local.py** executes the next routine:
* Install npm dependencies (requires to have node 16 LTS installed and npm path enabled)
* execute all or certain builds with multi-process
* delete assets on dist builds (also on multi locale case)
* create a tar.gz with all folder dist without assets
Once you have dist.tar.gz file must be send to server and untar/unzip on the server

#### Fill assets
With dist folder without assets, must be required to filled with that, the python script **build_fill_assets.py**, fill the assets from ONLY the generated folders (dist folders must be have the same name of the project folders)

#### Nginx config generator
The python file **nginx/nginx_conf_create.py** create the config according to .env_nginx_py (check the **.env_nginx_py_template**) and according to projectes on the dist folder (only works when build local is performed). At **nginx/confs_example** folder could check an example of possible expected results. This confs also can be used for other methods to fill the **nginx/confs** folder