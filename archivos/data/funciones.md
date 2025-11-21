# Funciones

¿Por que usamos funciones en programación?
Cuando escribimos un programa, muchas veces necesitamos repetir ciertas operaciones u organizar el código para que sea más claro y fácil de mantener. Ahí es donde las funciones juegan un papel crucial.

## ¿Qué es una función?
Una función es un bloque de código que realiza una tarea específica. Puedes pensar en ella como una "mini-programa" dentro de tu programa. Las funciones pueden recibir entradas (llamadas parámetros) y pueden devolver un resultado.

Lo mejor que se puede hacer cuando creamos una función es que realice una sola tarea específica, no solo que sea para imprimir algo en pantalla, sino que haga un cálculo o procese datos.

Podemos crear librerias de funcuones que podemos reutilizar en diferentes programas. De forma que asi podamos actualizar las funciones en un solo lugar y todos los programas que las usan se benefician de la actualización.

Las funciones nos sirven para definir las cosas una sola vez y usarlas muchas veces. Lo que nos gusta es que estas reciban argumentos y que retornen valores.

Una funcion nos permite:
- Reutilizar código, es decir aislar el codigo y usarlo una y otra vez.
- Dividir el problema en partes mas pequeñas y manejables. (tambien lo hace más facil de entender)
- Evitar la repetición de código.
- Hacer pruebas más fáciles, ya que podemos probar cada función de manera independiente (dentro del programa podemos buscar errores más fácilmente y probarla en distintos escenarios).

## ¿Qué pasa si no usamos funciones?
Si no usamos funciones, nuestro código puede volverse largo, repetitivo y difícil de entender. Por ejemplo, si necesitamos realizar la misma operación en varios lugares de nuestro programa, tendríamos que escribir el mismo código una y otra vez, lo que aumenta la probabilidad de errores y hace que el mantenimiento sea complicado.

En resumen, las funciones son herramientas esenciales en la programación que nos ayudan a escribir código más limpio, eficiente y fácil de mantener.

## Sintaxis básica de una función en Python

```python
def nombre_de_la_funcion(parametro1, parametro2):
    # Bloque de código que realiza una tarea específica
    resultado = parametro1 + parametro2
    return resultado
```
Una funcion puede recibir más de un paraqmetro, o ninguno. Si no recibe parámetros, los paréntesis quedan vacíos. Y retornar un valor es opcional.
Cuando los parentesis quedan vacíos, la función no recibe ningún parámetro. Y se usa cuando la función no necesita información externa para realizar su tarea. 

## Diferencia entre funciones y procedimientos
Aunque a menudo se usan indistintamente, hay una diferencia sutil entre funciones y procedimientos:
- **Funciones**: Son bloques de código que realizan una tarea específica y devuelven un valor.
- **Procedimientos**: Son bloques de código que realizan una tarea específica pero no devuelven un valor.
- En Python, todas las funciones pueden considerarse procedimientos si no devuelven un valor explícito (es decir, si no usan la palabra clave `return`).

## Algunos puntos clave sobre las funciones
- **Definición**: Se define una función usando la palabra clave `def`, seguida del nombre de la función y paréntesis que pueden contener parámetros.
- **Llamada**: Para usar una función, simplemente la llamas por su nombre y le pasas los argumentos necesarios.
-**Parametros**: son las variables que se definen en la declaración de la función y que reciben los valores cuando se llama a la función.
- **Argumentos**: son los valores reales que se pasan a la función cuando se llama
- **Retorno**: Una función puede devolver un valor usando la palabra clave `return`. Si no se especifica un valor de retorno, la función devuelve `None` por defecto.

**Nota importante** : En Python no se ejeucuta el bloque de código dentro de la función hasta que se llama a la función.

Cuando se usa el comando print dentro de una función, la función realiza la acción de imprimir en pantalla, pero no devuelve un valor que pueda ser utilizado en otras partes del programa. Por lo tanto, si intentas asignar el resultado de una función que solo imprime a una variable, esa variable contendrá `None`, ya que la función no tiene un valor de retorno explícito.

## Ambito de las variables en funciones
El ámbito de una variable se refiere a la parte del programa donde esa variable es accesible. En Python, las variables definidas dentro de una función tienen un ámbito local, lo que significa que solo son accesibles dentro de esa función. Por otro lado, las variables definidas fuera de cualquier función tienen un ámbito global y pueden ser accesibles desde cualquier parte del programa, incluyendo dentro de las funciones, a menos que se declare una variable local con el mismo nombre.

¿Qué es el scope o ámbito de una variable?
El ámbito de una variable se refiere a la parte del programa donde esa variable es accesible. En Python, las variables definidas dentro de una función tienen un ámbito local, lo que significa que solo son accesibles dentro de esa función. 

Funciones locales y globales:
- **Variables locales**: Son aquellas definidas dentro de una función. Solo pueden ser utilizadas dentro de esa función y no son accesibles desde fuera.
- **Variables globales**: Son aquellas definidas fuera de cualquier función. Pueden ser accedidas desde cualquier parte del programa, incluyendo dentro de las funciones, a menos que se declare una variable local con el mismo nombre.

Python busca las variables en el siguiente orden:
1. Ámbito local: Primero busca la variable dentro de la función.
2. Ámbito escoling: Si la función está anidada dentro de otra función, busca en la función contenedora.
3. Ámbito global: Luego busca en el ámbito global del módulo.
4. Ámbito built-in: Finalmente, busca en las funciones incorporadas de Python.

## Argumentos para personalizar el resultado de una función
Los argumentos son valores que se pasan a una función cuando se llama. Estos valores permiten personalizar el comportamiento de la función según las necesidades específicas del momento. Por ejemplo, si tienes una función que calcula el área de un rectángulo, puedes pasarle los valores de la base y la altura como argumentos para obtener el área correspondiente.  

## Paso de argumentos:

Existen diferentes formas de pasar argumentos a una función en Python:
- **Por posición**: Los argumentos se pasan en el orden en que se definen los parámetros en la función.
- **Por nombre**: Los argumentos se pasan especificando el nombre del parámetro, lo que permite cambiar el orden de los argumentos. Si usamos los nombres no es necesario respetar el orden.
- **Valores por defecto**: Los parámetros pueden tener valores por defecto, que se usan si no se proporciona un argumento al llamar a la función. Es para decir que si no se pasa un valor, la función usará el valor por defecto.
- **Argumentos variables**: Se pueden usar `*args` para pasar un número variable de argumentos posicionales y `**kwargs` para pasar un número variable de argumentos nombrados. Permite que una cantidad variable de argumentos sean pasados a la función.

Por ejemplo como usar ars y kwargs:
```python
def suma (*numeros):
    total = 0
    for numero in numeros:
        total += numero
    return total
resultado = suma(1, 2, 3, 4, 5)
print(resultado)  # Salida: 15
```

```python
def imprimir_info(**info):
    for clave, valor in info.items():
        print(f"{clave}: {valor}")  
imprimir_info(nombre="Ana", edad=30, ciudad="Madrid")
# Salida:
# nombre: Ana
# edad: 30      

```

## Buenas prácticas al usar funciones:
- **Nombres descriptivos**: Usa nombres claros y descriptivos para las funciones y sus parámetros.
- **Una sola tarea**: Cada función debe realizar una sola tarea específica.
- **Retornar valores, no imprimir**: Evita usar `print` dentro de las funciones; en su lugar, retorna valores para que puedan ser usados posteriormente.
- **Valores por defecto**: Usa valores por defecto para parámetros cuando sea apropiado, para hacer las funciones más flexibles.
- **Docstrings**: Incluye docstrings para describir lo que hace la función, sus parámetros y su valor de retorno. Docstrings son cadenas de texto que se colocan justo después de la definición de una función para documentar su propósito y uso.
  
```python
def sumar(a, b):
    """Suma dos números y devuelve el resultado.    
    Parámetros:
    a (int, float): El primer número.
    b (int, float): El segundo número.  
    Retorna:
    int, float: La suma de a y b.
    """
    return a + b
```
-**Probar con assert**: Usa declaraciones `assert` para verificar que las funciones funcionan como se espera durante el desarrollo.
- **Validad salidas**: Asegúrate de que las funciones manejen adecuadamente entradas inválidas o inesperadas.
- **Modularidad**: Divide el código en funciones pequeñas y reutilizables en lugar de tener grandes bloques de código monolíticos.

