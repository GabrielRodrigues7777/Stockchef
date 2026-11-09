from sqlalchemy import text
from backend.models.usuario import db

# Mapeia os valores usados no front-end para os códigos numéricos que as
# filtros de consulta esperam.
MAPA_FILTRO_DATA = {
    'hoje': 0,
    'semana': 1,
    'todos': 2,
}

MAPA_FILTRO_TIPO = {
    'entrada': 0,
    'saida': 1,
    'todos': 2,
}

class HistoricoRepository:
    """Executa consultas SQL do banco relacionadas ao módulo Histórico."""

    @staticmethod
    def get_resumo(id_usuario):
        """
        Soma entradas e saidas
        para o usuário logado.
        """
        entradas = db.session.execute(
            text("""
SELECT COALESCE(SUM(mi.quantidade), 0) AS total_acumulado_entradas
    FROM movimentacoes m
    INNER JOIN movimentacao_itens mi ON m.id_movimentacao = mi.id_movimentacao
    INNER JOIN produtos p ON mi.id_produto = p.id_produto
    WHERE p.id_usuario = :id
      AND m.tipo = 'Entrada';
"""),
            {"id": id_usuario}
        ).mappings().first()

        saidas = db.session.execute(
            text("""
SELECT COALESCE(SUM(mi.quantidade), 0) AS total_acumulado_saidas
    FROM movimentacoes m
    INNER JOIN movimentacao_itens mi ON m.id_movimentacao = mi.id_movimentacao
    INNER JOIN produtos p ON mi.id_produto = p.id_produto
    WHERE p.id_usuario = :id
      AND m.tipo = 'Saida';
"""),
            {"id": id_usuario}
        ).mappings().first()

        db.session.commit()

        return {
            "total_entradas": float(entradas["total_acumulado_entradas"]) if entradas else 0,
            "total_saidas": float(saidas["total_acumulado_saidas"]) if saidas else 0,
        }

    @staticmethod
    def listar_movimentacoes(id_usuario, filtro_data='todos', filtro_tipo='todos'):
        """
        Lista movimentacoes convertendo os filtros
        recebidos (strings) para os codigos numericos da consulta.
        """
        codigo_data = MAPA_FILTRO_DATA.get(filtro_data, 2)
        codigo_tipo = MAPA_FILTRO_TIPO.get(filtro_tipo, 2)

        resultado = db.session.execute(
            text("""
SELECT
        p.nome AS nome_produto,
        m.data_movimentacao AS data_registro,
        m.tipo AS tipo_movimentacao,
        c.nome AS categoria,
        u.sigla AS unidade,
        mi.quantidade AS quantidade_movimentada
    FROM movimentacoes m
    INNER JOIN movimentacao_itens mi ON m.id_movimentacao = mi.id_movimentacao
    INNER JOIN produtos p ON mi.id_produto = p.id_produto
    INNER JOIN categorias c ON p.id_categoria = c.id_categoria
    INNER JOIN unidades_medida u ON p.id_unidade = u.id_unidade
    WHERE p.id_usuario = :id

      AND (
          :tipo = 2
          OR (:tipo = 0 AND m.tipo = 'Entrada')
          OR (:tipo = 1 AND m.tipo = 'Saida')
      )

      AND (
          :data = 2
          OR (:data = 0 AND DATE(m.data_movimentacao) = CURRENT_DATE)
          OR (:data = 1 AND m.data_movimentacao >= date_trunc('week', CURRENT_DATE))
      )

    ORDER BY m.data_movimentacao DESC;
"""),
            {"id": id_usuario, "data": codigo_data, "tipo": codigo_tipo}
        ).mappings().all()

        db.session.commit()

        return [
            {
                "produto": linha["nome_produto"],
                "categoria": linha["categoria"],
                "tipo": linha["tipo_movimentacao"],
                "unidade": linha["unidade"],
                "quantidade": float(linha["quantidade_movimentada"]) if linha["quantidade_movimentada"] is not None else 0,
                "data_registro": linha["data_registro"].isoformat() if linha["data_registro"] else None,
            }
            for linha in resultado
        ]
