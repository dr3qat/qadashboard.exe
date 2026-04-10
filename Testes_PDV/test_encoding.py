# -*- coding: utf-8 -*-
"""
Teste rápido para validar encoding UTF-8 de acentos e emojis.
Execute: pytest test_encoding.py -v -s
"""
import sys
from config import logger


def test_encoding_acentos():
    """Testa exibição de acentos portugueses."""
    logger.info("==> TESTANDO ACENTUAÇÃO")
    logger.info("-> Café com açúcar")
    logger.info("-> Pão de queijo")
    logger.info("-> Atenção com a configuração")
    logger.info("->Ição e ção")
    logger.info("==> ACENTUAÇÃO CONCLUÍDA")
    assert True


def test_encoding_emojis():
    """Testa exibição de emojis."""
    logger.info("==> TESTANDO EMOJIS")
    logger.info("🖱️ [CLICK] Clicando no botão")
    logger.info("⌨️ [DIGITAR] Digitando texto")
    logger.info("✅ [OK] Teste passou")
    logger.info("❌ [ERRO] Teste falhou")
    logger.info("📜 [SCROLL] Rolando tela")
    logger.info("🔍 [BUSCA] Buscando elemento")
    logger.info("⏳ [AGUARDAR] Aguardando...")
    logger.info("==> EMOJIS CONCLUÍDOS")
    assert True


def test_encoding_completo():
    """Testa mensagem completa com acentos e emojis."""
    logger.info("==> INICIANDO VENDA FUTURA - ENTREGA EM DOMICÍLIO")
    logger.info("-> Selecionando tipo de entrega: Domicílio")
    logger.info("-> Selecionando vendedor")
    logger.info("-> Buscando cliente CPF: 1")
    logger.info("-> Adicionando produto 1234 tamanho 38")
    logger.info("-> Avançando para pagamento")
    logger.info("-> Configurando pagamento à vista")
    logger.info("-> Verificando popup de bônus")
    logger.info("-> Selecionando forma de pagamento: Dinheiro")
    logger.info("-> Finalizando venda")
    logger.info("-> Respondendo diálogo de impressão")
    logger.info("==> VENDA FUTURA DOMICÍLIO CONCLUÍDA")

    logger.info("")
    logger.info("✅ Todos os caracteres devem estar legíveis!")
    logger.info("🎉 Se você vê acentos e emojis corretamente, o encoding está OK!")

    assert True


def test_encoding_info():
    """Mostra informações sobre o encoding atual."""
    logger.info("==> INFORMAÇÕES DE ENCODING")
    logger.info(f"-> sys.stdout.encoding: {sys.stdout.encoding}")
    logger.info(f"-> sys.stderr.encoding: {sys.stderr.encoding}")
    logger.info(f"-> sys.getdefaultencoding(): {sys.getdefaultencoding()}")

    import os
    logger.info(f"-> PYTHONIOENCODING: {os.environ.get('PYTHONIOENCODING', 'não definido')}")

    logger.info("==> FIM DAS INFORMAÇÕES")
    assert True
