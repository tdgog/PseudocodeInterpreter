import pseudocode

while True:
    text = input(f'λ ')
    result, error = pseudocode.run(f'λ', text)

    if error: 
        print(error.as_string())
    else:
        print(result)
