import numpy as np
import pandas as pd
import matrix_input
import calculation_output
import linear_systems
import calculations

from shiny import App, Inputs, Outputs, Session, render, ui
    
def page_title(title):
    '''
    This function handles the output for page titles to be displayed at the top
    of nav_panels. 
    Args:
        title: a string that is the title to be displayed.
    Returns:
        a ui.column component holding the title of a nav_panel with a larger
        font.
    '''
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

# The nav_panel contents in this UI are mostly created using modules. Modules
# allow you to create a subsection of an app that can be reused. Like the 
# main ui, they have a ui function and a server function. IDs used in a module
# are independent of other modules (including repeats of themselves), and of
# the main app. When they are called, their first input is a string naming the
# module. For each module, its ui section should be called in the creation of
# app_ui with name exactly matching a call to the server section in the server
# function.

app_ui = ui.page_navbar(
    # This first panel will be explained. Other panels follow the same
    # structure.
    ui.nav_panel(
        "Reduced Row Echelon and Row Echelon Form Calculator",
        page_title(
            "Reduced Row Echelon and Row Echelon Form Calculator"
        ),
        # The module to handle matrix input for this nav_panel is added.
        matrix_input.matrix_input_ui("ref_and_rref_input"),
        # The module to handle calculation output for this nav_panel is added.
        calculation_output.calculation_output_ui(
            "ref_and_rref_output",
            # The text to be displayed on the button triggering calculations
            # is passed to this module.
            calculate_button_label = "Row Reduce Matrix"
        )
    ),
    ui.nav_panel(
        "Linear System Solver",
        page_title(
            "Linear System Solver"
        ),
        matrix_input.matrix_input_ui(
            "linear_systems_input",
            input_method_label = "Choose your preferred method for " + \
                "inputting a linear system:"
        ),
        calculation_output.calculation_output_ui(
            "linear_systems_output",
            calculate_button_label = "Solve Linear System"
        )
    ),
    ui.nav_panel(
        "Determinant Calculator",
        page_title("Determinant Calculator"),
        matrix_input.matrix_input_ui("determinants_input"),
        calculation_output.calculation_output_ui(
            "determinants_output",
            calculate_button_label = "Calculate Determinant"
        )
    ),
    ui.nav_panel(
        "Inverse Matrix Calculator",
        page_title("Inverse Matrix Calculator"),
        matrix_input.matrix_input_ui("inverse_input"),
        calculation_output.calculation_output_ui(
            "inverse_output",
            calculate_button_label = "Calculate Inverse"
        )
    ),
    title = "Linear Algebra Calculator"
)

# Outputs are held in a server function. UI components that depend on inputs
# are updated in the server function.

def server(input: Inputs, outputs: Outputs, session: Session):

    # The server part of the matrix_input module for each nav_panel is called
    # and its outputs are stored.
    ref_and_rref_input_tuple = matrix_input.matrix_input_server(
        "ref_and_rref_input"
    )

    linear_systems_input_tuple = matrix_input.matrix_input_server(
        "linear_systems_input", 
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
                'integers, decimals, or fractions of the format "a/b".',
        augmented_column = "True",
        augmented_column_name = "Constant"
    )

    determinants_input_tuple = matrix_input.matrix_input_server(
        "determinants_input",
        square_matrix = True,
        csv_entry_label =  "Your file should consist of integers, decimals" +\
                        " or fractions " + \
                        " of the format \"a/b\". It must hold a square " + \
                        " matrix, meaning that the number of rows and " + \
                        "columns should match."
    )

    inverse_input_tuple = matrix_input.matrix_input_server(
        "inverse_input",
        square_matrix = True,
        csv_entry_label =  "Your file should consist of integers, decimals" +\
                        " or fractions " + \
                        " of the format \"a/b\". It must hold a square " + \
                        " matrix, meaning that the number of rows and " + \
                        "columns should match."
    )

    # The server component of the calculation_output module for each nav_panel
    # is called and values outputted from the matrix_input modules are passed
    # to them. Additionally, objects containing calculation functions whose
    # output will be displayed in a nav_panel along with other attributes
    # associated with these functions are passed to the server component of
    # this module for each nav_panel.
    calculation_output.calculation_output_server(
        "ref_and_rref_output",
        ref_and_rref_input_tuple[0],
        ref_and_rref_input_tuple[1],
        calculation_output.Output_Function(
            "Row Echelon Form",
            True,
            calculations.row_echelon_form
        ),
        calculation_output.Output_Function(
            "Reduced Row Echelon Form",
            True,
            calculations.reduced_row_echelon_form
        )
    )

    calculation_output.calculation_output_server(
        "linear_systems_output",
        linear_systems_input_tuple[0],
        linear_systems_input_tuple[1],
        calculation_output.Output_Function(
            "Solution",
            True,
            linear_systems.solution_set
        ),
        calculation_output.Output_Function(
            "Solution in Parametric Vector Form",
            True,
            linear_systems.parametric_vector_solution_set
        )
    )

    calculation_output.calculation_output_server(
        "determinants_output",
        determinants_input_tuple[0],
        determinants_input_tuple[1],
        calculation_output.Output_Function(
            "Determinant",
            False,
            calculations.determinant
        )
    )

    calculation_output.calculation_output_server(
        "inverse_output",
        inverse_input_tuple[0],
        inverse_input_tuple[1],
        calculation_output.Output_Function(
            "Inverse Matrix",
            True,
            calculations.inverse
        )
    )

# An app object that actually runs the app is created. 
app = App(app_ui, server)