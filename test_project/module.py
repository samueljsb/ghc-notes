"""A fake module that contains a note of GHC."""

# Note [This is a test note]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# This is a note that exists in the fake test project. It can be found by the
# end-to-end tests that run the CLI tools on a directory.
#
# This note starts on line 3 of `module.py` and is referenced on line 15.


def f() -> None:
    """Do nothing.

    This function's docstring references a note.
    See Note [This is a test note]
    """
