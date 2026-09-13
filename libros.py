import json
import uuid
import re
import os

ARCHIVO_DATOS = "libros.json"

usuarios = []
autores = []
isbns = []
titulos = []
editoriales = []
formatos = []
idiomas = []

def cargar_datos():
    global usuarios, autores, isbns, titulos, editoriales, formatos, idiomas
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
                usuarios = contenido.get("usuarios", [])
                autores = contenido.get("autores", [])
                isbns = contenido.get("isbns", [])
                titulos = contenido.get("titulos", [])
                editoriales = contenido.get("editoriales", [])
                formatos = contenido.get("formatos", [])
                idiomas = contenido.get("idiomas", [])
        except json.JSONDecodeError:
            print("El archivo JSON está vacío o dañado. Se iniciará con listas vacías.")

def guardar_datos():
    contenido = {
        "usuarios": usuarios,
        "autores": autores,
        "isbns": isbns,
        "titulos": titulos,
        "editoriales": editoriales,
        "formatos": formatos,
        "idiomas": idiomas
    }
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(contenido, archivo, indent=4, ensure_ascii=False)

def validar_correo(correo):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(patron, correo):
        return True
    return False

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

def generar_codigo():
    return str(uuid.uuid4())[:8]

def usuario_nuevo():
    nombre = input("Nombre del usuario: ")
    while True:
        correo = input("Ingrese correo: ")
        if validar_correo(correo):
            print("Correo válido.")
            break
        else:
            print("Correo inválido. Inténtalo de nuevo.")

    password = input("Ingrese contraseña: ")
    
    nuevo_usuario = {
        "nombre": nombre,
        "correo": correo,
        "password": password
    }
    usuarios.append(nuevo_usuario)
    guardar_datos()
    return nuevo_usuario

def autor_nuevo():
    nombre = input("Ingrese nombre del autor: ")
    id_autor = generar_codigo() 
    nuevo_autor = {"nombre": nombre, "id_autor": id_autor}
    autores.append(nuevo_autor)
    guardar_datos()
    print(f"Registro completado! Autor: {nombre} | ID Autor: {id_autor}")
    return nuevo_autor

def editorial_nueva():
    nombre = input("Ingrese nombre de la editorial: ")
    id_editorial = generar_codigo()
    nueva_editorial = {"nombre": nombre, "id_editorial": id_editorial}
    editoriales.append(nueva_editorial)
    guardar_datos()
    print("Registro completado!")
    print(f"Editorial: {nombre} | id_editorial: {id_editorial}")
    return nueva_editorial

def ingresar_isbn():
    while True:
        isbn = input("Introduce el código ISBN-13: ")
        if validador_isbn13(isbn):
            print(f"ISBN {isbn}, registrado con éxito")
            if isbn not in isbns:
                isbns.append(isbn)
                guardar_datos()
            return isbn  
        else:
            print("El ISBN no es válido. Inténtalo de nuevo.")

def formato_nuevo():
    tipo_formato = input("Tipo de formato del libro: ")
    id_formato = generar_codigo()
    nuevo_formato = {"tipo_formato": tipo_formato, "id_formato": id_formato}
    formatos.append(nuevo_formato)
    guardar_datos()
    print(f"Formato: {tipo_formato}, {id_formato}, registrado correctamente")
    return nuevo_formato

def idioma_nuevo():
    language = input("Ingrese idioma del libro: ")
    id_idioma = generar_codigo()
    nuevo_idioma = {"idioma": language, "id_idioma": id_idioma}
    idiomas.append(nuevo_idioma)
    guardar_datos()
    print(f"Idioma: {language}, registrado correctamente")
    return nuevo_idioma

# --- FUNCIONES GENÉRICAS (CRUD & CONSULTA) ---
def editar_elemento(lista, clave_id, campos_editables):
    if not lista:
        print("No hay elementos registrados para editar.")
        return False
        
    id_buscado = input("Ingrese el ID del elemento que desea editar: ")
    for elemento in lista:
        if elemento.get(clave_id) == id_buscado:
            print(f"\nElemento encontrado: {elemento}")
            print("Deje el espacio en blanco y presione Enter si no desea cambiar un campo.")
            
            for campo in campos_editables:
                valor_actual = elemento[campo]
                nuevo_valor = input(f"Nuevo valor para '{campo}' [{valor_actual}]: ")
                if nuevo_valor.strip() != "":
                    elemento[campo] = nuevo_valor
                    
            guardar_datos()
            print("¡Actualización completada con éxito!")
            return True
            
    print("No se encontró ningún elemento con ese identificador.")
    return False

def buscar_elemento_generico(lista, clave_id):
    if not lista:
        print("No hay elementos registrados.")
        return None
        
    id_buscado = input("Ingrese el ID del elemento que desea buscar: ")
    for elemento in lista:
        if elemento.get(clave_id) == id_buscado:
            print(f"\nElemento encontrado: {elemento}")
            return elemento
            
    print("No se encontró ningún elemento con ese ID.")
    return None

def consultar_elementos(lista, campos_busqueda):
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
        for campo in campos_busqueda:
            valor = str(item.get(campo, "")).lower()
            if criterio in valor:
                coincide = True
                break
        if coincide:
            encontrados.append(item)
            
    if encontrados:
        print(f"\n--- Resultados de la consulta ({len(encontrados)}) ---")
        for idx, item in enumerate(encontrados, start=1):
            if "titulo" in item:
                print(f"\nResultado #{idx}")
                print(f"  • Título: {item.get('titulo')}")
                print(f"  • Edición: {item.get('edicion')}")
                print(f"  • ISBN: {item.get('isbn')}")
            else:
                print(f"{idx}. {item}")
    else:
        print("No se encontraron elementos que coincidan con la consulta.")

def eliminar_elemento(lista, clave_id):
    if not lista:
        print("No hay elementos para eliminar.")
        return False
        
    id_buscado = input("Ingrese el ID del elemento que desea eliminar: ")
    for indice, elemento in enumerate(lista):
        if elemento.get(clave_id) == id_buscado:
            print(f"Elemento a eliminar: {elemento}")
            confirmacion = input("¿Está seguro de eliminarlo? (s/n): ").lower()
            if confirmacion == 's':
                lista.pop(indice)
                guardar_datos()
                print("¡Elemento eliminado con éxito!")
                return True
            else:
                print("Operación cancelada.")
                return False
                
    print("No se encontró ningún elemento con ese ID.")
    return False

def buscar_autor(lista_autores):
    nombre_buscado = input("Ingrese el nombre del autor a buscar: ")
    for autor in lista_autores:
        if autor["nombre"].lower() == nombre_buscado.lower():
            return autor
            
    while True:
        respuesta = input("Autor no encontrado, desea ingresar uno nuevo (s/n): ").lower()
        if respuesta == "s":
            return autor_nuevo()
        elif respuesta == "n":
            return None
        else:
            print("Respuesta incorrecta, seleccione (s/n): ")

def buscar_editorial(lista_editoriales):
    nombre_buscado = input("Ingrese el nombre de la editorial a buscar: ")
    for editorial in lista_editoriales:
        if editorial["nombre"].lower() == nombre_buscado.lower():
            return editorial
            
    while True:
        respuesta = input("Editorial no encontrada, desea ingresar editorial nueva (s/n): ").lower()
        if respuesta == "s":
            return editorial_nueva()
        elif respuesta == "n":
            return None
        else:
            print("Respuesta incorrecta, seleccione (s/n): ")

def buscar_formato(lista_formatos):
    tipo_buscado = input("Ingrese el formato a buscar: ")
    for formato in lista_formatos:
        if formato["tipo_formato"].lower() == tipo_buscado.lower():
            return formato
            
    while True:
        respuesta = input("Formato no encontrado, desea ingresar formato nuevo (s/n): ").lower()
        if respuesta == "s":
            return formato_nuevo()
        elif respuesta == "n":
            return None
        else:
            print("Respuesta incorrecta, seleccione (s/n): ")

def buscar_idioma(lista_idiomas):
    idioma_buscado = input("Ingrese el idioma a buscar: ")
    for idioma in lista_idiomas:
        if idioma["idioma"].lower() == idioma_buscado.lower():
            return idioma
            
    while True:
        respuesta = input("Idioma no encontrado, desea ingresar idioma nuevo (s/n): ").lower()
        if respuesta == "s":
            return idioma_nuevo()
        elif respuesta == "n":
            return None
        else:
            print("Respuesta incorrecta, seleccione (s/n): ")

def ingresar_titulo():
    nombre = input("Ingrese título del libro: ")
    edicion = input("Ingrese edición del libro: ")
    isbn = ingresar_isbn()
    
    autor = buscar_autor(autores)
    editorial = buscar_editorial(editoriales)
    formato = buscar_formato(formatos)
    idioma = buscar_idioma(idiomas)

    lista_de_autores_libro = [autor] if autor else []
    while True:
        respuesta = input("¿Hay más de un autor para este libro? (s/n): ").lower()
        if respuesta == "s":
            extra_autor = buscar_autor(autores)
            if extra_autor:
                lista_de_autores_libro.append(extra_autor)
        elif respuesta == "n":
            break
        else:
            print("Seleccione respuesta correcta (s/n)")

    libro_completo = {
        "titulo": nombre,
        "edicion": edicion,
        "isbn": isbn,
        "autores": lista_de_autores_libro,
        "editorial": editorial,
        "formato": formato,
        "idioma": idioma
    }
    
    titulos.append(libro_completo)
    guardar_datos()
    print("¡Libro registrado con éxito!")
    return libro_completo

def iniciar_sesion(lista_usuarios):
    print("\n--- Iniciar Sesión ---")
    correo = input("Ingrese su correo: ")
    password = input("Ingrese su contraseña: ")
    
    for usuario in lista_usuarios:
        if usuario["correo"] == correo and usuario["password"] == password:
            print(f"¡Bienvenido de nuevo, {usuario['nombre']}!")
            return usuario 
            
    print("Correo o contraseña incorrectos.")
    return None

def mostrar_autores(lista_autores):
    print("\n--- Lista de Autores registrados ---")
    if not lista_autores:
        print("No hay autores registrados.")
        return
        
    for indice, autor in enumerate(lista_autores, start=1):
        print(f"{indice}. Nombre: {autor['nombre']} | ID: {autor['id_autor']}")

def mostrar_libros(lista_titulos):
    print("\n--- Catálogo de Libros ---")
    if not lista_titulos:
        print("No hay libros registrados.")
        return
    for indice, libro in enumerate(lista_titulos, start=1):
        print(f"\nLibro #{indice}")
        print(f"  • Título: {libro['titulo']}")
        print(f"  • Edición: {libro['edicion']}")
        print(f"  • ISBN: {libro['isbn']}")
        autor_nombres = ", ".join([a['nombre'] for a in libro['autores']]) if libro['autores'] else "Sin autor"
        print(f"  • Autores: {autor_nombres}")
        print(f"  • Editorial: {libro['editorial']['nombre'] if libro['editorial'] else 'N/A'}")
        print(f"  • Formato: {libro['formato']['tipo_formato'] if libro['formato'] else 'N/A'}")
        print(f"  • Idioma: {libro['idioma']['idioma'] if libro['idioma'] else 'N/A'}")

def mostrar_isbns(lista_isbns):
    print("\n--- Lista de ISBNs registrados ---")
    if not lista_isbns:
        print("No hay ISBNs registrados.")
        return
    for indice, isbn in enumerate(lista_isbns, start=1):
        print(f"{indice}. {isbn}")

def mostrar_editoriales(lista_editoriales):
    print("\n--- Lista de Editoriales ---")
    if not lista_editoriales:
        print("No hay editoriales registradas.")
        return
    for indice, ed in enumerate(lista_editoriales, start=1):
        print(f"{indice}. Nombre: {ed['nombre']} | ID: {ed['id_editorial']}")

def mostrar_formatos(lista_formatos):
    print("\n--- Lista de Formatos ---")
    if not lista_formatos:
        print("No hay formatos registrados.")
        return
    for indice, f in enumerate(lista_formatos, start=1):
        print(f"{indice}. Formato: {f['tipo_formato']} | ID: {f['id_formato']}")

def mostrar_idiomas(lista_idiomas):
    print("\n--- Lista de Idiomas ---")
    if not lista_idiomas:
        print("No hay idiomas registrados.")
        return
    for indice, i in enumerate(lista_idiomas, start=1):
        print(f"{indice}. Idioma: {i['idioma']} | ID: {i['id_idioma']}")

def menu_autores(usuario):
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
            autor_nuevo()
        elif opcion == "2":
            mostrar_autores(autores)
        elif opcion == "3":
            buscar_elemento_generico(autores, "id_autor")
        elif opcion == "4":
            consultar_elementos(autores, ["nombre"])
        elif opcion == "5":
            editar_elemento(autores, "id_autor", ["nombre"])
        elif opcion == "6":
            eliminar_elemento(autores, "id_autor")
        elif opcion == "7":
            break
        else:
            print("Elija una opción válida por favor.")

def menu_libros(usuario):
    while True:
        print("\n--- Menú de Libros ---")
        print("1. Registrar nuevo libro")
        print("2. Mostrar catálogo de libros")
        print("3. Consultar libro por título o ISBN")
        print("4. Volver al menú principal")

        opcion = input("Ingrese una opción: ")
        if opcion == "1":
            ingresar_titulo()
        elif opcion == "2":
            mostrar_libros(titulos)
        elif opcion == "3":
            consultar_elementos(titulos, ["titulo", "isbn"])
        elif opcion == "4":
            break
        else:
            print("Elija una opción válida por favor.")

def menu_isbns(usuario):
    while True:
        print("\n--- Menú de ISBNs ---")
        print("1. Registrar y validar nuevo ISBN")
        print("2. Mostrar lista de ISBNs")
        print("3. Consultar ISBN")
        print("4. Volver al menú principal")

        opcion = input("Ingrese una opción: ")
        if opcion == "1":
            ingresar_isbn()
        elif opcion == "2":
            mostrar_isbns(isbns)
        elif opcion == "3":
            # Para la lista simple de isbns (que son strings), adaptamos una consulta directa
            criterio = input("Ingrese parte del ISBN a buscar: ").strip()
            resultados = [i for i in isbns if criterio in i]
            print(f"Resultados encontrados: {resultados}")
        elif opcion == "4":
            break
        else:
            print("Elija una opción válida por favor.")

def menu_editoriales(usuario):
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
            editorial_nueva()
        elif opcion == "2":
            mostrar_editoriales(editoriales)
        elif opcion == "3":
            buscar_elemento_generico(editoriales, "id_editorial")
        elif opcion == "4":
            consultar_elementos(editoriales, ["nombre"])
        elif opcion == "5":
            editar_elemento(editoriales, "id_editorial", ["nombre"])
        elif opcion == "6":
            eliminar_elemento(editoriales, "id_editorial")
        elif opcion == "7":
            break
        else:
            print("Elija una opción válida por favor.")

def menu_formatos(usuario):
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
            formato_nuevo()
        elif opcion == "2":
            mostrar_formatos(formatos)
        elif opcion == "3":
            buscar_elemento_generico(formatos, "id_formato")
        elif opcion == "4":
            consultar_elementos(formatos, ["tipo_formato"])
        elif opcion == "5":
            editar_elemento(formatos, "id_formato", ["tipo_formato"])
        elif opcion == "6":
            eliminar_elemento(formatos, "id_formato")
        elif opcion == "7":
            break
        else:
            print("Elija una opción válida por favor.")

def menu_idiomas(usuario):
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
            idioma_nuevo()
        elif opcion == "2":
            mostrar_idiomas(idiomas)
        elif opcion == "3":
            buscar_elemento_generico(idiomas, "id_idioma")
        elif opcion == "4":
            consultar_elementos(idiomas, ["idioma"])
        elif opcion == "5":
            editar_elemento(idiomas, "id_idioma", ["idioma"])
        elif opcion == "6":
            eliminar_elemento(idiomas, "id_idioma")
        elif opcion == "7":
            break
        else:
            print("Elija una opción válida por favor.")

def menu_principal(usuario):
    nombre = usuario.get("nombre", usuario) if isinstance(usuario, dict) else usuario
    
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
            menu_libros(usuario)
        elif opcion == "2":
            menu_autores(usuario)
        elif opcion == "3":
            menu_editoriales(usuario)
        elif opcion == "4":
            menu_formatos(usuario)
        elif opcion == "5":
            menu_idiomas(usuario)
        elif opcion == "6":
            menu_isbns(usuario)
        elif opcion == "7":
            print("Cerrando sesión...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

def menu_inicio():
    cargar_datos()
    while True:
        print("\nBienvenido al control de libros")
        print("1. Iniciar sesion")
        print("2. Crear nuevo usuario")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            usuario_logueado = iniciar_sesion(usuarios)
            if usuario_logueado:
                menu_principal(usuario_logueado)
        elif opcion == "2":
            usuario_nuevo()
            print("Usuario creado con éxito. Ahora puedes iniciar sesión.")
        elif opcion == "3":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    menu_inicio()