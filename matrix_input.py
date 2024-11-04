import numpy as np
import pandas as pd

# Mostly express will be used in this module for the spaced_section function.
from format import spaced_section_express as spaced_section, \
    spaced_section_core

from shiny import App, Inputs, Outputs, Session, render, ui, module, \
    reactive, express

# This module defines the ui that will be displayed to the user as they enter
# their matrix. It acts similarly to the ui section of an app.
@module.ui
def matrix_input_ui(
    input_method_label = \
        "Choose your preferred method for inputting a matrix."
):
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
        "format \"a/b\"."
):
    
    # A reactive value for the user's input matrix will be returned as a way
    # of passing the input matrix from this module to the outer app. It is 
    # initially set to None, so if this value is set to None when it is used
    # in some other module or the larger app, it should indicate that the user
    # did not upload a file.
    return_matrix = reactive.value(None)

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

            # The input_matrix function is made global so that the
            # return_matrix can be set to the user-entered values in the
            # DataGrid.
            global input_matrix
            
            spaced_section(manual_entry_label)

            # This function displays the actual input matrix to the user.
            @render.data_frame
            def input_matrix():

                column_names = []

                # Column names is either set to the user-chosen names or
                # default names of the form: Column 1, Column 2, etc...
                if column_name_choice:

                    column_names = np.transpose(
                        column_name_input.data_view().to_numpy()
                    ).tolist()[0] 

                else:
                    for i in range(column_number):
                        # The column number is one higher than the index in
                        # the range.
                        column_names.append("Column " + str(i + 1))
                
                if column_name_choice:
                    # It is checked that every column name is unique.
                    repeat_column_error = \
                        column_names_unique(
                            column_names
                        )
                    
                    # This returns a DataFrame with one column named "" if
                    # there are no repeats.
                    if repeat_column_error.columns[0] != "":
                        return render.DataGrid(
                            data = repeat_column_error,
                            width = "80%"
                        )
                    
                    # So far column_name_choice is only available for
                    # linear systems and in this case, the augmented column
                    # is named constant. This likely will be changed later.
                    column_names.append("Consant")

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

        # The following code is reached when the input type is a CSV file.
        else:
            spaced_section(
                csv_entry_label
            )

            ui.input_file("matrix_input", "Add your CSV file here:",
                            accept = ["csv"], multiple = False)

    # In this function, return_matrix is set to whatever the user entered.
    @reactive.effect
    def set_return_matrix():
        if input.input_method() == "CSV" and input.input_file != None:
            # File inputs return a list of dictionaries where
            # each dictionary corresponds with a file. Since
            # there is only one file, index 0 of the list is
            # accessed.
            return_matrix.set(input.input_file()[0]["datapath"])

        elif input.input_method() == "Matrix":
            return_matrix.set(input_matrix.data_view())

    # The user-inputted matrix is returned. It will either be a panda or None.
    return return_matrix   
                    

def column_names_unique(column_names):
    '''
    This function finds if every column name in column_names is unique.
    Args:
        variable_names: a list of variable names that are strings.
    Returns:
        a panda DataFrame explaining the error if variable names are repeated
        and None if they are not.
    '''

    # Sets are like dictionaries without values or like lists without allowing
    # repeats or having an order. They use add method for addition rather than 
    # a key name like with dictionaries or append like with lists.
    occured_name_set = set()

    repeat_frame = pd.DataFrame()

    repeat_frame[""] = []

    for column_name in column_names:
        if column_name in occured_name_set:

            # inplace means the original DataFrame is modified rather than
            # a copy.
            repeat_frame.rename(
                columns = {"": "You used the same name \
                multiple times which is not allowed. Please\
                edit your names."},
                inplace = True
            )
                        

            return repeat_frame
        
        else:
            occured_name_set.add(column_name)

    if "Constant" in occured_name_set:

        # inplace means the original DataFrame is modified rather than
        # a copy.
        repeat_frame.rename(
            columns = {"": 'You cannot use the name \
            "Constant". Please change that name.'},
            inplace = True
        )
        
        return repeat_frame

    return repeat_frame