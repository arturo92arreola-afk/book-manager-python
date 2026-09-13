import json
import uuid
import re
import csv
from pathlib import Path
import flet as ft


class Utilerias:
    @staticmethod
    def generar_codigo():
        return str(uuid.uuid4())[:8]

    @staticmethod
    def validar_correo(correo):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(patron, correo))

    @staticmethod
    def validador_isbn13(isbn_str):
        isbn_limpio = isbn_str.replace("-", "").replace(" ", "")
        if len(isbn_limpio) != 13 or not isbn_limpio.isdigit():
            return False

        suma = 0
        for indice, digito in enumerate(isbn_limpio[:-1]):
            peso = 1 if indice % 2 == 0 else 3
            suma += int(digito) * peso

        digito_control_calculado = (10 - (suma % 10)) % 10
        return digito_control_calculado == int(isbn_limpio[-1])


class CargadorCSV:
    @staticmethod
    def leer_csv(ruta_archivo):
        ruta_obj = Path(ruta_archivo)
        if not ruta_obj.exists():
            return []

        registros = []
        try:
            with open(ruta_obj, mode="r", encoding="utf-8-sig", newline="") as archivo:
                muestra = archivo.read(2048)
                delimitador = ";" if ";" in muestra else ","
                archivo.seek(0)
                lector = csv.DictReader(archivo, delimiter=delimitador)
                registros.extend(dict(fila) for fila in lector)
            return registros
        except Exception:
            return []


class Autor:
    def __init__(self, nombre, id_autor=None):
        self.nombre = nombre
        self.id_autor = id_autor if id_autor else Utilerias.generar_codigo()

    def to_dict(self):
        return {"nombre": self.nombre, "id_autor": self.id_autor}

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("nombre"), data.get("id_autor"))


class Editorial:
    def __init__(self, nombre, id_editorial=None):
        self.nombre = nombre
        self.id_editorial = id_editorial if id_editorial else Utilerias.generar_codigo()

    def to_dict(self):
        return {"nombre": self.nombre, "id_editorial": self.id_editorial}

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("nombre"), data.get("id_editorial"))


class Formato:
    def __init__(self, tipo_formato, id_formato=None):
        self.tipo_formato = tipo_formato
        self.id_formato = id_formato if id_formato else Utilerias.generar_codigo()

    def to_dict(self):
        return {"tipo_formato": self.tipo_formato, "id_formato": self.id_formato}

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("tipo_formato"), data.get("id_formato"))


class Idioma:
    def __init__(self, idioma, id_idioma=None):
        self.idioma = idioma
        self.id_idioma = id_idioma if id_idioma else Utilerias.generar_codigo()

    def to_dict(self):
        return {"idioma": self.idioma, "id_idioma": self.id_idioma}

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("idioma"), data.get("id_idioma"))


class Usuario:
    def __init__(self, nombre, correo, password):
        self.nombre = nombre
        self.correo = correo
        self.password = password

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "correo": self.correo,
            "password": self.password,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("nombre"), data.get("correo"), data.get("password"))


class Libro:
    def __init__(self, titulo, edicion, isbn, autores, editorial, formato, idioma):
        self.titulo = titulo
        self.edicion = edicion
        self.isbn = isbn
        self.autores = autores
        self.editorial = editorial
        self.formato = formato
        self.idioma = idioma

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "edicion": self.edicion,
            "isbn": self.isbn,
            "autores": [
                a.to_dict() if hasattr(a, "to_dict") else a for a in self.autores
            ],
            "editorial": (
                self.editorial.to_dict()
                if hasattr(self.editorial, "to_dict")
                else self.editorial
            ),
            "formato": (
                self.formato.to_dict()
                if hasattr(self.formato, "to_dict")
                else self.formato
            ),
            "idioma": (
                self.idioma.to_dict()
                if hasattr(self.idioma, "to_dict")
                else self.idioma
            ),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("titulo"),
            data.get("edicion"),
            data.get("isbn"),
            data.get("autores", []),
            data.get("editorial"),
            data.get("formato"),
            data.get("idioma"),
        )


class GestorBiblioteca:
    RUTA_PROYECTO = Path(r"C:\Users\arreola.arturo\ARTURO JR\PROYECTOS PYTHON\libros")
    ARCHIVO_DATOS = RUTA_PROYECTO / "libros.json"

    def __init__(self):
        self.usuarios = []
        self.autores = []
        self.isbns = []
        self.titulos = []
        self.editoriales = []
        self.formatos = []
        self.idiomas = []
        self.RUTA_PROYECTO.mkdir(parents=True, exist_ok=True)
        self.cargar_datos()

    def cargar_datos(self):
        if not self.ARCHIVO_DATOS.exists():
            return

        try:
            with open(self.ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)

            self.usuarios = [
                Usuario.from_dict(u) for u in contenido.get("usuarios", [])
            ]
            self.autores = [
                Autor.from_dict(a) for a in contenido.get("autores", [])
            ]
            self.isbns = contenido.get("isbns", [])
            self.titulos = [
                Libro.from_dict(t) for t in contenido.get("titulos", [])
            ]
            self.editoriales = [
                Editorial.from_dict(e) for e in contenido.get("editoriales", [])
            ]
            self.formatos = [
                Formato.from_dict(f) for f in contenido.get("formatos", [])
            ]
            self.idiomas = [
                Idioma.from_dict(i) for i in contenido.get("idiomas", [])
            ]
        except (json.JSONDecodeError, OSError):
            pass

    def guardar_datos(self):
        contenido = {
            "usuarios": [u.to_dict() for u in self.usuarios],
            "autores": [a.to_dict() for a in self.autores],
            "isbns": self.isbns,
            "titulos": [t.to_dict() for t in self.titulos],
            "editoriales": [e.to_dict() for e in self.editoriales],
            "formatos": [f.to_dict() for f in self.formatos],
            "idiomas": [i.to_dict() for i in self.idiomas],
        }

        with open(self.ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(contenido, archivo, indent=4, ensure_ascii=False)


class BibliotecaFlet:
    def __init__(self, page: ft.Page):
        self.page = page
        self.gestor = GestorBiblioteca()
        self.usuario = None

        self.page.title = "Control de Libros"
        self.page.padding = 0
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.width = 1100
        self.page.window.height = 750

        self.mostrar_login()

    # ---------- Utilidades de UI ----------

    def snack(self, mensaje, error=False):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje),
            open=True,
        )
        self.page.update()

    def limpiar(self):
        self.page.controls.clear()

    def titulo_pagina(self, texto, subtitulo=None):
        controles = [
            ft.Text(texto, size=28, weight=ft.FontWeight.BOLD),
        ]
        if subtitulo:
            controles.append(ft.Text(subtitulo, color=ft.Colors.GREY_700))
        return ft.Column(controles, spacing=4)

    def boton_volver(self, destino):
        return ft.TextButton("← Volver", on_click=lambda e: destino())

    # ---------- Login / registro ----------

    def mostrar_login(self):
        self.limpiar()

        correo = ft.TextField(
            label="Correo",
            prefix_icon=ft.Icons.EMAIL,
            width=360,
        )
        password = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=360,
        )

        def iniciar(e):
            for usuario in self.gestor.usuarios:
                if usuario.correo == correo.value.strip() and usuario.password == password.value:
                    self.usuario = usuario
                    self.mostrar_menu()
                    return
            self.snack("Correo o contraseña incorrectos.", True)

        def registrar(e):
            self.mostrar_registro()

        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.MENU_BOOK, size=64),
                        ft.Text("Control de Libros", size=30, weight=ft.FontWeight.BOLD),
                        ft.Text("Inicia sesión para continuar"),
                        correo,
                        password,
                        ft.Button("Iniciar sesión", on_click=iniciar, width=360),
                        ft.TextButton("Crear nuevo usuario", on_click=registrar),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=16,
                ),
                padding=40,
            )
        )

        self.page.add(
            ft.Container(
                content=card,
                alignment=ft.Alignment.CENTER,
                expand=True,
            )
        )
        self.page.update()

    def mostrar_registro(self):
        self.limpiar()

        nombre = ft.TextField(label="Nombre", width=360)
        correo = ft.TextField(label="Correo", width=360)
        password = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=360,
        )

        def guardar(e):
            if not nombre.value.strip() or not correo.value.strip() or not password.value:
                self.snack("Completa todos los campos.", True)
                return

            if not Utilerias.validar_correo(correo.value.strip()):
                self.snack("El correo no es válido.", True)
                return

            if any(u.correo.lower() == correo.value.strip().lower() for u in self.gestor.usuarios):
                self.snack("Ese correo ya está registrado.", True)
                return

            usuario = Usuario(nombre.value.strip(), correo.value.strip(), password.value)
            self.gestor.usuarios.append(usuario)
            self.gestor.guardar_datos()
            self.snack("Usuario creado correctamente.")
            self.mostrar_login()

        self.page.add(
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                self.titulo_pagina("Crear usuario"),
                                nombre,
                                correo,
                                password,
                                ft.Button("Guardar", on_click=guardar, width=360),
                                ft.TextButton(
                                    "Ya tengo una cuenta",
                                    on_click=lambda e: self.mostrar_login(),
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=16,
                        ),
                        padding=40,
                    )
                ),
                alignment=ft.Alignment.CENTER,
                expand=True,
            )
        )
        self.page.update()

    # ---------- Menú principal ----------

    def mostrar_menu(self):
        self.limpiar()

        def cerrar(e):
            self.usuario = None
            self.mostrar_login()

        menu = [
            ("Libros", ft.Icons.MENU_BOOK, self.menu_libros),
            ("Autores", ft.Icons.PEOPLE, self.menu_autores),
            ("Editoriales", ft.Icons.BUSINESS, self.menu_editoriales),
            ("Formatos", ft.Icons.FOLDER, self.menu_formatos),
            ("Idiomas", ft.Icons.LANGUAGE, self.menu_idiomas),
            ("ISBNs", ft.Icons.QR_CODE, self.menu_isbns),
        ]

        botones = []
        for nombre, icono, funcion in menu:
            botones.append(
                ft.Button(
                    content=ft.Row(
                        [ft.Icon(icono), ft.Text(nombre)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    on_click=lambda e, f=funcion: f(),
                    width=260,
                    height=55,
                )
            )

        self.page.add(
            ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    "Control de Libros",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"Usuario: {self.usuario.nombre}",
                                    color=ft.Colors.GREY_700,
                                ),
                                ft.Container(expand=True),
                                ft.TextButton("Cerrar sesión", on_click=cerrar),
                            ],
                        ),
                        padding=20,
                    ),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Menú principal", size=22, weight=ft.FontWeight.BOLD),
                                ft.Text("Selecciona el módulo que deseas administrar."),
                                ft.Row(
                                    botones[:3],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Row(
                                    botones[3:],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=18,
                        ),
                        padding=30,
                        expand=True,
                    ),
                ],
                expand=True,
            )
        )
        self.page.update()

    # ---------- Componentes reutilizables ----------

    def vista_lista(self, titulo, filas, columnas, volver):
        self.limpiar()

        contenido = [
            ft.Row(
                [
                    self.boton_volver(volver),
                    self.titulo_pagina(titulo),
                ],
                spacing=20,
            ),
            ft.Divider(),
        ]

        if filas:
            contenido.append(
                ft.DataTable(
                    columns=[ft.DataColumn(ft.Text(c)) for c in columnas],
                    rows=[
                        ft.DataRow(cells=[ft.DataCell(ft.Text(str(v))) for v in fila])
                        for fila in filas
                    ],
                )
            )
        else:
            contenido.append(ft.Text("No hay registros.", size=18))

        self.page.add(
            ft.Container(
                content=ft.Column(contenido, scroll=ft.ScrollMode.AUTO),
                padding=25,
                expand=True,
            )
        )
        self.page.update()

    # ---------- Autores ----------

    def menu_autores(self):
        self.limpiar()

        def registrar(e):
            nombre = ft.TextField(label="Nombre del autor")

            def guardar(ev):
                if not nombre.value.strip():
                    self.snack("Escribe el nombre.", True)
                    return
                autor = Autor(nombre.value.strip())
                self.gestor.autores.append(autor)
                self.gestor.guardar_datos()
                self.snack(f"Autor registrado. ID: {autor.id_autor}")
                self.menu_autores()

            self.dialogo("Registrar autor", [nombre], guardar)

        def buscar(e):
            self.buscar_por_id(
                "Buscar autor",
                self.gestor.autores,
                "id_autor",
                ["nombre", "id_autor"],
            )

        def consultar(e):
            self.consultar_texto(
                "Consultar autor",
                self.gestor.autores,
                lambda a: a.nombre,
            )

        def eliminar(e):
            self.eliminar_por_id(
                "Eliminar autor",
                self.gestor.autores,
                "id_autor",
                lambda: self.menu_autores(),
            )

        self.menu_crud(
            "Autores",
            [
                ("Registrar nuevo autor", registrar),
                ("Mostrar lista", lambda e: self.vista_lista(
                    "Autores",
                    [(a.nombre, a.id_autor) for a in self.gestor.autores],
                    ["Nombre", "ID"],
                    self.menu_autores,
                )),
                ("Buscar por ID", buscar),
                ("Consultar por texto", consultar),
                ("Eliminar", eliminar),
            ],
            self.mostrar_menu,
        )

    # ---------- Editoriales ----------

    def menu_editoriales(self):
        self.menu_crud(
            "Editoriales",
            [
                ("Registrar nueva editorial", lambda e: self.registrar_simple(
                    "Editorial", Editorial, "nombre", self.gestor.editoriales, self.menu_editoriales
                )),
                ("Mostrar lista", lambda e: self.vista_lista(
                    "Editoriales",
                    [(x.nombre, x.id_editorial) for x in self.gestor.editoriales],
                    ["Nombre", "ID"],
                    self.menu_editoriales,
                )),
                ("Buscar por ID", lambda e: self.buscar_por_id(
                    "Buscar editorial", self.gestor.editoriales, "id_editorial", ["nombre", "id_editorial"]
                )),
                ("Consultar por texto", lambda e: self.consultar_texto(
                    "Consultar editorial", self.gestor.editoriales, lambda x: x.nombre
                )),
                ("Eliminar", lambda e: self.eliminar_por_id(
                    "Eliminar editorial", self.gestor.editoriales, "id_editorial", self.menu_editoriales
                )),
            ],
            self.mostrar_menu,
        )

    # ---------- Formatos ----------

    def menu_formatos(self):
        self.menu_crud(
            "Formatos",
            [
                ("Registrar nuevo formato", lambda e: self.registrar_simple(
                    "Formato", Formato, "tipo_formato", self.gestor.formatos, self.menu_formatos
                )),
                ("Mostrar lista", lambda e: self.vista_lista(
                    "Formatos",
                    [(x.tipo_formato, x.id_formato) for x in self.gestor.formatos],
                    ["Formato", "ID"],
                    self.menu_formatos,
                )),
                ("Buscar por ID", lambda e: self.buscar_por_id(
                    "Buscar formato", self.gestor.formatos, "id_formato", ["tipo_formato", "id_formato"]
                )),
                ("Consultar por texto", lambda e: self.consultar_texto(
                    "Consultar formato", self.gestor.formatos, lambda x: x.tipo_formato
                )),
                ("Eliminar", lambda e: self.eliminar_por_id(
                    "Eliminar formato", self.gestor.formatos, "id_formato", self.menu_formatos
                )),
            ],
            self.mostrar_menu,
        )

    # ---------- Idiomas ----------

    def menu_idiomas(self):
        self.menu_crud(
            "Idiomas",
            [
                ("Registrar nuevo idioma", lambda e: self.registrar_simple(
                    "Idioma", Idioma, "idioma", self.gestor.idiomas, self.menu_idiomas
                )),
                ("Mostrar lista", lambda e: self.vista_lista(
                    "Idiomas",
                    [(x.idioma, x.id_idioma) for x in self.gestor.idiomas],
                    ["Idioma", "ID"],
                    self.menu_idiomas,
                )),
                ("Buscar por ID", lambda e: self.buscar_por_id(
                    "Buscar idioma", self.gestor.idiomas, "id_idioma", ["idioma", "id_idioma"]
                )),
                ("Consultar por texto", lambda e: self.consultar_texto(
                    "Consultar idioma", self.gestor.idiomas, lambda x: x.idioma
                )),
                ("Eliminar", lambda e: self.eliminar_por_id(
                    "Eliminar idioma", self.gestor.idiomas, "id_idioma", self.menu_idiomas
                )),
            ],
            self.mostrar_menu,
        )

    # ---------- ISBN ----------

    def menu_isbns(self):
        self.menu_crud(
            "ISBNs",
            [
                ("Registrar y validar ISBN-13", lambda e: self.registrar_isbn()),
                ("Mostrar lista", lambda e: self.vista_lista(
                    "ISBNs",
                    [(x,) for x in self.gestor.isbns],
                    ["ISBN"],
                    self.menu_isbns,
                )),
                ("Consultar ISBN", lambda e: self.consultar_texto(
                    "Consultar ISBN", self.gestor.isbns, lambda x: x
                )),
            ],
            self.mostrar_menu,
        )

    def registrar_isbn(self):
        campo = ft.TextField(label="ISBN-13", hint_text="978...")
        self.dialogo("Registrar ISBN", [campo], lambda e: self.guardar_isbn(campo))

    def guardar_isbn(self, campo):
        isbn = campo.value.strip()
        if not Utilerias.validador_isbn13(isbn):
            self.snack("El ISBN-13 no es válido.", True)
            return

        if isbn not in self.gestor.isbns:
            self.gestor.isbns.append(isbn)
            self.gestor.guardar_datos()
            self.snack("ISBN registrado correctamente.")
        else:
            self.snack("Ese ISBN ya existe.")
        self.menu_isbns()

    # ---------- Libros ----------

    def menu_libros(self):
        self.limpiar()

        def nuevo(e):
            self.formulario_libro()

        def mostrar(e):
            filas = []
            for libro in self.gestor.titulos:
                autores = ", ".join(
                    a.get("nombre", "") if isinstance(a, dict) else getattr(a, "nombre", "")
                    for a in (libro.autores or [])
                )
                editorial = (
                    libro.editorial.get("nombre", "")
                    if isinstance(libro.editorial, dict)
                    else getattr(libro.editorial, "nombre", "")
                )
                formato = (
                    libro.formato.get("tipo_formato", "")
                    if isinstance(libro.formato, dict)
                    else getattr(libro.formato, "tipo_formato", "")
                )
                idioma = (
                    libro.idioma.get("idioma", "")
                    if isinstance(libro.idioma, dict)
                    else getattr(libro.idioma, "idioma", "")
                )
                filas.append(
                    (
                        libro.titulo,
                        libro.edicion,
                        libro.isbn,
                        autores or "Sin autor",
                        editorial or "N/A",
                        formato or "N/A",
                        idioma or "N/A",
                    )
                )

            self.vista_lista(
                "Catálogo de libros",
                filas,
                ["Título", "Edición", "ISBN", "Autores", "Editorial", "Formato", "Idioma"],
                self.menu_libros,
            )

        def consultar(e):
            campo = ft.TextField(label="Título o ISBN")

            def ejecutar(ev):
                criterio = campo.value.strip().lower()
                resultados = [
                    l for l in self.gestor.titulos
                    if criterio in str(l.titulo).lower()
                    or criterio in str(l.isbn).lower()
                ]
                self.page.dialog.open = False
                self.page.update()

                if resultados:
                    filas = [(l.titulo, l.edicion, l.isbn) for l in resultados]
                    self.vista_lista(
                        f"Resultados ({len(resultados)})",
                        filas,
                        ["Título", "Edición", "ISBN"],
                        self.menu_libros,
                    )
                else:
                    self.snack("No se encontraron libros.")

            self.dialogo("Consultar libro", [campo], ejecutar)

        def importar(e):
            campo = ft.TextField(label="Nombre del CSV", hint_text="libros.csv")

            def ejecutar(ev):
                ruta = self.gestor.RUTA_PROYECTO / campo.value.strip()
                registros = CargadorCSV.leer_csv(ruta)

                if not registros:
                    self.snack("No se pudo leer el CSV o está vacío.", True)
                    return

                importados = 0
                for fila in registros:
                    titulo = (fila.get("titulo") or "").strip()
                    isbn = (fila.get("isbn") or "").strip()

                    if not titulo or not Utilerias.validador_isbn13(isbn):
                        continue

                    autor = self.obtener_autor(fila.get("autor"))
                    editorial = self.obtener_editorial(fila.get("editorial"))
                    formato = self.obtener_formato(fila.get("formato"))
                    idioma = self.obtener_idioma(fila.get("idioma"))

                    libro = Libro(
                        titulo,
                        fila.get("edicion"),
                        isbn,
                        [autor.to_dict()] if autor else [],
                        editorial.to_dict() if editorial else {},
                        formato.to_dict() if formato else {},
                        idioma.to_dict() if idioma else {},
                    )
                    self.gestor.titulos.append(libro)
                    if isbn not in self.gestor.isbns:
                        self.gestor.isbns.append(isbn)
                    importados += 1

                self.gestor.guardar_datos()
                self.snack(f"Se importaron {importados} libros.")
                self.menu_libros()

            self.dialogo("Importar CSV", [campo], ejecutar)

        self.menu_crud(
            "Libros",
            [
                ("Registrar nuevo libro", nuevo),
                ("Mostrar catálogo", mostrar),
                ("Consultar por título o ISBN", consultar),
                ("Importar desde CSV", importar),
            ],
            self.mostrar_menu,
        )

    def formulario_libro(self):
        self.limpiar()

        titulo = ft.TextField(label="Título")
        edicion = ft.TextField(label="Edición")
        isbn = ft.TextField(label="ISBN-13")

        autores = ft.Dropdown(
            label="Autor",
            options=[ft.DropdownOption(key=a.id_autor, text=a.nombre) for a in self.gestor.autores],
        )
        editoriales = ft.Dropdown(
            label="Editorial",
            options=[
                ft.DropdownOption(key=e.id_editorial, text=e.nombre)
                for e in self.gestor.editoriales
            ],
        )
        formatos = ft.Dropdown(
            label="Formato",
            options=[
                ft.DropdownOption(key=f.id_formato, text=f.tipo_formato)
                for f in self.gestor.formatos
            ],
        )
        idiomas = ft.Dropdown(
            label="Idioma",
            options=[
                ft.DropdownOption(key=i.id_idioma, text=i.idioma)
                for i in self.gestor.idiomas
            ],
        )

        def guardar(e):
            if not titulo.value.strip() or not isbn.value.strip():
                self.snack("Título e ISBN son obligatorios.", True)
                return

            if not Utilerias.validador_isbn13(isbn.value.strip()):
                self.snack("El ISBN-13 no es válido.", True)
                return

            autor = next(
                (a for a in self.gestor.autores if a.id_autor == autores.value),
                None,
            )
            editorial = next(
                (x for x in self.gestor.editoriales if x.id_editorial == editoriales.value),
                None,
            )
            formato = next(
                (x for x in self.gestor.formatos if x.id_formato == formatos.value),
                None,
            )
            idioma = next(
                (x for x in self.gestor.idiomas if x.id_idioma == idiomas.value),
                None,
            )

            libro = Libro(
                titulo.value.strip(),
                edicion.value.strip(),
                isbn.value.strip(),
                [autor.to_dict()] if autor else [],
                editorial.to_dict() if editorial else {},
                formato.to_dict() if formato else {},
                idioma.to_dict() if idioma else {},
            )

            self.gestor.titulos.append(libro)
            if isbn.value.strip() not in self.gestor.isbns:
                self.gestor.isbns.append(isbn.value.strip())

            self.gestor.guardar_datos()
            self.snack("Libro registrado correctamente.")
            self.menu_libros()

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                self.boton_volver(self.menu_libros),
                                self.titulo_pagina("Registrar libro"),
                            ]
                        ),
                        ft.Divider(),
                        titulo,
                        edicion,
                        isbn,
                        autores,
                        editoriales,
                        formatos,
                        idiomas,
                        ft.Button("Guardar libro", on_click=guardar),
                    ],
                    spacing=14,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=25,
                expand=True,
            )
        )
        self.page.update()

    # ---------- Helpers CRUD ----------

    def menu_crud(self, titulo, acciones, volver):
        self.limpiar()

        controles = [
            ft.Row(
                [
                    self.boton_volver(volver),
                    self.titulo_pagina(titulo),
                ],
                spacing=20,
            ),
            ft.Divider(),
        ]

        for texto, funcion in acciones:
            controles.append(
                ft.Button(texto, on_click=funcion, width=360, height=48)
            )

        self.page.add(
            ft.Container(
                content=ft.Column(
                    controles,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=14,
                    scroll=ft.ScrollMode.AUTO,
                ),
                padding=25,
                expand=True,
            )
        )
        self.page.update()

    def dialogo(self, titulo, campos, guardar):
        def cerrar(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo),
            content=ft.Column(campos, tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar),
                ft.Button("Guardar", on_click=guardar),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def buscar_por_id(self, titulo, lista, atributo_id, atributos):
        campo = ft.TextField(label="ID")

        def ejecutar(e):
            valor = campo.value.strip()
            encontrado = next(
                (x for x in lista if getattr(x, atributo_id, None) == valor),
                None,
            )
            self.page.dialog.open = False
            self.page.update()

            if encontrado:
                datos = [
                    ft.Text(f"{a}: {getattr(encontrado, a, '')}")
                    for a in atributos
                ]
                self.page.dialog = ft.AlertDialog(
                    title=ft.Text(titulo),
                    content=ft.Column(datos, tight=True),
                    actions=[
                        ft.TextButton(
                            "Cerrar",
                            on_click=lambda ev: self.cerrar_dialogo(),
                        )
                    ],
                )
                self.page.dialog.open = True
                self.page.update()
            else:
                self.snack("No se encontró el registro.")

        self.dialogo(titulo, [campo], ejecutar)

    def consultar_texto(self, titulo, lista, getter):
        campo = ft.TextField(label="Texto a buscar")

        def ejecutar(e):
            criterio = campo.value.strip().lower()
            resultados = [x for x in lista if criterio in str(getter(x)).lower()]

            self.page.dialog.open = False
            self.page.update()

            if resultados:
                filas = [(getter(x),) for x in resultados]
                self.vista_lista(
                    f"{titulo} ({len(resultados)})",
                    filas,
                    ["Resultado"],
                    self.mostrar_menu,
                )
            else:
                self.snack("No se encontraron coincidencias.")

        self.dialogo(titulo, [campo], ejecutar)

    def eliminar_por_id(self, titulo, lista, atributo_id, volver):
        campo = ft.TextField(label="ID")

        def ejecutar(e):
            valor = campo.value.strip()
            elemento = next(
                (x for x in lista if getattr(x, atributo_id, None) == valor),
                None,
            )

            if elemento is None:
                self.snack("No se encontró el registro.")
                return

            lista.remove(elemento)
            self.gestor.guardar_datos()
            self.page.dialog.open = False
            self.page.update()
            self.snack("Registro eliminado.")
            volver()

        self.dialogo(titulo, [campo], ejecutar)

    def registrar_simple(self, etiqueta, clase, atributo, lista, volver):
        campo = ft.TextField(label=etiqueta)

        def guardar(e):
            valor = campo.value.strip()
            if not valor:
                self.snack("El campo es obligatorio.", True)
                return

            elemento = clase(valor)
            lista.append(elemento)
            self.gestor.guardar_datos()
            self.page.dialog.open = False
            self.page.update()
            self.snack(f"{etiqueta} registrado correctamente.")
            volver()

        self.dialogo(f"Registrar {etiqueta.lower()}", [campo], guardar)

    def cerrar_dialogo(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    # ---------- Resolución de relaciones ----------

    def obtener_autor(self, nombre):
        if not nombre:
            return None
        for x in self.gestor.autores:
            if x.nombre.lower() == nombre.strip().lower():
                return x
        x = Autor(nombre.strip())
        self.gestor.autores.append(x)
        return x

    def obtener_editorial(self, nombre):
        if not nombre:
            return None
        for x in self.gestor.editoriales:
            if x.nombre.lower() == nombre.strip().lower():
                return x
        x = Editorial(nombre.strip())
        self.gestor.editoriales.append(x)
        return x

    def obtener_formato(self, nombre):
        if not nombre:
            return None
        for x in self.gestor.formatos:
            if x.tipo_formato.lower() == nombre.strip().lower():
                return x
        x = Formato(nombre.strip())
        self.gestor.formatos.append(x)
        return x

    def obtener_idioma(self, nombre):
        if not nombre:
            return None
        for x in self.gestor.idiomas:
            if x.idioma.lower() == nombre.strip().lower():
                return x
        x = Idioma(nombre.strip())
        self.gestor.idiomas.append(x)
        return x


def main(page: ft.Page):
    BibliotecaFlet(page)


if __name__ == "__main__":
    ft.run(main)
