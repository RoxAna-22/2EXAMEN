from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'


@app.route("/")
def index():
    if 'productos' not in session:
        session['productos'] = []
    productos = session.get('productos', [])
    return render_template('index.html', productos = productos)


#Para el contador  de id
def generar_id():
    if 'productos' in session and len(session['productos']) > 0:
        return max(item['id'] for item in session['productos']) +1
    else:
        return 1



@app.route("/nuevo", methods =['GET','POST'])
def nuevo():
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha = request.form['fecha']
        categoria = request.form['categoria']


        nuevo_producto = {
            'id':generar_id(), 
            'nombre':nombre, 
            'cantidad':cantidad,
            'precio':precio,
            'fecha':fecha,
            'categoria':categoria
        }
        if 'productos' not in session:
            session['productos'] =[]

        session['productos'].append(nuevo_producto)
        session.modified = True
        return redirect(url_for('index'))
    return render_template('nuevo.html')




#EDITAR
@app.route('/editar/<int:id>', methods =['GET', 'POST'])
def editar(id):
    lista_productos = session.get('productos', [])
    producto = next((c for c in lista_productos  if c['id'] == id), None)

    if not producto:
        return redirect(url_for('index'))

    if request.method == 'POST':
        
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha'] = request.form['fecha']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    return render_template('editar.html', producto = producto)



#ELIMINAR
@app.route('/eliminar/<int:id>', methods =['GET', 'POST'])
def eliminar(id):

    lista_productos = session.get('productos', []) #en caso de que no haya una lista vacia 
    producto = next((c for c in lista_productos  if c['id'] == id), None) #iteramos esta lista,  si id == id
    if producto:
        session['productos'].remove(producto)
        session.modified = True
    return redirect(url_for('index'))
    

if __name__ == "__main__":
    app.run(debug = True)
