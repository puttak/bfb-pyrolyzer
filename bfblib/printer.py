import textwrap


def print_params(p):
    """
    here
    """

    p_string = f"""
    === Parameters ===
    {'di':10} {p.di} \t Inner diameter of reactor [m]
    {'dp':10} {p.dp} \t Mean particle diameter [m]
    """

    p_dedent = textwrap.dedent(p_string)
    print(p_dedent)
