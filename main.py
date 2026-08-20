import os

from automata import Automata
import UI_2
import UI_1


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pedir_letra() -> str:
    entrada = input("Ingresa una letra: ").strip()
    return entrada


def jugar_partida():
    juego = Automata()

    while not juego.esta_terminado():
        limpiar_pantalla()
        print(UI_1.renderizar_pantalla(juego))
        print()

        entrada = pedir_letra()
        resultado_turno = juego.jugar_turno(entrada)

        print()
        print(UI_1.mostrar_mensaje_resultado(resultado_turno))
        print()
        print("Tabla del AID:")
        UI_2.imprimir_tabla_aid(juego.obtener_tabla_aid())

        input("\nPresiona ENTER para continuar...")

    # Pantalla final
    limpiar_pantalla()
    print(UI_1.renderizar_pantalla(juego))
    print()
    print(UI_1.mostrar_fin_de_juego(juego))
    UI_2.imprimir_motivo_finalizacion(juego)


def main():
    while True:
        jugar_partida()
        de_nuevo = input("\n¿Jugar de nuevo? (s/n): ").strip().lower()
        if de_nuevo != "s":
            print("¡Gracias por jugar!")
            break


if __name__ == "__main__":
    main()
