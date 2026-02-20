def choose_move(mesa_de_jogo):
    moves = mesa_de_jogo.available_actions()
    selected_move = ''
    print('Movimentos possíveis:')
    print(moves)
    while(selected_move not in moves):
        selected_move = input('Movimento: ')
    return selected_move