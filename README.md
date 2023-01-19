# Docker / React / Redux / Django / Python SPA that allows users to simulate e-commerce
The download takes some time. If the app hasn't been used for an hour, the Heroku server puts it to sleep.
# [GameLand SPA test demo version](https://ambercity-demo.herokuapp.com/)

- This application was built using Dockerizing, React, and Django. 
- The application allows the users to simulate e-purchases using the PayPal sandbox. 
- Moreover, it allows you to use it as a real e-commerce if to upload on the server EC2. 
- User just needs to regester account and use it as a e-commerce.

<img src="https://raw.githubusercontent.com/Spartak-Belov-Floresku/react_django_docker_project/main/images/first_screen.png">

<img src="https://raw.githubusercontent.com/Spartak-Belov-Floresku/react_django_docker_project/main/images/second_screen.png">

#### To install the application on a local server is necessary.
- Clone the code.
- Create ```.env``` file in the top directory and copy the contents of the transfer from ```.env.sample```
- To stop server ```Ctrl+C``` and ```docker-compose -f docker-compose-deploy.yml down```
- In bash run commands ```docker-compose -f docker-compose-deploy.yml build``` 
- Applying migrations and collecting static files ```docker-compose -f docker-compose-deploy.yml up```
- To run tests ```docker-compose -f docker-compose-deploy.yml run --rm backend sh -c "python manage.py test"```
- To upload tests products ```docker-compose -f docker-compose-deploy.yml run --rm backend sh -c "python manage.py loaddata products"```
- To create super user ```docker-compose -f docker-compose-deploy.yml run --rm backend sh -c "python manage.py createsuperuser"```
- To start application ```docker-compose -f docker-compose-deploy.yml up```
- The application will run ```http://http://127.0.0.1:8000/```

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
