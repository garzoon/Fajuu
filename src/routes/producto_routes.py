from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from ..controller import *
from ..models import Producto, Categoria

producto_scope = Blueprint("producto_scope", __name__)
PATH_URL_PRODUCTO = "producto" # Acortador de url

 
@producto_scope.route('/', methods = ['GET', 'POST'])
def producto():

    connection = create_connection()
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

    if connection:
        cur = connection.cursor()
        cur.execute(query, parameters)
        product_list_result = cur.fetchall()

    list_producto = []
    
    for producto in product_list_result:
        producto = Producto(*producto[:6])
        categoria = Categoria(*get_product_category(producto.cate_copiaid)[0])
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


@producto_scope.route('/producto_add', methods = ['GET'])
def producto_add():
    return render_template(f'{PATH_URL_PRODUCTO}/producto_create.html')

@producto_scope.route('/create', methods = ['POST' ,'GET'])
def create():
    if request.method == 'POST':
        try:
            producto_id = None
            producto_descripcion = request.form.get('producto_descripcion')
            producto_categoria = request.form.get('producto_categoria')
            producto_precio = request.form.get('producto_precio')
            producto_medida = request.form.get('producto_medida')

            producto = Producto(
                producto_id, 
                producto_descripcion, 
                producto_categoria, 
                producto_medida, 
                producto_precio
            )
            producto_create(producto)

            flash(f"Producto {producto_descripcion} fue agregado", "success")
            return redirect(url_for('producto_scope.producto'))
        except Exception as ex:
            raise Exception(ex)
            
    
@producto_scope.route('/producto_delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    try:
        producto = Producto(*producto_select(id)[0])
        producto_delete(producto)
        flash(f'Producto ({producto.prod_id}) {producto.prod_descripcion} fue eliminado', "success")
        return redirect(url_for('producto_scope.producto'))
    except Exception as ex:
        raise Exception(ex)

@producto_scope.route('/producto_update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        producto_search = Producto(*producto_select(id)[0])
        try:
            producto_id = producto_search.prod_id
            producto_descripcion = request.form.get('producto_descripcion')
            producto_categoria = request.form.get('producto_categoria')
            producto_medida = request.form.get('producto_medida')
            producto_precio = request.form.get('producto_precio')
            producto_estado = producto_search.prod_estado

            producto_update(
                producto = Producto(
                    producto_id, 
                    producto_descripcion, 
                    producto_categoria, 
                    producto_medida, 
                    producto_precio, 
                    producto_estado
                ))

            flash(f"Producto {producto_id} fue actualizado", "success")
            return redirect(url_for('producto_scope.producto'))
        except Exception as ex:
            raise Exception(ex)
        
    producto = Producto(*producto_select(id)[0])

    return render_template(f'{PATH_URL_PRODUCTO}/producto_update.html', producto = producto)

@producto_scope.route('/producto_details/<int:id>', methods = ['GET'])
def producto_details(id):
    producto = Producto(*producto_select(id)[0])
    categoria = Categoria(*get_product_category(producto.cate_copiaid)[0])
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
