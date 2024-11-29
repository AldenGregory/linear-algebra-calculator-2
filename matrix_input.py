import numpy as np
import pandas as pd
import calculations

# Mostly express will be used in this module for the spaced_section function.
from format import spaced_section_express as spaced_section, \
    spaced_section_core

from shiny import App, Inputs, Outputs, Session, render, ui, module, \
    reactive

# This module defines the ui that will be displayed to the user as they enter
# their matrix. It acts similarly to the ui section of an app.
@module.ui
def matrix_input_ui(
    input_method_label = \
        "Choose your preferred method for inputting a matrix."
):
    '''
    This function defines the ui for user inputs in a nav_panel. These involve
    options for how the user wants to input their matrix and ways for the user
    to input their matrix.
    Args: 
        input_method_label: A label that will display above the option of
        whether to input a matrix manually or with a CSV file.
    Returns:
        a ui.column component holding the ui that allows the user to input
        their matrix.
    '''
    # A column taking up the whole width is returned.
    return ui.column(
        12,
        # The items below allow the user to select how they want numbers to be
        # outputted and how they want to input their matrix.
        spaced_section_core(
            "Choose your preferred output number format:"
        ),
        ui.input_radio_buttons(
            id = "number_format",
            label = "",
            choices = {"decimal": "Decimal", "fraction": "Fraction"}
        ),
        spaced_section_core(
            input_method_label
        ),
        ui.input_radio_buttons(
            id = "input_method",
            label = "",
            choices = {"CSV": "CSV File", "Manual": "Manual Entry"}
        ),
        # These two components render depending on inputs and therefore have
        # behavior defined in the @module.server function.
        ui.output_ui("display_manual_choices"),
        ui.output_ui("display_input")
    )

@module.server
def matrix_input_server(
    input, 
    output, 
    session,
    square_matrix = False,
    column_num_meaning = "Columns",
    row_num_meaning = "Rows",
    column_name_choice = False,
    column_name_meaning = "column",
    manual_entry_label = \
        "Enter your values into the matrix below (all entries " + \
        'must  be numbers or fractions of the format "a/b"):',
    csv_entry_label = \
        "Add a CSV file holding your matrix. Your file should " + \
        "consist of integers, decimals, or fractions of the " + \
        "format \"a/b\".",
    augmented_column = False,
    augmented_column_name = None
):
    '''
    This function defines the server function for the matrix_input module and
    changes its ui based on user input.
    Args:
        input, output, session: Arguments necessary for all server functions in
        shiny that do not actually need to be passed to them when they are
        called.
        square_matrix: A boolean that is True if the user input has to be
        square and False otherwise.
        column_num_meaning: A string specifying what the number of columns
        represents the number of. For example, in a linear system the number of
        columns represents the number of variables. This string should be
        capital and plural, so in the case of linear systems,
        column_num_meaning would be set to "Variables"
        row_num_meaning: A string specifying what the number of rows represents
        the number of. For example, in a linear system, the number rows
        represents the number of equations. This should be capital and plural
        so for linear systems this would be set to "Equations".
        column_name_choice: A boolean that is True if the user gets to choose
        column names in the input matrix and False otherwise.
        column_name_meaning: A string representing what a column name is a name
        for. This should be lower case and singular. So in the case of linear
        systems, this parameter would be set to "variable".
        manual_entry_label: A string representing the label that should display
        above an input matrix in the nav_panel this module is in.
        csv_entry_label: A string representing the label that should display
        above a CSV file input section in the nav_panel this module is in.
        augmented_column: a boolean that is True if there is an augmented
        column in the input matrix and False otherwise.
        augmented_column_name: a string holding the name that will be given to
        the augmented column of the input matrix.
    Returns:
        a tuple where the first item is a reactive.Value object holding a
        reactive.Value object holding a pandas DataFrame holding the user's
        input matrix and the second item is a reactive.Value object holding a
        string that is either "decimal" or "fraction" depending on the type of
        output the user prefers.
    '''
    # A reactive value, return_matrix, for the user's input matrix will be
    # returned as a way of passing the input matrix from this module to the
    # outer app. 

    # For manual input, return_matrix should hold a data_view which is itself a
    # reactive value. It cannot hold the value held in data_view as based on
    # trial and error, this can cause errors when the program tries to access
    # the value in data_view using data_view() before it has been set.

    # Additionally, data_view itself is reactively updated, but if
    # return_matrix were set to the value held in data_view, changing data_view
    # would not affect the reactive variable value of return_matrix already
    # returned outside of  this function, as the value inside data_view is not
    # reactive.
    # Outside the function there would only be a reactive.Value
    # object holding some number specified by data_view() at the time
    # return_matrix was returned. An int is immutable, so the value in the
    # reactive.Value object would never change.

    # So return matrix is  initially set to a reactive value holding a reactive
    # value holding 
    # an empty DataFrame. The reason it holds a reactive value in a reactive
    # value, is that based on trial and error, once the server function is
    # called, it returns
    # return_matrix before its inner functions are called. If return_matrix
    # were simply a reactive value and were to be set to another reactive
    # value when the input method changes, or a new CSV file is added,
    # return_matrix would be affected by being set to a new object, but
    # the Value object that was already returned would not be affected. So
    # by wrapping a reactive value in a reactive value, and setting the outer
    # reactive value to a different inner reactive value upon input updates,
    # it is possible for updates to return_matrix to effect the reactive value
    # returned by the server module outside of the server module.
    
    # A reactive value in a reactive value is only necessary for manual input
    # since data_view is a reactive value, but it is done in all cases since
    # other functions will treat the output of the server function as a
    # reactive value in a reactive value.
    return_matrix = reactive.value(reactive.value(pd.DataFrame()))

    # This function is kept separate from display_input as based on trial and
    # error, shiny does not allow an input to be used in the same function it
    # is created. When this occurs, it will not render anything in the
    # function. This is true for express functions. It will only display
    # something if the user chooses to manually enter their matrix.
    @render.express
    def display_manual_choices():

        if input.input_method() == "Manual":

            # Square matrices only have one dimension input since they're both
            # the same. Otherwise there are two dimension inputs.
            if square_matrix:
                spaced_section(
                    ui.input_numeric(
                        id = "dimension",
                        label = "Dimension of Square Matrix",
                        value = 1, 
                        min = 1
                    )
                )
            
            # Rather than displaying number of rows and columns, the user will
            # be prompted to input the number of whatever the rows and columns
            # mean.
            else:
                spaced_section(
                    ui.input_numeric(
                        id = "row_number",
                        label = "Number of " + row_num_meaning.capitalize(),
                        value = 1, 
                        min = 1
                    ),
                    ui.input_numeric(
                        id = "column_number",
                        label = "Number of " + column_num_meaning.capitalize(),
                        value = 1, 
                        min = 1
                    )
                )
    
    # This function written in shiny express contains the ui components
    # necessary for the user to input their matrix.
    @render.express
    def display_input():
        if input.input_method() == "Manual":

            row_number = 0
            column_number = 0

            # The row number and column number are set based on whether or not
            # the matrix is square.
            if square_matrix:
                row_number = input.dimension()
                column_number = input.dimension()

            else:
                row_number = input.row_number()
                column_number = input.column_number()
            
            # If the user gets to choose the column names, a DataGrid where
            # they can enter column names will be rendered.
            if column_name_choice:

                # For uses of column_name_meaning, what column names are names
                # for, where the meaning should be capitalized, capital meaning
                # is created.
                capital_meaning = column_name_meaning.capitalize()

                # A label for the column_name_input is created.
                spaced_section(
                    ("Enter your {} names from first " +
                    "to last below or leave the default names. " +
                    "{}  names must be  unique.").format(
                        column_name_meaning, capital_meaning)
                )

                # The column_name_input function is made global so that its
                # user-entered column names can be used for the actual input
                # matrix.
                global column_name_input

                # This function displays a DataGrid that lets users change
                # column names.
                @render.data_frame
                def column_name_input():
                    column_name_array = np.full(
                        (column_number, 1), 
                        ""
                    )

                    # The type of this numpy array must be reset, as
                    # the strings added to it are "" so the array's
                    # type
                    # is set to U1. But the column names have multiple
                    # characters so U1 will not work. U is a unicode 
                    # datatype and the number that follows is how many
                    # characters it can hold.

                    # The longest default column name will be one
                    # higher than the highest column number, so the
                    # numpy type will be set to U + that number.

                    longest_column_name_length = 1 + \
                    len(str(column_number))

                    column_name_array = np.astype(
                        column_name_array,
                        "U" + str(longest_column_name_length)
                    )

                    # This dictionary specifies the subscript version
                    # of each digit.
                    subscript_numbers = {"0": "\u2080", 
                                            "1" : "\u2081",
                                            "2" : "\u2082",
                                            "3": "\u2083",
                                            "4": "\u2084",
                                            "5": "\u2085",
                                            "6": "\u2086",
                                            "7": "\u2087",
                                            "8": "\u2088",
                                            "9": "\u2089",}
                    
                    # From the dictionary, the maketrans method makes a
                    # translation table that works with the translate
                    # method.
                    subscript_translator = str.maketrans(
                        subscript_numbers
                        )
                    for i in range(0, column_number):
                        
                        # Column numbers strings are translated to
                        # subscript numbers using the subscript_numbers
                        # dictionary.

                        name = "x" + str(i + 1).translate(
                            subscript_translator
                            )

                        column_name_array[i, 0] = name

                    column_entry_frame = pd.DataFrame(
                            data = column_name_array
                            )
                    
                    # The column label at the top of this 1 column DataGrid is
                    # set here.
                    column_entry_frame.columns = \
                        [capital_meaning + " Names"]

                    return render.DataGrid(
                        data = column_entry_frame,
                        editable = True
                    )
            
            # The label for the manual entry table is displayed.
            navigation_instructions = "To move to the right in "+\
            "the input table, press tab. To move to the left press, shift " + \
            "+ tab. To move down press enter. To move up press shift " + \
            "+ enter. " 

            spaced_section(navigation_instructions)

            spaced_section(manual_entry_label)

            # This function displays the actual input matrix to the user.
            @render.data_frame
            def input_matrix():

                column_names = []

                # Column names is either set to the user-chosen names or
                # default names of the form: Column 1, Column 2, etc...
                if column_name_choice:
                    
                    # The columns of the system_frame panda will be set
                    # to column_names. The user enters the variable 
                    # names vertically, so the panda containing their 
                    # entry is first converted to a 2d numpy array with
                    # 1 column, then transposed meaning that its rows
                    # and columns are switched. This means that the
                    # variable names are now horizontal in a 2d numpy
                    # array where the first row contains every variable
                    # name. To access the 1d list of variable names,
                    # index 0 of this 2d array is accessed. Then, since
                    # the columns attribute of DataFrame is a list, the
                    # array is converted to a list. Lastly, the column
                    # title "Constant" is appended to the list because
                    # the entry matrix is augmented with the equations'
                    # solutions.
                    column_names = np.transpose(
                        column_name_input.data_view().to_numpy()
                    ).tolist()[0] 

                else:
                    for i in range(column_number):
                        # The column number is one higher than the index in
                        # the range.
                        column_names.append("Column " + str(i + 1))
                
                if column_name_choice and augmented_column:
                    # It is checked that every column name is unique.
                    repeat_column_error = \
                        calculations.column_names_valid(
                            column_names,
                            augmented_column_name
                        )
                    
                    # This returns a DataFrame with one column named "" if
                    # there are no repeats.
                    if repeat_column_error.columns[0] != "":
                        return render.DataGrid(
                            data = repeat_column_error,
                            width = "80%"
                        )
                    
                    # The augmented column is added if there is one.
                    if augmented_column:
                        column_names.append(augmented_column_name)
                    

                # In case something has been appended onto column names,
                # the column number depends on the length of column names
                # rather than the variable column_number.
                matrix_array = np.full(
                    (row_number, len(column_names)),
                    0
                )

                matrix_frame = pd.DataFrame(data = matrix_array)

                matrix_frame.columns = column_names

                return render.DataGrid(
                    data = matrix_frame,
                    editable = True,
                    width = "80%"
                )

            # The set function returns True, so to prevent shiny express from
            # displaying its output interactively is assigned to a variable.
            holder = return_matrix.set(input_matrix.data_view)

        # The following code is reached when the input type is a CSV file.
        else:
            spaced_section(
                csv_entry_label
            )

            ui.input_file("matrix_input", "Add your CSV file here:",
                            accept = ["csv"], multiple = False)

    # The user-inputted matrix is returned. It will either be a panda or None.
    # Additionally, the input number format, either "Decimal" or "Fraction"
    # will be returned.

    @reactive.effect
    def update_return_csv():

        # If the input type is a CSV file, then the return_matrix value should
        # be updated whenever a new CSV file is added. This function depends on
        # the reactive value, matrix_input, which changes whenever a new file
        # is uploaded, invalidating this function and causing it to run again.
        # So return_matrix is reset whenever a new file is added.
        if input.input_method() == "CSV" and input.matrix_input() != None:
            
            # The user will only enter column names as a header if they get to
            # choose column names. In that case the header will be set to row
            # 0. Otherwise, there will be no header.

            header = None

            if column_name_choice:
                header = 0

            updated_matrix = \
                pd.read_csv(
                    input.matrix_input()[0]["datapath"],
                    header = header
                )
            
            # When there is an augmented column, the user will enter the values
            # for that column but should not enter a header. If they do that
            # header will be disregarded and set to the augmented_column name.
            if augmented_column:

                # According to the pandas documentation, the columns attribute
                # of DataFrames are immutable pandas.Index objects. They are
                # similar to tuples, but with added functionality. To convert
                # Index objects to a list, the method to_list can be used.
                columns_list = updated_matrix.columns.to_list()

                columns_list[len(columns_list) - 1] = \
                    augmented_column_name
                
                updated_matrix.columns = columns_list

            # return_matrix is set to a reactive value holding the updated
            # matrix.
            return_matrix.set(reactive.value(
                updated_matrix
            ))

    return return_matrix, input.number_format