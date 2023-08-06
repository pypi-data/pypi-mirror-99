# -*- coding: utf-8 -*-
"""
Package etdot
=======================================

A 'hello world' example.
"""
__version__ = "1.3.0"

try:
    import etdot.dotc
except ModuleNotFoundError as e:
    # Try to build this binary extension:
    from pathlib import Path
    import click
    from et_micc_build.cli_micc_build import auto_build_binary_extension
    msg = auto_build_binary_extension(Path(__file__).parent, 'dotc')
    if not msg:
        import etdot.dotc
    else:
        click.secho(msg, fg='bright_red')

try:
    import etdot.dotf
except ModuleNotFoundError as e:
    # Try to build this binary extension:
    from pathlib import Path
    import click
    from et_micc_build.cli_micc_build import auto_build_binary_extension
    msg = auto_build_binary_extension(Path(__file__).parent, 'dotf')
    if not msg:
        import etdot.dotf
    else:
        click.secho(msg, fg='bright_red')


def dot(a,b):
    """Compute the dot product of a and b.
    
    :param a: array a
    :param b: array b
    :return: the dot product of a and b
    """
    n = len(a)
    nb = len(b)
    if n != nb:
        raise RuntimeError("a and b should be of the same length")
    sum = 0.0
    for i in range(n):
        sum += a[i]*b[i]
    return sum

# eof
