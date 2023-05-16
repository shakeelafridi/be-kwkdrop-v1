# kwkDrop v1 (API's Service)
kwkDrop is a comprehensive platform that offers E-Commerce,
Delivery, and Taxi Services. It facilitates the registration of sellers 
and their shops, allowing them to showcase their products. Buyers can
conveniently purchase products from nearby shops, and a dedicated driver will
ensure doorstep delivery. Additionally, users can easily locate nearby taxi 
services for their transportation needs.


## Tools and Technologies
        PostgresSQL
        Python3
        Django==3.24
        nginx


## Running the Project

To run the project, follow these steps:

1. Set up a virtual environment using the command: `python -m venv venv`
2. Activate the virtual environment.
3. Install the required packages by running: `pip install -r requirement.txt`
4. Migrate Database Schema: `python manage.py migrate`
5. Start the Django development server: `python manage.py runserver`
6. Access the website in your browser at: `http://localhost:8000/`


## Directory structure
    .
    |
    |-- authModule
    |   |-- urls
    |   |-- models
    |   |-- views
    |-- kwk
    |   |-- settings
    |   |-- urls
    |-- seller
    |   |-- urls
    |   |-- models
    |   |-- views
    |-- driver
    |   |-- urls
    |   |-- models
    |   |-- views
    |-- payment
    |   |-- urls
    |   |-- models
    |   |-- views
    |-- buyer
    |   |-- urls
    |   |-- models
    |   |-- views
    |-- utilies
    |-- requirement.txt
    |-- manage.py

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push the branch to your forked repository: `git push origin feature-name`
5. Open a pull request on GitHub.

Please ensure that your code follows the project's coding conventions and includes appropriate tests.