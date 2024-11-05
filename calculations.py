import pandas as pd
import numpy as np

from fractions import Fraction
from decimal import Decimal

# This class makes it possible to hold matrices in DataFrames that keep track
# of row swaps since the original matrix. This class is primarily designed to
# be used within the calculations.py file. It is also only used for matrices
# where it is necessary to keep track of row swaps.

class Matrix(pd.DataFrame):
    row_swaps_from_original = 0

def row_echelon_form(matrix, output_decimal = False):
    '''
    The purpose of this function is to convert a user-entered matrix to a
    row equivalent matrix in row echelon form.
    Args:
        matrix - A panda DataFrame that holds the matrix entered by the user.
        The type of elements within the DataFrame may vary.
        output_decimal - a boolean that is true if the user wants the output
        matrix to have decimals rather than fractions
    Returns:
        A panda DataFrame that holds a matrix in row echelon form that is row
        equivalent to the matrix entered by the user.
    '''

    matrix = matrix.astype(object)

    # The matrix is converted to floats so that it can be created to a numpy
    # array of floats that can have math done on it.
    all_decimals = convert_to_fractions(matrix)

    # If the matrix is not all fractions, an error DataFrame is returned.
    if not all_decimals:

        empty = np.array([])

        error_frame = Matrix(empty)

        error_frame.columns = ["At least one of the entries in\
        your matrix is not a valid number."]

        return error_frame

    # The DataFrame is converted to numpy array so math can be done on it.
    matrix_array = matrix.to_numpy()

    # corner_row and corner_column are the row and column of the portion of the
    # matrix currently being reduced to row echelon form

    total_row_swaps = 0

    corner_row = 0

    corner_column = 0

    # The operations to row reduce this matrix to echelon form are performed in
    # this while loop. Each time a column is filled with zeros below the pivot
    # position, the corner is moved one down and one to the right.
    # Each time there is a zero column, the corner is moved one ot the right.
    # Once the corner is outside the matrix, the while loop ends. 
    while corner_row < matrix_array.shape[0] and corner_column < \
        matrix_array.shape[1]:

        zero_column = False

        # The code below brings the row with the highest value in the corner
        # column to the corner row to reduce errors associated with large
        # numbers caused by multiplying rows by ratios above 1.

        i = corner_row + 1

        # This while loop finds the row that has the highest absolute value in
        # the corner_column.

        max_row = corner_row

        while i < matrix_array.shape[0]:

            if fraction_absolute_value(matrix_array[i][corner_column]) > \
                fraction_absolute_value(matrix_array[max_row][corner_column]):
                max_row = i
            
            i += 1

        # The first row with is switched with the row having the highest
        # absolute value in corner_column.

        if max_row != corner_row:
            total_row_swaps += 1

        temp = matrix_array[max_row].copy()

        matrix_array[max_row] = matrix_array[corner_row]

        matrix_array[corner_row] = temp

        # If the max row has 0 in its corner_column then the column is a zero
        # column
        if matrix_array[corner_row][corner_column] == 0:
            zero_column = True
            
            # The pivot position within the corner row is moved one to the
            # right

            corner_column += 1

        # This if statement brings all rows entries in the corner column below
        # that of the corner row to zero. This is only possible if the column
        # is not a zero column.
        if not zero_column:           
            
            corner_num = matrix_array[corner_row, corner_column]

            # This for loop brings every entry in the corner column below the
            # corner row to zero.
            for i in range(corner_row + 1, matrix_array.shape[0]):
                
                ratio = matrix_array[i, corner_column] / corner_num

                matrix_array[i] += -1 * ratio * matrix_array[corner_row]

            # The corner row is moved one down and the column is moved one to
            # the right.
            corner_row += 1
            corner_column += 1

    if output_decimal:
        convert_fractions_to_decimal(matrix_array)

    ref_matrix = Matrix(
            data = matrix_array
        )
    
    ref_matrix.row_swaps_from_original = total_row_swaps

    return ref_matrix

def convert_to_fractions(matrix):
    '''
    The purpose of this function is to convert every element of a matrix to
    fractions. It also returns true or false depending on if the matrix values
    are all possible to convert to fraction.
    Args:
        matrix - a panda DataFrame consisting of entries that vary in type.
        The elements of this DataFrame correspond to a user entered matrix.
    Returns:
        a boolean that is True if the matrix elements can be converted to
        fractions and false otherwise or if the matrix is empty.
    '''

    if matrix.empty:
        return False

    # This loop attempts to convert every element of the matrix to a float. If
    # there is an error in this process, the function will return false
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):

            # The entry is made into a string so that the fractin version of
            # the entry will be equal to the number the user entered rather
            # than a float directly converted to a fraction.
            entry = str(matrix.iat[i, j])

            try:
                
                # This converts fractions written with / to floats
                if str(entry).find("/") != -1:

                    divide_index = entry.index("/")

                    # A fraction can only be passed strings that can be made
                    # into ints if both the numerator and denominator are set.
                    # It can only take one argument if the number passed to it
                    # is a decimal. Because of this, in case the user entered
                    # decimals in the fraction, the numerator and denominator
                    # wll be set to fractions that are then divided.
                    numerator = Fraction(entry[:divide_index])
                    denominator = Fraction(entry[divide_index + 1:])

                    matrix.iat[i, j] = numerator / denominator

                else :
                    matrix.iat[i, j] = Fraction(entry)
                
            except:
                return False
 
    return True

def convert_fractions_to_decimal(matrix_array):
    '''
    This function converts all of the fractions in a matrix to the decimal
    type. 
    Args:
        matrix: a numpy 2d array with entries of type Fraction that holds
        a matrix
    Returns:
        None 
    '''

    for i in range(matrix_array.shape[0]):
        for j in range(matrix_array.shape[1]):
            matrix_array[i][j] = Decimal(matrix_array[i][j].numerator) / \
            Decimal(matrix_array[i][j].denominator)

def fraction_absolute_value(number):
    '''
    This function is meant to return the absolute value of a Fraction object.
    Args:
        number: an object of the Fraction class whose absolute value is being
        found
    Returns:
        a Fraction that is the absolute value of the number argument
    '''

    if number < 0:
        number *= -1

    return number

def reduced_row_echelon_form(matrix, output_decimal = False):
    '''
    The purpose of this function is to find the reduced row echelon form of
    a user-entered matrix.
    Args:
        matrix - a panda DataFrame consisting of entries that vary in type.
        The elements of this DataFrame correspond to a user entered matrix.
    Returns:
        A panda DataFrame that holds a matrix in reduced row echelon form that
        is row equivalent to the matrix entered by the user.
    '''

    # The first step of converting a matrix to reduced row echelon form is to
    # convert it to row echelon form.

    ref_matrix = row_echelon_form(matrix)

    # If the row echelon form function returns an error DataFrame because not
    # all elements of the matrix can be converted to floats, this function
    # also returns an empty DataFrame
    if ref_matrix.empty:
        return ref_matrix

    # When ref_matrix is converted to a numpy array, there is no need to
    # convert each element to a fraction since that was already done in the
    # row_echelon_form function.

    matrix_array = ref_matrix.to_numpy()

    lowest_nonzero_row = matrix_array.shape[0] - 1

    # The np.all method checks if a condition is true for every element of a
    # numpy array. The condition written as all's argument is checked for every
    # element of the array.

    # This while loop is exited once lowest_nonzero_row is the lowest row that
    # does not have all zeros. If every row is all zeros, it is exited with
    # lowest_nonzero equal to -1.

    while lowest_nonzero_row >= 0 and np.all(matrix_array[lowest_nonzero_row]
                                              == 0):
        lowest_nonzero_row -= 1

    current_row = lowest_nonzero_row

    while current_row >= 0:
        
        pivot_column = 0

        # The pivot_column in each row is the leftmost number in a row. This is
        # found by traversing through a row of the matrix from the left until 
        # a nonzero number is found.

        while matrix_array[current_row, pivot_column] == 0:
            pivot_column += 1

        # Each row should be divided by the number in its pivot column so that
        # the pivot number is 1.

        matrix_array[current_row] /= matrix_array[current_row, pivot_column]

        # All numbers in each pivot column aside from the pivot number should
        # be 0. All numbers below each pivot position are already 0 from
        # reducing to row echelon form, so the numbers in the pivot column
        # above the pivot need to be made 0

        for i in range(0, current_row):
            num_in_pivot_column = matrix_array[i, pivot_column]

            # The number in the pivot column in the current row has already
            # been set to 0. So to eliminate the number in the pivot column
            # in each row, all that is necessary is to multiply the current
            # row by the opposite of the number in row i in the pivot column
            # and add that to row i.

            matrix_array[i] += -1 * num_in_pivot_column * \
                matrix_array[current_row]

            # Due to round-off errors, entries in the pivot_column
            # above the corner row may not be exactly brought to 0. But 
            # the operation above is known to bring all of these entries to
            # 0. Other minor errors are less important, but a nonzero number
            # where there should be a zero changes the pivot positions in
            # columns, so they will manually be set to 0 to correct for these
            # errors

            matrix_array[i, pivot_column] = 0

        current_row -= 1

    if output_decimal:
        convert_fractions_to_decimal(matrix_array)

    rref_matrix = pd.DataFrame(
        data = matrix_array
        )

    return rref_matrix

def determinant(matrix, output_decimal = False):
    '''
    This function is meant to calculate the determinant of a user-entered
    matrix.
    Args:
        matrix: a pandas DataFrame holding the matrix of which the determinant 
        will be calculated.
        output_decimal: a boolean that is True if the determinant should be
        outputted as a decimal and False otherwise.
    Returns:
        The determinant of the user-entered matrix.
    '''
    if matrix.shape[0] != matrix.shape[1]:
        return "The numbers of rows and columns in your matrix do not " + \
        "match, so the determinant cannot be calculated"

    ref_matrix = row_echelon_form(matrix)

    # If the row echelon form function returns an error DataFrame because not
    # all elements of the matrix can be converted to floats, this function
    # also returns an empty DataFrame
    if ref_matrix.empty:

        # This function does not return a DataFrame so the error should be
        # returned as a string.
        return ref_matrix.columns[0]
    
    determinant = 1

    # The absolute value of the determinant is equal to the product of the 
    # elements in the diagonal once the matrix is reduced to row echelon form.
    # This is because row operations where a multiple of one row is added to
    # another do not change the determinant and switching two rows only changes
    # the sign of the determinant. Doing cofactor expansion down the first
    # column over and over leads to the product of the entries on the diagonal.
    for i in range(ref_matrix.shape[0]):
        determinant *= ref_matrix.iat[i, i]

    # Each row swap changes the sign of the determinant so this is undone here.
    determinant *= (-1) ** ref_matrix.row_swaps_from_original

    if output_decimal:
        determinant = Decimal(determinant.numerator) / \
            Decimal(determinant.denominator)
    
    return determinant

def file_generator_from_frame(input_frame):
    '''
    This generator function yields one line of a pandas DataFrame converted to
    a CSV file at a time.
    Args:
        input_frame: the panda DataFrame that will be converted to lines of a 
        CSV file
    Yields:
        a string that is the next line in the CSV file that will be created
        from input_frame
    '''

    # According to 
    # https://www.geeksforgeeks.org/use-yield-keyword-instead-
    # return-keyword-python/ yield statements are like return
    # statements for a generator functions. It works like a return
    # statement in that the function stops after each
    # yield but each time but the function can resume.
    # Generator functions work like series
    # in that when their outputs are iterated over, each time an 
    # output is used, the next yield will be returned. This means
    # that the functions works like a series but does not require
    # that everything in the series be stored at once. Basically, 
    # rather than ending a function like return, yield causes a
    # function to pause until next value generator function
    # generates is used. When function is paused its execution is 
    # stopped but its state is saved. When creating a temporary
    # file for the user to be downloaded, one line of the file is
    # yielded at a time (in the background shiny probably iterates)
    # over the output of this function to write lines to the
    # temporary file.

    input_as_array = input_frame.to_numpy()

    for row in input_as_array:
        line = ""
        for entry in row:
            line += str(entry) + ","
        
        # The last comma is removed from the line and a new line is added.
        line = line[:len(line) - 1] + "\n"

        yield line

def column_names_valid(column_names, augmented_name):
    '''
    This function finds if every column name in column_names is valid. (It is
    unique and does not share a name with the augmented column.)
    Args:
        variable_names: a list of variable names that are strings.
        augmented_name: a string that is the name of the augmented column and
        cannot be used as a column name by the user.
    Returns:
        a panda DataFrame explaining the error if columns are not valid
        and None if they are.
    '''

    # Sets are like dictionaries without values or like lists without allowing
    # repeats or having an order. They use add method for addition rather than 
    # a key name like with dictionaries or append like with lists.
    occured_name_set = set()

    valid_frame = pd.DataFrame()

    valid_frame[""] = []

    for column_name in column_names:
        if column_name in occured_name_set:

            name_error_column(
                error_frame = valid_frame,
                error_message = "The name " + column_name + " occurred " + \
                "multiple times. If you repeated this name, please " +
                "remove all repeats. Otherwise, this name will be used in " +
                "the output, so you cannot use it as a column name."
            )             

            return valid_frame
        
        elif column_name == "":

            name_error_column(
                error_frame = valid_frame,
                error_message = "One of your column names is empty. You " + \
                "cannot use blank column names. Please edit your column names."
            )

        else:
            occured_name_set.add(column_name)

    if augmented_name in occured_name_set:

        name_error_column(
            error_frame = valid_frame,
            error_message = 'You cannot use the name "' + augmented_name + \
            '". Please change that name.'
        )
        
        return valid_frame

    return valid_frame

def name_error_column(error_frame, error_message):
    '''
    This function sets the first column of the error frame to an error.
    message.
    Args:
        error_frame: an empty panda DataFrame with one column name set to ""
        error_message: a string that is the message that the column name of
        error_frame will be set to 
    Returns:
        None
    '''

    # inplace means the original DataFrame is modified rather than
    # a copy.

    error_frame.rename(
        columns = {"":  error_message},
        inplace = True
    )
