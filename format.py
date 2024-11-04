'''
This file contains general formatting functions that will be used across the
project.
'''

from shiny import ui, express

def spaced_section_core(*args):
    return ui.div(args).add_style("padding: 30px 0px 15px 0px;")

@express.expressify
def spaced_section_express(*args):
    with express.ui.div().add_style("padding: 30px 0px 15px 0px;"):
        # List comprehension used in shiny examples.
        [arg for arg in args]
