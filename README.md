# React/Redux/Django/Python SPA that allows users to simulate e-commerce

# [GameLand SPA test demo version](https://ambercity-demo.herokuapp.com/)

- This application was built using React and Django. 
- The application allows the users to simulate e-purchases using the PayPal sandbox. 
- Moreover, it allows you to use it as a real e-commerce if to make some slight changes. 
- User just needs to regester account and use it as a e-commerce.

<img src="https://raw.githubusercontent.com/Spartak-Belov-Floresku/react_django_docker_project/main/frontend/public/images/first_screen.png">

<img src="https://raw.githubusercontent.com/Spartak-Belov-Floresku/react_django_docker_project/main/frontend/public/images/second_screen.png">

#### To install the application on a local server is necessary.
- Clone the code.
- In bash run commands ```docker build .```, ```docker-compose build```, ```docker-compose up```.
- To run tests ```docker-compose run --rm backend sh -c "python manage.py test"```
- To upload tests products ```docker-compose run --rm backend sh -c "python manage.py loaddata products"```
- To create super user ```docker-compose run --rm backend sh -c "python manage.py createsuperuser"```
- To stop server ```docker-compose down```
- In bash go to frontend and run the commands ```npm install```, ```npm start```
- The application will run on your local server for frontend ```http://localhost:3000``` for a backend  ```http://localhost:8000/admin```

<img src="https://raw.githubusercontent.com/Spartak-Belov-Floresku/react_django_docker_project/main/frontend/public/images/third_screen.png">

<img src="https://raw.githubusercontent.com/Spartak-Belov-Floresku/react_django_docker_project/main/frontend/public/images/fourth_screen.png">

### Technology used in this project:
- Django / Python
- React / Redux / JavaScript
- RestFul API
- JSON
- Bootstrap
- CSS3
- HTML5
