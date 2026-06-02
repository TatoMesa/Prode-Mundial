"""
Carga el fixture completo del torneo: equipos y partidos de fase de grupos.

Uso:
    python manage.py load_fixture            # carga todo
    python manage.py load_fixture --reset    # borra todo y vuelve a cargar

Los partidos de fase eliminatoria (dieciseisavos en adelante) se cargan
desde el admin una vez que se conocen los clasificados.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from datetime import datetime
import pytz

from apps.matches.models import Team, Match


# ── Año del torneo ─────────────────────────────────────────────────────────────
YEAR = 2026

# ── Equipos: (nombre, código, emoji bandera) ───────────────────────────────────
TEAMS = [
    # Grupo A
    ("México",          "MEX", "\U0001F1F2\U0001F1FD"),
    ("Sudáfrica",       "RSA", "\U0001F1FF\U0001F1E6"),
    ("Corea del Sur",   "KOR", "\U0001F1F0\U0001F1F7"),
    ("Rep. Checa",      "CZE", "\U0001F1E8\U0001F1FF"),
    # Grupo B
    ("Canadá",          "CAN", "\U0001F1E8\U0001F1E6"),
    ("Qatar",           "QAT", "\U0001F1F6\U0001F1E6"),
    ("Suiza",           "SUI", "\U0001F1E8\U0001F1ED"),
    ("Bosnia y Her.",   "BIH", "\U0001F1E7\U0001F1E6"),
    # Grupo C
    ("Brasil",          "BRA", "\U0001F1E7\U0001F1F7"),
    ("Marruecos",       "MAR", "\U0001F1F2\U0001F1E6"),
    ("Haití",           "HAI", "\U0001F1ED\U0001F1F9"),
    ("Escocia",         "SCO", "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F"),
    # Grupo D
    ("EE.UU.",          "USA", "\U0001F1FA\U0001F1F8"),
    ("Australia",       "AUS", "\U0001F1E6\U0001F1FA"),
    ("Paraguay",        "PAR", "\U0001F1F5\U0001F1FE"),
    ("Turquía",         "TUR", "\U0001F1F9\U0001F1F7"),
    # Grupo E
    ("Alemania",        "GER", "\U0001F1E9\U0001F1EA"),
    ("Curazao",         "CUW", "\U0001F1E8\U0001F1FC"),
    ("Ecuador",         "ECU", "\U0001F1EA\U0001F1E8"),
    ("Costa de Marfil", "CIV", "\U0001F1E8\U0001F1EE"),
    # Grupo F
    ("Países Bajos",    "NED", "\U0001F1F3\U0001F1F1"),
    ("Japón",           "JPN", "\U0001F1EF\U0001F1F5"),
    ("Túnez",           "TUN", "\U0001F1F9\U0001F1F3"),
    ("Suecia",          "SWE", "\U0001F1F8\U0001F1EA"),
    # Grupo G
    ("Bélgica",         "BEL", "\U0001F1E7\U0001F1EA"),
    ("Egipto",          "EGY", "\U0001F1EA\U0001F1EC"),
    ("Nueva Zelanda",   "NZL", "\U0001F1F3\U0001F1FF"),
    ("Irán",            "IRN", "\U0001F1EE\U0001F1F7"),
    # Grupo H
    ("España",          "ESP", "\U0001F1EA\U0001F1F8"),
    ("Cabo Verde",      "CPV", "\U0001F1E8\U0001F1FB"),
    ("Uruguay",         "URU", "\U0001F1FA\U0001F1FE"),
    ("Arabia Saudita",  "KSA", "\U0001F1F8\U0001F1E6"),
    # Grupo I
    ("Francia",         "FRA", "\U0001F1EB\U0001F1F7"),
    ("Senegal",         "SEN", "\U0001F1F8\U0001F1F3"),
    ("Irak",            "IRQ", "\U0001F1EE\U0001F1F6"),
    ("Noruega",         "NOR", "\U0001F1F3\U0001F1F4"),
    # Grupo J
    ("Argentina",       "ARG", "\U0001F1E6\U0001F1F7"),
    ("Argelia",         "ALG", "\U0001F1E9\U0001F1FF"),
    ("Austria",         "AUT", "\U0001F1E6\U0001F1F9"),
    ("Jordania",        "JOR", "\U0001F1EF\U0001F1F4"),
    # Grupo K
    ("Portugal",        "POR", "\U0001F1F5\U0001F1F9"),
    ("Uzbekistán",      "UZB", "\U0001F1FA\U0001F1FF"),
    ("Colombia",        "COL", "\U0001F1E8\U0001F1F4"),
    ("RD Congo",        "COD", "\U0001F1E8\U0001F1E9"),
    # Grupo L
    ("Inglaterra",      "ENG", "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F"),
    ("Croacia",         "CRO", "\U0001F1ED\U0001F1F7"),
    ("Ghana",           "GHA", "\U0001F1EC\U0001F1ED"),
    ("Panamá",          "PAN", "\U0001F1F5\U0001F1E6"),
]

# ── Partidos: (código local, código visitante, "DD/MM HH:MM") ──────────────────
MATCHES = [
    # ── GRUPO A ────────────────────────────────────────────────────────────────
    ("MEX", "RSA", "11/06 16:00"),
    ("KOR", "CZE", "11/06 23:00"),
    ("CZE", "RSA", "18/06 13:00"),
    ("MEX", "KOR", "18/06 22:00"),
    ("CZE", "MEX", "24/06 22:00"),
    ("RSA", "KOR", "24/06 22:00"),
    # ── GRUPO B ────────────────────────────────────────────────────────────────
    ("CAN", "BIH", "12/06 16:00"),
    ("QAT", "SUI", "13/06 16:00"),
    ("SUI", "BIH", "18/06 16:00"),
    ("CAN", "QAT", "18/06 19:00"),
    ("SUI", "CAN", "24/06 16:00"),
    ("BIH", "QAT", "24/06 16:00"),
    # ── GRUPO C ────────────────────────────────────────────────────────────────
    ("BRA", "MAR", "13/06 19:00"),
    ("HAI", "SCO", "13/06 22:00"),
    ("SCO", "MAR", "19/06 19:00"),
    ("BRA", "HAI", "19/06 21:30"),
    ("SCO", "BRA", "24/06 19:00"),
    ("MAR", "HAI", "24/06 19:00"),
    # ── GRUPO D ────────────────────────────────────────────────────────────────
    ("USA", "PAR", "12/06 22:00"),
    ("AUS", "TUR", "14/06 01:00"),
    ("TUR", "PAR", "20/06 01:00"),
    ("USA", "AUS", "19/06 16:00"),
    ("TUR", "USA", "25/06 23:00"),
    ("PAR", "AUS", "25/06 23:00"),
    # ── GRUPO E ────────────────────────────────────────────────────────────────
    ("GER", "CUW", "14/06 14:00"),
    ("CIV", "ECU", "14/06 20:00"),
    ("GER", "CIV", "20/06 17:00"),
    ("ECU", "CUW", "20/06 23:00"),
    ("ECU", "GER", "25/06 17:00"),
    ("CUW", "CIV", "25/06 17:00"),
    # ── GRUPO F ────────────────────────────────────────────────────────────────
    ("NED", "JPN", "14/06 17:00"),
    ("SWE", "TUN", "14/06 23:00"),
    ("NED", "SWE", "20/06 14:00"),
    ("TUN", "JPN", "21/06 01:00"),
    ("TUN", "NED", "25/06 20:00"),
    ("JPN", "SWE", "25/06 20:00"),
    # ── GRUPO G ────────────────────────────────────────────────────────────────
    ("BEL", "EGY", "15/06 16:00"),
    ("IRN", "NZL", "15/06 22:00"),
    ("BEL", "IRN", "21/06 16:00"),
    ("NZL", "EGY", "21/06 22:00"),
    ("NZL", "BEL", "27/06 00:00"),
    ("EGY", "IRN", "27/06 00:00"),
    # ── GRUPO H ────────────────────────────────────────────────────────────────
    ("ESP", "CPV", "15/06 13:00"),
    ("KSA", "URU", "15/06 19:00"),
    ("ESP", "KSA", "21/06 13:00"),
    ("URU", "CPV", "21/06 19:00"),
    ("URU", "ESP", "26/06 21:00"),
    ("CPV", "KSA", "26/06 21:00"),
    # ── GRUPO I ────────────────────────────────────────────────────────────────
    ("FRA", "SEN", "16/06 16:00"),
    ("IRQ", "NOR", "16/06 19:00"),
    ("FRA", "IRQ", "22/06 18:00"),
    ("NOR", "SEN", "22/06 21:00"),
    ("NOR", "FRA", "26/06 16:00"),
    ("SEN", "IRQ", "26/06 16:00"),
    # ── GRUPO J ────────────────────────────────────────────────────────────────
    ("ARG", "ALG", "16/06 22:00"),
    ("AUT", "JOR", "17/06 01:00"),
    ("ARG", "AUT", "22/06 14:00"),
    ("JOR", "ALG", "23/06 00:00"),
    ("JOR", "ARG", "27/06 23:00"),
    ("ALG", "AUT", "27/06 23:00"),
    # ── GRUPO K ────────────────────────────────────────────────────────────────
    ("POR", "COD", "17/06 14:00"),
    ("UZB", "COL", "17/06 23:00"),
    ("POR", "UZB", "23/06 14:00"),
    ("COL", "COD", "23/06 23:00"),
    ("COL", "POR", "27/06 20:30"),
    ("COD", "UZB", "27/06 20:30"),
    # ── GRUPO L ────────────────────────────────────────────────────────────────
    ("ENG", "CRO", "17/06 17:00"),
    ("GHA", "PAN", "17/06 20:00"),
    ("ENG", "GHA", "23/06 17:00"),
    ("PAN", "CRO", "23/06 20:00"),
    ("PAN", "ENG", "27/06 18:00"),
    ("CRO", "GHA", "27/06 18:00"),
]


def _parse_kickoff(date_str: str) -> datetime:
    """
    Convierte "DD/MM HH:MM" a datetime aware en la zona horaria del proyecto.
    Usa el año definido en YEAR.
    """
    tz = pytz.timezone("America/Argentina/Buenos_Aires")
    dt = datetime.strptime(f"{date_str}/{YEAR}", "%d/%m %H:%M/%Y")
    return tz.localize(dt)


class Command(BaseCommand):
    help = "Carga los equipos y partidos de fase de grupos del torneo."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Elimina todos los partidos y equipos antes de cargar.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            Match.objects.all().delete()
            Team.objects.all().delete()
            self.stdout.write(self.style.WARNING("Base de datos limpiada."))

        # ── Equipos ────────────────────────────────────────────────────────────
        self.stdout.write("Cargando equipos...")
        teams = {}
        created_count = 0

        for name, code, flag in TEAMS:
            team, created = Team.objects.update_or_create(
                code=code,
                defaults={"name": name, "flag": flag},
            )
            teams[code] = team
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"  {created_count} equipos creados, "
            f"{len(TEAMS) - created_count} actualizados."
        ))

        # ── Partidos ───────────────────────────────────────────────────────────
        self.stdout.write("Cargando partidos...")
        match_created = 0
        match_skipped = 0

        for home_code, away_code, date_str in MATCHES:
            home = teams[home_code]
            away = teams[away_code]
            kickoff = _parse_kickoff(date_str)

            _, created = Match.objects.get_or_create(
                home_team=home,
                away_team=away,
                kickoff_time=kickoff,
                defaults={"status": Match.Status.PENDING},
            )
            if created:
                match_created += 1
            else:
                match_skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"  {match_created} partidos creados, "
            f"{match_skipped} ya existían (omitidos)."
        ))

        self.stdout.write(self.style.SUCCESS(
            f"\n✓ Fixture cargado: {len(TEAMS)} equipos, "
            f"{match_created} partidos de fase de grupos."
        ))
        self.stdout.write(
            "  Los partidos eliminatorios se cargan desde el admin "
            "una vez que se conocen los clasificados."
        )