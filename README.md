# linear-algebra-calculator

The goal of this project is to provide a user-friendly way to automatically
perform introductory level linear algebra calculations.

Website Application Link: https://aldenaccount.shinyapps.io/linear-algebra-calculator/

Calculator Functions Included (More Will Be Added):

1. Bringing a Matrix to Row Echelon and Reduced Row Echelon Form
2. Finding the Solution Set to a System of Linear Equations
3. Calculating the Determinant of a Square Matrix
4. Calculating the Inverse of a Square Matrix
5. Calculating Bases for the Fundamental Subspaces of a Matrix
6. LU Factorizing a Matrix

Information for Development:

This program has two requirements folders.

1. requirements.txt: This folder is used for deploying the web app and should only include packages actually used by the app.
2. requirements-for-development.txt: This folder includes all packages used for development and is the requirements folder whose contents should be installed in a virtual environment.

To install the libraries necessary for development of this project, a virtual environment should be created. Within the virtual environment, the following command should be run:

pip freeze > requirements.txt
