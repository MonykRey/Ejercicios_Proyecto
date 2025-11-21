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
