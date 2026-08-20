from Funciones import LetrasJugadas
import random


class Automata:
   
    PARTES_AHORCADO = [
        "Cabeza",
        "Torso",
        "Brazo izquierdo",
        "Brazo derecho",
        "Pie izquierdo",
        "Pie derecho",
    ]
    MAX_INTENTOS = len(PARTES_AHORCADO)

    def __init__(self):
        self.banco_palabras = {
            "Nombres": ["MARÍA", "JUAN", "JOSÉ", "BORIS", "PABLO", "DIEGO", "ÁNGEL", "CHISTOPHER", "ARIANA", "GRACIELA"],
            "Animales": ["PERRO", "GATO", "TOPO", "LEÓN", "TIGRE", "BALLENA", "CAMARÓN", "TUNGTUNG", "GUACAMAYA", "ARDILLA"],
            "Videojuegos": ["MINECRAFT", "SMASH BROS", "CLUB PENGUIN", "CALL OF DUTY", "FIFA", "DARK SOULS", "HOLLOW KNIGHT", "PEAK", "FORTNITE", "SUPER SMASH BROS"],
            "Celebridades": ["TOM HOLLAND", "BEN AFFLECK", "TOM CRUISE", "GUILLERMO DEL TORO", "FARAON LOVE SHADY", "ROSALÍA", "ZENDAYA", "ROBERT DOWNEY JR", "SYDELLE NOEL", "NICOLAS CAGE"],
            "Peliculas": ["TIBURÓN", "ALIEN", "RATATOUILLE", "WHIPLASH", "MOON", "ROMA", "TIMECRIMES", "DRIVE", "AMÉLIE", "COHERENCE"],
            "Idiomas": ["CROATA", "ESPAÑOL", "COREANO", "MANDARÍN", "TURCO", "RUMANO", "KAKCHIQUEL", "INGLÉS", "BÚLGARO"],
        }
        self.palabra = None            # lista de palabras, p. ej. ["SMASH", "BROS"]
        self.pista = None              # categoría
        self.letras_check = LetrasJugadas()

        self.estado = "EN_JUEGO"
        self.intentos_fallidos = 0
        self.tabla_aid = []            # historial de eventos para la UI 2
        self.motivo_fin = None         # se llena cuando el juego termina

        self.iniciar()

    def iniciar(self):
        categorias = list(self.banco_palabras.keys())
        cat = random.choice(categorias)
        palabras = self.banco_palabras[cat]
        palabra = random.choice(list(palabras))

        self.palabra = palabra.split()
        self.pista = cat

        self.letras_check.reiniciar()
        self.estado = "EN_JUEGO"
        self.intentos_fallidos = 0
        self.tabla_aid = []
        self.motivo_fin = None

        return self.palabra

    def evaluar_entrada(self, texto):
        
        texto = texto.upper()
        chars = list(texto.strip())
        resultado, mensaje, palabra_mostrada = self.letras_check.procesar(chars, self.palabra)
        return resultado, mensaje, palabra_mostrada

    def jugar_turno(self, texto):
        
        estado_previo = self.estado

        if self.estado != "EN_JUEGO":
            fila = self._registrar_fila(
                entrada=texto,
                resultado="IGNORADO",
                mensaje="La partida ya finalizó. Reinicia para jugar de nuevo.",
                estado_previo=estado_previo,
                estado_nuevo=self.estado,
            )
            return {
                "resultado": "IGNORADO",
                "mensaje": fila["mensaje"],
                "palabra_mostrada": self.letras_check._mostrar_palabra(self.palabra),
                "estado": self.estado,
                "intentos_fallidos": self.intentos_fallidos,
                "parte_dibujada": None,
                "fila_aid": fila,
            }

        resultado, mensaje, palabra_mostrada = self.evaluar_entrada(texto)
        parte_dibujada = None

        if resultado == self.letras_check.ERROR_FATAL:
            self.estado = "PERDIDO"
            self.motivo_fin = mensaje

        elif resultado == self.letras_check.FALLO:
            self.intentos_fallidos += 1
            if self.intentos_fallidos <= self.MAX_INTENTOS:
                parte_dibujada = self.PARTES_AHORCADO[self.intentos_fallidos - 1]
            if self.intentos_fallidos >= self.MAX_INTENTOS:
                self.estado = "PERDIDO"
                self.motivo_fin = "Se agotaron los intentos: el ahorcado se completó."

        elif resultado == self.letras_check.ACIERTO:
            if self.letras_check.palabra_completa(self.palabra):
                self.estado = "GANADO"
                self.motivo_fin = "¡Palabra adivinada por completo!"


        fila = self._registrar_fila(
            entrada=texto,
            resultado=resultado,
            mensaje=mensaje,
            estado_previo=estado_previo,
            estado_nuevo=self.estado,
        )

        return {
            "resultado": resultado,
            "mensaje": mensaje,
            "palabra_mostrada": palabra_mostrada,
            "estado": self.estado,
            "intentos_fallidos": self.intentos_fallidos,
            "parte_dibujada": parte_dibujada,
            "fila_aid": fila,
        }

    def _registrar_fila(self, entrada, resultado, mensaje, estado_previo, estado_nuevo):
        fila = {
            "n": len(self.tabla_aid) + 1,
            "entrada": entrada,
            "estado_previo": estado_previo,
            "resultado": resultado,
            "estado_nuevo": estado_nuevo,
            "mensaje": mensaje,
            "intentos_fallidos": self.intentos_fallidos,
        }
        self.tabla_aid.append(fila)
        return fila

    def obtener_tabla_aid(self):
        return list(self.tabla_aid)

    def obtener_palabra_mostrada(self):
        return self.letras_check._mostrar_palabra(self.palabra)

    def obtener_letras_usadas(self):
        return sorted(self.letras_check.obtener_usadas())

    def obtener_partes_dibujadas(self):
        return self.PARTES_AHORCADO[: self.intentos_fallidos]

    def esta_terminado(self):
        return self.estado != "EN_JUEGO"
