#Referencia de Alfabeto

VOCALES = set("AEIOU")
VOCALES_CON_TILDE = set("ÁÉÍÓÚ")
CONSONANTES = set("BCDFGHJKLMNÑPQRSTVWXYZ")

# Alfabeto castellano completo (incluye Ñ y vocales con tilde)
ALFABETO_CASTELLANO = VOCALES | VOCALES_CON_TILDE | CONSONANTES


#Validacion en base a las reglas
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


#Validacion de un solo caracter

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


#Validacion de una palabra completa

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


#Gestion de letras jugadas

class LetrasJugadas:

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