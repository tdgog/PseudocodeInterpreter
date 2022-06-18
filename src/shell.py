import utils.lexer as u_lexer

while True:
    text = input(f'λ ')
    result, error = u_lexer.run(f'λ', text)

    if error: 
        print(error.as_string())
    else:
        print(result)
