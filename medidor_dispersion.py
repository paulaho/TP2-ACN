import sys
import re
from typing import Dict, List, Tuple


def parse_solution(solution_file: str) -> Dict[str, int]:
    """
    Lee el archivo de solución y extrae el día asignado para cada parcial.

    Formato esperado: x$P<ID>#<Slot>#<Dia> ...
    Ejemplo: x$P0#1#9 ... -> Parcial 'P0' está en el día 9
    """
    exam_days: Dict[str, int] = {}
    
    # Expresión regular para capturar el nombre del parcial (ej: P0, P12) 
    # y el día (ej: 9, 12)
    # Patrón:
    #   x\$     -> "x$" literal
    #   (P\d+)  -> Grupo 1: "P" seguido de uno o más dígitos (el nombre del parcial)
    #   #\d+#   -> "#" seguido de dígitos (slot) seguido de "#"
    #   (\d+)   -> Grupo 2: uno o más dígitos (el día)
    pattern = re.compile(r'x\$(P\d+)#\d+#(\d+)')

    try:
        with open(solution_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                match = pattern.search(line)
                if match:
                    partial_name = match.group(1)
                    try:
                        day = int(match.group(2))
                        exam_days[partial_name] = day
                    except ValueError:
                        print(f"Advertencia: No se pudo convertir el día a número en la línea: {line}")
                else:
                    # Opcional: avisar si una línea no coincide, aunque puede ser ruido
                    # print(f"Info: Línea ignorada (no coincide formato): {line}")
                    pass
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo de solución: {solution_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo de solución: {e}")
        sys.exit(1)
        
    if not exam_days:
        print("Advertencia: No se pudo parsear ningún parcial del archivo de solución.")
        
    return exam_days

def parse_common_students(common_file: str) -> List[Tuple[str, str, int]]:
    """
    Lee el archivo de estudiantes en común.

    Formato esperado: <Parcial1> <Parcial2> <CantidadEstudiantes>
    Ejemplo: P0 P1 50
    """
    common_students: List[Tuple[str, str, int]] = []
    
    try:
        with open(common_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'): # Ignorar líneas vacías o comentarios
                    continue
                
                parts = line.split()
                if len(parts) == 3:
                    p1, p2, count_str = parts
                    try:
                        count = int(count_str)
                        common_students.append((p1, p2, count))
                    except ValueError:
                        print(f"Advertencia: Ignorando línea mal formada (conteo no es número) "
                              f"en {common_file}, línea {line_num}: {line}")
                else:
                    print(f"Advertencia: Ignorando línea mal formada (no tiene 3 columnas) "
                          f"en {common_file}, línea {line_num}: {line}")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo de estudiantes en común: {common_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer el archivo de estudiantes en común: {e}")
        sys.exit(1)
        
    return common_students

def calculate_dispersion(exam_days: Dict[str, int], common_students: List[Tuple[str, str, int]]) -> Dict[str, int]:
    """
    Calcula la dispersión contando los estudiantes en cada categoría de solapamiento.
    """
    counts = {
        "same_day": 0,
        "consecutive": 0,       # 1 día de diferencia
        "one_day_between": 0,   # 2 días de diferencia
        "two_plus_days": 0,     # 3+ días de diferencia
        "missing_exam": 0       # Conteo de estudiantes donde falta un parcial
    }
    
    missing_pairs = set()

    for p1, p2, count in common_students:
        # Verificar que ambos parciales están en nuestro diccionario de días
        if p1 not in exam_days:
            if p1 not in missing_pairs:
                print(f"Advertencia: El parcial '{p1}' del archivo común no se encontró en la solución.")
                missing_pairs.add(p1)
            counts["missing_exam"] += count
            continue
            
        if p2 not in exam_days:
            if p2 not in missing_pairs:
                print(f"Advertencia: El parcial '{p2}' del archivo común no se encontró en la solución.")
                missing_pairs.add(p2)
            counts["missing_exam"] += count
            continue
            
        # Obtener los días
        day1 = exam_days[p1]
        day2 = exam_days[p2]
        
        # Calcular la diferencia absoluta de días
        day_diff = abs(day1 - day2)
        
        # Clasificar y sumar el conteo de estudiantes
        if day_diff == 0:
            counts["same_day"] += count
        elif day_diff == 1:
            counts["consecutive"] += count
        elif day_diff == 2:
            counts["one_day_between"] += count
        elif day_diff >= 3:
            counts["two_plus_days"] += count
            
    return counts

def main():
    """
    Función principal del script.
    """
    # Espera dos argumentos: <archivo_solucion> <archivo_comun>
    solution_file = "asignacionej3_v3.txt"
    common_file = "estudiantes-en-comun.dat"
    
    print(f"Leyendo solución desde: {solution_file}")
    exam_days = parse_solution(solution_file)
    print(f"Se cargaron los días de {len(exam_days)} parciales.")
    
    print(f"Leyendo estudiantes en común desde: {common_file}")
    common_students = parse_common_students(common_file)
    print(f"Se cargaron {len(common_students)} pares de parciales.")
    
    if not exam_days or not common_students:
        print("Error: Uno de los archivos de entrada está vacío o no se pudo procesar. Abortando.")
        sys.exit(1)
    
    print("\nCalculando dispersión...")
    results = calculate_dispersion(exam_days, common_students)
    
    print("\n--- RESULTADOS DEL ANÁLISIS DE DISPERSIÓN ---")
    print(f"Estudiantes con 2 parciales el MISMO DÍA (0 días dif):          {results['same_day']}")
    print(f"Estudiantes con 2 parciales en DÍAS CONSECUTIVOS (1 día dif):   {results['consecutive']}")
    print(f"Estudiantes con 2 parciales con 1 DÍA de por medio (2 días dif): {results['one_day_between']}")
    print(f"Estudiantes con 2 parciales con 2+ DÍAS de por medio (3+ días dif): {results['two_plus_days']}")
    
    if results['missing_exam'] > 0:
        print("\n--- ADVERTENCIAS ---")
        print(f"Estudiantes ignorados por parciales no encontrados en la solución: {results['missing_exam']}")

if __name__ == "__main__":
    main()