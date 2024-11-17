import pandas as pd
import numpy as np
import calculations

def solution_set(linear_system, output_decimal):
    '''
    The purpose of this function is to find the solution set of a linear system
    and return it as a frame of strings that can be outputted and easily read.
    Args:
        linear_system: a DataFrame holding the augmented matrix for the linear
        system with variable names as headers.
        output_decimal: a boolean that is true if the user wants their output as
        decimals and false if they want it as fractions.
    Returns:
        a DataFrame of strings representing each variable's solution. The
        header of this DataFrame will already be set.
    '''

    if linear_system.empty:
        return linear_system
    
    # The columns are saved here since the function to convert to row echelon
    # form does not keep column titles.

    # The columns object is list-like but must be cast to a list so the pop
    # method works on it.
    variable_names = list(linear_system.columns)

    # This removes the constant column name.
    variable_names.pop(len(variable_names) - 1)

    solved_system_frame = calculations.reduced_row_echelon_form(
        linear_system,
        output_decimal
        )
    
    # This occurs if the user's matrix is not formatted correctly so there are
    # entries in their matrix that aren't numbers.
    if solved_system_frame.empty:
        return solved_system_frame
    
    solved_system_array = solved_system_frame.to_numpy()
    
    # This 2d list will be vertical and will only have one column.
    # In each row there will be a string representing the solution to a
    # variable.
    solutions_for_variables = []

    # This will be used to access constants when solving for variables.
    last_column_index = solved_system_array.shape[1] - 1

    # Since each row's search will start at the previous_pivot + 1,
    # previous_pivot will start at -1.
    previous_pivot = -1

    # Once a zero_row is reached, there will be no more pivots so there is not
    # point checking lower rows.
    zero_row_reached = False

    i = 0

    # This checks that the bottom row has not yet been reached, there have been
    # no zero rows yet, and the last column has not yet been a pivot. If any of
    # these conditions are violated, then this loop will end.
    while i < solved_system_array.shape[0] and not zero_row_reached and \
        previous_pivot + 1 < solved_system_array.shape[1] - 1:

        variable_solution_row = []

        variable_solution = ""

        pivot_column_reached = False

        # j goes up to the second to last column since the last column
        # represents constants. It starts one higher than the previous pivot
        # because in row echelon form there will never be a pivot that is not to
        # the right of the previous pivot position.
        for j in range(previous_pivot + 1, solved_system_array.shape[1] - 1):

            coefficient = solved_system_array[i, j]

            # This indicates that the row is a zero row

            if not pivot_column_reached and j == solved_system_array.shape[1] -\
                2 and coefficient == 0:
                
                # This ensures that the final column will be added as a free 
                # variable.

                solutions_for_variables.append(
                    [f"{variable_names[j]} is free"]
                )

                zero_row_reached = True

            elif not pivot_column_reached and coefficient == 0:
                # If there is a 0 coefficient in a column that exists before the
                # first pivot position in its row and after the pivot in the
                # previous row, that column is not a pivot column so its
                # variable is free.

                solutions_for_variables.append(
                    [f"{variable_names[j]} is free"])

            elif not pivot_column_reached and coefficient != 0:
                pivot_column_reached = True

                # Once the pivot column has reached, the solution for the
                # variable in that column will first be set as equal to the
                # number in the constant column.

                previous_pivot = j
                
                row_constant = solved_system_array[i, last_column_index]
                
                variable_solution += f"{variable_names[j]} = {row_constant}"
            
            # This block is only reached if pivot_column_reached is true
            # and the coefficient is not 0.
            elif coefficient != 0:
                
                term_coefficient_string = ""

                # Since the coefficient should be brought to the solution side,
                # it is multiplied by negative 1 in the solution.
                term_coefficient_value = -1 * coefficient

                # There is no point in including a 1 before the variable since
                # that is implied, so if the coefficient is 1, the string before
                # the variable will be nothing.
                if term_coefficient_value == 1 or term_coefficient_value == -1:
                    term_coefficient_string == ""

                # The term in the parentheses will always be positive. Negative
                # values will be accounted for with a - sign rather than a + 
                # sign. The coefficient term is always in parentheses in case
                # the user chooses variable names that start with numbers.

                if term_coefficient_value < 0:
                    term_coefficient_string = \
                        f"({-1 * term_coefficient_value})"

                else:
                    term_coefficient_string = f"({term_coefficient_value})"

                # If the current variable is the first after the constant and
                # the constant is 0, the zero is removed as it is unnecessary.
                # 0 is only included if it is the only element of the equation.
                
                if variable_solution[len(variable_solution) - 3 : 
                                     len(variable_solution)] == "= 0":
                    
                    # This is variable solution without the last zero, as it is 
                    # no longer necessary since constants are being added.
                    variable_solution = variable_solution[0 : 
                                                    len(variable_solution) - 1]
                    
                    # Since this term is the first term in the equation, a
                    # a negative sign should be included for negative numbers.

                    if term_coefficient_value < 0:
                        term_coefficient_string = "-" + term_coefficient_string

                else:

                    if term_coefficient_value < 0:
                        variable_solution += " - "

                    else:
                        variable_solution += " + "


                variable_solution += \
                f"{term_coefficient_string}{variable_names[j]}"
                
        # If a zero row is reached then there is nothing to append.
        if (not zero_row_reached):   
            variable_solution_row.append(variable_solution)

            solutions_for_variables.append(variable_solution_row)

        i += 1

    # If the last column has been a pivot, it is still possible for the system
    # to be inconsistent. The while loop only catches inconsistent systems where
    # there are free variables between the last pivot column and the pivot in
    # the constant column. Since the row after a pivot in the last column is
    # guaranteed to be a zero row, if there is a row after the pivot in the last
    # column, the program will only check if there is a nonzero number in the 
    # constant column of that row. Since all rows entirely full of zeros are at
    # the bottom in reduced row echelon form, there is no need to check lower
    # rows. If a zero row has been reached, then that row is the only row that
    # can have a pivot in its augmented column rather than the row after the
    # the last row checked in the loop, so 1 is subtracted from i.

    if zero_row_reached:
        i -= 1

    if i < solved_system_array.shape[0]:

        if solved_system_array[i, last_column_index] != 0:

            inconsistent_array = np.array([["This system is inconsistent so \
                                            there are no solutions."]])
            
            inconsistent_frame = pd.DataFrame (
                data = inconsistent_array,
                columns = ["Solution Set"]
            )

            return inconsistent_frame
        
    # If the pivot in the last row is not the same as the last column then the
    # the variables for columns that follow will be considered free. This is
    # only necessary if there are no zero rows and the last row has a pivot
    # before the last column. If a zero row is reached, then the loop will add
    # the free variables because every column between two pivots in the loop is
    # considered to be free and a pivot is never reached in a zero row.
    if not zero_row_reached:
        for j in range(previous_pivot + 1, solved_system_array.shape[1] - 1):
            solutions_for_variables.append(
                [f"{variable_names[j]} is free"]
                )
        
    solution_string_array = np.array(solutions_for_variables)

    solution_string_frame = pd.DataFrame(
        data = solution_string_array,
        columns = ["Solution Set"]
    )

    return solution_string_frame

def parametric_vector_solution_set(linear_system, output_decimal, 
                                   return_vectors = False):
    '''
    The purpose of this function is to find the solution set to a linear system
    and return the solution in a way that that it can be displayed in
    parametric vector form.
    Args:
        linear_system: a DataFrame holding the augmented matrix for the linear
        system with variable names as headers.
        output_decimal: a boolean that is True if the user wants their output
        as decimals and False if they want it as fractions.
        return_vectors: a boolean that is True if the function should return a
        DataFrame of the solution vectors. (This will mainly be the case when
        this function is called by other functions, as by default, this
        function returns a DataFrame meant to be easy to read, not easy to
        use for other purposes.)
    Returns:
        a DataFrame holding the solution to the linear system in parametric
        vector form.
    '''

    if linear_system.empty:
        return linear_system
    
    # The columns are saved here since the function to convert to row echelon
    # form does not keep column titles.

    # The columns object is list-like but must be cast to a list so the pop
    # method works on it.
    variable_names = list(linear_system.columns)

    # This removes the constant column name.
    variable_names.pop(len(variable_names) - 1)

    solved_system_frame = calculations.reduced_row_echelon_form(
        linear_system,
        output_decimal
        )
    
    # This occurs if the user's matrix is not formatted correctly so there are
    # entries in their matrix that aren't numbers.
    if solved_system_frame.empty:
        return solved_system_frame
    
    solved_system_array = solved_system_frame.to_numpy()

    # A dictionary of solution vectors is created. The constant vector is added
    # by default in case there are no free variables and every variable is
    # equal to zero.
    solution_vectors = {"Constant" : [0] * len(variable_names)}

    # This will be used to access constants when solving for variables.
    last_column_index = solved_system_array.shape[1] - 1

    # Since each row's search will start at the previous_pivot + 1,
    # previous_pivot will start at -1.
    previous_pivot = -1

    # Once a zero_row is reached, there will be no more pivots so there is not
    # point checking lower rows.
    zero_row_reached = False

    i = 0

    # This checks that the bottom row has not yet been reached, there have been
    # no zero rows yet, and the last column has not yet been a pivot. If any of
    # these conditions are violated, then this loop will end.
    while i < solved_system_array.shape[0] and not zero_row_reached and \
        previous_pivot + 1 < solved_system_array.shape[1] - 1:

        pivot_column_reached = False

        # j goes up to the second to last column since the last column
        # represents constants. It starts one higher than the previous pivot
        # because in row echelon form there will never be a pivot that is not
        # to the right of the previous pivot position.
        for j in range(previous_pivot + 1, solved_system_array.shape[1] - 1):

            coefficient = solved_system_array[i, j]

            # This indicates that the row is a zero row

            if not pivot_column_reached and j == solved_system_array.shape[1]-\
                2 and coefficient == 0:
                
                # This ensures that the final column will be added as a free 
                # variable by adding it to the solution vector dictionary if it
                # has not been already.
                if not variable_names[j] in solution_vectors:
                    current_vector = [0] * len(variable_names)

                    # This sets the free variable equal to itself.
                    current_vector[j] = 1

                    solution_vectors[variable_names[j]] = current_vector

                zero_row_reached = True

            elif not pivot_column_reached and coefficient == 0:
                # If there is a 0 coefficient in a column that exists before
                # the first pivot position in its row and after the pivot in
                # the previous row, that column is not a pivot column so its
                # variable is free.

                # This ensures that this column will be added as a free 
                # variable by adding it to the solution vector dictionary if it
                # has not been already.
                if not variable_names[j] in solution_vectors:
                    current_vector = [0] * len(variable_names)

                    # This sets the free variable equal to itself.
                    current_vector[j] = 1

                    solution_vectors[variable_names[j]] = current_vector

            elif not pivot_column_reached and coefficient != 0:
                pivot_column_reached = True

                # Once the pivot column has reached, the solution for the
                # variable in that column will first be set as equal to the
                # number in the constant column.

                previous_pivot = j
                
                row_constant = solved_system_array[i, last_column_index]

                # The constant vector has its row corresponding with this pivot
                # variable set to the constant in this row of the solution
                # array.
                solution_vectors["Constant"][j] = row_constant
            
            # This block is only reached if pivot_column_reached is true
            # and the coefficient is not 0.
            elif coefficient != 0:

                # Since the variable should be brought to the solution side,
                # it is multiplied by negative 1 in the solution.
                variable_multiple = -1 * coefficient

                # This ensures that this column will be added as a free 
                # variable by adding it to the solution vector dictionary if it
                # has not been already.
                if not variable_names[j] in solution_vectors:
                    current_vector = [0] * len(variable_names)

                    # This sets the free variable equal to itself.
                    current_vector[j] = 1

                    solution_vectors[variable_names[j]] = current_vector

                # The row of the solution vector for this free variable 
                # corresponding to the pivot variable is set to the variable 
                # multiple in this row of the solution array.
                solution_vectors[variable_names[j]][previous_pivot] = \
                    variable_multiple

        i += 1

    # If the last column has been a pivot, it is still possible for the system
    # to be inconsistent. The while loop only catches inconsistent systems 
    # where there are free variables between the last pivot column and the
    # pivot in the constant column. Since the row after a pivot in the last
    # column is guaranteed to be a zero row, if there is a row after the pivot
    # in the last column, the program will only check if there is a nonzero
    # number in the constant column of that row. Since all rows entirely full
    # of zeros are at the bottom in reduced row echelon form, there is no need
    # to check  lower rows. If a zero row has been reached, then that row is
    # the only row that can have a pivot in its augmented column rather than
    # the row after the  the last row checked in the loop, so 1 is subtracted
    # from i.

    if zero_row_reached:
        i -= 1

    if i < solved_system_array.shape[0]:

        if solved_system_array[i, last_column_index] != 0:

            inconsistent_array = np.array([
                ["This system is inconsistent so there are no solutions."]]
                )
            
            inconsistent_frame = pd.DataFrame (
                data = inconsistent_array,
                columns = ["Solution Set"]
            )

            return inconsistent_frame
        
    # If the pivot in the last row is not the same as the last column then the
    # the variables for columns that follow will be considered free. This is
    # only necessary if there are no zero rows and the last row has a pivot
    # before the last column. If a zero row is reached, then the loop will add
    # the free variables because every column between two pivots in the loop is
    # considered to be free and a pivot is never reached in a zero row.
    if not zero_row_reached:
        for j in range(previous_pivot + 1, solved_system_array.shape[1] - 1):
            
            # This ensures that this column will be added as a free 
            # variable by adding it to the solution vector dictionary if it
            # has not been already.
            if not variable_names[j] in solution_vectors:
                current_vector = [0] * len(variable_names)

                # This sets the free variable equal to itself.
                current_vector[j] = 1

                solution_vectors[variable_names[j]] = current_vector

    # As long as the constant vector is not the only vector, it is removed if
    # it consists of all zeros. For homogenous equations, it will always be all
    # zeros so will be removed unless it is the only solution vector. The
    # reason is that a vector of all zeros is implied unless it is the only
    # vector in the solution.
    if len(solution_vectors) > 1:
        constant_all_zeros = True

        constant_index = 0

        # If the constant vectors is all zeros it will be removed from the
        # dictionary unless it is the only vector.

        constant_vector = solution_vectors["Constant"]

        # This loop checks for nonzeros in the constant vector until a nonzero
        # is found or the length of the constant vector is reached.
        while constant_index < len(constant_vector) and constant_all_zeros:

            if constant_vector[constant_index] != 0:
                constant_all_zeros = False

            constant_index += 1

        if constant_all_zeros:
            solution_vectors.pop("Constant")
        
    # Dictionary is finished here so after this it needs to be formatted into 
    # DataFrame that the user can read. But if the vectors are needed directly,
    # a DataFrame with just the solution vectors is returned as readability is
    # less important than functionaltiy.

    if return_vectors:
        # The solution vectors will be made into a list with vectors
        # horizontal. This is done as the values method does not return a list
        # so cannot correctly be converted to a numpy array. Lists of multiple
        # dimensions can be converted into multidimensional numpy array.
        vector_list = list(solution_vectors.values())

        # vector_list is converted into a 2d numpy array. Then that array is
        # transposed so that vectors can be vertical rather than horizontal.
        vector_array = np.transpose(np.array(vector_list))

        return pd.DataFrame(data = vector_array)

    parametric_vector_frame = pd.DataFrame()

    parametric_vector_frame["Column 1"] = variable_names

    # The equals symbol is added in the middle of the third column. 
    equal_column = [""] * len(variable_names)

    equal_column[len(variable_names) // 2] = "="

    parametric_vector_frame["Column 2"] = equal_column

    # This variable will be incremented later as columns are added to the 
    # parametric_vector_frame.
    current_column = 3

    if "Constant" in solution_vectors:
        parametric_vector_frame["Column 3"] = solution_vectors["Constant"]

        current_column += 1

    for i in range(len(variable_names)):
        variable_name = variable_names[i]

        # Entering this if statement means that variable_names[i] is a free
        # variable.
        if variable_name in solution_vectors:

            # This if statement is only not entered for the first vector 
            # when there is no constant vector.
            if current_column > 3:
    
                # The plus symbol is added in the middle of the next
                # column. 
                plus_column = [""] * len(variable_names)

                plus_column[len(variable_names) // 2] = "+"

                parametric_vector_frame[f"Column {current_column}"] = \
                    plus_column

                current_column += 1

            # The variable name is added in the middle of the third
            # column. 
            variable_column = [""] * len(variable_names)

            variable_column[len(variable_names) // 2] = variable_name

            parametric_vector_frame[f"Column {current_column}"] = \
                variable_column

            current_column += 1

            # The column containing the vector associated with the variable
            # is added.

            vector_column = solution_vectors[variable_name]

            parametric_vector_frame[f"Column {current_column}"] = \
                vector_column
            
            current_column += 1

    return parametric_vector_frame