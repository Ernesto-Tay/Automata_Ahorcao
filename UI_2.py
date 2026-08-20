ENCABEZADOS = ["#", "Estado previo", "Entrada", "Resultado", "Estado nuevo", "Mensaje"]
ANCHOS = [3, 13, 8, 12, 13, 45]


def _formatear_fila(valores):
    celdas = []
    for valor, ancho in zip(valores, ANCHOS):
        texto = str(valor)
        if len(texto) > ancho:
            texto = texto[: ancho - 3] + "..."
        celdas.append(texto.ljust(ancho))
    return " | ".join(celdas)


def _linea_separadora():
    return "-+-".join("-" * ancho for ancho in ANCHOS)


def imprimir_encabezado():
    print(_formatear_fila(ENCABEZADOS))
    print(_linea_separadora())


def imprimir_fila(fila: dict):
    """Imprime una única fila de la tabla del AID (para actualizarla en
    vivo, turno a turno)."""
    valores = [
        fila["n"],
        fila["estado_previo"],
        fila["entrada"],
        fila["resultado"],
        fila["estado_nuevo"],
        fila["mensaje"],
    ]
    print(_formatear_fila(valores))


def imprimir_tabla_aid(tabla_aid: list):
    """Imprime la tabla completa del AID de una sola vez."""
    imprimir_encabezado()
    if not tabla_aid:
        print("(sin movimientos todavía)")
        return
    for fila in tabla_aid:
        imprimir_fila(fila)


def imprimir_motivo_finalizacion(juego):
    """Muestra el motivo de finalización cuando la partida termina por
    un error fatal o por agotar los intentos/ganar."""
    if juego.estado == "EN_JUEGO":
        return
    print()
    print("=" * 60)
    print(f"PARTIDA FINALIZADA - Estado: {juego.estado}")
    print(f"Motivo: {juego.motivo_fin}")
    print("=" * 60)