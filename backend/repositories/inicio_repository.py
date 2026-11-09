from sqlalchemy import text
from backend.models.usuario import db
from backend.repositories.estoque_repository import EstoqueRepository

class InicioRepository:
    """Executa consultas SQL do banco relacionadas ao módulo Início."""

    @staticmethod
    def get_resumo(id_usuario):
        """
        Consulta os totais de produtos e de estoque baixo
        e de lotes vencendo para o usuario logado.
        """
        cadastrados = db.session.execute(
            text("""
SELECT COUNT(*) AS total_itens_cadastrados
    FROM produtos
    WHERE id_usuario = :id
      AND ativo = TRUE;
"""),
            {"id": id_usuario}
        ).mappings().first()

        estoque_baixo = db.session.execute(
            text("""
SELECT COUNT(*) AS total_itens_estoque_baixo
    FROM (
        SELECT p.id_produto
        FROM produtos p
        LEFT JOIN lotes l ON p.id_produto = l.id_produto
        WHERE p.id_usuario = :id
          AND p.ativo = TRUE
        GROUP BY p.id_produto, p.estoque_minimo
        HAVING COALESCE(SUM(l.quantidade_atual), 0) < p.estoque_minimo
    ) AS produtos_abaixo_do_minimo;
"""),
            {"id": id_usuario}
        ).mappings().first()

        vencendo_7_dias = db.session.execute(
            text("""
SELECT COUNT(*) AS total_lotes_vencendo_7_dias
    FROM lotes l
    INNER JOIN produtos p ON l.id_produto = p.id_produto
    WHERE p.id_usuario = :id
      AND p.ativo = TRUE
      AND l.quantidade_atual > 0
      AND l.validade <= (CURRENT_DATE + 7);
"""),
            {"id": id_usuario}
        ).mappings().first()

        db.session.commit()

        return {
            "total_cadastrados": cadastrados["total_itens_cadastrados"],
            "total_estoque_baixo": estoque_baixo["total_itens_estoque_baixo"],
            "total_vencendo_7_dias": vencendo_7_dias["total_lotes_vencendo_7_dias"],
        }

    @staticmethod
    def get_estoque_baixo(id_usuario, limite=5):
        """
        Lista o estoque (com unidade de medida) e filtra apenas os produtos cuja
        quantidade atual está abaixo do mínimo configurado.
        """
        # Usa o mesmo estoque agrupado da tela de Estoque, que já traz a
        # unidade de medida (kg, un, l...) de cada produto.
        produtos = EstoqueRepository.listar_estoque(id_usuario)

        abaixo_do_minimo = [
            {
                "produto": produto["produto"],
                "categoria": produto["categoria"],
                "quantidade": produto["quantidade_total"],
                "valor_minimo": produto["valor_minimo"],
                "unidade": produto["unidade"],
            }
            for produto in produtos
            if produto["quantidade_total"] < produto["valor_minimo"]
        ]

        return abaixo_do_minimo[:limite]

    @staticmethod
    def get_vencendo_7_dias(id_usuario):
        """
        Retorna a lista de
        lotes que vencem nos próximos 7 dias (incluindo hoje) para o
        usuário logado.
        """
        resultado = db.session.execute(
            text("""
SELECT
        l.id_lote,
        l.id_produto,
        p.nome AS produto,
        l.numero_lote,
        l.validade,
        l.quantidade_atual,
        l.custo_unitario
    FROM lotes l
    INNER JOIN produtos p ON l.id_produto = p.id_produto
    WHERE p.id_usuario = :id
      AND p.ativo = TRUE
      AND l.quantidade_atual > 0
      AND l.validade <= (CURRENT_DATE + 7)
    ORDER BY l.validade ASC;
"""),
            {"id": id_usuario}
        ).mappings().all()

        db.session.commit()

        return [
            {
                "id_lote": linha["id_lote"],
                "id_produto": linha["id_produto"],
                "produto": linha["produto"],
                "numero_lote": linha["numero_lote"],
                "validade": linha["validade"].isoformat() if linha["validade"] else None,
                "quantidade_atual": float(linha["quantidade_atual"]) if linha["quantidade_atual"] is not None else None,
                "custo_unitario": float(linha["custo_unitario"]) if linha["custo_unitario"] is not None else None,
            }
            for linha in resultado
        ]
