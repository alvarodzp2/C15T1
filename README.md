# C15T1 - problema 3: Sistema Dinamico de Inventario y Pedidos

## Instrucciones de ejecucion

Requiere Python 3.10 o superior (se usa union de tipos `|` en una anotacion).

```bash
python C15T1.py
```

No se necesitan librerias externas. Solo se importa `datetime` de la
biblioteca estandar.

---

## Contexto y problema que resuelve

Este sistema integra lo desarrollado en el problema 1 (C13T1, sistema de
almacen con pilas) y el problema 2 (C14T1, gestion de colas) en un unico
programa coherente de inventario y pedidos para un almacen.

El sistema resuelve tres problemas concproblemas:

1. **Inventario dinamico:** la cantidad de productos no se conoce de
   antemano y cambia constantemente. Una estructura estatica (array fijo)
   desperdiciaría memoria o requeriria redimensionamiento costoso.

2. **Historial con deshacer:** operaciones criticas como eliminar un
   producto o modificar su stock deben poder revertirse ante un error
   del operador, sin recargar toda la base de datos.

3. **Cola de pedidos justa:** los pedidos de clientes deben procesarse
   en el orden exacto en que llegaron, sin posibilidad de que un pedido
   tarde "se cuele" delante de uno anterior.

---

## Funcionalidades implementadas

### Modulo Inventario (Lista Enlazada)
- Agregar producto con codigo, nombre, cantidad y precio.
- Eliminar producto por codigo.
- Modificar stock de un producto existente.
- Mostrar inventario completo con alerta de stock bajo (< 5 unidades).

### Modulo Pedidos (Cola FIFO)
- Registrar un pedido de cliente indicando producto y cantidad.
- Procesar el siguiente pedido en la cola: descuenta stock y lo marca
  como procesado. Si el stock es insuficiente, el pedido vuelve al
  final de la cola con un mensaje de aviso.
- Ver todos los pedidos pendientes en orden de llegada.

### Modulo Historial (Pila)
- Ver el historial de acciones desde la mas reciente.
- Deshacer la ultima accion registrada (agregar producto, eliminar
  producto, modificar stock, procesar pedido).

---

## Estructuras de datos utilizadas y justificacion

### Lista Enlazada — Inventario

Cada nodo almacena un `Producto`. Los nodos se encadenan mediante
punteros `siguiente`, sin reservar memoria contigua.


### Pila — Historial y Deshacer

Cada entrada en la pila es un diccionario que describe la accion y
guarda el estado anterior necesario para revertirla.

**Justificacion:** el deshacer es naturalmente LIFO: la ultima accion
realizada es la primera que se revierte. La pila implementa esto de
forma exacta y eficiente. Conecta directamente con lo trabajado en el
problema 1 (C13T1), donde la pila se uso para guardar movimientos del
robot y revertirlos ante obstaculos.

### Cola FIFO — Pedidos

Los pedidos se encolan por el final y se desencolan por el frente,
garantizando orden de llegada estricto.

**Justificacion:** la equidad en la atencion de pedidos es un requisito
de negocio. Una cola FIFO es la unica estructura que garantiza que
ningun pedido tarde se adelante a uno anterior. Conecta directamente
con el problema 2 (C14T1), donde se implementaron colas para gestion de
procesos y emergencias.

---

## Ejemplo de sesion

```
1. Inventario -> Agregar producto
   Codigo   : LAPTOP01
   Nombre   : Laptop Dell XPS
   Cantidad : 10
   Precio   : 1200.00
   -> Producto 'Laptop Dell XPS' agregado al inventario.

2. Pedidos -> Registrar pedido
   Cliente         : Juan Perez
   Codigo producto : LAPTOP01
   Cantidad        : 2
   -> Pedido #1 registrado en la cola.

3. Pedidos -> Procesar siguiente pedido
   -> Pedido #1 procesado.
   -> Cliente: Juan Perez | Producto: LAPTOP01 | Cantidad: 2
   -> Stock restante de 'Laptop Dell XPS': 8

4. Historial -> Deshacer ultima accion
   -> Deshecho: procesamiento del Pedido #1 revertido.
   -> Stock restaurado a 10.
```

---

## Relacion con los problemas anteriores

| problema | Archivo | Conexion con problema 3 |
|---|---|---|
| problema 1 | C13T1problema1.py | La pila de movimientos del robot evoluciona a pila de historial de operaciones del almacen |
| problema 2 | C14T1problema1.py | La cola basica del problema 2 es la misma estructura usada para la cola de pedidos |
| problema 2 | C14T1problema3.py | La cola de prioridad del hospital inspira la alerta de stock bajo y pedidos urgentes |