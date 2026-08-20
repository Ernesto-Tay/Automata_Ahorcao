# Etapas del dibujo: índice 0 = sin fallos, índice 6 = ahorcado completo
# (Cabeza, Torso, Brazo izq., Brazo der., Pie izq., Pie der.)
ETAPAS_AHORCADO = [
    # 0 fallos: solo la horca
    r"""
  _______
 |/      |
 |
 |
 |
 |
_|___
""",
    # 1 fallo: + Cabeza
    r"""
  _______
 |/      |
 |      (_)
 |
 |
 |
_|___
""",
    # 2 fallos: + Torso
    r"""
  _______
 |/      |
 |      (_)
 |       |
 |
 |
_|___
""",
    # 3 fallos: + Brazo izquierdo
    r"""
  _______
 |/      |
 |      (_)
 |      /|
 |
 |
_|___
""",
    # 4 fallos: + Brazo derecho
    r"""
  _______
 |/      |
 |      (_)
 |      /|\
 |
 |
_|___
""",
    # 5 fallos: + Pie izquierdo
    r"""
  _______
 |/      |
 |      (_)
 |      /|\
 |      /
 |
_|___
""",
    # 6 fallos: + Pie derecho -> ahorcado completo (derrota)
    r"""
  _______
 |/      |
 |      (_)
 |      /|\
 |      / \
 |
_|___
""",
]


def dibujar_ahorcado(intentos_fallidos: int) -> str:
    """Devuelve el arte ASCII correspondiente a la cantidad de fallos
    actuales (se limita entre 0 y 6, por si llega un valor fuera de rango)."""
    etapa = max(0, min(intentos_fallidos, len(ETAPAS_AHORCADO) - 1))
    return ETAPAS_AHORCADO[etapa]


def mostrar_palabra(palabra_mostrada: str) -> str:
    """Da formato a la palabra oculta agregando espacio entre cada
    carácter, para que se lea como '_ _ A _ _' en vez de '__A__'."""
    partes = []
    for token in palabra_mostrada.split(" "):
        partes.append(" ".join(token))
    return "   ".join(partes)  # espacio extra entre palabras distintas


def mostrar_letras_usadas(letras_usadas) -> str:
    """Muestra las letras jugadas hasta el momento, separadas por coma."""
    if not letras_usadas:
        return "(ninguna letra jugada todavía)"
    return ", ".join(letras_usadas)


def mostrar_intentos_restantes(intentos_fallidos: int, max_intentos: int) -> str:
    restantes = max(0, max_intentos - intentos_fallidos)
    return f"Intentos restantes: {restantes}/{max_intentos}"


def renderizar_pantalla(juego) -> str:
    """Arma la pantalla completa del juego a partir de una instancia de
    Automata. Es lo único que necesita llamar main.py."""
    lineas = []
    lineas.append(f"Categoría: {juego.pista}")
    lineas.append(dibujar_ahorcado(juego.intentos_fallidos))
    lineas.append("Palabra: " + mostrar_palabra(juego.obtener_palabra_mostrada()))
    lineas.append("Letras jugadas: " + mostrar_letras_usadas(juego.obtener_letras_usadas()))
    lineas.append(mostrar_intentos_restantes(juego.intentos_fallidos, juego.MAX_INTENTOS))
    return "\n".join(lineas)


def mostrar_mensaje_resultado(resultado_turno: dict) -> str:
    """Mensaje corto para mostrar debajo del dibujo tras cada jugada."""
    return f">> {resultado_turno['mensaje']}"


def mostrar_fin_de_juego(juego) -> str:
    if juego.estado == "GANADO":
        return f"¡GANASTE! La palabra era: {' '.join(juego.palabra)}"
    if juego.estado == "PERDIDO":
        return (
            f"PERDISTE. La palabra era: {' '.join(juego.palabra)}\n"
            f"Motivo: {juego.motivo_fin}"
        )
    return ""
