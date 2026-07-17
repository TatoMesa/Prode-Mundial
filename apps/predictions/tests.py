from django.test import TestCase
from apps.predictions.scoring import calculate_points


class ScoringTests(TestCase):
    """
    Tests unitarios para la lógica de puntuación de pronósticos.
    Cubre todos los casos posibles del sistema de puntos.
    """

    # ── Resultado exacto (5 puntos) ───────────────────────────────────────

    def test_resultado_exacto_gana_local(self):
        points, is_exact, is_winner = calculate_points(2, 1, 2, 1)
        self.assertEqual(points, 5)
        self.assertTrue(is_exact)
        self.assertTrue(is_winner)

    def test_resultado_exacto_gana_visitante(self):
        points, is_exact, is_winner = calculate_points(0, 3, 0, 3)
        self.assertEqual(points, 5)
        self.assertTrue(is_exact)
        self.assertTrue(is_winner)

    def test_resultado_exacto_empate(self):
        points, is_exact, is_winner = calculate_points(1, 1, 1, 1)
        self.assertEqual(points, 5)
        self.assertTrue(is_exact)
        self.assertTrue(is_winner)

    def test_resultado_exacto_cero_a_cero(self):
        points, is_exact, is_winner = calculate_points(0, 0, 0, 0)
        self.assertEqual(points, 5)
        self.assertTrue(is_exact)
        self.assertTrue(is_winner)

    # ── Ganador correcto pero resultado inexacto (2 puntos) ───────────────

    def test_ganador_correcto_local_goles_distintos(self):
        """Real 2-1, pronóstico 3-2 — acertó ganador pero no el resultado exacto."""
        points, is_exact, is_winner = calculate_points(2, 1, 3, 2)
        self.assertEqual(points, 2)
        self.assertFalse(is_exact)
        self.assertTrue(is_winner)

    def test_ganador_correcto_visitante(self):
        """Real 0-2, pronóstico 1-3 — acertó ganador visitante."""
        points, is_exact, is_winner = calculate_points(0, 2, 1, 3)
        self.assertEqual(points, 2)
        self.assertFalse(is_exact)
        self.assertTrue(is_winner)

    def test_ganador_correcto_empate_goles_distintos(self):
        """Real 1-1, pronóstico 2-2 — acertó empate pero no goles exactos."""
        points, is_exact, is_winner = calculate_points(1, 1, 2, 2)
        self.assertEqual(points, 2)
        self.assertFalse(is_exact)
        self.assertTrue(is_winner)

    # ── Fallo (0 puntos) ──────────────────────────────────────────────────

    def test_fallo_pronostico_local_resultado_visitante(self):
        """Real 2-1, pronóstico 1-2 — se invirtió el resultado."""
        points, is_exact, is_winner = calculate_points(2, 1, 1, 2)
        self.assertEqual(points, 0)
        self.assertFalse(is_exact)
        self.assertFalse(is_winner)

    def test_fallo_pronostico_empate_resultado_local(self):
        """Real 1-0, pronóstico 1-1 — pronosticó empate pero ganó local."""
        points, is_exact, is_winner = calculate_points(1, 0, 1, 1)
        self.assertEqual(points, 0)
        self.assertFalse(is_exact)
        self.assertFalse(is_winner)

    def test_fallo_pronostico_visitante_resultado_empate(self):
        """Real 2-2, pronóstico 1-3 — pronosticó visitante pero empataron."""
        points, is_exact, is_winner = calculate_points(2, 2, 1, 3)
        self.assertEqual(points, 0)
        self.assertFalse(is_exact)
        self.assertFalse(is_winner)

    def test_fallo_pronostico_local_resultado_empate(self):
        """Real 0-0, pronóstico 1-0 — pronosticó local pero empataron."""
        points, is_exact, is_winner = calculate_points(0, 0, 1, 0)
        self.assertEqual(points, 0)
        self.assertFalse(is_exact)
        self.assertFalse(is_winner)

    # ── Casos del ejemplo de la consigna ─────────────────────────────────

    def test_ejemplo_consigna_exacto(self):
        """Resultado real 2-1, pronóstico 2-1 → 5 puntos."""
        points, is_exact, is_winner = calculate_points(2, 1, 2, 1)
        self.assertEqual(points, 5)

    def test_ejemplo_consigna_ganador(self):
        """Resultado real 2-1, pronóstico 3-2 → 2 puntos."""
        points, is_exact, is_winner = calculate_points(2, 1, 3, 2)
        self.assertEqual(points, 2)

    def test_ejemplo_consigna_fallo(self):
        """Resultado real 2-1, pronóstico 1-1 → 0 puntos."""
        points, is_exact, is_winner = calculate_points(2, 1, 1, 1)
        self.assertEqual(points, 0)