
import PIL.Image

ascii_chars = r".'`^\",;:Il!i<>~+_-?][}{1()|/tfjrxnvuczXYUJCQ0OZwmqdpbkhwao*#MW&8%B@$"

def resize_image(image, new_width=100):
    w, h = image.size
    h = int(new_width * (h / w * 0.55))
    return image.resize((new_width, h))

def greify(image):
    return image.convert("L")

def pixel_ascii(image):
    pixels = image.getdata()
    chars = ""
    n = len(ascii_chars)
    for p in pixels:
        chars += ascii_chars[p * (n - 1) // 255]
    return chars

def main(new_width=300):
    fundo = input("Fundo light ou dark? ").strip().lower()
    path = input("Caminho da imagem: ").strip()

    try:
        img = PIL.Image.open(path)
    except:
        print("Caminho inválido.")
        return
    
    data = pixel_ascii(greify(resize_image(img, new_width)))
    if fundo == "light":
        data = data[::-1]

    ascii_img = "\n".join(data[i:i+new_width] for i in range(0, len(data), new_width))
    print(ascii_img)

    if input("Salvar em .txt? (s/n): ").strip().lower() == "s":
        nome = input("Nome do arquivo: ").strip() or "ascii_art"
        with open(f"{nome}.txt", "w", encoding="utf-8") as f:
            f.write(ascii_img)
        print(f"Salvo em {nome}.txt")

if __name__ == "__main__":
    main()
