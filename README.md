# Movies-Website

How to run:
1. Login to Nova
2. ssh delta-tomcat-vm
3. cd specific/scratch/dvirsalomon/django/
4. check if your user is running a screen process (type "screen -ls") and if it is type "pkill screen"
5. source env/bin/activate.csh
6. setenv PYTHONPATH /specific/scratch/dvirsalomon/mysql-connector-python/
7. screen
8. press enter
9. python app.py

Now you can press "ctrl+a" then "d" to detach the screen process (app.py would still run in background).

For reattaching your screen type "screen -r".
