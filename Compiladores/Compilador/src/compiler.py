import language

while True:
    text = ">_"
    result, error = language.run(text)

    if error:
        text = "Arrombado"
        print(text)
        break
    else:
        text = result
        print(text)
