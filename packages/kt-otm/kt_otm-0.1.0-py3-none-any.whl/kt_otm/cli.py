"""
Scripts de console
"""
from kt_otm import kt_otm
import click


@click.command()
@click.argument("preco")
def cli(preco):
    """Calcula strikes fora do dinheiro."""
    preco = float(preco)
    call_otm = kt_otm.call(preco)
    put_otm = kt_otm.put(preco)
    click.echo("%.2f" % call_otm)
    click.echo("%.2f" % put_otm)
