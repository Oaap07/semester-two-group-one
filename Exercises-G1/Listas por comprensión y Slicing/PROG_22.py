"""
PROG_22: El departamento de ciberseguridad necesita enviar mensajes
encriptados a los agentes en campo. Tu tarea será construir el algoritmo
de encriptado utilizando herramientas nativas de Python y luego utilizar
Inteligencia Artificial (ChatGPT, Gemini, etc.) como asistente para
desarrollar el desencriptador, documentando todo el proceso.
Parte 1: El Encriptador (Programación en Python)
Escriban un script en Python que tome el siguiente mensaje base:
Mensaje: "Hola James Bond, deberás ir a Cabildo y Juramento. Fin del
Mensaje"

Resultado: "101j97sn101m l101d n105f .111tn101m97r117j y 111dl105b97c
97 r105 sár101b101d ,dn111b s101m97j 97l111h"
Y aplique los siguientes pasos de transformación:

1. Inversión y Normalización: Invierte el texto completo y
conviértelo a minúsculas. Es obligatorio utilizar slicing.

2. Sustitución por ASCII: Genera el mensaje cifrado final
reemplazando cada vocal (a, e, i, o, u) por su correspondiente
código ASCII (convertido a texto). Es obligatorio utilizar una
Lista por Comprensión y .join().

3. Muestra por pantalla el mensaje encriptado resultante.
Parte 2: El Desafío de Desencriptación con IA
Una vez que tengan el mensaje encriptado:

1. Utilizar una herramienta de Inteligencia Artificial para
solicitarle que cree una función en Python capaz de desencriptar
el texto y recuperar la frase original.

2. Ejecutar el código proporcionado por la IA y verificar si recupera
el texto exactamente como era al principio.

3. Documentar el resultado final:
o ¿Cómo resolvió la IA el problema de devolver los códigos
ASCII (como '101' o '97') a sus vocales originales?
o ¿En qué parte del código de la IA se utilizó slicing para
volver a dar vuelta la cadena?
"""

def encriptado(mensaje):
    mensaje = mensaje.lower()[::-1]
    encriptado = ["97" if l == "a" else "101" if l == "e" else "105" if l == "i" else "111" if l == "o" else "117" if l == "u" else l for l in mensaje]
    encriptado= "".join(encriptado)
    print(encriptado)   




encriptado("Hola James Bond, deberás ir a Cabildo y Juramento. Fin del Mensaje")




