Podemos usar indices negativos para accedet a un elemento de la lista.

para cambiar un elemento de la lista, basta con enumerar su posición y ponerle el nuevo valor com:

lista [0] = 'z'
esto es, en la posición 0, cambia el elemento por z.

Para cortar una lista, debemos darle las posiciones, por ejemplo:

Slide: lista [1:4] #quiero que imprimas los valores que estan en la posicion del 1 al 3, por que el primer valor que queremos es inclusivo, pero el segundo no, es decir, te regresa un numero antes del que pusiste el límite.

A veces uno no puede poner la posicion de inicio o posicion de final y extraeria los valores desde el inicio o hasta el final, para eso se usa:

Slide: lista [:4] #esto regresa los valores desde el inicio hasta la posicion 3

Slide: lista [2:] #esto regresa los valores desde la posicion 2 hasta el final

Slide: lista [:] #esto regresa todos los valores de la lista

Tambien podemos ir saltando valores dentro de la lista, por ejemplo:

Slide: lista [::2] #esto regresa todos los valores, pero de dos en dos

Esto tambien puede hacerse con numeros negativos:

Slide: lista [::-2] #esto regresa todos los valores, pero de dos en dos, pero empezando desde el final hacia el inicio

Los string tambien pueden ser recorridos por que son objetos iterables, por ejemplo:

secuencia = "ATGCTTCG"
Podemos iterar en esta secuencia como si fuera una lista:

por ejemplo: 
secuencia[::-1] #esto regresa la secuencia invertida

La listas tambien tienen funciones como:

- append(): agrega un elemento al final de la lista
se agrega como:
nombre de la lista.append('nuevo_elemento') #esto para un valor, pero se puede agregar una lista, completa como:
nombre de la lista.extend(['elemento1', 'elemento2', 'elemento3']) #esto agrega varios elementos a la lista, el problema es que los agrega como una lista dentro de la lista, si queremos agregar los elementos de una lista a otra, debemos usar extend.
-extend(): agrega varios elementos al final de la lista, funciona igual que append pero con varios elementos y es mejor que append para agregar varios elementos.
- insert(): agrega un elemento en una posicion especifica
- remove(): elimina un elemento especifico, no por su pposicion, sino por su valor o nombre en la lista, ademas solo elimina la primera ocurrencia del elemento.
- pop(): elimina un elemento en una posicion especifica y lo regresa
- sort(): ordena la lista
- reverse(): invierte el orden de la lista  
- clear(): elimina todos los elementos de la lista

## Buscar elementos
- index(): regresa la posicion de un elemento especifico
- count(): regresa el numero de veces que un elemento aparece en la lista


## Compresion de listas (List comprehension)

La compresion de listas es una forma concisa de crear listas. La sintaxis es:

[nueva_expresion for item in iterable if condicion]

Componenetes:
- nueva_expresion: es la expresion, operacion o transformacion que se aplicara a cada item del iterable.
- item: es la variable que representa cada elemento del iterable.
- iterable: es cualquier objeto que se pueda recorrer, como una lista, tupla, conjunto
- for variable in iterable: es el bucle que recorre cada elemento dee la secuencia (lista, tupla, conjunto)
- if condicion (opcional): es una condicion que filtra los elementos del iterable, solo se incluyen los elementos que cumplen con la condicion.

Ejemplo 1: crear una lista simple:

>>> [x for x in range (5)]
[0, 1, 2, 3, 4] #crea una lista con los numeros del 0 al 4

Ejemplo 2: el cuadrado de los numeros 0 al 4 (son 5 numeros)

>>> [x**2 for x in range (5)]
[0, 1, 4, 9, 16] #toma el primer numero 0, lo eleva al cuadrado, luego toma el segundo numero 1, lo eleva al cuadrado, y asi sucesivamente hasta el 4.

Ejemplo 3: sumar 10 a cada elemento de una lista existente:
>>> lista = [1, 2, 3, 4, 5]
>>> [x + 10 for x in lista]
[11, 12, 13, 14, 15] #toma cada elemento de la lista y le suma 10.

Ejemplo 4: obtener los numeros pares de una lista existente:
>>> lista = [1, 2, 3, 4, 5,6,7,8,9,10]
>>> [x for x in lista if x % 2 == 0]
[2, 4, 6, 8, 10] #toma cada elemento de la lista y verifica si es par (si el residuo de la division entre 2 es 0), si es par, lo incluye en la nueva lista.

Ejemplo 5: de una lista existente, poner si es par o impar:
>>> lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> ['par' if x % 2 == 0 else 'impar' for x in lista]
['impar', 'par', 'impar', 'par', 'impar', 'par', 'impar', 'par', 'impar', 'par'] #toma cada elemento de la lista y verifica si es par o impar, si es par, agrega 'par' a la nueva lista, si es impar, agrega 'impar'.


bases = ["A","T","C", "G"]
bases [2]
bases [1] = "U"
bases 
['A', 'U', 'C', 'G']

secuencia = list"ATGCTTCG"
contar el numero de veces que aparece cada base con comprension de listas
secuencia = "ATGCTTCG"
bases = ["A","T","C", "G"]

[secuencia.count(base) for base  in bases] #primero cuenta cuantas veces aparece la base A en la secuencia, luego cuenta cuantas veces aparece la base T, y asi sucesivamente.

Podriamos poner la base y su conteo en un diccionario usando comprension de diccionarios:
 [ [base,secuencia.count(base)] for base  in bases] #esto crea una lista de listas, donde cada sublista contiene la base y su conteo.

 Dada una lista de bases eliminar cualquier base que no sea A o T usando comprension de listas:
    secuencia = ["A", "T", "C", "G", "A", "T", "C", "G"]
    bases_permitidas = ["A", "T"]
    secuencia_filtrada = [base for base in secuencia if base in bases_permitidas]
    secuencia_filtrada #funciona como toma una base de la secuencia, verifica si esta en las bases permitidas, si es asi, la agrega a la nueva lista.

Otro ejemplo:
tengo ua secuencia de DNA y la quiero convertir a RNA, para eso debo cambiar todas las T por U, usando comprension de listas:
    secuencia_dna = "ATGCTTCG"
    secuencia_rna = ''.join(['U' if base == 'T' else base for base in secuencia_dna])




# Tuplas en Python
Una tupla es una colección ordenada e inmutable de elementos. Se definen usando paréntesis () y los elementos están separados por comas. Es similar a una lista, pero no se pueden modificar después de su creación.

¿Por que existen las tuplas si ya existen las listas? Las tuplas son útiles cuando se desea asegurar que los datos no se modifiquen accidentalmente. También pueden ser más eficientes en términos de memoria y rendimiento en ciertos casos.

cuando queremos asignar un solo valor a una tupla, debemos poner una coma despues del valor, por ejemplo:
tupla = (5,) #esto crea una tupla con un solo elemento, el valor 5.

Ya que si no ponemos la coma, Python lo interpreta como un entero normal

Tambien podemos crear tuplas mixtas, es decir, con diferentes tipos de datos, por ejemplo:
tupla_mixta = (1, "hola", 3.14, True)   

Además podemos hacer tuplas anidadas, es decir, tuplas dentro de tuplas, por ejemplo:
tupla_anidada = (1, (2, 3), (4, 5, 6))      

Otra forma de hacer tuplas es hacerlas con listas dentros o flotantes, etc.
tupla_con_listas = ( [1, 2, 3], [4, 5, 6] ) 

Cuando hacemos referencia a un elemento de la tupla, lo hacemos igual que con las listas, es decir, usando indices, por ejemplo:
tupla = (10, 20, 30, 40, 50)
tupla[0] #esto regresa el primer elemento de la tupla, que es

# Metodos de las tuplas
Las tuplas tienen algunos métodos incorporados, aunque son limitados debido a su inmutabilidad. Algunos de los métodos más comunes son: 
- count(): devuelve el número de veces que un elemento aparece en la tupla.
- index(): devuelve el índice de la primera aparición de un elemento en la tupla.   

**NO HAY COMPRESION DE TUPLAS EN PYTHON**
pero podemos convertir una lista en una tupla usando la función tuple(), por ejemplo:
tuple (x**2 for x in range (5)) #esto crea una tupla con los cuadrados de los numeros del 0 al 4.


# Diccionarios en Python
Un diccionario es una colección desordenada, modificable e indexada de pares clave-valor. Se definen usando llaves {} y los pares clave-valor están separados por comas. Cada clave debe ser única dentro del diccionario.

Se usa para relacionar una clave (key) con un valor (value), por ejemplo, podemos tener un diccionario que relacione nombres de personas con sus edades:
edades = {"Juan": 25, "Maria": 30, "Pedro": 35}     

¿Como acceder a los valores en un diccionario?
Para acceder a un valor en un diccionario, usamos la clave correspondiente entre corchetes [], por ejemplo:
edades["Juan"] #esto regresa el valor asociado a la clave "Juan", que es 25.

## Diccionarios anidados
Los diccionarios pueden contener otros diccionarios como valores, lo que permite crear estructuras de datos más complejas. Por ejemplo:
persona = {
    "nombre": "Juan",
    "edad": 25,
    "direccion": {
        "calle": "Calle Falsa 123",
        "ciudad": "Springfield",
        "pais": "USA"
    }
}   

Ejemplo 2
genes = {
    "lacZ"
}