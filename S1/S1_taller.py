from datetime import datetime


print("----- Iniciando sistema del Agente -------")

# Credenciales base por rol.
credenciales = {
    "invitado": "invitado123",
    "admin": "admin123",
}

usuario_actual = ""
rol_actual = ""
login_exitoso = False
intentos_restantes = 3

# Esta lógica controla el bloqueo por intentos:
# 1) El ciclo se mantiene mientras haya intentos disponibles y no exista login exitoso.
# 2) En cada vuelta se pide usuario y contraseña y se valida contra las credenciales.
# 3) Si falla, se descuenta un intento y se informa cuántos quedan.
# 4) Cuando llega a 0 intentos, el sistema se bloquea y termina la ejecución.
while intentos_restantes > 0 and not login_exitoso:
    usuario_ingresado = input("Usuario: ").strip().lower()
    password_ingresada = input("Contraseña: ").strip()

    if (
        usuario_ingresado in credenciales
        and password_ingresada == credenciales[usuario_ingresado]
    ):
        login_exitoso = True
        usuario_actual = usuario_ingresado
        rol_actual = usuario_ingresado
        print(f"[Acceso concedido] Bienvenido/a, {usuario_actual}.")
    else:
        intentos_restantes -= 1
        if intentos_restantes > 0:
            print(f"[Error] Credenciales inválidas. Intentos restantes: {intentos_restantes}")

if not login_exitoso:
    print("[Alerta] Usuario bloqueado. Cerrando sistema.")
else:
    sistema_activo = True
    while sistema_activo:
        cmd = input("Agente>: ").strip().lower()

        if cmd == "salir":
            print("------Agente apagado. Vuelve pronto.------")
            sistema_activo = False

        elif cmd == "ping":
            print("pong!")

        elif cmd == "contar":
            frase = input("Ingresa una frase: ").lower()
            total_vocales = 0
            total_consonantes = 0

            for letra in frase:
                if letra in "aeiou":
                    total_vocales += 1
                elif letra.isalpha():
                    total_consonantes += 1

            print(f"Vocales: {total_vocales}")
            print(f"Consonantes: {total_consonantes}")

        elif cmd == "fecha_hoy":
            if rol_actual == "admin":
                fecha_actual = datetime.now().strftime("%Y-%m-%d")
                print(f"Fecha actual: {fecha_actual}")
            else:
                print("[Acceso Denegado] Este comando requiere privilegios de administrador.")

        elif cmd == "validar_pass":
            nueva_pass = input("Ingresa una nueva contraseña propuesta: ").strip()

            if len(nueva_pass) < 8:
                print("[Rechazada] La contraseña debe tener al menos 8 caracteres.")
            elif nueva_pass == usuario_actual:
                print("[Rechazada] La contraseña no puede ser igual al nombre de usuario.")
            else:
                print("[Éxito] Contraseña válida.")

        elif cmd == "calculadora":
            # Los valores que llegan por input son texto (str), no números.
            # Por eso usamos float() para convertirlos y poder sumar, restar, multiplicar o dividir.
            # Si no hacemos casting, operaciones como "2" + "3" concatenan texto ("23")
            # y expresiones como "2" - "3" lanzarían un TypeError.
            try:
                num1 = float(input("Ingresa el primer número: ").strip())
                operador = input("Ingresa el operador (+, -, *, /): ").strip()
                num2 = float(input("Ingresa el segundo número: ").strip())
            except ValueError:
                print("[Error] Debes ingresar valores numéricos válidos.")
                continue

            if operador == "+":
                print(f"Resultado: {num1 + num2}")
            elif operador == "-":
                print(f"Resultado: {num1 - num2}")
            elif operador == "*":
                print(f"Resultado: {num1 * num2}")
            elif operador == "/":
                if num2 == 0:
                    print("[Error] No se puede dividir entre cero.")
                else:
                    print(f"Resultado: {num1 / num2}")
            else:
                print("[Error] Operador no válido.")

        else:
            print("------Comando desconocido. Intente de nuevo.-------")