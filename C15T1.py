#librerias
from datetime import datetime

#clases par alas estructuras de datos
class NodoLista:
    """Nodo de la lista enlazada para el inventario."""

    def __init__(self, producto):
        self.producto  = producto
        self.siguiente = None


class ListaEnlazada:
    """
    Lista enlazada simple que almacena los productos del inventario.
    Permite insercion, eliminacion y busqueda en O(n).
    """

    def __init__(self):
        self.cabeza  = None
        self._tamano = 0

    def agregar(self, producto):
        """Inserta un producto al final de la lista."""
        nuevo = NodoLista(producto)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._tamano += 1

    def eliminar(self, codigo):
        """Elimina el producto con el codigo dado. Retorna el producto o None."""
        actual   = self.cabeza
        anterior = None
        while actual:
            if actual.producto.codigo == codigo:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                self._tamano -= 1
                return actual.producto
            anterior = actual
            actual   = actual.siguiente
        return None

    def buscar(self, codigo):
        """Retorna el producto con el codigo dado o None si no existe."""
        actual = self.cabeza
        while actual:
            if actual.producto.codigo == codigo:
                return actual.producto
            actual = actual.siguiente
        return None

    def listar(self):
        """Retorna todos los productos como lista de Python."""
        resultado = []
        actual    = self.cabeza
        while actual:
            resultado.append(actual.producto)
            actual = actual.siguiente
        return resultado

    def tamano(self):
        """Retorna el numero de productos en el inventario."""
        return self._tamano


class NodoPila:
    """Nodo de la pila para el historial de acciones."""

    def __init__(self, valor):
        self.valor     = valor
        self.siguiente = None


class Pila:
    """
    Pila LIFO para el historial de operaciones.
    Cada entrada guarda suficiente informacion para deshacer la accion.
    """

    def __init__(self):
        self.cima   = None
        self.tamano = 0

    def push(self, valor):
        """Apila una accion en el historial."""
        nuevo           = NodoPila(valor)
        nuevo.siguiente = self.cima
        self.cima       = nuevo
        self.tamano    += 1

    def pop(self):
        """Desapila y retorna la ultima accion registrada."""
        if self.esta_vacia():
            raise IndexError("pila vacia")
        valor       = self.cima.valor
        self.cima   = self.cima.siguiente
        self.tamano -= 1
        return valor

    def peek(self):
        """Retorna la ultima accion sin eliminarla."""
        if self.esta_vacia():
            raise IndexError("pila vacia")
        return self.cima.valor

    def esta_vacia(self):
        """Retorna True si no hay acciones en el historial."""
        return self.cima is None

    def listar(self):
        """Retorna todas las acciones desde la mas reciente."""
        resultado = []
        actual    = self.cima
        while actual:
            resultado.append(actual.valor)
            actual = actual.siguiente
        return resultado


class NodoCola:
    """Nodo de la cola FIFO para pedidos."""

    def __init__(self, dato):
        self.dato      = dato
        self.siguiente = None


class Cola:
    """
    Cola FIFO para gestionar pedidos en orden de llegada.
    Garantiza que el primer pedido en llegar sea el primero en procesarse.
    """

    def __init__(self):
        self.frente  = None
        self.final   = None
        self.tamano  = 0

    def enqueue(self, dato):
        """Agrega un pedido al final de la cola."""
        nuevo = NodoCola(dato)
        if self.final is None:
            self.frente = nuevo
            self.final  = nuevo
        else:
            self.final.siguiente = nuevo
            self.final           = nuevo
        self.tamano += 1

    def dequeue(self):
        """Elimina y retorna el pedido al frente de la cola."""
        if self.esta_vacia():
            raise IndexError("cola vacia")
        dato        = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self.tamano -= 1
        return dato

    def esta_vacia(self):
        """Retorna True si no hay pedidos en espera."""
        return self.frente is None

    def listar(self):
        """Retorna todos los pedidos desde el frente."""
        resultado = []
        actual    = self.frente
        while actual:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado


# =============================================================================
#  MODELOS DE DOMINIO
# =============================================================================

class Producto:
    """Representa un producto en el inventario del almacen."""

    def __init__(self, codigo, nombre, cantidad, precio):
        self.codigo   = codigo.upper()
        self.nombre   = nombre
        self.cantidad = cantidad
        self.precio   = precio

    def __str__(self):
        return (f"[{self.codigo}] {self.nombre:<22} "
                f"Cant: {self.cantidad:>4}  Precio: ${self.precio:>8.2f}")


class Pedido:
    """Representa un pedido de un cliente sobre un producto."""

    _contador = 0

    def __init__(self, cliente, codigo_producto, cantidad):
        Pedido._contador += 1
        self.id_pedido       = Pedido._contador
        self.cliente         = cliente
        self.codigo_producto = codigo_producto.upper()
        self.cantidad        = cantidad
        self.timestamp       = datetime.now().strftime("%H:%M:%S")
        self.estado          = "PENDIENTE"

    def __str__(self):
        return (f"Pedido #{self.id_pedido:>3}  Cliente: {self.cliente:<16} "
                f"Producto: {self.codigo_producto}  "
                f"Cant: {self.cantidad}  [{self.estado}]  @{self.timestamp}")


# =============================================================================
#  SISTEMA PRINCIPAL
# =============================================================================

class SistemaAlmacen:
    """
    Integra las tres estructuras de datos:
      - ListaEnlazada : inventario dinamico de productos.
      - Pila          : historial de operaciones con soporte de deshacer.
      - Cola          : pedidos FIFO pendientes de procesamiento.
    """

    def __init__(self):
        self.inventario = ListaEnlazada()
        self.historial  = Pila()
        self.pedidos    = Cola()

    # ── Inventario (Lista Enlazada) ───────────────────────────────────────────

    def agregar_producto(self, codigo, nombre, cantidad, precio):
        """Agrega un producto nuevo al inventario."""
        if self.inventario.buscar(codigo.upper()):
            print(f"  Ya existe un producto con codigo '{codigo.upper()}'.")
            return
        producto = Producto(codigo, nombre, cantidad, precio)
        self.inventario.agregar(producto)
        self.historial.push({
            "accion"  : "AGREGAR_PRODUCTO",
            "producto": Producto(codigo, nombre, cantidad, precio)
        })
        print(f"  Producto '{nombre}' agregado al inventario.")

    def eliminar_producto(self, codigo):
        """Elimina un producto del inventario y guarda la accion para deshacer."""
        producto = self.inventario.eliminar(codigo.upper())
        if producto is None:
            print(f"  Producto '{codigo.upper()}' no encontrado.")
            return
        self.historial.push({
            "accion"  : "ELIMINAR_PRODUCTO",
            "producto": producto
        })
        print(f"  Producto '{producto.nombre}' eliminado.")

    def modificar_stock(self, codigo, nueva_cantidad):
        """Modifica la cantidad en stock de un producto."""
        producto = self.inventario.buscar(codigo.upper())
        if producto is None:
            print(f"  Producto '{codigo.upper()}' no encontrado.")
            return
        cantidad_anterior = producto.cantidad
        producto.cantidad = nueva_cantidad
        self.historial.push({
            "accion"           : "MODIFICAR_STOCK",
            "codigo"           : producto.codigo,
            "cantidad_anterior": cantidad_anterior,
            "cantidad_nueva"   : nueva_cantidad
        })
        print(f"  Stock de '{producto.nombre}' actualizado: "
              f"{cantidad_anterior} -> {nueva_cantidad}.")

    def mostrar_inventario(self):
        """Muestra todos los productos del inventario."""
        productos = self.inventario.listar()
        if not productos:
            print("  Inventario vacio.")
            return
        print(f"\n  Inventario ({self.inventario.tamano()} productos):")
        for p in productos:
            alerta = "  *** STOCK BAJO ***" if p.cantidad < 5 else ""
            print(f"  {p}{alerta}")

    # ── Historial / Deshacer (Pila) ───────────────────────────────────────────

    def deshacer(self):
        """Deshace la ultima operacion registrada en el historial."""
        if self.historial.esta_vacia():
            print("  No hay acciones para deshacer.")
            return

        accion = self.historial.pop()
        tipo   = accion["accion"]

        if tipo == "AGREGAR_PRODUCTO":
            self.inventario.eliminar(accion["producto"].codigo)
            print(f"  Deshecho: agregar '{accion['producto'].nombre}'.")

        elif tipo == "ELIMINAR_PRODUCTO":
            self.inventario.agregar(accion["producto"])
            print(f"  Deshecho: eliminar '{accion['producto'].nombre}' "
                  f"(restaurado al inventario).")

        elif tipo == "MODIFICAR_STOCK":
            producto = self.inventario.buscar(accion["codigo"])
            if producto:
                producto.cantidad = accion["cantidad_anterior"]
                print(f"  Deshecho: stock de '{producto.nombre}' "
                      f"restaurado a {accion['cantidad_anterior']}.")

        elif tipo == "PROCESAR_PEDIDO":
            producto = self.inventario.buscar(accion["codigo_producto"])
            if producto:
                producto.cantidad += accion["cantidad"]
            self.pedidos.enqueue(accion["pedido"])
            accion["pedido"].estado = "PENDIENTE"
            print(f"  Deshecho: procesamiento del Pedido "
                  f"#{accion['pedido'].id_pedido} revertido.")

    def mostrar_historial(self):
        """Muestra las acciones en el historial desde la mas reciente."""
        acciones = self.historial.listar()
        if not acciones:
            print("  Historial vacio.")
            return
        print(f"\n  Historial ({len(acciones)} accion(es), mas reciente primero):")
        for i, a in enumerate(acciones, 1):
            tipo = a["accion"]
            if tipo == "AGREGAR_PRODUCTO":
                detalle = f"Agregar producto '{a['producto'].nombre}'"
            elif tipo == "ELIMINAR_PRODUCTO":
                detalle = f"Eliminar producto '{a['producto'].nombre}'"
            elif tipo == "MODIFICAR_STOCK":
                detalle = (f"Modificar stock '{a['codigo']}': "
                           f"{a['cantidad_anterior']} -> {a['cantidad_nueva']}")
            elif tipo == "PROCESAR_PEDIDO":
                detalle = f"Procesar Pedido #{a['pedido'].id_pedido}"
            else:
                detalle = tipo
            print(f"  {i:>2}. {detalle}")

    # ── Pedidos (Cola FIFO) ───────────────────────────────────────────────────

    def registrar_pedido(self, cliente, codigo_producto, cantidad):
        """Agrega un pedido a la cola FIFO."""
        if not self.inventario.buscar(codigo_producto.upper()):
            print(f"  Producto '{codigo_producto.upper()}' no existe en inventario.")
            return
        pedido = Pedido(cliente, codigo_producto, cantidad)
        self.pedidos.enqueue(pedido)
        print(f"  Pedido #{pedido.id_pedido} registrado en la cola.")

    def procesar_siguiente_pedido(self):
        """Procesa el primer pedido de la cola y descuenta el stock."""
        if self.pedidos.esta_vacia():
            print("  No hay pedidos pendientes.")
            return

        pedido   = self.pedidos.dequeue()
        producto = self.inventario.buscar(pedido.codigo_producto)

        if producto is None:
            print(f"  Producto '{pedido.codigo_producto}' ya no existe.")
            pedido.estado = "CANCELADO"
            return

        if producto.cantidad < pedido.cantidad:
            print(f"  Stock insuficiente para Pedido #{pedido.id_pedido}. "
                  f"Disponible: {producto.cantidad}, solicitado: {pedido.cantidad}.")
            pedido.estado = "PENDIENTE"
            self.pedidos.enqueue(pedido)
            return

        producto.cantidad -= pedido.cantidad
        pedido.estado      = "PROCESADO"

        self.historial.push({
            "accion"         : "PROCESAR_PEDIDO",
            "pedido"         : pedido,
            "codigo_producto": pedido.codigo_producto,
            "cantidad"       : pedido.cantidad
        })

        print(f"  Pedido #{pedido.id_pedido} procesado.")
        print(f"  Cliente: {pedido.cliente}  |  "
              f"Producto: {pedido.codigo_producto}  |  "
              f"Cantidad: {pedido.cantidad}")
        print(f"  Stock restante de '{producto.nombre}': {producto.cantidad}")

    def mostrar_pedidos(self):
        """Muestra todos los pedidos pendientes en la cola."""
        pedidos = self.pedidos.listar()
        if not pedidos:
            print("  No hay pedidos en cola.")
            return
        print(f"\n  Cola de pedidos ({len(pedidos)} pendiente(s)):")
        for p in pedidos:
            print(f"  {p}")


# =============================================================================
#  HELPERS DE ENTRADA
# =============================================================================

def pedir_entero(mensaje, minimo=0):
    """Solicita un entero con validacion."""
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor < minimo:
                print(f"  El valor debe ser >= {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Ingrese un numero entero valido.")


def pedir_float(mensaje, minimo=0.0):
    """Solicita un flotante con validacion."""
    while True:
        try:
            valor = float(input(mensaje).strip())
            if valor < minimo:
                print(f"  El valor debe ser >= {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Ingrese un numero valido.")


# =============================================================================
#  MENUS
# =============================================================================

def menu_inventario(sistema):
    while True:
        print("\n  -- Inventario --")
        print("  1. Agregar producto")
        print("  2. Eliminar producto")
        print("  3. Modificar stock")
        print("  4. Mostrar inventario")
        print("  0. Volver")
        op = input("  Opcion: ").strip()

        if op == "1":
            codigo   = input("  Codigo    : ").strip()
            nombre   = input("  Nombre    : ").strip()
            cantidad = pedir_entero("  Cantidad  : ", minimo=0)
            precio   = pedir_float("  Precio    : ", minimo=0.0)
            if not codigo or not nombre:
                print("  Codigo y nombre no pueden estar vacios.")
                continue
            sistema.agregar_producto(codigo, nombre, cantidad, precio)

        elif op == "2":
            codigo = input("  Codigo a eliminar: ").strip()
            sistema.eliminar_producto(codigo)

        elif op == "3":
            codigo   = input("  Codigo del producto: ").strip()
            cantidad = pedir_entero("  Nueva cantidad    : ", minimo=0)
            sistema.modificar_stock(codigo, cantidad)

        elif op == "4":
            sistema.mostrar_inventario()

        elif op == "0":
            break
        else:
            print("  Opcion invalida.")


def menu_pedidos(sistema):
    while True:
        print("\n  -- Pedidos --")
        print("  1. Registrar pedido")
        print("  2. Procesar siguiente pedido")
        print("  3. Ver cola de pedidos")
        print("  0. Volver")
        op = input("  Opcion: ").strip()

        if op == "1":
            cliente  = input("  Nombre del cliente     : ").strip()
            codigo   = input("  Codigo del producto    : ").strip()
            cantidad = pedir_entero("  Cantidad solicitada    : ", minimo=1)
            if not cliente or not codigo:
                print("  Cliente y codigo no pueden estar vacios.")
                continue
            sistema.registrar_pedido(cliente, codigo, cantidad)

        elif op == "2":
            sistema.procesar_siguiente_pedido()

        elif op == "3":
            sistema.mostrar_pedidos()

        elif op == "0":
            break
        else:
            print("  Opcion invalida.")


def menu_historial(sistema):
    while True:
        print("\n  -- Historial --")
        print("  1. Ver historial de acciones")
        print("  2. Deshacer ultima accion")
        print("  0. Volver")
        op = input("  Opcion: ").strip()

        if op == "1":
            sistema.mostrar_historial()

        elif op == "2":
            sistema.deshacer()

        elif op == "0":
            break
        else:
            print("  Opcion invalida.")


def main():
    sistema = SistemaAlmacen()

    print("=" * 58)
    print("  C15T1 - Sistema Dinamico de Inventario y Pedidos")
    print("  Integracion: Lista Enlazada + Pila + Cola FIFO")
    print("=" * 58)

    while True:
        print("\n  1. Inventario  (lista enlazada)")
        print("  2. Pedidos     (cola FIFO)")
        print("  3. Historial   (pila / deshacer)")
        print("  0. Salir")
        op = input("\n  Opcion: ").strip()

        if op == "1":
            menu_inventario(sistema)
        elif op == "2":
            menu_pedidos(sistema)
        elif op == "3":
            menu_historial(sistema)
        elif op == "0":
            print("\n  Sistema cerrado.")
            break
        else:
            print("  Opcion invalida.")


if __name__ == "__main__":
    main()