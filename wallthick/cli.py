# -*- coding: utf-8 -*-

"""Console script for wallthick."""

import click


@click.command()
def main(args=None):
    """Console script for wallthick."""
    click.echo("Welcome to wallthick.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
