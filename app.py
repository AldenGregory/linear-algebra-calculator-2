import numpy as np
import pandas as pd
import matrix_input

from shiny import App, Inputs, Outputs, Session, render, ui
    
def page_title(title):
    # There are 12 vertical sections in each page in a fluid layout (the
    # default for nav_panel layouts). The column below takes up all 12
    # sections.
    return ui.column(
            12,
            ui.div(
                title
            ).add_style(
                style = "font-size: 200%;"
            )
        )

# Inputs are held in a page container object. They are arguments at the start
# of the initialization call.

app_ui = ui.page_navbar(
    ui.nav_panel(
        "Reduced Row Echelon and Row Echelon Form Calculator",
        page_title(
            "Reduced Row Echelon and Row Echelon Form Calculator"
        ),
        matrix_input.matrix_input_ui("ref_and_rref")
    ),
    ui.nav_panel(
        "Linear System Solver",
        page_title(
            "Linear System Solver"
        ),
        matrix_input.matrix_input_ui(
            "linear_systems",
            input_method_label = "Choose your preferred method for " + \
                "inputting a linear system:"
        )
    ),
    ui.nav_panel(
        "Determinant Calculator",
        page_title("Determinant Calculator"),
        matrix_input.matrix_input_ui("determinants")
    ),
    title = "Linear Algebra Calculator"
)

# Outputs are held in a server function. UI components that depend on inputs
# are updated in the server function.

def server(input: Inputs, outputs: Outputs, session: Session):
    matrix_input.matrix_input_server(
        "ref_and_rref"
    )

    matrix_input.matrix_input_server(
        "linear_systems", 
        column_num_meaning = "variables",
        row_num_meaning = "equations",
        column_name_choice = True,
        column_name_meaning = "variable",
        manual_entry_label = "Enter your system into the augmented matrix " + \
            "below." + \
            " Your coefficients should either be entered as" + \
            ' numbers or fractions of the format "a/b".',
        csv_entry_label = "Upload a CSV file containing the augmented matrix"+\
                " for your system. The top row must contain a unique name " +\
                "for the variable that each column represents. The " + \
                "augmented column does not need a name and can be left " + \
                "blank in " + \
                " the top row. The last column in your file will " + \
                " be assumed to be the augmented column. The " + \
                "coefficients in the matrix should be written as " +\
                'integers, decimals, or fractions of the format "a/b".'
    )

    matrix_input.matrix_input_server(
        "determinants",
        square_matrix = True,
        csv_entry_label =  "Your file should consist of integers, decimals" +\
                        "or fractions " + \
                        " of the format \"a/b\". It must hold a square " + \
                        " matrix, meaning that the number of rows and " + \
                        "columns should match."
    )

# An app object that actually runs the app is created. 
app = App(app_ui, server)