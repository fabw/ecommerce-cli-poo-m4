from datetime import datetime


class ProductoNoEncontradoError(Exception):
    """Excepción personalizada para productos inexistentes."""
    pass


class CantidadInvalidaError(Exception):
    """Excepción personalizada para cantidades inválidas."""
    pass


class Producto:
    def __init__(self, id_producto, nombre, categoria, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio

    def mostrar_info(self):
        print(
            f"ID: {self.id_producto} | "
            f"Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | "
            f"Precio: {self.precio:.2f}€"
        )

    def convertir_a_linea(self):
        return f"{self.id_producto},{self.nombre},{self.categoria},{self.precio}\n"


class Catalogo:
    def __init__(self):
        self.productos = [
            Producto(1, "camiseta", "ropa", 15.99),
            Producto(2, "auriculares", "tecnologia", 29.90),
            Producto(3, "lampara", "hogar", 18.50),
            Producto(4, "balon de futbol", "deportes", 22.00),
            Producto(5, "gel de ducha", "aseo", 4.75)
        ]

    def listar_productos(self):
        if not self.productos:
            print("El catálogo está vacío.")
            return

        print("\nCatálogo de productos:")
        for producto in self.productos:
            producto.mostrar_info()

    def buscar_producto_por_id(self, id_producto):
        for producto in self.productos:
            if producto.id_producto == id_producto:
                return producto

        raise ProductoNoEncontradoError("Producto no encontrado.")

    def buscar_productos(self, texto_busqueda):
        resultados = []
        texto_busqueda = texto_busqueda.lower()

        for producto in self.productos:
            if (
                texto_busqueda in producto.nombre.lower()
                or texto_busqueda in producto.categoria.lower()
            ):
                resultados.append(producto)

        return resultados

    def crear_producto(self, id_producto, nombre, categoria, precio):
        try:
            self.buscar_producto_por_id(id_producto)
            print("Ya existe un producto con ese ID.")
        except ProductoNoEncontradoError:
            nuevo_producto = Producto(id_producto, nombre, categoria, precio)
            self.productos.append(nuevo_producto)
            print("Producto creado correctamente.")

    def actualizar_producto(self, id_producto, nuevo_nombre, nueva_categoria, nuevo_precio):
        producto = self.buscar_producto_por_id(id_producto)

        producto.nombre = nuevo_nombre
        producto.categoria = nueva_categoria
        producto.precio = nuevo_precio

        print("Producto actualizado correctamente.")

    def eliminar_producto(self, id_producto):
        producto = self.buscar_producto_por_id(id_producto)
        self.productos.remove(producto)
        print("Producto eliminado correctamente.")

    def guardar_catalogo(self, nombre_archivo="catalogo.txt"):
        try:
            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                for producto in self.productos:
                    archivo.write(producto.convertir_a_linea())

            print(f"Catálogo guardado correctamente en {nombre_archivo}.")

        except OSError:
            print("Error al guardar el catálogo en el archivo.")

        finally:
            print("Operación de guardado finalizada.")


class ItemCarrito:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.producto.precio * self.cantidad

    def mostrar_info(self):
        print(
            f"Producto: {self.producto.nombre} | "
            f"Cantidad: {self.cantidad} | "
            f"Precio unitario: {self.producto.precio:.2f}€ | "
            f"Subtotal: {self.calcular_subtotal():.2f}€"
        )


class Carrito:
    def __init__(self):
        self.items = []

    def agregar_producto(self, producto, cantidad):
        if cantidad <= 0:
            raise CantidadInvalidaError("La cantidad debe ser mayor que cero.")

        for item in self.items:
            if item.producto.id_producto == producto.id_producto:
                item.cantidad += cantidad
                print("Cantidad actualizada en el carrito.")
                return

        nuevo_item = ItemCarrito(producto, cantidad)
        self.items.append(nuevo_item)
        print("Producto agregado al carrito correctamente.")

    def ver_carrito(self):
        if not self.items:
            print("El carrito está vacío.")
            return

        print("\nCarrito de compras:")
        for item in self.items:
            item.mostrar_info()

        print(f"Total a pagar: {self.calcular_total():.2f}€")

    def calcular_total(self):
        total = 0

        for item in self.items:
            total += item.calcular_subtotal()

        return total

    def esta_vacio(self):
        return len(self.items) == 0

    def vaciar_carrito(self):
        self.items.clear()


class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre


class Admin(Usuario):
    def __init__(self, nombre, catalogo):
        super().__init__(nombre)
        self.catalogo = catalogo

    def mostrar_menu(self):
        print("\n--- MENÚ ADMIN ---")
        print("1) Listar productos")
        print("2) Crear producto")
        print("3) Actualizar producto")
        print("4) Eliminar producto")
        print("5) Guardar catálogo en archivo")
        print("0) Salir")


class Cliente(Usuario):
    def __init__(self, nombre, catalogo):
        super().__init__(nombre)
        self.catalogo = catalogo
        self.carrito = Carrito()

    def mostrar_menu(self):
        print("\n--- MENÚ CLIENTE ---")
        print("1) Ver catálogo")
        print("2) Buscar producto")
        print("3) Agregar producto al carrito")
        print("4) Ver carrito y total")
        print("5) Confirmar compra")
        print("0) Salir")

    def confirmar_compra(self, nombre_archivo="ordenes.txt"):
        if self.carrito.esta_vacio():
            print("No se puede confirmar la compra porque el carrito está vacío.")
            return

        try:
            with open(nombre_archivo, "a", encoding="utf-8") as archivo:
                fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                archivo.write("----- NUEVA COMPRA -----\n")
                archivo.write(f"Cliente: {self.nombre}\n")
                archivo.write(f"Fecha y hora: {fecha_hora}\n")

                for item in self.carrito.items:
                    archivo.write(
                        f"Producto: {item.producto.nombre} | "
                        f"Cantidad: {item.cantidad} | "
                        f"Precio unitario: {item.producto.precio:.2f}€ | "
                        f"Subtotal: {item.calcular_subtotal():.2f}€\n"
                    )

                archivo.write(f"Total: {self.carrito.calcular_total():.2f}€\n")
                archivo.write("------------------------\n\n")

            print("Compra confirmada correctamente.")
            print(f"Orden registrada en {nombre_archivo}.")
            self.carrito.vaciar_carrito()

        except OSError:
            print("Error al registrar la compra en el archivo.")

        finally:
            print("Operación de compra finalizada.")


class Tienda:
    def __init__(self):
        self.catalogo = Catalogo()

    def iniciar(self):
        print("Bienvenido/a al Ecommerce CLI - Módulo 4")

        nombre = input("Ingrese su nombre: ")
        rol = input("Ingrese su rol ADMIN o CLIENTE: ").upper()

        if rol == "ADMIN":
            admin = Admin(nombre, self.catalogo)
            self.ejecutar_menu_admin(admin)

        elif rol == "CLIENTE":
            cliente = Cliente(nombre, self.catalogo)
            self.ejecutar_menu_cliente(cliente)

        else:
            print("Rol no válido. Debe ingresar ADMIN o CLIENTE.")

    def ejecutar_menu_admin(self, admin):
        opcion = ""

        while opcion != "0":
            admin.mostrar_menu()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                admin.catalogo.listar_productos()

            elif opcion == "2":
                self.crear_producto_admin(admin)

            elif opcion == "3":
                self.actualizar_producto_admin(admin)

            elif opcion == "4":
                self.eliminar_producto_admin(admin)

            elif opcion == "5":
                admin.catalogo.guardar_catalogo()

            elif opcion == "0":
                print("Saliendo del menú ADMIN.")

            else:
                print("Opción no válida.")

    def ejecutar_menu_cliente(self, cliente):
        opcion = ""

        while opcion != "0":
            cliente.mostrar_menu()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                cliente.catalogo.listar_productos()

            elif opcion == "2":
                self.buscar_producto_cliente(cliente)

            elif opcion == "3":
                self.agregar_producto_cliente(cliente)

            elif opcion == "4":
                cliente.carrito.ver_carrito()

            elif opcion == "5":
                cliente.confirmar_compra()

            elif opcion == "0":
                print("Saliendo del menú CLIENTE.")

            else:
                print("Opción no válida.")

    def crear_producto_admin(self, admin):
        try:
            id_producto = int(input("Ingrese el ID del nuevo producto: "))
            nombre = input("Ingrese el nombre del producto: ")
            categoria = input("Ingrese la categoría del producto: ")
            precio = float(input("Ingrese el precio del producto: "))

            if precio <= 0:
                print("El precio debe ser mayor que cero.")
                return

            admin.catalogo.crear_producto(id_producto, nombre, categoria, precio)

        except ValueError:
            print("Error: debe ingresar valores numéricos válidos.")

    def actualizar_producto_admin(self, admin):
        try:
            id_producto = int(input("Ingrese el ID del producto a actualizar: "))
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            nueva_categoria = input("Ingrese la nueva categoría: ")
            nuevo_precio = float(input("Ingrese el nuevo precio: "))

            if nuevo_precio <= 0:
                print("El precio debe ser mayor que cero.")
                return

            admin.catalogo.actualizar_producto(
                id_producto,
                nuevo_nombre,
                nueva_categoria,
                nuevo_precio
            )

        except ProductoNoEncontradoError as error:
            print(error)

        except ValueError:
            print("Error: debe ingresar valores numéricos válidos.")

    def eliminar_producto_admin(self, admin):
        try:
            id_producto = int(input("Ingrese el ID del producto a eliminar: "))
            admin.catalogo.eliminar_producto(id_producto)

        except ProductoNoEncontradoError as error:
            print(error)

        except ValueError:
            print("Error: debe ingresar un ID numérico válido.")

    def buscar_producto_cliente(self, cliente):
        texto = input("Ingrese nombre o categoría del producto: ")
        resultados = cliente.catalogo.buscar_productos(texto)

        if resultados:
            print("\nResultados encontrados:")
            for producto in resultados:
                producto.mostrar_info()
        else:
            print("No se encontraron productos.")

    def agregar_producto_cliente(self, cliente):
        try:
            id_producto = int(input("Ingrese el ID del producto: "))
            cantidad = int(input("Ingrese la cantidad: "))

            producto = cliente.catalogo.buscar_producto_por_id(id_producto)
            cliente.carrito.agregar_producto(producto, cantidad)

        except ProductoNoEncontradoError as error:
            print(error)

        except CantidadInvalidaError as error:
            print(error)

        except ValueError:
            print("Error: debe ingresar valores numéricos válidos.")


tienda = Tienda()
tienda.iniciar()