
import pyxel

class CardInfo:
    def __init__(self,num):
        if num <= 9:
            self.suit = 'H'
            self.rank = num - 0*9 + 5
        elif num <= 18:
            self.suit = 'D'
            self.rank = num - 1*9 + 5
        elif num <= 27:
            self.suit = 'C'
            self.rank = num - 2*9 + 5
        else: # num <= 36
            self.suit = 'S'
            self.rank = num - 3*9 + 5   


class Card:
    __ranks = [6,7,8,9,10,11,12,13,14]
    __suits = ['H','D','C','S']
    __colors = {'H': 8, 'D': 10,'C': 11,'S' : 12}

    def __init__(self,suit='H',rank=0,x=0,y=0):
        self.rank = rank
        self.suit = suit
        self.color = self.__colors[suit]
        self.x = x
        self.y = y
        self.w = 10
        self.h = 14
        self.clicked = False
        self.in_hand = True
        self.bg_color = 0
        self.can_move = True

    def in_card(self):
        if (pyxel.mouse_x >= self.x 
            and pyxel.mouse_x <= self.x + self.w
            and pyxel.mouse_y >= self.y
            and pyxel.mouse_y <= self.y + self.h):
            return True
        return False
    
    def draw(self,sq):
        pyxel.rect(sq.x,sq.y,sq.w,sq.h,self.bg_color)
        if self.clicked:
            pyxel.rect(sq.x,sq.y,sq.w,sq.h,self.color)
            pyxel.rect(sq.x+1,sq.y+1,sq.w-2,sq.h-2,0)
        rank_text = str(self.rank)
        if self.rank == 11:
            rank_text = 'J'
        elif self.rank == 12:
            rank_text = 'Q'
        elif self.rank == 13:
            rank_text = 'K'
        elif self.rank == 14:
            rank_text = 'A'
        pyxel.text(sq.x+sq.w/4,sq.y+sq.h/4,rank_text,self.color)


class Square:
    def __init__(self,x=0,y=0,w=10,h=14,margin=1,col=1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.margin = margin
        self.color = col
        self.has_card = False
        self.card = Card()

    def in_square(self):
        if (pyxel.mouse_x >= self.x 
            and pyxel.mouse_x <= self.x + self.w
            and pyxel.mouse_y >= self.y
            and pyxel.mouse_y <= self.y + self.h):
            return True
        return False

    def draw(self):
        pyxel.rect(self.x,self.y,self.w,self.h,self.color)
        pyxel.rect(self.x+self.margin,self.y+self.margin,
                   self.w-2*self.margin,self.h-2*self.margin,13)
        if self.has_card:
            self.card.draw(self)

class PileUpPoker:
    def __init__(self):
        pyxel.init(80,120)
        self.board = []
        self.board.append(Square(24,16))
        num_rows = 4
        num_cols = 4
        r = 0
        while r < num_rows:
            c = 0
            while c < num_cols-1:
                self.board.append(Square(self.board[-1].x+self.board[-1].w+self.board[-1].margin,
                                   self.board[-1].y))
                c += 1
            r += 1
            if r < num_rows:
                self.board.append(Square(self.board[0].x,
                                          self.board[-1].y+self.board[-1].h+self.board[-1].margin))

        self.card_clicked = False
        self.clicked_square = Square()

        self.hand_squares = []
        hand_x = 20
        hand_y = 100
        num_hand_squares = 0
        self.dealt_cards = []
        while num_hand_squares < 5:
            self.hand_squares.append(Square(hand_x,100))
            # self.hand_squares[-1].has_card = True
            while not self.hand_squares[-1].has_card:
                dealt_num = pyxel.rndi(1,36)
                if dealt_num not in self.dealt_cards:
                    self.dealt_cards.append(dealt_num)
                    info = CardInfo(dealt_num)
                    x = self.hand_squares[-1].x
                    y = self.hand_squares[-1].y
                    self.hand_squares[-1].card = Card(info.suit,info.rank,x,y)
                    self.hand_squares[-1].has_card = True

            num_hand_squares += 1
            hand_x += 10
        self.num_in_hand = 5

        self.discard_x = 10
        self.discard_y = 30
        self.discard_squares = []

        self.game_over = False
        self.to_next_hand = False

        self.next_hand_button_x = 25
        self.next_hand_button_y = 80
        self.next_hand_button_w = 41
        self.next_hand_button_h = 13

        self.game_over_x = self.next_hand_button_x
        self.game_over_y = self.next_hand_button_y
        # pyxel.load("card.pyxres")

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def new_hand(self):
        for sq in self.hand_squares:
            while not sq.has_card:
                dealt_num = pyxel.rndi(1,36)
                if dealt_num not in self.dealt_cards:
                    self.dealt_cards.append(dealt_num)
                    info = CardInfo(dealt_num)
                    sq.card = Card(info.suit,info.rank,sq.x,sq.y)
                    sq.has_card = True
        self.num_in_hand = 5
        self.to_next_hand = False

    def update(self):
        if not self.card_clicked:
            for sq in self.board + self.hand_squares:
                clickable_card = sq.has_card and sq.card.can_move
                if sq.in_square() and clickable_card and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    sq.card.clicked = True
                    self.card_clicked = True
                    self.clicked_square = sq
        else:
            for sq in self.board + self.hand_squares:
                clickable_square = not sq.has_card or sq.card.can_move
                if self.clicked_square in self.hand_squares and self.num_in_hand == 1:
                    clickable_square = clickable_square and (sq.has_card or sq in self.hand_squares)
                if sq.in_square() and clickable_square and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    old_sq = self.clicked_square
                    old_card = old_sq.card
                    old_has_card = old_sq.has_card
                    old_sq.card = sq.card
                    old_sq.has_card = sq.has_card
                    sq.card = old_card
                    sq.has_card = old_has_card
                    sq.card.clicked = False
                    self.card_clicked = False
                    self.clicked_square = sq

        num_in_hand = 0
        for sq in self.hand_squares:
            if sq.has_card:
                num_in_hand += 1
        self.num_in_hand = num_in_hand
        if self.num_in_hand == 1:
            if self.to_next_hand:
                for sq in self.board:
                    if sq.has_card:
                        sq.card.can_move = False
                        sq.card.bg_color = 7
                for sq in self.hand_squares:
                    if sq.has_card:
                        card = sq.card
                        self.discard_squares.append(Square(self.discard_x,self.discard_y))
                        self.discard_squares[-1].card = card
                        self.discard_squares[-1].has_card = True
                        self.discard_squares[-1].card.can_move = False
                        self.discard_squares[-1].card.bg_color = 7
                        sq.has_card = False
                        # card.in_hand = False
                        # card.x = self.discard_x
                        # card.y = self.discard_y
                        self.discard_y += sq.h+1
                        # self.num_in_hand -= 1
                    # card.bg_color = 7 # 0
                    # card.can_move = False
                if len(self.dealt_cards) < 20:
                    self.new_hand()
                else:
                    self.game_over = True
            else:
                next_button = (pyxel.mouse_x >= self.next_hand_button_x
                    and pyxel.mouse_x <= self.next_hand_button_x + self.next_hand_button_w
                    and pyxel.mouse_y >= self.next_hand_button_y
                    and pyxel.mouse_y <= self.next_hand_button_y + self.next_hand_button_h)
                if next_button and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.to_next_hand = True

    def draw(self):
        pyxel.cls(0)

        for sq in self.board + self.hand_squares + self.discard_squares:
            sq.draw()

        if self.num_in_hand == 1:
            next_hand_color = 7
        else:
            next_hand_color = 1
        pyxel.rect(self.next_hand_button_x,
                    self.next_hand_button_y,
                    self.next_hand_button_w,
                    self.next_hand_button_h,
                    next_hand_color)
        pyxel.rect(self.next_hand_button_x+1,
                    self.next_hand_button_y+1,
                    self.next_hand_button_w-2,
                    self.next_hand_button_h-2,
                    0)
        pyxel.text(self.next_hand_button_x+1,self.next_hand_button_y+1,
                    'ADVANCE TO \nNEXT HAND',next_hand_color)
        if self.game_over:
            pyxel.text(self.game_over_x,self.game_over_y,'GAME OVER',7)
        # pyxel.blt(0,0,pyxel.images[0],2,34,22-2+1,64-34+1)

PileUpPoker()