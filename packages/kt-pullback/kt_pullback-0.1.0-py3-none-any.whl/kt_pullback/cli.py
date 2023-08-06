"""
Scripts do console
"""
from kt_pullback import kt_pullback
import click


@click.command()
@click.argument("preco_final")
@click.argument("preco_inicial")
def cli(preco_final, preco_inicial):
    """Calcula retracoes de uma perna no grafico."""
    prc_final = float(preco_final)
    prc_inicial = float(preco_inicial)
    tamanho = kt_pullback.tamanho_perna(prc_final, prc_inicial)
    metade = kt_pullback.metade_perna(tamanho)
    terco = kt_pullback.terco_perna(tamanho)
    recuo1 = kt_pullback.retracao_um_terco(prc_final, terco)
    recuo2 = kt_pullback.retracao_metade(prc_final, metade)
    recuo3 = kt_pullback.retracao_dois_tercos(prc_final, terco)
    click.echo("%.2f" % recuo1)
    click.echo("%.2f" % recuo2)
    click.echo("%.2f" % recuo3)
