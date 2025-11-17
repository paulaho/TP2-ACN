import os

# 1. Definir los días disponibles
dias_disponibles = [1, 2, 3, 4, 5, 9, 10, 11, 12]

# 2. Definir la función de penalización
def calcular_penalizacion(d1, d2):
    """
    Calcula la penalización basada en la diferencia numérica.
    Respeta la regla de que 5 y 9 NO son consecutivos.
    """
    if d1 == d2:
        return 10  # Mismo día
    elif abs(d1 - d2) == 1:
        return 5   # Días numéricamente consecutivos (ej: 4-5)
    elif abs(d1 - d2) == 2:
        return 2   # Un día numéricamente en el medio (ej: 3-5)
    else:
        return 0   # Otro caso (incluye 5-9, donde abs=4)

# 3. Nombre del archivo de salida
output_filename = "penalizaciones.dat"

# 4. Generar el archivo de texto
try:
    with open(output_filename, 'w', encoding='utf-8') as f:
        # Iterar sobre todas las combinaciones de días
        for d1 in dias_disponibles:
            for d2 in dias_disponibles:
                # Calcular la penalización para este par
                penalizacion = calcular_penalizacion(d1, d2)
                
                # Escribir la línea con 3 columnas separadas por espacio
                # Formato: d1 d2 penalizacion
                f.write(f"{d1} {d2} {penalizacion}\n")
        
    print(f"¡Éxito! Archivo '{output_filename}' generado correctamente.")
    print(f"Contiene {len(dias_disponibles)**2} filas.")

except Exception as e:
    print(f"Error al escribir el archivo: {e}")
    print(f"Error al escribir el archivo: {e}")