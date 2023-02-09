# Docker / React / Redux / Django / Python SPA that allows users to simulate e-commerce
# [GameLand SPA test demo version](http://ec2-34-232-52-170.compute-1.amazonaws.com/)

- This application was built using Dockerizing, React, and Django. 
- The application allows the users to simulate e-purchases using the PayPal sandbox. 
- Moreover, it allows you to use it as a real e-commerce if to upload on the server EC2. 
- User just needs to regester account and use it as a e-commerce.

<img src="https://raw.githubusercontent.com/Spartak-Belov-Floresku/react_django_docker_project/main/images/first_screen.png">

<img src="https://raw.githubusercontent.com/Spartak-Belov-Floresku/react_django_docker_project/main/images/second_screen.png">

#### To install the application on a local server is necessary.
- Clone the code.
- If you want to run locally, in file ```docker-compose-deploy.yml```, on the row 37 cahnge ```80:8000``` to ```8000:8000```
- Create ```.env``` file in the top directory and copy the contents of the transfer from ```.env.sample```
- To stop server ```Ctrl+C``` and ```docker-compose -f docker-compose-deploy.yml down```
- In bash run commands ```docker-compose -f docker-compose-deploy.yml build``` 
- Applying migrations and collecting static files ```docker-compose -f docker-compose-deploy.yml up```
- If will get an error ```/docker-entrypoint.sh: exec: line 47: /run.sh: not found``` convert the file ```run.sh``` in editor from ```CRLF``` to ```LF``` in ```\scripts\run.sh``` and ```\proxy\run.sh```. Also re-run command ```docker-compose -f docker-compose-deploy.yml build```.
- To run tests ```docker-compose -f docker-compose-deploy.yml run --rm backend sh -c "python manage.py test"```
- To upload tests products ```docker-compose -f docker-compose-deploy.yml run --rm backend sh -c "python manage.py loaddata products"```
- To create super user ```docker-compose -f docker-compose-deploy.yml run --rm backend sh -c "python manage.py createsuperuser"```
- To start application ```docker-compose -f docker-compose-deploy.yml up```
- The application will run on ```http://127.0.0.1:8000/```

<img src="https://raw.githubusercontent.com/Spartak-Belov-Floresku/react_django_docker_project/main/images/third_screen.png">

<img src="https://raw.githubusercontent.com/Spartak-Belov-Floresku/react_django_docker_project/main/images/fourth_screen.png">

### Technology used in this project:
- Docker
- React / Redux / JavaScript
- Django / Python
- RestFul API
- JSON
- Bootstrap
- CSS3
- HTML5
