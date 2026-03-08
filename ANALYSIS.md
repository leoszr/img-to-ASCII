# Análise do Projeto img-to-ascii

## O que o projeto faz
Conversor de imagens para arte ASCII em Python usando Pillow.

## Como funciona (main.py)
- `resize_image()`: redimensiona imagem para largura especificada (fator 0.55 para compensar proporção de caracteres)
- `greify()`: converte para escala de cinza
- `pixel_ascii()`: mapeia cada pixel para caractere ASCII baseado na intensidade

## O que melhorar
1. **Redimensionamento**: parâmetro `new_width` hardcoded (padrão 300) - deveria ser input do usuário
2. **Resolução fixa**: usuário não controla a quantidade de pixels/caracteres de saída
3. **Sem tratamento de erros**: except genérico sem logging
4. **Código monolítico**: tudo em um arquivo, sem estrutura
5. **Sem CLI**: execução interativa apenas, sem argparse
6. **Caracteres ASCII**: string fixa, poderia ser customizável

## Como diminuir pixels na imagem
Para reduzir a quantidade de pixels (caracteres ASCII na saída), altere o valor de `new_width` na chamada `main(new_width=300)`:
- `main(100)` = 100 caracteres de largura
- `main(50)` = 50 caracteres de largura

O código atual já suporta isso via parâmetro, mas não expõe essa opção ao usuário.
