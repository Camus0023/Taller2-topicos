from flask import Flask, jsonify, render_template
import random, socket, os
import boto3

from .models import pokeneas

app = Flask(__name__)
s3 = boto3.client('s3')
BUCKET = os.environ['S3_BUCKET']
REGION = os.environ.get('AWS_DEFAULT_REGION')

def get_container_id():
    return socket.gethostname()

@app.route('/api/pokenea')
def random_json():
    p = random.choice(pokeneas)
    return jsonify({
        "id": p["id"],
        "nombre": p["nombre"],
        "altura": p["altura"],
        "habilidad": p["habilidad"],
        "container_id": get_container_id()
    })

#@app.route('/pokenea')
#def random_html():
    p = random.choice(pokeneas)
    # URL pública directa: https://bucket.s3-region.amazonaws.com/key
    url = f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{p['imagen_key']}"
    return render_template('pokenea.html',
                           imagen_url=url,
                           frase=p['frase'],
                           container_id=get_container_id())

@app.route('/pokenea')
def random_html():
    # 1. Listar todos los objetos en el bucket
    resp = s3.list_objects_v2(Bucket=BUCKET)
    contents = resp.get("Contents", [])
    if not contents:
        return "No hay imágenes en el bucket", 404

    # 2. Elegir una key al azar
    key = random.choice([obj["Key"] for obj in contents])

    # 3. Construir la URL pública
    url = f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{key}"

    # 4. (Opcional) buscar en tu lista la frase que corresponda a esa imagen
    match = next((x for x in pokeneas if x["imagen_key"] == key), None)
    frase = match["frase"] if match else ""
    print(f"Imagen elegida: {key}")
    print(f"Frase elegida: {frase}")
    print(f"URL: {url}")
    # 5. (Opcional) Imprimir el ID del contenedor   

    # 5. Renderizar
    return render_template(
        'pokenea.html',
        imagen_url=url,
        frase=frase,
        container_id=get_container_id()
    )