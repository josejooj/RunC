import io, json

def salvarJson(data, caminho='data.json'):
    with io.open(caminho, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def pegarJson(caminho='data.json'):
    with io.open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)
        