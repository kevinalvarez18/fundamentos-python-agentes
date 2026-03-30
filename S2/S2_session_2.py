## Día 1: Lista y Diccionarios 
## Día 2: Anidaciones - [[],[],[]...], {"a": {1: []}}, [{},{}]

import datetime
print("-----------Iniciando el pseudoagente estilo consola--------------------")

##Login

intentos = 0
rol_actual = ""
tiene_acceso = False

while intentos < 3 and not tiene_acceso:
    # strip() limpia espacios sobrantes y lower() normaliza el texto para comparar usuarios sin problemas de mayúsculas.
    usuario = input("Usuario: ").strip().lower()
    password = input("Contraseña: ").strip()
    
    if usuario == "admin" and password == "admin123":
        rol_actual = "admin"
        tiene_acceso = True
        print("[Sistema] Acceso concedido. Privilegios de Administrador activados.")
        
    elif usuario == "invitado" and password == "1234":
        rol_actual = "invitado"
        tiene_acceso = True
        print("[Sistema] Acceso concedido. Modo Invitado.")
        
    else:
        intentos += 1
        print(f"[Error] Credenciales incorrectas. Te quedan {3 - intentos} intentos.")

## Pseudoagente
if tiene_acceso:
    # historial_chat guarda cada acción como un diccionario con fecha, comando, rol y descripción.
    historial_chat=[{'timestamp': '2026-03-18 13:50:51', 'cmd': 'ping', 'rol': 'invitado', 'descripcion': 'Se ha enviado un ping y de respuesta se devolvió un pong.'}, {'timestamp': '2026-03-18 13:50:56', 'cmd': 'fecha_hoy', 'rol': 'invitado', 'descripcion': '[Acceso Denegado] Este comando requiere privilegios de administrador.'}, {'timestamp': '2026-03-18 13:51:02', 'cmd': 'dormir', 'rol': 'invitado', 'descripcion': 'Comando no existe. Intente de nuevo'}, {'timestamp': '2026-03-18 13:51:07', 'cmd': 'salir', 'rol': 'invitado', 'descripcion': 'Se ha solicitado terminar la sesión.'}] 
    pseudo_activo = True
    mensaje = ""

    while pseudo_activo:
        # split() separa el comando principal de opciones como "historial all" o "historial clear".
        entrada_usuario = input(f"\n{usuario}@PseudoAgente>: ").strip()
        partes_cmd = entrada_usuario.lower().split()
        cmd = partes_cmd[0] if partes_cmd else ""
        registrar_historial = True

        if cmd == "salir":
            print("[PseudoAgente] Apagando sistemas...")
            pseudo_activo = False
            mensaje = "Se ha solicitado terminar la sesión."
        elif cmd == "historial":
            if len(partes_cmd) > 1 and partes_cmd[1] == "all":
                if historial_chat:
                    print("[PseudoAgente] Historial completo:")
                    for registro in historial_chat:
                        print(f"- {registro['timestamp']} | {registro['rol']} | {registro['cmd']} | {registro['descripcion']}")
                    mensaje = "Se mostró todo el historial almacenado."
                else:
                    mensaje = "[PseudoAgente] El historial está vacío."
                    print(mensaje)
            elif len(partes_cmd) > 1 and partes_cmd[1] == "clear":
                historial_chat.clear()
                registrar_historial = False
                mensaje = "[PseudoAgente] El historial fue eliminado correctamente."
                print(mensaje)
            else:
                palabra_clave = input("Ingresa la palabra clave a buscar: ").strip().lower()
                coincidencias = 0

                for registro in historial_chat:
                    # Uso split() para detectar opciones del comando y lower() junto con in para saber si la palabra clave está dentro de la descripción sin importar mayúsculas o minúsculas.
                    if palabra_clave in registro["descripcion"].lower():
                        coincidencias += 1
                        print(f"Autor: {registro['rol']} | Mensaje: {registro['descripcion']}")

                if coincidencias == 0:
                    mensaje = "[PseudoAgente] No encontré registros que coincidan con esa palabra."
                    print(mensaje)
                else:
                    mensaje = f"[PseudoAgente] Se encontraron {coincidencias} coincidencias."
                    print(mensaje)
        elif cmd == "ping":
            print("pong~")
            mensaje = "Se ha enviado un ping y de respuesta se devolvió un pong."            
        elif cmd == "contar":
            pal = input("Ingrese una palabra: ").strip().lower()
            tot_letras = len(pal)
            tot_vocales = 0
            tot_cons = 0
            for p in pal:
                if p in "aeiou":
                    tot_vocales += 1
                elif p.isalpha(): 
                    tot_cons += 1                    
            print(f"Palabra ingresada: {pal}")
            print(f"Total de vocales: {tot_vocales}")
            print(f"Total de consonantes: {tot_cons}")
            print(f"Total de letras: {tot_letras}")
            mensaje = f"""Se solicitó el conteo de la palabra {pal}, dando como resultados:
            Vocales: {tot_vocales}
            Consonantes: {tot_cons}
            Total: {tot_letras}"""
        elif cmd == "fecha_hoy":
            if rol_actual == "admin":
                ahora = datetime.datetime.now()
                mensaje = f"[PseudoAgente] La fecha y hora actual es: {ahora.strftime('%Y-%m-%d %H:%M:%S')}"
                print(mensaje)
                
            else:
                mensaje = "[Acceso Denegado] Este comando requiere privilegios de administrador."
                print(mensaje)

        elif cmd == "validar_pass":
            print("Validar pass")
            mensaje = ""
        elif cmd == "calculadora":
            print("Calculadora")
            mensaje = ""
        elif cmd == "":
            mensaje = "Comando vacío. Intente de nuevo"
            print(mensaje)
        else:
            mensaje = "Comando no existe. Intente de nuevo"
            print(mensaje)

        # now() obtiene la fecha actual y strftime() la convierte al formato de texto que guardaremos en el historial.
        if registrar_historial:
            d_log = {"timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "cmd": entrada_usuario.lower(),
                    "rol": rol_actual,
                    "descripcion": mensaje}

            # append() agrega el nuevo registro al final de la lista historial_chat.
            historial_chat.append(d_log)

else:
    print("Acceso denegado.")
