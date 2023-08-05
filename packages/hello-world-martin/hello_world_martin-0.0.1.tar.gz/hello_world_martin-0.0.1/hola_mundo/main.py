# main.py


def hola_mundo(nombre: str) -> None:
    """
    :param nombre: str
    Nombre de la persona a la que quieres saludar
    :return: None
    """
    print(f'¡Hola, {nombre}!')


if __name__ == '__main__':
    help(hola_mundo)