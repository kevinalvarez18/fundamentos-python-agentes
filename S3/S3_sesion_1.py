import datetime
from typing import Dict, List, Tuple

print("-----------Iniciando el pseudoagente estilo consola--------------------")

# Darle un alias a la memoria hace que humanos y modelos de IA entiendan rapido el contrato de datos que se espera en cada herramienta.
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]


def login(usuario: str, password: str) -> Tuple[bool, str, str]:
    """Valida credenciales y devuelve (acceso, rol, mensaje)."""
    if usuario == "admin" and password == "admin123":
        return True, "admin", "[Sistema] Acceso concedido. Privilegios de Administrador activados."

    if usuario == "invitado" and password == "1234":
        return True, "invitado", "[Sistema] Acceso concedido. Modo Invitado."

    return False, "", "[Error] Credenciales incorrectas."


def gestionar_historial(accion: str, memoria: MemoriaAgente) -> str:
    """Procesa historial all, historial clear o busqueda por palabra y retorna texto formateado."""
    accion_normalizada = accion.strip().lower()

    if accion_normalizada == "all":
        if not memoria:
            return "[PseudoAgente] El historial esta vacio."

        lineas: List[str] = ["[PseudoAgente] Historial completo:"]
        for registro in memoria:
            lineas.append(
                f"- {registro['timestamp']} | {registro['rol']} | {registro['cmd']} | {registro['descripcion']}"
            )
        return "\n".join(lineas)

    if accion_normalizada == "clear":
        memoria.clear()
        return "[PseudoAgente] El historial fue eliminado correctamente."

    if accion_normalizada == "":
        return "[PseudoAgente] Debes ingresar una palabra clave para buscar."

    resultados: List[Recuerdo] = []
    for registro in memoria:
        if accion_normalizada in registro["descripcion"].lower():
            resultados.append(registro)

    if not resultados:
        return "[PseudoAgente] No encontre registros que coincidan con esa palabra."

    lineas_resultado: List[str] = [f"[PseudoAgente] Se encontraron {len(resultados)} coincidencias:"]
    for item in resultados:
        lineas_resultado.append(f"Autor: {item['rol']} | Mensaje: {item['descripcion']}")
    return "\n".join(lineas_resultado)


def contar_letras(palabra: str) -> str:
    """Cuenta vocales, consonantes y letras de una palabra, ignorando mayusculas."""
    palabra_normalizada = palabra.strip().lower()
    vocales = sum(1 for letra in palabra_normalizada if letra in "aeiou")
    consonantes = sum(1 for letra in palabra_normalizada if letra.isalpha() and letra not in "aeiou")
    total = sum(1 for letra in palabra_normalizada if letra.isalpha())

    return (
        f"[PseudoAgente] Conteo para '{palabra_normalizada}':\n"
        f"Vocales: {vocales}\n"
        f"Consonantes: {consonantes}\n"
        f"Total de letras: {total}"
    )


def validar_password(password: str) -> str:
    """Valida reglas minimas de seguridad para una contrasena."""
    tiene_mayuscula = any(caracter.isupper() for caracter in password)
    tiene_minuscula = any(caracter.islower() for caracter in password)
    tiene_numero = any(caracter.isdigit() for caracter in password)
    longitud_valida = len(password) >= 8

    if all([tiene_mayuscula, tiene_minuscula, tiene_numero, longitud_valida]):
        return "[PseudoAgente] Password valido: cumple reglas basicas de seguridad."

    return (
        "[PseudoAgente] Password invalido: requiere minimo 8 caracteres, "
        "al menos una mayuscula, una minuscula y un numero."
    )


def calculadora(operacion: str, numero_1: float, numero_2: float) -> str:
    """Ejecuta una operacion matematica basica y retorna el resultado en texto."""
    if operacion == "+":
        return f"[PseudoAgente] Resultado: {numero_1 + numero_2}"
    if operacion == "-":
        return f"[PseudoAgente] Resultado: {numero_1 - numero_2}"
    if operacion == "*":
        return f"[PseudoAgente] Resultado: {numero_1 * numero_2}"
    if operacion == "/":
        if numero_2 == 0:
            raise ValueError("No se puede dividir para cero.")
        return f"[PseudoAgente] Resultado: {numero_1 / numero_2}"

    raise ValueError("Operacion no valida. Usa +, -, * o /.")


def obtener_fecha_hoy(rol_actual: str) -> str:
    """Devuelve la fecha actual solo si el rol tiene privilegios de administrador."""
    if rol_actual != "admin":
        # Aqui lanzo (raise) el error en la logica del comando y luego el menu principal lo atrapa con except para mostrar un mensaje sin apagar el programa.
        raise PermissionError("Privilegios insuficientes")

    ahora = datetime.datetime.now()
    return f"[PseudoAgente] La fecha y hora actual es: {ahora.strftime('%Y-%m-%d %H:%M:%S')}"


def registrar_evento(memoria: MemoriaAgente, comando: str, rol: str, descripcion: str) -> None:
    """Guarda un registro de ejecucion en la memoria del agente."""
    registro: Recuerdo = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cmd": comando,
        "rol": rol,
        "descripcion": descripcion,
    }
    memoria.append(registro)


intentos = 0
rol_actual = ""
tiene_acceso = False
usuario = ""

while intentos < 3 and not tiene_acceso:
    usuario = input("Usuario: ").strip().lower()
    password = input("Contrasena: ").strip()

    tiene_acceso, rol_actual, mensaje_login = login(usuario, password)
    if not tiene_acceso:
        intentos += 1
        print(f"{mensaje_login} Te quedan {3 - intentos} intentos.")
    else:
        print(mensaje_login)

if tiene_acceso:
    historial_chat: MemoriaAgente = [
        {
            "timestamp": "2026-03-18 13:50:51",
            "cmd": "ping",
            "rol": "invitado",
            "descripcion": "Se ha enviado un ping y de respuesta se devolvio un pong.",
        }
    ]

    pseudo_activo = True

    while pseudo_activo:
        entrada_usuario = input(f"\n{usuario}@PseudoAgente>: ").strip()
        partes = entrada_usuario.lower().split(maxsplit=1)
        comando = partes[0] if partes else ""
        descripcion = ""
        registrar_en_historial = True

        try:
            if comando == "salir":
                pseudo_activo = False
                descripcion = "[PseudoAgente] Apagando sistemas..."

            elif comando == "ping":
                descripcion = "[PseudoAgente] pong~"

            elif comando == "historial":
                if len(partes) > 1:
                    accion_historial = partes[1]
                else:
                    accion_historial = input("Ingresa la palabra clave a buscar: ").strip()

                descripcion = gestionar_historial(accion_historial, historial_chat)
                if accion_historial.strip().lower() == "clear":
                    registrar_en_historial = False

            elif comando == "contar":
                palabra = input("Ingresa una palabra: ")
                descripcion = contar_letras(palabra)

            elif comando == "validar_pass":
                password_usuario = input("Ingresa la contrasena a validar: ").strip()
                descripcion = validar_password(password_usuario)

            elif comando == "calculadora":
                operacion = input("Operacion (+, -, *, /): ").strip()
                numero_1_txt = input("Numero 1: ").strip()
                numero_2_txt = input("Numero 2: ").strip()

                try:
                    numero_1 = float(numero_1_txt)
                    numero_2 = float(numero_2_txt)
                except ValueError as error_conversion:
                    raise ValueError("Debes ingresar numeros validos en la calculadora.") from error_conversion

                descripcion = calculadora(operacion, numero_1, numero_2)

            elif comando == "fecha_hoy":
                descripcion = obtener_fecha_hoy(rol_actual)

            elif comando == "":
                descripcion = "[PseudoAgente] Comando vacio. Intente de nuevo."

            else:
                descripcion = "[PseudoAgente] Comando no existe. Intente de nuevo."

        except PermissionError as error_permiso:
            descripcion = f"[Alerta] {error_permiso}. Este comando requiere privilegios de administrador."
        except ValueError as error_datos:
            descripcion = f"[Error de datos] {error_datos}"

        print(descripcion)

        if registrar_en_historial:
            registrar_evento(historial_chat, entrada_usuario.lower(), rol_actual, descripcion)

else:
    print("Acceso denegado.")




