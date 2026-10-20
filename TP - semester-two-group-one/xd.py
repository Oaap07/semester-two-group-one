import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 1, 5, 3]
plt.plot(x, y, marker='o')

# Tus líneas guía actuales (nota: recuerda escribir 'label' en minúscula)
plt.axhline(y=3, color='r', linestyle='--', label='Umbral horizontal (y=3)')
plt.axvline(x=2.5, color='g', linestyle=':', label='Línea vertical (x=2.5)')

# --- ESTA ES LA NUEVA LÍNEA QUE DEBES AGREGAR ---
plt.grid(True, axis='y', linestyle=':', color='gray', alpha=0.6)

plt.legend()
plt.show()
