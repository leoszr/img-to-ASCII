# img-to-ascii

Conversor de imagens para arte ASCII via linha de comando. Suporta ajuste de largura, inversão de cores, detecção automática de resolução e saída para arquivo.

## Tecnologias

- Python 3
- Pillow (PIL)

## Pré-requisitos

- Python 3.10+

## Instalação

1. Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como usar

### Modo CLI (recomendado)

```bash
python main.py -i caminho/para/imagem.jpg
```

### Opções disponíveis

| Flag               | Descrição                                       | Padrão |
| ------------------ | ----------------------------------------------- | ------ |
| `-i`, `--input`    | Caminho para a imagem de entrada (obrigatório)  | —      |
| `-w`, `--width`    | Largura da saída em caracteres                  | `120`  |
| `-o`, `--output`   | Salvar resultado em arquivo de texto            | —      |
| `-inv`, `--invert` | Inverter a intensidade (para fundos claros)     | off    |
| `--auto`           | Detectar largura automaticamente pela resolução | off    |
| `--fastfetch`      | Modo rápido com largura 50 (preview)            | off    |

### Exemplos

```bash
# Conversão básica (saída no terminal)
python main.py -i foto.jpg

# Largura personalizada
python main.py -i foto.jpg -w 80

# Detectar largura automaticamente
python main.py -i foto.jpg --auto

# Fundo claro (invertido)
python main.py -i foto.jpg --invert

# Salvar em arquivo
python main.py -i foto.jpg -o arte.txt

# Preview rápido
python main.py -i foto.jpg --fastfetch
```

### Modo interativo (legado)

Execute sem argumentos para o modo interativo:

```bash
python main.py
```

Responda as perguntas sobre o fundo (light/dark) e o caminho da imagem.

## Como funciona

1. A imagem é carregada e redimensionada para a largura especificada
2. Um fator de `0.55` corrige a proporção dos caracteres no terminal
3. A imagem é convertida para escala de cinza
4. Cada pixel é mapeado para um caractere ASCII de acordo com seu brilho

## Formatos suportados

Todos os formatos suportados pelo Pillow: JPEG, PNG, BMP, GIF, WEBP, entre outros.
