from PIL import Image, ImageDraw

image = Image.new("RGB", (800, 500), "white")

draw = ImageDraw.Draw(image)

draw.rectangle(
    (200, 100, 600, 400),
    fill="blue"
)

draw.text(
    (400, 220),
    "TEST IMAGE",
    fill="white",
    anchor="mm"
)

draw.text(
    (400, 280),
    "PDF Alchemy",
    fill="white",
    anchor="mm"
)

image.save("./tests/assets/test.png")

print("Imagen creada: ./tests/assets/test.png")
