'''
Important: tomorrow change this to handle outputs as a whole but make separate
module for displaying each individual output. Do this by outputting modules
with single matrix outputs using list comprehension.
'''

import numpy as np
import pandas as pd
import matrix_input
import calculations

from shiny import App, Inputs, Outputs, Session, render, ui, module, reactive

from format import spaced_section_express as spaced_section, \
spaced_section_core

# Create class that holds a function and has a property indicating the label
# for the output and whether the output will be a number or a pandas DataFrame

class Output_Function:

    def __init__(self, output_label, returns_frame, inner_function):
        self.output_label = output_label
        self.returns_frame = returns_frame
        self.inner_function = inner_function

@module.ui
def calculation_output_ui(calculate_button_label):
    '''
    This function displays the outputs of the calculations performed in a
    nav_panel in the main app.
    Args:
        calculate_button_label: A string outlining the text that will be
        contained in the button that triggers a calculation when pressed.
    Returns:
        a ui.column component
        holding all of the output calculationr results.
    '''
    return ui.column(
        12,
        spaced_section_core(
            # This button triggers the calculation outputs to render. They are
            # controlled by a button because calculations are somewhat large
            # functions that should only be run when the user indicates that
            # their input is ready.
            ui.input_action_button(
                "perform_calculation",
                calculate_button_label,
                style = "background-color: #AFE1AF;"
            )
        ),
        # This displays the ui defined by the display_outputs function in the
        # server section of this module. This function is written using shiny
        # express rather than shiny core.
        ui.output_ui("display_outputs")
    )

@module.server
def calculation_output_server(
    input, 
    output,
    session,
    input_matrix,
    output_decimal,
    *output_functions,
    square = False
):
    '''
    This function defines the parts of the calculation_output module that
    depend on user input and can change.
    Args:
        input, output, session: arguments necessary for all server functions in
        shiny that do not actually need to be passed to them when they are
        called.
        input_matrix: a reactive.Value object holding a reactive.Value object
        holding a DataFrame representing the user-inputted matrix.
        output_decimal: a reactive.Value object holding a string that is either
        equal to "decimal" or "fraction".
        *output_functions: Output_Function objects holding the functions whose
        outputs should be displayed in the UI that take in the user-inputted
        matrix from the nav_panel this module is used in.
    Returns:
        None
    '''

    # This function is read interactively like in Shiny Express. It is used to
    # output the results of calculations performed in the nav_panel this module
    # is in, once the button to trigger the calculation is pressed.
    @render.express
    @reactive.event(input.perform_calculation)
    def display_outputs():

        # The inputted matrix in the reactive.Value object in the Value object
        # assigned to input_matrix_value is accessed. This is why there are two
        # invocations.
        input_matrix_value = input_matrix()()

        # This is True if the output is a decimal and False otherwise.
        output_decimal_value = output_decimal.get() == "decimal"

        # The only case where there is no input matrix is when the user did not
        # add a CSV file. The reason for this is that if the user chooses
        # manual entry, the input matrix will automatically be created.
        if input_matrix_value.empty:
            "You have not yet added your input CSV file. Please add that file "
            "before performing this calculation."
            return
        
        # This checks if the user entered a non-square matrix for a function
        # that requires a square matrix. If they did, an error will show.
        if square and not input_matrix_value.shape[0] == \
            input_matrix_value.shape[1]:
            "You did not enter a square matrix as the number of columns in "
            "the matrix in your CSV file differed from the number of rows."
            return
        
        # It is checked that every column name is unique. Since the
        # matrix_input module sets the augmented column to the augmented name,
        # it is not necessary to check if the augmented column name was used as
        # a variable name, as if it was, then that name will not be unique. So
        # augmented_column_name is set to None, so that no columns will match
        # with it.
        invalid_column_error = \
            calculations.column_names_valid(
                input_matrix_value.columns,
                None
            )
        
        # This returns a DataFrame with one column named "" if
        # there are no repeats.
        if invalid_column_error.columns[0] != "":

            # Normally this outputs an error matrix. But here it is only
            # necessary to output the error specified in the first column name
            # of the error matrix.
            invalid_column_error.columns[0]

            return
      
        # For every Output_Function in output_functions, a module to display
        # the output of the inner function held in the Output_Function is
        # called. Each calculation output is handled in its own module so that
        # duplicate IDs are not an issue and because based on trial and error,
        # @render.data_frame functions do not seem to work in a for loop, but
        # rather run after the for loop. Module calls, on the other hand, do
        # work in a for loop.
        for i in range(len (output_functions)):
            
            # The result of the output_functions[i]'s inner function is
            # calculated.
            output_calculation = output_functions[i].inner_function(
                input_matrix_value,
                output_decimal_value
            )

            # A single_output_ui module written in Shiny Core is called. Its
            # name is based on the function number (i) so that it is unique and
            # whether it returns a frame or text to be outputted is determined
            # by the returns_frame property of the current Output_Function
            # object.

            if output_functions[i].returns_frame:

                # If the output returns a frame, it is checked if that frame is
                # empty.
                single_output_ui(
                    "Output_Calculation_" + str(i),
                    True,
                    output_calculation.empty
                )

            else:
                # If the output does not return a frame, no value is passed for
                # the parameter about whether the output frame is empty.
                single_output_ui(
                    "Output_Calculation_" + str(i),
                    False
                )

            # The server side component of the output module for this
            # calculation is created with a name that matches the ui side
            # component for this iteration of the for loop.
            single_output_server(
                "Output_Calculation_" + str(i),
                output_label = output_functions[i].output_label,
                output_calculation = output_calculation
            ) 

@module.ui
def single_output_ui(returns_frame, frame_empty = False):
    '''
    This function defines the ui component of specific calculation outputs. It
    either displays an output matrix with an option to download it or output
    text.
    Args:
        returns_frame: a boolean set to True if the output should display a
        data_frame and False if it should display text.
        frame: empty is a boolean set to true if the output frame is empty.
        This variable is only applicable if returns_frame is True.
    Returns:
        a ui.column component holding either the output frame and a download
        button or output text.
    '''

    # This defines the ui output if a data_frame should be outputted.
    if returns_frame and not frame_empty:
        return ui.column(
            12,
            # Unlike output_text, output_text_verbatim surrounds text in gray
            # box.
            spaced_section_core(
                ui.output_text_verbatim("display_output_label"),
                ui.output_data_frame("display_output_frame")
            ),
            ui.download_button(
                id = "download_output_matrix",
                label = "Download Results",
                style = "background-color: #AFE1AF;"
            )
        )
    
    # The download button will not appear if the returned frame is emtpy.
    # Usually this is the case when the returned frame describes an error.
    elif returns_frame:
        return ui.column(
            12,
            # Unlike output_text, output_text_verbatim surrounds text in gray
            # box.
            spaced_section_core(
                ui.output_text_verbatim("display_output_label"),
                ui.output_data_frame("display_output_frame")
            )
        )
    
    # This defines how to display calculation output when the output is text.
    else:
        return ui.column(
            12,
            spaced_section_core(
                ui.output_text_verbatim("display_output_label"),
                ui.output_text("display_output_text")
            )
        )
    
@module.server
def single_output_server(
    input, 
    output,
    session,
    output_label,
    output_calculation
):
    
    '''
    This function defines the server aspects of the single_output module, such
    as DataGrid outputs, text outputs, and the option to download DataGrids.
    Args: 
        input, output, session: Arguments necessary for all server functions in
        shiny that do not actually need to be passed to them when they are
        called.
        output_label: A string that is a label to be displayed above a
        calculation output.
        output_calculation: A result of a calculation that will either be
        displayed as a matrix or as text. Multiple types will be passed here
        such as Fractions, Decimals, and pd.DataFrames.
    '''

    # This function label each calculation output, whether it is text or a
    # matrix.
    @render.text
    def display_output_label():
        return output_label
    
    # This function outputs calculations that return DataFrames.
    @render.data_frame
    def display_output_frame():

        # Calculation functions only return an empty DataGrid if there is some
        # error with the user's entry. When this is the case, the error will be
        # displayed in the title of the first column of the empty matrix.
        if output_calculation.empty:
            return render.DataGrid(
                data = output_calculation
            )

        # Some calculation functions set the column titles of the output matrix
        # while others do not. No function that sets column titles sets the
        # first column to the int 0. So the columns will only be set here if
        # the first column in the output_calculation DataFrame is equal to 0.

        if output_calculation.columns[0] == 0:
            column_titles = []

            # Each column is numbered.
            for i in range(len(output_calculation.columns)):
                column_titles.append("Column" + str(i + 1))

            # The output matrix's columns are set to the new column names.
            output_calculation.columns = column_titles

        return render.DataGrid(
            data = output_calculation,
            width = "80%"
        )
     
    # This function display's calculations whose outputs are displayed as text.
    @render.text
    def display_output_text():
        return output_calculation
    
    # This function handles the downloading of output DataFrames.
    @render.download(filename = output_label + ".csv")
    def download_output_matrix():

        # To create the download file line by line, Shiny requires that the
        # download function yield each line in the file.
        for line in calculations.file_generator_from_frame(output_calculation):
            yield line