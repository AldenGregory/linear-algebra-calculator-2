'''
This file contains general formatting functions that will be used across the
project.
'''

from shiny import ui, express

def spaced_section_core(*args):
    '''
    This function defines a ui component that is spaced apart from the
    components above and below it.
    Args:
        *args: ui components to be displayed in the spaced section.
    Returns:
        a ui.div component with styling added to create space above and below
        it.
    '''
    
    return ui.div(args).add_style("padding: 30px 0px 15px 0px;")

@express.expressify
def spaced_section_express(*args):
    '''
    This function defines a ui component that is spaced apart from the
    components above and below it.
    Args:
        *args: ui components to be displayed in the spaced section.
    Returns:
        a ui.div component with styling added to create space above and below
        it.
    '''

    with express.ui.div().add_style("padding: 30px 0px 15px 0px;"):
        # List comprehension used in shiny examples.
        [arg for arg in args]
