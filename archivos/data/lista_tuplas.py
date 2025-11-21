results = [("seq1", 45.29879),("seq2", 30.134567), ("seq3", 78.934564), ("seq4", 12.4)]
print(f"{'secuencia':<10} {'GC%':>10}")  #Encabezados con formato el :< izquierda y >: derecha y el numero es el espacio asignado
print("-" * 21)  #línea separadora, dentro de los printns se pueden hacer operaciones
for seq_id, gc_content in results:
    print(f"{seq_id: <10}\t{gc_content:>10.2f}")  #Imprime sin formato")
        

#:.2f sirve para limitar el número de decimales a 2, despues de los dos puntos se especifica el formato, en este caso f de float (número decimal)


##condicional ternario

edad = 10
print("Mayor de edad") if edad >= 18 else print("Menor de edad") # la primer condicion es la verdadera, la segunda la falsa