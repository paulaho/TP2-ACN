import collections

# --- Configuración ---
ARCHIVO_ASIGNACIONES = "asignacionej2.rtf" # Tu archivo de solución 
ARCHIVO_TRIOS = "trios.dat"             # Tu archivo con los tríos incompatibles

# --- Lógica ---

# 1. Parsear el archivo de asignaciones 
#    Crearemos un diccionario: { 'dia' -> {set_de_parciales_ese_dia} }
#    Ej: asignaciones_por_dia['1'] = {'P0', 'P21', 'P22', 'P58', ...}
print(f"Leyendo asignaciones desde '{ARCHIVO_ASIGNACIONES}'...")
asignaciones_por_dia = collections.defaultdict(set)

try:
    with open(ARCHIVO_ASIGNACIONES, 'r') as f:
        for line in f:
            parts = line.strip().split()
            
            # Si la línea está vacía o no es una variable, la ignoramos
            if not parts or not parts[0].startswith("x$"):
                continue
                
            var_name = parts[0]
            # 'x$P0#1#9' -> 'P0#1#9'
            info_str = var_name.lstrip("x$")
            
            # 'P0#1#9' -> ['P0', '1', '9']
            info_parts = info_str.split('#')
            
            if len(info_parts) == 3:
                parcial_id = info_parts[0]
                dia_id = info_parts[1]
                # No necesitamos la hora, solo el día
                
                # Agregamos el parcial al set de ese día
                asignaciones_por_dia[dia_id].add(parcial_id)

except FileNotFoundError:
    print(f"¡Error! No se pudo encontrar el archivo '{ARCHIVO_ASIGNACIONES}'.")
    exit()

print(f"Asignaciones leídas. Se procesaron {len(asignaciones_por_dia)} días.")

# 2. Cargar la lista de tríos
print(f"Leyendo tríos incompatibles desde '{ARCHIVO_TRIOS}'...")
lista_trios = []
try:
    with open(ARCHIVO_TRIOS, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            # Leemos los 3 parciales de la línea y los guardamos como un set
            parts = line.split()
            if len(parts) == 3:
                lista_trios.append(set(parts))
                
except FileNotFoundError:
    print(f"¡Error! No se pudo encontrar el archivo '{ARCHIVO_TRIOS}'.")
    print("Asegúrate de haber corrido primero el script 'buscar_trios.py'")
    exit()

print(f"Tríos leídos. Se verificarán {len(lista_trios)} tríos.")

# 3. Verificar la restricción
print("\n--- 🔍 Verificando Restricción (Máx. 2 por trío por día) ---")
violations_found = 0

# Iteramos sobre cada día que tiene asignaciones
for dia, parciales_ese_dia in asignaciones_por_dia.items():
    # Iteramos sobre cada trío incompatible
    for trio in lista_trios:
        
        # Vemos cuántos miembros del trío están asignados ese día
        # Usamos la intersección de sets
        asignados_del_trio = parciales_ese_dia.intersection(trio)
        
        # Si la intersección tiene 3 o más (debería ser 3)
        if len(asignados_del_trio) >= 3:
            # ¡Encontramos una violación!
            violations_found += 1
            print(f"  [VIOLACIÓN] Día {dia}: Los 3 miembros del trío {trio} están asignados.")

# 4. Reporte final
print("-------------------------------------------------")
if violations_found == 0:
    print("\n✅ ¡Verificación Exitosa!")
    print("Tu solución CUMPLE la restricción. No se encontraron 3 parciales de un mismo trío asignados en el mismo día.")
else:
    print(f"\n❌ ¡Auditoría Fallida! Se encontraron {violations_found} violaciones.")
    print("Revisa los mensajes de [VIOLACIÓN] de arriba.")