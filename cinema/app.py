from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        return render_template('index.html',nombre=session['nombre'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Usuario WHERE email = %s", [email])
        usuario = cur.fetchone()
        if usuario and bcrypt.check_password_hash(usuario[3], password):
            session['loggedin'] = True
            session['id'] = usuario[0]
            session['nombre'] = usuario[1]
            return redirect(url_for('index'))
        else:
            flash('Login incorrecto. Por favor, intenta de nuevo.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Usuario (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password))
        mysql.connection.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('nombre', None)
    return redirect(url_for('login'))



@app.route('/usuarios')
def usuarios():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Usuario')
        usuarios = cur.fetchall()
        return render_template('usuarios.html', usuarios=usuarios)
    return redirect(url_for('login'))

@app.route('/edit_usuario/<int:id>', methods=['GET', 'POST'])
def edit_usuario(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            nombre = request.form['nombre']
            email = request.form['email']
            password = request.form['password']
            if password:  # Si se proporciona una nueva contraseña, hashearla
                password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                cur.execute("UPDATE Usuario SET nombre=%s, email=%s, password=%s WHERE id=%s", (nombre, email, password_hash, id))
            else:  # Si no se proporciona una nueva contraseña, no actualizar el campo password
                cur.execute("UPDATE Usuario SET nombre=%s, email=%s WHERE id=%s", (nombre, email, id))
            mysql.connection.commit()
            return redirect(url_for('usuarios'))
        cur.execute("SELECT * FROM Usuario WHERE id=%s", [id])
        usuario = cur.fetchone()
        return render_template('edit_usuario.html', usuario=usuario)
    return redirect(url_for('login'))

@app.route('/delete_usuario/<int:id>', methods=['GET', 'POST'])
def delete_usuario(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Usuario WHERE id=%s", [id])
        mysql.connection.commit()
        return redirect(url_for('usuarios'))
    return redirect(url_for('login'))


# CRUD para Películas

@app.route('/peliculas')
def peliculas():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Pelicula')
        peliculas = cur.fetchall()
        return render_template('peliculas.html', peliculas=peliculas)
    return redirect(url_for('login'))

@app.route('/add_pelicula', methods=['POST'])
def add_pelicula():
    if 'loggedin' in session:
        if request.method == 'POST':
            titulo = request.form['titulo']
            duracion = request.form['duracion']
            clasificacion = request.form['clasificacion']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Pelicula (titulo, duracion, clasificacion) VALUES (%s, %s, %s)", (titulo, duracion, clasificacion))
            mysql.connection.commit()
            return redirect(url_for('peliculas'))
    return redirect(url_for('login'))

@app.route('/edit_pelicula/<int:id>', methods=['GET', 'POST'])
def edit_pelicula(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            titulo = request.form['titulo']
            duracion = request.form['duracion']
            clasificacion = request.form['clasificacion']
            cur.execute("UPDATE Pelicula SET titulo=%s, duracion=%s, clasificacion=%s WHERE id=%s", (titulo, duracion, clasificacion, id))
            mysql.connection.commit()
            return redirect(url_for('peliculas'))
        cur.execute("SELECT * FROM Pelicula WHERE id=%s", [id])
        pelicula = cur.fetchone()
        return render_template('edit_pelicula.html', pelicula=pelicula)
    return redirect(url_for('login'))

@app.route('/delete_pelicula/<int:id>', methods=['GET', 'POST'])
def delete_pelicula(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Pelicula WHERE id=%s", [id])
        mysql.connection.commit()
        return redirect(url_for('peliculas'))
    return redirect(url_for('login'))

# CRUD para Salas
@app.route('/salas')
def salas():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM Sala')
        salas = cur.fetchall()
        return render_template('salas.html', salas=salas)
    return redirect(url_for('login'))

@app.route('/add_sala', methods=['POST'])
def add_sala():
    if 'loggedin' in session:
        if request.method == 'POST':
            nombre = request.form['nombre']
            capacidad = request.form['capacidad']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Sala (nombre, capacidad) VALUES (%s, %s)", (nombre, capacidad))
            mysql.connection.commit()
            return redirect(url_for('salas'))
    return redirect(url_for('login'))

@app.route('/edit_sala/<int:id>', methods=['GET', 'POST'])
def edit_sala(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            nombre = request.form['nombre']
            capacidad = request.form['capacidad']
            cur.execute("UPDATE Sala SET nombre=%s, capacidad=%s WHERE id=%s", (nombre, capacidad, id))
            mysql.connection.commit()
            return redirect(url_for('salas'))
        cur.execute("SELECT * FROM Sala WHERE id=%s", [id])
        sala = cur.fetchone()
        return render_template('edit_sala.html', sala=sala)
    return redirect(url_for('login'))

@app.route('/delete_sala/<int:id>', methods=['GET', 'POST'])
def delete_sala(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Sala WHERE id=%s", [id])
        mysql.connection.commit()
        return redirect(url_for('salas'))
    return redirect(url_for('login'))

# CRUD para Reservas
@app.route('/reservas')
def reservas():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT r.id, u.nombre, p.titulo, s.nombre, r.asientos, r.fecha, r.hora FROM Reserva r JOIN Usuario u ON r.usuario_id = u.id JOIN Pelicula p ON r.pelicula_id = p.id JOIN Sala s ON r.sala_id = s.id')
        reservas = cur.fetchall()
        return render_template('reservas.html', reservas=reservas)
    return redirect(url_for('login'))

@app.route('/add_reserva', methods=['POST'])
def add_reserva():
    if 'loggedin' in session:
        if request.method == 'POST':
            id_usuario = request.form['id_usuario']
            id_pelicula = request.form['id_pelicula']
            id_sala = request.form['id_sala']
            asientos = request.form['asientos']
            fecha = request.form['fecha']
            hora = request.form['hora']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Reserva (usuario_id, pelicula_id, sala_id, asientos, fecha, hora) VALUES (%s, %s, %s, %s, %s, %s)", 
                    (id_usuario, id_pelicula, id_sala, asientos, fecha, hora))
            mysql.connection.commit()
            return redirect(url_for('reservas'))
    return redirect(url_for('add_reserva.html'))

@app.route('/edit_reserva/<int:id>', methods=['GET', 'POST'])
def edit_reserva(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            id_usuario = request.form['id_usuario']
            id_pelicula = request.form['id_pelicula']
            id_sala = request.form['id_sala']
            asientos = request.form['asientos']
            fecha = request.form['fecha']
            hora = request.form['hora']
            cur.execute("UPDATE Reserva SET usuario_id=%s, pelicula_id=%s, sala_id=%s, asientos=%s, fecha=%s, hora=%s WHERE id=%s",
                         (id_usuario, id_pelicula, id_sala, asientos, fecha, hora, id))
            mysql.connection.commit()
            return redirect(url_for('reservas'))
        cur.execute("SELECT * FROM Reserva WHERE id=%s", [id])
        reserva = cur.fetchone()
        return render_template('edit_reserva.html', reserva=reserva)
    return redirect(url_for('login'))

@app.route('/delete_reserva/<int:id>', methods=['GET', 'POST'])
def delete_reserva(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Reserva WHERE id=%s", [id])
        mysql.connection.commit()
        return redirect(url_for('reservas'))
    return redirect(url_for('login'))

@app.route("/cine_magia")
def cine_magia():
    return render_template('cine_magia.html')

if __name__ == '__main__':
    app.run(debug=True)
