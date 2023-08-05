def saludo(nombre: str) -> None:
    """
    Función que sirve para saludar
    :param nombre: str
    El nombre de la persona a quien vas a saludar
    :return: None
    """
    print(f'Hola, {nombre}')


def main():
    # Si queremos conocer los detalles de una función
    # siempre podemos usar help(nombre_funcion)
    # help(saludo)
    saludo("Martín")


if __name__ == "__main__":
    main()

"""
Configuraciones oficiales de setup.py:
https://setuptools.readthedocs.io/en/latest/references/keywords.html
"""

"""
Licencias:
MIT -> https://choosealicense.com/licenses/mit/
TODAS -> https://choosealicense.com/licenses/
"""