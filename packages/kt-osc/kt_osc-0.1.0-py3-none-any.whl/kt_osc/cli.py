"""
Scripts do console
"""
from kt_osc import kt_osc
import click


@click.command()
@click.argument("preco-final")
@click.argument("preco-inicial")
def cli(preco_final, preco_inicial):
    """Calcula oscilacao entre preco final e preco inicial."""
    click.echo(kt_osc.osc(float(preco_final), float(preco_inicial)))


if __name__ == "__main__":
    cli()
