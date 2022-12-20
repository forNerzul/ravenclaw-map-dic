from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import folium

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Creando los modelos para la base de datos
class EntidadFinanciera (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    pagina = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    def __init__(self, nombre, categoria, pagina, contacto, lat, lon):
        self.nombre = nombre
        self.categoria = categoria
        self.pagina = pagina
        self.contacto = contacto
        self.lat = lat
        self.lon = lon

@app.route('/agregar-marcadores', methods=['GET', 'POST'])
def agregar_marcadores ():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        pagina = request.form['pagina']
        contacto = request.form['contacto']
        lat = request.form['lat']
        lon = request.form['lon']

        entidad_financiera = EntidadFinanciera(nombre=nombre, categoria=categoria, pagina=pagina, contacto=contacto, lat=lat, lon=lon)
        db.session.add(entidad_financiera)
        db.session.commit()

        return redirect(url_for('mapa'))
    return render_template('agregar_marcadores.html')

@app.route('/mapa')
def mapa ():
    coordenadas_inicio = [-25.30234132846098, -57.58115713076387] 
    mapa = folium.Map(location=coordenadas_inicio, zoom_start=20) # creamos el mapa pasandole las coordenadas y el nivel de zoom y guardamos en la variable mapa

    ubicaciones = EntidadFinanciera.query.all() # obtenemos todas las ubicaciones de la base de datos
    
    tarjeta = """<h1>Hola</h1>"""

    for ubicacion in ubicaciones:
        folium.Marker([ubicacion.lat, ubicacion.lon], popup=tarjeta, tooltip=ubicacion.categoria).add_to(mapa)
    
    """ coor_marcador_1 = [-25.30228494972107, -57.58155946210697]
    tooltip = "Hola mundo"
    folium.Marker(coor_marcador_1, popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip).add_to(mapa) """

    return mapa._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
    with app.app_context():
        db.create_all(bind_key='__all__')