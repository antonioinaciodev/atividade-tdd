import pytest
from unittest.mock import MagicMock
from pedido.pedido import Item, Pedido, contar_frete_gratis


# =============================================================
# EXEMPLO — um teste pronto, para você copiar o formato
# =============================================================

def test_exemplo_quantidade_total(pedido_pequeno):
    # 1 café + 2 pães de queijo = 3 unidades
    assert pedido_pequeno.quantidade_total() == 3


# =============================================================
# PARTE 1 — Encontre os bugs
# Escreva um teste para cada bug. Cada teste deve FALHAR
# no código original. Não altere src/pedido/pedido.py ainda.
# =============================================================


def test_subtotal_considera_quantidade(pedido_pequeno):
    assert pedido_pequeno.subtotal() == 15.0


def test_frete_gratis_com_exatamente_50():
    pedido = Pedido("Carla", [Item("Combo", 50.0, 1)])
    assert pedido.tem_frete_gratis() is True


def test_item_mais_barato(pedido_grande):
    assert pedido_grande.item_mais_barato().nome == "Refrigerante"


def test_total_com_desconto_de_10_por_cento():
    pedido = Pedido("Davi", [Item("Pizza", 100.0, 1)])
    assert pedido.total_com_desconto(10) == 90.0




# =============================================================
# PARTE 2 — Implemente com TDD
# Siga o ciclo: 🔴 escreva o teste → 🟢 implemente → 🟡 refatore
# =============================================================

# Requisito 1 — contar_frete_gratis(pedidos) -> int
# Escreva os testes ANTES de implementar a função


def pedido_com_subtotal(valor, cliente="Cliente"):
    return Pedido(cliente, [Item("Lanche", valor, 1)])


def test_contar_frete_gratis_todos():
    pedidos = [pedido_com_subtotal(50.0), pedido_com_subtotal(80.0), pedido_com_subtotal(120.0)]
    assert contar_frete_gratis(pedidos) == 3


def test_contar_frete_gratis_nenhum():
    pedidos = [pedido_com_subtotal(10.0), pedido_com_subtotal(49.99)]
    assert contar_frete_gratis(pedidos) == 0


def test_contar_frete_gratis_lista_mista(pedido_pequeno, pedido_grande):
    pedidos = [pedido_pequeno, pedido_grande, pedido_com_subtotal(50.0), pedido_com_subtotal(30.0)]
    assert contar_frete_gratis(pedidos) == 2


def test_contar_frete_gratis_lista_vazia():
    assert contar_frete_gratis([]) == 0




# Requisito 2 — situacao(unidades_indisponiveis) -> str
# Escreva os testes ANTES de implementar o método


def test_situacao_cancelado_mesmo_com_frete_gratis(pedido_grande):
    assert pedido_grande.situacao(2) == "Cancelado por falta de estoque"


def test_situacao_confirmado_com_frete_gratis(pedido_grande):
    assert pedido_grande.situacao(0) == "Confirmado com frete grátis"


def test_situacao_confirmado(pedido_pequeno):
    assert pedido_pequeno.situacao(0) == "Confirmado"


def test_situacao_exatamente_25_por_cento_segue_para_frete():
    pedido = Pedido("Elis", [Item("Hambúrguer", 15.0, 4)])
    assert pedido.situacao(1) == "Confirmado com frete grátis"


def test_situacao_pouco_acima_de_25_por_cento():
    pedido = Pedido("Elis", [Item("Esfiha", 8.0, 7)])
    assert pedido.situacao(2) == "Cancelado por falta de estoque"




# Requisito 3 — sugerir_frete_gratis(sms_service) -> None
# Use MagicMock para simular o serviço de SMS
# Escreva os testes ANTES de implementar o método
