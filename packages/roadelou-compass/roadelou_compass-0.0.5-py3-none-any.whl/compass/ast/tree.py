#!/usr/bin/env python3

################################### METADATA ###################################

# Contributors: roadelou
# Contacts:
# Creation Date: 2021-03-12
# Language: Python3

################################### IMPORTS ####################################

# Standard library
from typing import List  # Used for type hints


# External imports
# Your imports from other packages go here


# Internal imports
from compass.ast.module import Module  # Used for type hints
from compass.ast.extern import Extern  # Used for type hints

################################### CLASSES ####################################


class Tree:
    """
    Class used to hold the AST of the compass language.
    """

    def __init__(self, module: Module, list_extern: List[Extern]):
        """
        Constructor of the Tree clas.

        Arguments
        =========
         - module: The Module declared in the current file.
         - list_extern: The list of declared extern submodules for this module.
        """
        # Storing the arguments.
        self.module = module
        self.externs = list_extern

    def rename(self, name: str):
        """
        Renames the main module in the AST to the provided name.
        """
        self.module.rename(name)


################################## FUNCTIONS ###################################

# Your functions go here

##################################### MAIN #####################################

if __name__ == "__main__":
    # The code to run when this file is used as a script goes here
    pass

##################################### EOF ######################################
