import json
import uuid
import re
import os
import csv
from pathlib import Path

class Utilerias:
    @staticmethod
    def generar_codigo():
        return str(uuid.uuid4())[:8]

    @staticmethod
    def validar_correo(correo):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
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
        digito_control_real = int(isbn_limpio[-1])
        return digito_control_calculado == digito_control_real


class CargadorCSV:
    @staticmethod
    def leer_csv(ruta_archivo):
        """Lee un archivo CSV y devuelve una lista de diccionarios utilizando la primera fila como cabecera."""
        ruta_obj = Path(ruta_archivo)
        if not ruta_obj.exists():
            print(f"El archivo '{ruta_obj}' no existe.")
            return []
        
        registros = []
        try:
            with open(ruta_obj, mode='r', encoding='utf-8-sig') as archivo:
                muestra = archivo.read(2048)
                delimitador = ';' if ';' in muestra else ','
                archivo.seek(0)
                
                lector = csv.DictReader(archivo, delimiter=delimitador)
                for fila in lector:
                    registros.append(dict(fila))
                    
            print(f"¡Éxito! Se cargaron {len(registros)} registros desde {ruta_obj.name}")
            return registros
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo CSV: {e}")
            return []


class Autor:
    def __init__(self, nombre, id_autor=None):
        self.nombre = nombre
        self.id_autor = id_autor if id_autor else Utilerias.generar_codigo()

    def to_dict(self):
        return {"nombre": self.nombre, "id_autor": self.id_autor}

    @classmethod
    def from_dict(cls, data):
        return cls(nombre=data.get("nombre"), id_autor=data.get("id_autor"))


class Editorial:
    def __init__(self, nombre, id_editorial=None):
        self.nombre = nombre
        self.id_editorial = id_editorial if id_editorial else Utilerias.generar_codigo()

    def to_dict(self):
        return {"nombre": self.nombre, "id_editorial": self.id_editorial}

    @classmethod
    def from_dict(cls, data):
        return cls(nombre=data.get("nombre"), id_editorial=data.get("id_editorial"))


class Formato:
    def __init__(self, tipo_formato, id_formato=None):
        self.tipo_formato = tipo_formato
        self.id_formato = id_formato if id_formato else Utilerias.generar_codigo()

    def to_dict(self):
        return {"tipo_formato": self.tipo_formato, "id_formato": self.id_formato}

    @classmethod
    def from_dict(cls, data):
        return cls(tipo_formato=data.get("tipo_formato"), id_formato=data.get("id_formato"))


class Idioma:
    def __init__(self, idioma, id_idioma=None):
        self.idioma = idioma
        self.id_idioma = id_idioma if id_idioma else Utilerias.generar_codigo()

    def to_dict(self):
        return {"idioma": self.idioma, "id_idioma": self.id_idioma}

    @classmethod
    def from_dict(cls, data):
        return cls(idioma=data.get("idioma"), id_idioma=data.get("id_idioma"))


class Usuario:
    def __init__(self, nombre, correo, password):
        self.nombre = nombre
        self.correo = correo
        self.password = password

    def to_dict(self):
        return {"nombre": self.nombre, "correo": self.correo, "password": self.password}

    @classmethod
    def from_dict(cls, data):
        return cls(nombre=data.get("nombre"), correo=data.get("correo"), password=data.get("password"))


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
            "autores": [a.to_dict() if hasattr(a, 'to_dict') else a for a in self.autores],
            "editorial": self.editorial.to_dict() if hasattr(self.editorial, 'to_dict') else self.editorial,
            "formato": self.formato.to_dict() if hasattr(self.formato, 'to_dict') else self.formato,
            "idioma": self.idioma.to_dict() if hasattr(self.idioma, 'to_dict') else self.idioma
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            titulo=data.get("titulo"),
            edicion=data.get("edicion"),
            isbn=data.get("isbn"),
            autores=data.get("autores", []),
            editorial=data.get("editorial"),
            formato=data.get("formato"),
            idioma=data.get("idioma")
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
        if self.ARCHIVO_DATOS.exists():
            try:
                with open(self.ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
                    contenido = json.load(archivo)
                    self.usuarios = [Usuario.from_dict(u) for u in contenido.get("usuarios", [])]
                    self.autores = [Autor.from_dict(a) for a in contenido.get("autores", [])]
                    self.isbns = contenido.get("isbns", [])
                    self.titulos = [Libro.from_dict(t) for t in contenido.get("titulos", [])]
                    self.editoriales = [Editorial.from_dict(e) for e in contenido.get("editoriales", [])]
                    self.formatos = [Formato.from_dict(f) for f in contenido.get("formatos", [])]
                    self.idiomas = [Idioma.from_dict(i) for i in contenido.get("idiomas", [])]
            except json.JSONDecodeError:
                print("El archivo JSON está vacío o dañado. Se iniciará con colecciones vacías.")

    def guardar_datos(self):
        contenido = {
            "usuarios": [u.to_dict() for u in self.usuarios],
            "autores": [a.to_dict() for a in self.autores],
            "isbns": self.isbns,
            "titulos": [t.to_dict() for t in self.titulos],
            "editoriales": [e.to_dict() for e in self.editoriales],
            "formatos": [f.to_dict() for f in self.formatos],
            "idiomas": [i.to_dict() for i in self.idiomas]
        }
        with open(self.ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(contenido, archivo, indent=4, ensure_ascii=False)

    def importar_libros_csv(self):
        nombre_archivo = input("Ingrese el nombre del archivo CSV de libros (ej. libros.csv): ").strip()
        archivo_csv = self.RUTA_PROYECTO / nombre_archivo
        
        registros = CargadorCSV.leer_csv(archivo_csv)
        if not registros:
            return

        importados = 0
        for fila in registros:
            titulo = fila.get("titulo")
            edicion = fila.get("edicion")
            isbn = fila.get("isbn")
            autor_nombre = fila.get("autor")
            editorial_nombre = fila.get("editorial")
            formato_tipo = fila.get("formato")
            idioma_nombre = fila.get("idioma")

            if not titulo or not isbn:
                continue

            if not Utilerias.validador_isbn13(isbn):
                print(f"ISBN inválido para el libro '{titulo}': {isbn}. Omitido.")
                continue

            autor_obj = None
            if autor_nombre:
                for a in self.autores:
                    if a.nombre.lower() == autor_nombre.lower():
                        autor_obj = a
                        break
                if not autor_obj:
                    autor_obj = Autor(nombre=autor_nombre)
                    self.autores.append(autor_obj)

            editorial_obj = None
            if editorial_nombre:
                for e in self.editoriales:
                    if e.nombre.lower() == editorial_nombre.lower():
                        editorial_obj = e
                        break
                if not editorial_obj:
                    editorial_obj = Editorial(nombre=editorial_nombre)
                    self.editoriales.append(editorial_obj)

            formato_obj = None
            if formato_tipo:
                for f in self.formatos:
                    if f.tipo_formato.lower() == formato_tipo.lower():
                        formato_obj = f
                        break
                if not formato_obj:
                    formato_obj = Formato(tipo_formato=formato_tipo)
                    self.formatos.append(formato_obj)

            idioma_obj = None
            if idioma_nombre:
                for i in self.idiomas:
                    if i.idioma.lower() == idioma_nombre.lower():
                        idioma_obj = i
                        break
                if not idioma_obj:
                    idioma_obj = Idioma(idioma=idioma_nombre)
                    self.idiomas.append(idioma_obj)

            lista_autores_dict = [autor_obj.to_dict()] if autor_obj else []
            editorial_dict = editorial_obj.to_dict() if editorial_obj else {}
            formato_dict = formato_obj.to_dict() if formato_obj else {}
            idioma_dict = idioma_obj.to_dict() if idioma_obj else {}

            nuevo_libro = Libro(titulo, edicion, isbn, lista_autores_dict, editorial_dict, formato_dict, idioma_dict)
            self.titulos.append(nuevo_libro)

            if isbn not in self.isbns:
                self.isbns.append(isbn)

            importados += 1

        self.guardar_datos()
        print(f"¡Se importaron {importados} libros nuevos exitosamente!")

    def editar_elemento(self, lista, clave_id, campos_editables):
        if not lista:
            print("No hay elementos registrados para editar.")
            return False
            
        id_buscado = input("Ingrese el ID del elemento que desea editar: ")
        for elemento in lista:
            if getattr(elemento, clave_id) == id_buscado:
                print(f"\nElemento encontrado: {elemento.to_dict()}")
                print("Deje el espacio en blanco y presione Enter si no desea cambiar un campo.")
                
                for campo in campos_editables:
                    valor_actual = getattr(elemento, campo)
                    nuevo_valor = input(f"Nuevo valor para '{campo}' [{valor_actual}]: ")
                    if nuevo_valor.strip() != "":
                        setattr(elemento, campo, nuevo_valor)
                        
                self.guardar_datos()
                print("¡Actualización completada con éxito!")
                return True
                
        print("No se encontró ningún elemento con ese identificador.")
        return False

    def buscar_elemento_generico(self, lista, clave_id):
        if not lista:
            print("No hay elementos registrados.")
            return None
            
        id_buscado = input("Ingrese el ID del elemento que desea buscar: ")
        for elemento in lista:
            if getattr(elemento, clave_id) == id_buscado:
                print(f"\nElemento encontrado: {elemento.to_dict()}")
                return elemento
                
        print("No se encontró ningún elemento con ese ID.")
        return None

    def consultar_elementos(self, lista, campos_busqueda):
        if not lista:
            print("No hay registros disponibles para consultar.")
            return
            
        criterio = input("Ingrese el texto o palabra clave a consultar: ").strip().lower()
        if not criterio:
            print("Consulta vacía.")
            return
            
        encontrados = []
        for item in lista:
            coincide = False
            item_dict = item.to_dict() if hasattr(item, 'to_dict') else item
            for campo in campos_busqueda:
                valor = str(item_dict.get(campo, "")).lower()
                if criterio in valor:
                    coincide = True
                    break
            if coincide:
                encontrados.append(item)
                
        if encontrados:
            print(f"\n--- Resultados de la consulta ({len(encontrados)}) ---")
            for idx, item in enumerate(encontrados, start=1):
                item_dict = item.to_dict() if hasattr(item, 'to_dict') else item
                if "titulo" in item_dict:
                    print(f"\nResultado #{idx}")
                    print(f"  • Título: {item_dict.get('titulo')}")
                    print(f"  • Edición: {item_dict.get('edicion')}")
                    print(f"  • ISBN: {item_dict.get('isbn')}")
                else:
                    print(f"{idx}. {item_dict}")
        else:
            print("No se encontraron elementos que coincidan con la consulta.")

    def eliminar_elemento(self, lista, clave_id):
        if not lista:
            print("No hay elementos para eliminar.")
            return False
            
        id_buscado = input("Ingrese el ID del elemento que desea eliminar: ")
        for indice, elemento in enumerate(lista):
            if getattr(elemento, clave_id) == id_buscado:
                print(f"Elemento a eliminar: {elemento.to_dict()}")
                confirmacion = input("¿Está seguro de eliminarlo? (s/n): ").lower()
                if confirmacion == 's':
                    lista.pop(indice)
                    self.guardar_datos()
                    print("¡Elemento eliminado con éxito!")
                    return True
                else:
                    print("Operación cancelada.")
                    return False
                    
        print("No se encontró ningún elemento con ese ID.")
        return False


class BibliotecaApp:
    def __init__(self):
        self.gestor = GestorBiblioteca()

    def registrar_usuario(self):
        nombre = input("Nombre del usuario: ")
        while True:
            correo = input("Ingrese correo: ")
            if Utilerias.validar_correo(correo):
                print("Correo válido.")
                break
            else:
                print("Correo inválido. Inténtalo de nuevo.")

        password = input("Ingrese contraseña: ")
        nuevo_usuario = Usuario(nombre, correo, password)
        self.gestor.usuarios.append(nuevo_usuario)
        self.gestor.guardar_datos()
        return nuevo_usuario

    def registrar_autor(self):
        nombre = input("Ingrese nombre del autor: ")
        nuevo_autor = Autor(nombre)
        self.gestor.autores.append(nuevo_autor)
        self.gestor.guardar_datos()
        print(f"Registro completado! Autor: {nombre} | ID Autor: {nuevo_autor.id_autor}")
        return nuevo_autor

    def registrar_editorial(self):
        nombre = input("Ingrese nombre de la editorial: ")
        nueva_editorial = Editorial(nombre)
        self.gestor.editoriales.append(nueva_editorial)
        self.gestor.guardar_datos()
        print("Registro completado!")
        print(f"Editorial: {nombre} | id_editorial: {nueva_editorial.id_editorial}")
        return nueva_editorial

    def ingresar_isbn(self):
        while True:
            isbn = input("Introduce el código ISBN-13: ")
            if Utilerias.validador_isbn13(isbn):
                print(f"ISBN {isbn}, registrado con éxito")
                if isbn not in self.gestor.isbns:
                    self.gestor.isbns.append(isbn)
                    self.gestor.guardar_datos()
                return isbn  
            else:
                print("El ISBN no es válido. Inténtalo de nuevo.")

    def registrar_formato(self):
        tipo_formato = input("Tipo de formato del libro: ")
        nuevo_formato = Formato(tipo_formato)
        self.gestor.formatos.append(nuevo_formato)
        self.gestor.guardar_datos()
        print(f"Formato: {tipo_formato}, {nuevo_formato.id_formato}, registrado correctamente")
        return nuevo_formato

    def registrar_idioma(self):
        language = input("Ingrese idioma del libro: ")
        nuevo_idioma = Idioma(language)
        self.gestor.idiomas.append(nuevo_idioma)
        self.gestor.guardar_datos()
        print(f"Idioma: {language}, registrado correctamente")
        return nuevo_idioma

    def buscar_autor(self):
        nombre_buscado = input("Ingrese el nombre del autor a buscar: ")
        for autor in self.gestor.autores:
            if autor.nombre.lower() == nombre_buscado.lower():
                return autor
                
        while True:
            respuesta = input("Autor no encontrado, desea ingresar uno nuevo (s/n): ").lower()
            if respuesta == "s":
                return self.registrar_autor()
            elif respuesta == "n":
                return None
            else:
                print("Respuesta incorrecta, seleccione (s/n): ")

    def buscar_editorial(self):
        nombre_buscado = input("Ingrese el nombre de la editorial a buscar: ")
        for editorial in self.gestor.editoriales:
            if editorial.nombre.lower() == nombre_buscado.lower():
                return editorial
                
        while True:
            respuesta = input("Editorial no encontrada, desea ingresar editorial nueva (s/n): ").lower()
            if respuesta == "s":
                return self.registrar_editorial()
            elif respuesta == "n":
                return None
            else:
                print("Respuesta incorrecta, seleccione (s/n): ")

    def buscar_formato(self):
        tipo_buscado = input("Ingrese el formato a buscar: ")
        for formato in self.gestor.formatos:
            if formato.tipo_formato.lower() == tipo_buscado.lower():
                return formato
                
        while True:
            respuesta = input("Formato no encontrado, desea ingresar formato nuevo (s/n): ").lower()
            if respuesta == "s":
                return self.registrar_formato()
            elif respuesta == "n":
                return None
            else:
                print("Respuesta incorrecta, seleccione (s/n): ")

    def buscar_idioma(self):
        idioma_buscado = input("Ingrese el idioma a buscar: ")
        for idioma in self.gestor.idiomas:
            if idioma.idioma.lower() == idioma_buscado.lower():
                return idioma
                
        while True:
            respuesta = input("Idioma no encontrado, desea ingresar idioma nuevo (s/n): ").lower()
            if respuesta == "s":
                return self.registrar_idioma()
            elif respuesta == "n":
                return None
            else:
                print("Respuesta incorrecta, seleccione (s/n): ")

    def ingresar_titulo(self):
        nombre = input("Ingrese título del libro: ")
        edicion = input("Ingrese edición del libro: ")
        isbn = self.ingresar_isbn()
        
        autor = self.buscar_autor()
        editorial = self.buscar_editorial()
        formato = self.buscar_formato()
        idioma = self.buscar_idioma()

        lista_de_autores_libro = [autor.to_dict() if hasattr(autor, 'to_dict') else autor] if autor else []
        while True:
            respuesta = input("¿Hay más de un autor para este libro? (s/n): ").lower()
            if respuesta == "s":
                extra_autor = self.buscar_autor()
                if extra_autor:
                    lista_de_autores_libro.append(extra_autor.to_dict() if hasattr(extra_autor, 'to_dict') else extra_autor)
            elif respuesta == "n":
                break
            else:
                print("Seleccione respuesta correcta (s/n)")

        editorial_dict = editorial.to_dict() if hasattr(editorial, 'to_dict') else editorial
        formato_dict = formato.to_dict() if hasattr(formato, 'to_dict') else formato
        idioma_dict = idioma.to_dict() if hasattr(idioma, 'to_dict') else idioma

        libro_completo = Libro(nombre, edicion, isbn, lista_de_autores_libro, editorial_dict, formato_dict, idioma_dict)
        
        self.gestor.titulos.append(libro_completo)
        self.gestor.guardar_datos()
        print("¡Libro registrado con éxito!")
        return libro_completo

    def iniciar_sesion(self):
        print("\n--- Iniciar Sesión ---")
        correo = input("Ingrese su correo: ")
        password = input("Ingrese su contraseña: ")
        
        for usuario in self.gestor.usuarios:
            if usuario.correo == correo and usuario.password == password:
                print(f"¡Bienvenido de nuevo, {usuario.nombre}!")
                return usuario 
                
        print("Correo o contraseña incorrectos.")
        return None

    def mostrar_autores(self):
        print("\n--- Lista de Autores registrados ---")
        if not self.gestor.autores:
            print("No hay autores registrados.")
            return
            
        for indice, autor in enumerate(self.gestor.autores, start=1):
            print(f"{indice}. Nombre: {autor.nombre} | ID: {autor.id_autor}")

    def mostrar_libros(self):
        print("\n--- Catálogo de Libros ---")
        if not self.gestor.titulos:
            print("No hay libros registrados.")
            return
        for indice, libro in enumerate(self.gestor.titulos, start=1):
            print(f"\nLibro #{indice}")
            print(f"  • Título: {libro.titulo}")
            print(f"  • Edición: {libro.edicion}")
            print(f"  • ISBN: {libro.isbn}")
            autores_lista = libro.autores if isinstance(libro.autores, list) else []
            autor_nombres = ", ".join([a.get('nombre', '') if isinstance(a, dict) else getattr(a, 'nombre', '') for a in autores_lista]) or "Sin autor"
            print(f"  • Autores: {autor_nombres}")
            
            ed = libro.editorial
            ed_nombre = ed.get('nombre', 'N/A') if isinstance(ed, dict) else getattr(ed, 'nombre', 'N/A')
            print(f"  • Editorial: {ed_nombre}")
            
            fmt = libro.formato
            fmt_tipo = fmt.get('tipo_formato', 'N/A') if isinstance(fmt, dict) else getattr(fmt, 'tipo_formato', 'N/A')
            print(f"  • Formato: {fmt_tipo}")
            
            idioma = libro.idioma
            idioma_nombre = idioma.get('idioma', 'N/A') if isinstance(idioma, dict) else getattr(idioma, 'idioma', 'N/A')
            print(f"  • Idioma: {idioma_nombre}")

    def mostrar_isbns(self):
        print("\n--- Lista de ISBNs registrados ---")
        if not self.gestor.isbns:
            print("No hay ISBNs registrados.")
            return
        for indice, isbn in enumerate(self.gestor.isbns, start=1):
            print(f"{indice}. {isbn}")

    def mostrar_editoriales(self):
        print("\n--- Lista de Editoriales ---")
        if not self.gestor.editoriales:
            print("No hay editoriales registradas.")
            return
        for indice, ed in enumerate(self.gestor.editoriales, start=1):
            print(f"{indice}. Nombre: {ed.nombre} | ID: {ed.id_editorial}")

    def mostrar_formatos(self):
        print("\n--- Lista de Formatos ---")
        if not self.gestor.formatos:
            print("No hay formatos registrados.")
            return
        for indice, f in enumerate(self.gestor.formatos, start=1):
            print(f"{indice}. Formato: {f.tipo_formato} | ID: {f.id_formato}")

    def mostrar_idiomas(self):
        print("\n--- Lista de Idiomas ---")
        if not self.gestor.idiomas:
            print("No hay idiomas registrados.")
            return
        for indice, i in enumerate(self.gestor.idiomas, start=1):
            print(f"{indice}. Idioma: {i.idioma} | ID: {i.id_idioma}")

    def menu_autores(self):
        while True:
            print("\n--- Menú de Autores ---")
            print("1. Registrar nuevo autor")
            print("2. Mostrar lista de autores")
            print("3. Buscar autor por ID")
            print("4. Consultar autor por texto")
            print("5. Editar autor")
            print("6. Eliminar autor")
            print("7. Volver al menú principal")

            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                self.registrar_autor()
            elif opcion == "2":
                self.mostrar_autores()
            elif opcion == "3":
                self.gestor.buscar_elemento_generico(self.gestor.autores, "id_autor")
            elif opcion == "4":
                self.gestor.consultar_elementos(self.gestor.autores, ["nombre"])
            elif opcion == "5":
                self.gestor.editar_elemento(self.gestor.autores, "id_autor", ["nombre"])
            elif opcion == "6":
                self.gestor.eliminar_elemento(self.gestor.autores, "id_autor")
            elif opcion == "7":
                break
            else:
                print("Elija una opción válida por favor.")

    def menu_libros(self):
        while True:
            print("\n--- Menú de Libros ---")
            print("1. Registrar nuevo libro")
            print("2. Mostrar catálogo de libros")
            print("3. Consultar libro por título o ISBN")
            print("4. Importar libros desde archivo CSV")
            print("5. Volver al menú principal")

            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                self.ingresar_titulo()
            elif opcion == "2":
                self.mostrar_libros()
            elif opcion == "3":
                self.gestor.consultar_elementos(self.gestor.titulos, ["titulo", "isbn"])
            elif opcion == "4":
                self.gestor.importar_libros_csv()
            elif opcion == "5":
                break
            else:
                print("Elija una opción válida por favor.")

    def menu_isbns(self):
        while True:
            print("\n--- Menú de ISBNs ---")
            print("1. Registrar y validar nuevo ISBN")
            print("2. Mostrar lista de ISBNs")
            print("3. Consultar ISBN")
            print("4. Volver al menú principal")

            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                self.ingresar_isbn()
            elif opcion == "2":
                self.mostrar_isbns()
            elif opcion == "3":
                criterio = input("Ingrese parte del ISBN a buscar: ").strip()
                resultados = [i for i in self.gestor.isbns if criterio in i]
                print(f"Resultados encontrados: {resultados}")
            elif opcion == "4":
                break
            else:
                print("Elija una opción válida por favor.")

    def menu_editoriales(self):
        while True:
            print("\n--- Menú de Editoriales ---")
            print("1. Registrar nueva editorial")
            print("2. Mostrar lista de editoriales")
            print("3. Buscar editorial por ID")
            print("4. Consultar editorial por texto")
            print("5. Editar editorial")
            print("6. Eliminar editorial")
            print("7. Volver al menú principal")

            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                self.registrar_editorial()
            elif opcion == "2":
                self.mostrar_editoriales()
            elif opcion == "3":
                self.gestor.buscar_elemento_generico(self.gestor.editoriales, "id_editorial")
            elif opcion == "4":
                self.gestor.consultar_elementos(self.gestor.editoriales, ["nombre"])
            elif opcion == "5":
                self.gestor.editar_elemento(self.gestor.editoriales, "id_editorial", ["nombre"])
            elif opcion == "6":
                self.gestor.eliminar_elemento(self.gestor.editoriales, "id_editorial")
            elif opcion == "7":
                break
            else:
                print("Elija una opción válida por favor.")

    def menu_formatos(self):
        while True:
            print("\n--- Menú de Formatos ---")
            print("1. Registrar nuevo formato")
            print("2. Mostrar lista de formatos")
            print("3. Buscar formato por ID")
            print("4. Consultar formato por texto")
            print("5. Editar formato")
            print("6. Eliminar formato")
            print("7. Volver al menú principal")

            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                self.registrar_formato()
            elif opcion == "2":
                self.mostrar_formatos()
            elif opcion == "3":
                self.gestor.buscar_elemento_generico(self.gestor.formatos, "id_formato")
            elif opcion == "4":
                self.gestor.consultar_elementos(self.gestor.formatos, ["tipo_formato"])
            elif opcion == "5":
                self.gestor.editar_elemento(self.gestor.formatos, "id_formato", ["tipo_formato"])
            elif opcion == "6":
                self.gestor.eliminar_elemento(self.gestor.formatos, "id_formato")
            elif opcion == "7":
                break
            else:
                print("Elija una opción válida por favor.")

    def menu_idiomas(self):
        while True:
            print("\n--- Menú de Idiomas ---")
            print("1. Registrar nuevo idioma")
            print("2. Mostrar lista de idiomas")
            print("3. Buscar idioma por ID")
            print("4. Consultar idioma por texto")
            print("5. Editar idioma")
            print("6. Eliminar idioma")
            print("7. Volver al menú principal")

            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                self.registrar_idioma()
            elif opcion == "2":
                self.mostrar_idiomas()
            elif opcion == "3":
                self.gestor.buscar_elemento_generico(self.gestor.idiomas, "id_idioma")
            elif opcion == "4":
                self.gestor.consultar_elementos(self.gestor.idiomas, ["idioma"])
            elif opcion == "5":
                self.gestor.editar_elemento(self.gestor.idiomas, "id_idioma", ["idioma"])
            elif opcion == "6":
                self.gestor.eliminar_elemento(self.gestor.idiomas, "id_idioma")
            elif opcion == "7":
                break
            else:
                print("Elija una opción válida por favor.")

    def menu_principal(self, usuario):
        nombre = usuario.nombre if isinstance(usuario, Usuario) else usuario
        
        while True:
            print(f"\n--- Menú Principal ---")
            print(f"Bienvenido, {nombre}")
            print("1. Menú de Libros")
            print("2. Menú de Autores")
            print("3. Menú de Editoriales")
            print("4. Menú de Formatos")
            print("5. Menú de Idiomas")
            print("6. Menú de ISBNs")
            print("7. Cerrar sesión")

            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.menu_libros()
            elif opcion == "2":
                self.menu_autores()
            elif opcion == "3":
                self.menu_editoriales()
            elif opcion == "4":
                self.menu_formatos()
            elif opcion == "5":
                self.menu_idiomas()
            elif opcion == "6":
                self.menu_isbns()
            elif opcion == "7":
                print("Cerrando sesión...")
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")

    def iniciar(self):
        while True:
            print("\nBienvenido al control de libros")
            print("1. Iniciar sesion")
            print("2. Crear nuevo usuario")
            print("3. Salir")

            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                usuario_logueado = self.iniciar_sesion()
                if usuario_logueado:
                    self.menu_principal(usuario_logueado)
            elif opcion == "2":
                self.registrar_usuario()
                print("Usuario creado con éxito. Ahora puedes iniciar sesión.")
            elif opcion == "3":
                print("Saliendo del programa. ¡Hasta luego!")
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")


if __name__ == "__main__":
    app = BibliotecaApp()
    app.iniciar()