from flask import Flask, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
from pathlib import Path
import os
import ast
import psutil
import platform


with open('ApiData.json', 'r', encoding='utf-8') as data:
    api_key = json.loads(data.read())["api_key"] # XXX.XXX.XXX
app = Flask(__name__)
KeyHash = generate_password_hash(api_key)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,  
    SESSION_COOKIE_SAMESITE='Lax'
)

# Página inicial
@app.route('/')
def home():
    return '404'

# Dados
@app.route('/<string:key>')
def data(key:str):
    if not check_password_hash(KeyHash, key):
        return '404'

    return jsonify({
        "sistema": platform.system(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_total": round(psutil.virtual_memory().total / 1024**2, 2),  # MB
        "ram_usada": round(psutil.virtual_memory().used / 1024**2, 2),
        "ram_percent": psutil.virtual_memory().percent,
        "disco_total": round(psutil.disk_usage('/').total / 1024**3, 2),  # GB
        "disco_usado": round(psutil.disk_usage('/').used / 1024**3, 2),
    })
    
# Abrir Json
@app.route('/<string:key>/Json/<string:name>')
def Json(key:str, name:str):
    if not check_password_hash(KeyHash, key):
        return '404'
    try:
        name = name.replace('>', '\\')
        if Path(f'{name}.json').exists() :
            with open(f'{name}.json', 'r', encoding='utf-8') as Json:
                return jsonify(json.loads(Json.read()))
        else:
            Json = Path(f'{name}.json')
            Json.touch(exist_ok=True)
            Json.write_text('{}', 'utf-8')
            return Json.name
    except Exception as e:
        print(f'[ERRO] Json/404 ({e})')
        return f'404 ({e})'
    
# Definir Json
@app.route('/<string:key>/SetJson/<string:name>/<string:Dict>')
def SetJson(key:str, name:str, Dict:dict):
    if not check_password_hash(KeyHash, key):
        return '404'
    
    try:
        name = name.replace('>', '\\')
        if Path(f'{name}.json').exists() :
            with open(f'{name}.json', 'w', encoding='utf-8') as Json:
                try:
                    Dict = json.loads(Dict)
                    Format = json.dumps(Dict, indent=4, sort_keys=True, ensure_ascii=False)
                    Json.write(Format)
                    return jsonify({'veri' : True})
                except:
                    return 'Erro'
        else:
            Json = Path(f'{name}.json')
            Json.touch(exist_ok=True)
            Dict = json.loads(Dict)
            Format = json.dumps(Dict, indent=4, sort_keys=True, ensure_ascii=False)
            Json.write_text(Format, 'utf-8')
            return Json.name
    except Exception as e:
        print(f'[ERRO] setJson/404 ({e})')
        return f'404 ({e})'

# Adicionar elemento
@app.route('/<string:key>/AddJson/<string:name>/<string:name_obj>/<string:value_obj>/<string:Type>')
def AddJson(key:str, name:str, name_obj:str, value_obj:str, Type:str):
    if not check_password_hash(KeyHash, key):
        return '404'
    
    try:
        name = name.replace('>', '\\')
        if Path(f'{name}.json').exists() :
            with open(f'{name}.json', 'r', encoding='utf-8') as Json:
                try:
                    Dict = json.loads(Json.read())
                    if Type == 'str':
                        Dict[name_obj] = (value_obj)
                    elif Type == 'int':
                        Dict[name_obj] = int(value_obj)
                    elif Type == 'float':
                        Dict[name_obj] = float(value_obj)
                    elif Type == 'data':
                        Dict[name_obj] = ast.literal_eval(value_obj)
                    Format = json.dumps(Dict, indent=4, sort_keys=True, ensure_ascii=False)
                    with open(f'{name}.json', 'w', encoding='utf-8') as Json:
                        Json.write(Format)
                    return jsonify({'veri' : True})
                except:
                    return 'Erro'
        else:
            Json = Path(f'{name}.json')
            Json.touch(exist_ok=True)
            Dict = json.loads(Dict)
            Format = json.dumps(Dict, indent=4, sort_keys=True, ensure_ascii=False)
            Json.write_text(Format, 'utf-8')
            return Json.name
    except Exception as e:
        print(f'[ERRO] AddJson/404 ({e})')
        return f'404 ({e})'

# Pegar um Objeto em especifico
@app.route('/<string:key>/GetObjectJson/<string:name>/<string:Object>')
def GetObject(key:str, name:str, Object:str):
    if not check_password_hash(KeyHash, key):
        return '404'
    try:
        name = name.replace('>', '\\')
        if Path(f'{name}.json').exists() :
            with open(f'{name}.json', 'r', encoding='utf-8') as Json:
                data = json.loads(Json.read())
                Object = data[Object]
                if isinstance(Object, (list, dict)):
                    return jsonify(Object)
                else:
                    return Object
        else:
            Json = Path(f'{name}.json')
            Json.touch(exist_ok=True)
            Json.write_text('{}', 'utf-8')
            return Json.name
    except Exception as e:
        print(f'[ERRO] GetObjectJson/404 ({e})')
        return f'404 ({e})'

# Base
@app.route('/<string:key>/Base/<string:name>')
def Base(key:str, name:str):
    if not check_password_hash(KeyHash, key):
        return '404'
    try:
        name = name.replace('>', '\\')
        base = Path(f'{name}')
        base.mkdir(exist_ok=True)
        return jsonify({'veri' : True})
    except Exception as e:
        print(f'[ERRO] Base/404 ({e})')
        return f'404 ({e})'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

