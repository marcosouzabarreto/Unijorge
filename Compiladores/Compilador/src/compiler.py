import language
while True:
    text = input(">_ ")
    result, error = language.run(text)

    if error:
        print(error.create_error_message())
    else:
        print(result)
