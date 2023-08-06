"""
Arquivo principal
"""


var_otm = 0.05


def call(preco):
    return preco * (1 + var_otm)


def put(preco):
    return preco * (1 - var_otm)
