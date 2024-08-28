from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from ..controller import *
from ..models import Producto, Categoria

producto_scope = Blueprint("producto_scope", __name__)
PATH_URL_PRODUCTO = "producto" # Acortador de url

 
@producto_scope.route('/', methods = ['GET', 'POST'])
def producto():
    query = """SELECT * FROM productos WHERE 1=1"""
    parameters = []

    if request.method == 'POST':
        producto_id = request.form.get('producto_id')
        producto_categoria = request.form.get('producto_categoria')
        producto_estado = request.form.get('producto_estado')
        
        if producto_id:
            query += " AND prod_id LIKE %s"
            parameters.append(f"%{producto_id}%")
            
        if producto_categoria:
            query += " AND cate_copiaid LIKE %s"
            parameters.append(f"%{producto_categoria}%")
            
        if producto_estado:
            query += " AND prod_estado LIKE %s"
            parameters.append(f"%{producto_estado}%")

    product_list_result = fetch_all(query, parameters)

    list_producto = []
    
    for producto in product_list_result:
        producto = Producto(*producto)
        categoria = get_producto_categoria(producto.cate_copiaid)
        item_producto = (
            producto.prod_id, 
            producto.prod_descripcion,
            categoria.cate_descripcion,
            producto.prod_unidad_medida,
            producto.prod_stock,
            producto.prod_estado
        )
        list_producto.append(item_producto)

    return render_template(f'{PATH_URL_PRODUCTO}/producto.html', list_producto = list_producto)

@producto_scope.route('/producto_create', methods = ['POST' ,'GET'])
def create_producto():
    if request.method == 'POST':
        try:
            producto_id = None
            producto_descripcion = request.form.get('producto_descripcion')
            producto_categoria = request.form.get('producto_categoria')
            producto_precio = request.form.get('producto_precio')
            producto_medida = request.form.get('producto_medida')
            producto_estado = None,
            producto_stock = None

            producto = Producto(
                producto_id, 
                producto_descripcion, 
                producto_categoria, 
                producto_medida, 
                producto_precio,
                producto_estado,
                producto_stock
            )
            producto_create(producto)

            flash(f"Producto {producto_descripcion} fue agregado", "success")
            return redirect(url_for('producto_scope.producto'))
        
        # Manejo de errores
        except mysql.connector.Error as ex:
            flash("Error al intentar crear el producto", "warning")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "warning")
    return render_template(f'{PATH_URL_PRODUCTO}/producto_create.html')
            
    
@producto_scope.route('/producto_delete/<int:id>', methods = ['GET', 'POST'])
def delete_producto(id):
    try:
        producto = producto_select(id)
        producto_delete(producto)
        flash(f'Producto {producto.prod_id} - {producto.prod_descripcion} fue eliminado', "success")
        return redirect(url_for('producto_scope.producto'))
    
    # Manejo de errores
    except mysql.connector.IntegrityError as ex:
        flash("No se puede eliminar el producto porque está en uso", "warning")
    except mysql.connector.Error as ex:
        flash("Error al intentar eliminar el producto", "warning")
    except Exception as ex:
        flash(f"Error inesperado: {ex}", "warning")
    return redirect(url_for('producto_scope.producto'))

@producto_scope.route('/producto_update/<int:id>', methods = ['GET', 'POST'])
def update_producto(id):
    if request.method == 'POST':
        producto_search = producto_select(id)
        try:
            producto_id = producto_search.prod_id
            producto_descripcion = request.form.get('producto_descripcion')
            producto_categoria = request.form.get('producto_categoria')
            producto_medida = request.form.get('producto_medida')
            producto_precio = request.form.get('producto_precio')
            producto_estado = producto_search.prod_estado
            producto_stock = producto_search.prod_stock

            producto_update(
                producto = Producto(
                    producto_id, 
                    producto_descripcion, 
                    producto_categoria, 
                    producto_medida, 
                    producto_precio, 
                    producto_estado,
                    producto_stock
                ))

            flash(f"Producto {producto_id} fue actualizado", "success")
            return redirect(url_for('producto_scope.producto'))
        # Manejo de errores
        except mysql.connector.Error as ex:
            flash("Error al intentar actualizar el producto", "warning")
        except Exception as ex:
            flash(f"Error inesperado: {ex}", "warning")
              
    producto = producto_select(id)
    return render_template(f'{PATH_URL_PRODUCTO}/producto_update.html', producto = producto)

@producto_scope.route('/producto_details/<int:id>', methods = ['GET'])
def details_producto(id):
    producto = producto_select(id)
    categoria = get_producto_categoria(producto.cate_copiaid)
    if producto:
        return jsonify({
            'id' : producto.prod_id,
            'descripcion' : producto.prod_descripcion,
            'categoria' : categoria.cate_descripcion,
            'unidad_medida' : producto.prod_unidad_medida,
            'precio' : producto.prod_precio,
            'estado' : producto.prod_estado,
            'stock' : producto.prod_stock
        })
    else:
        return jsonify({'Error' : "producto no encontrado"}), 404
