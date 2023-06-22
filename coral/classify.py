from pathlib import Path
from PIL import Image
from pycoral.adapters import common
from pycoral.adapters import classify
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.dataset import read_label_file

import shutil

def copiar_archivo(ruta_archivo, ruta_destino):
    try:
        shutil.copy2(ruta_archivo, ruta_destino)
        print("Copia del archivo creada exitosamente.")
    except IOError as e:
        print(f"Error al copiar el archivo: {e}")


script_dir = Path(__file__).parent.resolve()

model_file = script_dir/'models/astropi-day-vs-nite.tflite' # name of model
data_dir = script_dir/'data'
label_file = data_dir/'day-vs-night.txt' # Name of your label file
for i in range(2,517): 
    image_file = (f"{data_dir/'tests'}/imagenoir%s.jpg" %i) # Name of image for classification
    
    ruta_archivo_original = (f"{data_dir/'tests'}/imagenoir%s.jpg" %i)
    ruta_destino_copia = data_dir/'day_coral'
    
    interpreter = make_interpreter(f"{model_file}")
    interpreter.allocate_tensors()

    size = common.input_size(interpreter)
    image = Image.open(image_file).convert('RGB').resize(size, Image.ANTIALIAS)

    common.set_input(interpreter, image)
    interpreter.invoke()
    classes = classify.get_classes(interpreter, top_k=1)

    labels = read_label_file(label_file)
    for c in classes:
        #print(f"hola%s"%i)
        print(f'imagenoir%s {labels.get(c.id, c.id)} {c.score:.5f}' %i)
        if labels.get(c.id, c.id) == 'day':
            copiar_archivo(ruta_archivo_original, ruta_destino_copia)