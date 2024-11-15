# Generation: UK & I miniproject DE-NAT-3 Cohort

This is a command line interface (CLI) application for a cheesemongers shop. The aim of the project is for the author to practice and hone their python programming abilities. 

## Client Requirements

- [x] create a product, courier, or order and add it to a table
- [x] view all products, couriers, or orders
- [x] update the status of an order
- [ ] persist my data in a database
- [x] _STRETCH_ delete or update a product, order, or courier
- [x] _BONUS_ display orders by status or courier
- [ ] _BONUS_ CRUD a list of customers
- [ ] _BONUS_ track my product inventory
- [ ] _BONUS_ import/export my entities in CSV format

## Running program Requirements

Before executing the next steps some set-up is required. Firstly, we have to install the requirements of the program. This is done by running the following command:

```console
python -m pip install -r requirements.txt
```

After installing the program's requirements you can move on the following steps.

## How to run

Make sure you are in the project's root directory, then run the following in a terminal of your choosing:

```console
python run.py
```

## How to run test

Firstly, ensure you are in the root directory of the project.
Then confirm you have the pytest package installed either in a virtual or global environment.

Then run the following in a terminal: 
(If pytest is installed in a virtual environment then confirm it's activated)

```console
python -m pytest
```

## Project Reflections

### How did your design go about meeting the project's requirements?

The design is split into various classes handling separate functionality of the project. The main file (app.py) configures the menus and loads all data that is passed to the menu to be used and manipulated with. When the application exits all data is then persisted based on the configurations of in the app.py file.

### How did you guarantee the project's requirements?

I would following the weekly specifications ensuring I met the base requirements initially and then moving on to any Bonus/Stretch requirements.

### If you had more time, what is one thing you would improve upon?

I would implement the database persistence seeing as the functionality is mostly completed. It would also have been nice to containerise my project into a docker image to be run on any machine.

### What did you most enjoy implementing?

I enjoyed initially implementing a simple menu and then abstracting functionality away. This allowed me to configure the menus and data before hand and then run it without much frustrations. Then allowed me to be more extensible and refactoring to keep up with specifications was quick.