# Ecommerce CLI con POO - Módulo 4

Aplicación de consola desarrollada en Python que simula el funcionamiento básico de un ecommerce, aplicando Programación Orientada a Objetos, roles de usuario, manejo de excepciones y escritura de archivos de texto.

## Funcionalidades principales

La aplicación permite trabajar con dos tipos de usuario:

- ADMIN
- CLIENTE

Al iniciar el programa, el usuario debe indicar su nombre y seleccionar el rol con el que desea ingresar.

## Rol ADMIN

El usuario ADMIN puede:

- Listar productos del catálogo.
- Crear productos nuevos.
- Actualizar productos existentes.
- Eliminar productos del catálogo.
- Guardar el catálogo en un archivo de texto.

## Rol CLIENTE

El usuario CLIENTE puede:

- Ver el catálogo de productos.
- Buscar productos por nombre o categoría.
- Agregar productos al carrito indicando ID y cantidad.
- Ver el carrito con subtotales y total a pagar.
- Confirmar una compra.
- Registrar la compra en un archivo de texto.

## Estructura del proyecto

```bash
ecommerce-cli-poo-m4/
│── main.py
│── README.md
│── catalogo.txt
│── ordenes.txt
