"""
Interrupt
"""


def out(arg):
    import sys
    from Alexandria.general.console import print_color
    print_color(arg, 'red')
    sys.exit()
