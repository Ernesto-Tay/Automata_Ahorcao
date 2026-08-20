VOCALES = set("AEIOU")
VOCALES_CON_TILDE = set("ÁÉÍÓÚ")
CONSONANTES = set("BCDFGHJKLMNÑPQRSTVWXYZ")

# Alfabeto castellano completo (incluye Ñ y vocales con tilde)
ALFABETO_CASTELLANO = VOCALES | VOCALES_CON_TILDE | CONSONANTES


# Validación en base a las reglas
def es_mayuscula(caracter: str) -> str:
    return caracter.upper()


def no_tiene_numero_ni_simbolo(caracter: str) -> bool:
    return caracter.isalpha()


def pertenece_alfabeto_castellano(caracter: str) -> bool:
    return caracter in ALFABETO_CASTELLANO


def tilde_en_lugar_correcto(caracter: str) -> bool:
    if caracter in VOCALES_CON_TILDE:
        return True
    if caracter in CONSONANTES or caracter in VOCALES:
        return True
    # Cualquier otro caso (p. ej. una consonante "tildada" o símbolo raro)
    return False


# ---------------------------------------------------------------------
# Validación de un solo carácter
# ---------------------------------------------------------------------
def validar_letra(caracter: str) -> tuple[bool, str, str]:
    if len(caracter) != 1:
        return False, "Solo se permite ingresar un carácter a la vez.", caracter

    # Regla 1: se convierte automáticamente a mayúscula
    caracter = es_mayuscula(caracter)

    if not no_tiene_numero_ni_simbolo(caracter):
        return False, "No se permiten números ni símbolos.", caracter

    if not pertenece_alfabeto_castellano(caracter):
        return False, "El carácter no pertenece al alfabeto castellano.", caracter

    if not tilde_en_lugar_correcto(caracter):
        return False, "La tilde solo es válida sobre una vocal.", caracter

    return True, "Carácter válido.", caracter


# ---------------------------------------------------------------------
# Validación de una palabra completa
# ---------------------------------------------------------------------
def validar_palabra(palabra: str) -> tuple[bool, str, str]:
    if not palabra:
        return False, "La palabra no puede estar vacía.", palabra

    palabra_normalizada = ""
    for i, caracter in enumerate(palabra, start=1):
        valido, mensaje, caracter_normalizado = validar_letra(caracter)
        if not valido:
            return False, f"Carácter '{caracter}' (posición {i}) inválido: {mensaje}", palabra
        palabra_normalizada += caracter_normalizado

    return True, "Palabra válida.", palabra_normalizada


# ---------------------------------------------------------------------
# Gestión de letras jugadas
# ---------------------------------------------------------------------
class LetrasJugadas:

    # Códigos de resultado que devuelve procesar()
    ACIERTO = "ACIERTO"        # la letra es válida y SÍ está en la palabra
    FALLO = "FALLO"            # la letra es válida pero NO está en la palabra (cuenta como error de ahorcado)
    REPETIDA = "REPETIDA"      # la letra ya había sido jugada (no cuenta como error, solo se avisa)
    ERROR_FATAL = "ERROR_FATAL"  # entrada inválida (número, símbolo, fuera del alfabeto, tilde mal puesta, etc.)

    def __init__(self):
        self._usadas = set()

    def intentar_agregar(self, caracter: str) -> tuple[bool, str]:
        valido, mensaje, caracter = validar_letra(caracter)
        if not valido:
            return False, mensaje

        if caracter in self._usadas:
            return False, f"La letra '{caracter}' ya fue utilizada."

        self._usadas.add(caracter)
        return True, f"Letra '{caracter}' agregada correctamente."

    def ya_jugada(self, caracter: str) -> bool:
        return caracter in self._usadas

    def obtener_usadas(self) -> set:
        return set(self._usadas)

    def reiniciar(self) -> None:
        """Limpia las letras jugadas. Se usa al iniciar una nueva partida."""
        self._usadas = set()

    # -------------------------------------------------------------
    # Método que conecta la validación (Code 1) con la lógica
    # comparativa que necesita el Autómata / la tabla del AID (Code 2)
    # -------------------------------------------------------------
    def procesar(self, chars, palabra_objetivo: list[str]) -> tuple[str, str, str]:
        """
        chars: lista con el/los carácter(es) recién ingresados. El juego
               trabaja de a una letra por turno, así que se evalúa chars[0].
        palabra_objetivo: lista de palabras de la respuesta, p. ej.
                           ["SMASH", "BROS"].

        Retorna una tupla (resultado, mensaje, palabra_mostrada):
          - resultado: uno de ACIERTO / FALLO / REPETIDA / ERROR_FATAL
          - mensaje: texto explicativo para mostrar en la tabla del AID
          - palabra_mostrada: la palabra objetivo con las letras aún no
                               adivinadas reemplazadas por guiones bajos
        """
        if not chars:
            return self.ERROR_FATAL, "No se ingresó ningún carácter.", self._mostrar_palabra(palabra_objetivo)

        caracter = chars[0]
        valido, mensaje = self.intentar_agregar(caracter)

        if not valido:
            if "ya fue utilizada" in mensaje:
                # Letra repetida: NO es un error fatal, solo se informa
                return self.REPETIDA, mensaje, self._mostrar_palabra(palabra_objetivo)
            # Cualquier otro motivo de invalidez es error fatal
            # (número, símbolo, fuera del alfabeto castellano, tilde mal
            # colocada, más de un carácter ingresado, etc.)
            return self.ERROR_FATAL, mensaje, self._mostrar_palabra(palabra_objetivo)

        caracter = caracter.upper()
        letras_palabra = set("".join(palabra_objetivo))

        if caracter in letras_palabra:
            return (
                self.ACIERTO,
                f"¡Correcto! La letra '{caracter}' está en la palabra.",
                self._mostrar_palabra(palabra_objetivo),
            )

        return (
            self.FALLO,
            f"La letra '{caracter}' no forma parte de la palabra.",
            self._mostrar_palabra(palabra_objetivo),
        )

    def _mostrar_palabra(self, palabra_objetivo: list[str]) -> str:
        """Arma el string tipo '_ A _ _' con las letras ya adivinadas."""
        partes = []
        for palabra in palabra_objetivo:
            mostrada = "".join(letra if letra in self._usadas else "_" for letra in palabra)
            partes.append(mostrada)
        return " ".join(partes)

    def palabra_completa(self, palabra_objetivo: list[str]) -> bool:
        """True si todas las letras de la palabra objetivo ya fueron adivinadas."""
        letras_palabra = set("".join(palabra_objetivo))
        return letras_palabra.issubset(self._usadas)
