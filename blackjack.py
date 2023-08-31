import random
import sys

HEARTS = chr(9829)  # Символ 9829 — '♥'
DIAMONDS = chr(9830)  # Символ 9830 — '♦'
SPADES = chr(9824)  # Символ 9824 — '♠'
CLUBS = chr(9827)  # Символ 9827 — '♣'

BACKSIDE = 'backside'


def main():
    print('''Blackjack, by Al Sweigart al@inventwithpython.com
          Rules: Try to get as close to 21 without going over. Kings, Queens,
          and Jacks are worth 10 points. Aces are worth 1 or 11 points.
          Cards 2 through 10 are worth their face value. (H)it to take another
          card. (S)tand to stop taking cards. On your first play, you can
          (D)ouble down to increase your bet but must hit exactly one more
          time before standing. In case of a tie, the bet is returned to the
          player. The dealer stops hitting at 17.''')

    money = 5000

    # основной цикл игры
    while True:
        if money <= 0:
            print("You're broke!")
            print("Gosh thing you weren't playing with real money. LOL!!")
            print('Thanks for playing!')
            sys.exit()

        # Даем возможность игроку сделать ставку на раунд:
        print('Money:', money)
        bet = getBet(money)

        # Сдаем дилеру и игроку по две карты из колоды:
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # обработка действий игрока
        print('Bet:', bet)
        # Выполняем цикл до тех пор, пока игрок не скажет "хватит"
        # или у него не будет перебор
        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            # проверка на перебор у игрока
            if getHandValue(playerHand) > 21:
                break

            # получаем ход игрока: H, S, или D:
            move = getMove(playerHand, money - bet)

            # обработка действий игрока
            if move == 'D':
                # игрок удваивает, он может увеличить ставку:
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print('Bet increased to {}.'.format(bet))
                print('Bet:', bet)

            if move in ('H', 'D'):
                # "Еще" или "удваиваю": игрок берет еще одну карту.
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew a {} of {}.'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    continue  # перебор у игрока

            if move in ('S', 'D'):
                # "Хватит" или "удваиваю": переход хода к следующему игроку
                break

        # Обработка действий дилера:
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                # дилер берет еще карту:
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break  # Перебор у дилера
                input('Press Enter to continue...')
                print('\n\n')

        # отображает итоговые карты на руках:
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        # Проверяем, игрок выиграл, проиграл или сыграл вничью:
        if dealerValue > 21:
            print('Dealer busts! You win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif playerValue > dealerValue:
            print('You won ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('It\'s a tie, the bet is returned to you.')

        input('Press Enter to continue...')
        print('\n\n')


# Спрашиваем у игрока, сколько он ставит на этот раунд
def getBet(maxBet):
    #  Продолжаем спрашивать, пока не будет введено допустимое значение
    while True:
        print('How much do you bet? (1-{}, or QUIT)'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit

        if not bet.isdecimal():
            continue  # Если игрок не ответил — спрашиваем снова

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet  # Игрок ввел допустимое значение ставки


# Возвращаем список кортежей (номинал, масть) для всех 52 карт
def getDeck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))  # Добавляем числовые карты
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))  # Добавляем фигурные карты и тузы
    random.shuffle(deck)
    return deck


# Отображаем карты игрока и дилера. Скрываем первую карту дилера,
# если showDealerHand равно False
def displayHands(playerHand, dealerHand, showDealerHand):
    print()
    if showDealerHand:
        print('DEALER:', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        # Скрываем первую карту дилера:
        displayCards([BACKSIDE] + dealerHand[1:])

    # отображаем карты игрока:
    print('PLAYER:', getHandValue(playerHand))
    displayCards(playerHand)


# Возвращаем стоимость карт. Фигурные карты стоят 10, тузы — 11
# или 1 очко (эта функция выбирает подходящую стоимость карты)
def getHandValue(cards):
    value = 0
    numberOfAces = 0

    # добавляем стоимость карты - не туза:
    for card in cards:
        rank = card[0]  # карта представляет собой кортеж (номинал, масть)
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):  # Фигурные карты стоят 10 очков
            value += 10
        else:
            value += int(rank)  # стоимость числовых карт равна их номиналу

    # добавляем стоимость для тузов:
    value += numberOfAces  # Добавляем 1 для каждого туза
    for i in range(numberOfAces):
        #  Если можно добавить еще 10 с перебором, добавляем:
        if value + 10 <= 21:
            value += 10

    return value


# отображаем все карты из списка карт
def displayCards(cards):
    rows = ['', '', '', '', '']  # Отображаемый в каждой строке текст

    for i, card in enumerate(cards):
        rows[0] += ' ___  '  # Выводим верхнюю строку карты
        if card == BACKSIDE:
            # Выводим рубашку карты:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Выводим лицевую сторону карты:
            rank, suit = card  # Карта — структура данных типа кортеж.
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    # выводим все строки на экран
    for row in rows:
        print(row)

# Спрашиваем, какой ход хочет сделать игрок, и возвращаем 'H', если он
# хочет взять еще карту, 'S', если ему хватит, и 'D', если он удваивает


def getMove(playerHand, money):
    # Продолжаем итерации цикла, пока игрок не сделает допустимый ход
    while True:
        # Определяем, какие ходы может сделать игрок:
        moves = ['(H)it', '(S)tand']

        # Игрок может удвоить при первом ходе, это ясно из того,
        # что у игрока ровно две карты:
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        # получаем ход игрока
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move  # Игрок сделал допустимый ход.
        if move == 'D' and '(D)ouble down' in moves:
            return move  # Игрок сделал допустимый ход


 # Если программа не импортируется, а запускается, производим запуск:
if __name__ == '__main__':
    main()
