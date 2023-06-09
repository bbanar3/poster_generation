from reportlab.pdfgen.canvas import Canvas

canvas = Canvas("hello.pdf")

canvas.drawString(72, 72, "Hello, World!")

canvas.save()