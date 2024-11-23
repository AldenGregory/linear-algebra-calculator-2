import linear_systems
import calculations
import pandas as pd
import numpy as np

def null_space_basis(matrix, output_decimal):
    '''
    This function is meant to calculate a basis for the null space of a user
    inputted matrix.
    Args:
        matrix: A pandas DataFrame holding the matrix of which the null space 
        will be calculated.
        output_decimal: A boolean that is True if the null space should be
        outputted as decimals and False otherwise.
    Returns:
        A pandas DataFrame with columns holding vectors that make up the null
        space of the inputted matrix.
    '''
    # When finding the null space of a matrix, a set vectors whose linear
    # combinations represent all possible solutions to the homogenous equation
    # constructed with vectors in the input matrix needs to be found. This can
    # be done by adding an augmented column to the input_matrix and solving for
    # the solution set of the linear system represented by that matrix in
    # parametric vector form. Since multiple subspace functions are called on
    # the same matrix, rather than modifying the original matrix it is copied.

    homogenous_system_matrix = matrix.copy()

    # A constant column with as many 0's as the number of rows in the original
    # matrix is added at the end.
    homogenous_system_matrix["Constant"] = [0] * matrix.shape[0]

    # The vectors in the parametric_vector_solution_set represent a null space
    # basis, since their linear combinations all lead to zero solutions and
    # they are linearly independent. It is possible that this will only consist
    # of one vector: a constant vector of zeros. This means the null space is
    # the zero vector.
    null_space_frame = linear_systems.parametric_vector_solution_set(
        linear_system = homogenous_system_matrix,
        output_decimal = output_decimal,
        return_vectors = True
    )

    # This occurs when there was an error when calculating the solution to the
    # homogeneous equation. So the error will be returned and displayed to the
    # user.
    if null_space_frame.empty:
        return null_space_frame

    # Column names are manually added here so that default Column 1, Column 2,
    # ... that is added in the calculation_output module is not used.

    column_names = []

    for i in range(null_space_frame.shape[1]):
        column_names.append("Vector " + str(i + 1))

    null_space_frame.columns = column_names

    return null_space_frame

def column_space_basis(matrix, output_decimal):
    '''
    This function is meant to calculate a basis for the column space of a user
    inputted matrix.
    Args:
        matrix: A pandas DataFrame holding the matrix of which the column space 
        will be calculated.
        output_decimal: A boolean that is True if the column space should be
        outputted as decimals and False otherwise.
    Returns:
        A pandas DataFrame with columns holding vectors that make up the column
        space of the inputted matrix.
    '''

    # All that matters is the pivot columns so row echelon form of the input is
    # found rather than the reduced row echelon form.
    ref_matrix = calculations.row_echelon_form(matrix, output_decimal)

    # If ref_matrix is empty an error occurred and ref_matrix holds a column
    # title explaining the error. So the error is returned.

    if ref_matrix.empty:
        return ref_matrix
    
    # The order of column_names is the same as the order of columns in
    # ref_matrix. So when a pivot column index is found in ref_matrix, the 
    # column name corresponding to that index is added to pivot_column_names.
    # Column names from the original matrix are used because the column space
    # is composed of vectors from the original matrix.
    column_names = matrix.columns
    pivot_column_names = []

    # This loop finds pivot columns using the ref_matrix.
    # It does so by finding the leftmost nonzero entry in each nonzero row.

    zero_row_reached = False
    i = 0

    while not zero_row_reached and i < ref_matrix.shape[0]:

        pivot_reached = False
        j = 0

        # The entries in row i are looped through until either a pivot position
        # is reached or the end of the row is reached.
        while not pivot_reached and j < ref_matrix.shape[1]:

            # When the first nonzero entry in a row is reached, that means
            # position i, j is a pivot position. So column j is added to the
            # list of pivot columns.

            if ref_matrix.iat[i, j] != 0:

                # The name of the column in the original matrix corresponding
                # with column j is added to the list of pivot column names.
                pivot_column_names.append(column_names[j])
                pivot_reached = True

            j += 1

        # If a pivot position was not reached in row i, row i must contain all
        # zeros. So a zero_row has been reached in this case and
        # zero_row_reached should be set to True.
        if pivot_reached == False:
            zero_row_reached = True

        i += 1  

    vector_number = 1

    column_space_matrix = pd.DataFrame()

    # Each column that makes up the column space is added to the column space
    # matrix.
    for column_name in pivot_column_names:
        column_space_matrix["Vector " + str(vector_number)] = \
            matrix[column_name]
        
        vector_number += 1

    return column_space_matrix

def left_null_space_basis(matrix, output_decimal):
    '''
    This function is meant to calculate a bass for the left null space, the
    null space for row vectors left multiplied by the user inputted matrix.
    Args:
        matrix: A pandas DataFrame holding the matrix of which the row space 
        will be calculated.
        output_decimal: A boolean that is True if the row space should be
        outputted as decimals and False otherwise.
    Returns:
        A pandas DataFrame with columns holding vectors that make up the left
        null space of the user inputted matrix.
    '''

    # The left_null_space is found by calculating the null space of the
    # input matrix transposed. This works because left multiplying by a row
    # vector multiplies each entry in a column by each element of the vector
    # and adding them up for each column. Similarly right multiplying the
    # tranpose of a matrix by a column vector is like multiplying each entry
    # in the vector by what was each entry in each column of the original
    # matrix but is now each entry in each row, and adding them up. So in
    # each scenario, the same input vectors will lead to an output of the zero
    # vector.

    # Entry matrix is tranposed as an array
    matrix_array = matrix.to_numpy()

    transposed_array = np.transpose(matrix_array)

    transposed_matrix = pd.DataFrame(data = transposed_array)

    # The null space basis matrix of the transposed matrix or an error matrix
    # is returned.
    return null_space_basis(transposed_matrix, output_decimal)

def row_space_basis(matrix, output_decimal):
    '''
    This function is meant to calculate a basis for the row space of a user
    inputted matrix.
    Args:
        matrix: A pandas DataFrame holding the matrix of which the row space 
        will be calculated.
        output_decimal: A boolean that is True if the row space should be
        outputted as decimals and False otherwise.
    Returns:
        A pandas DataFrame with columns holding vectors that make up the row
        space of the inputted matrix.
    '''

    # The row space consists of all nonzero rows when the matrix is in row
    # echelon or reduced row echelon form. To make it easier to see that the
    # row vectors are linearly independent, the reduced row echelon form of
    # the input matrix will be used to find the row space.

    rref_matrix = calculations.reduced_row_echelon_form(matrix, output_decimal)

    # If rref_matrix is empty an error occurred and rref_matrix holds a column
    # title explaining the error. So the error is returned.

    if rref_matrix.empty:
        return rref_matrix
    
    rref_array = rref_matrix.to_numpy()

    # Nonzero rows will be added to this list. A list is used rather than a
    # numpy array so that append can be used rather than resize.
    basis_vectors = []

    zero_row_reached = False

    i = 0

    # Rows are added to the basis_vectors list until a zero row is reached or
    # the last row of rref_array is reached.
    while not zero_row_reached and i < rref_array.shape[0]:

        all_zeros = True

        j = 0

        # Each entry in row i is checked to see if it is equal to zero until a
        # nonzero entry has been found or the end of the row has been reached.
        while all_zeros and j < rref_array.shape[1]:

            # If a nonzero entry is found, all zeros is set to False.
            if rref_array[i, j] != 0:
                all_zeros = False

            j += 1

        # If row i is not a zero row, it will be converted to a list then
        # appended to the basis vectors list.
        if not all_zeros:
            basis_vectors.append(rref_array[i].tolist())
        
        else:
            zero_row_reached = True

        i += 1

    # Since the row space basis vectors are held as inner lists in the 
    # basis_vectors list, they are currently horizontal. But since vectors are
    # displayed to the user vertically, basis_vectors will be converted to a
    # numpy array and transposed.

    vertical_basis_vectors = np.transpose(np.array(basis_vectors))

    # A DataFrame holding the vertical basis vectors is returned. 

    return pd.DataFrame(data = vertical_basis_vectors)