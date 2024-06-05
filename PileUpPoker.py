
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
        self.h = 10
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
    
    def draw(self):
        pyxel.rect(self.x,self.y,self.w,self.h,self.bg_color)
        if self.clicked:
            pyxel.rect(self.x,self.y,self.w,self.h,self.color)
            pyxel.rect(self.x+1,self.y+1,self.w-2,self.h-2,0)
        rank_text = str(self.rank)
        if self.rank == 11:
            rank_text = 'J'
        elif self.rank == 12:
            rank_text = 'Q'
        elif self.rank == 13:
            rank_text = 'K'
        elif self.rank == 14:
            rank_text = 'A'
        pyxel.text(self.x+self.w/4,self.y+self.h/4,rank_text,self.color)


class Square:
    def __init__(self,x=0,y=0,w=10,h=10,margin=1,col=1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.margin = margin
        self.color = col

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
                   self.w-2*self.margin,self.h-2*self.margin,7)

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

        self.cards = []
        
        self.dealt_cards = []
        hand_x = 20
        while len(self.dealt_cards) < 5:
            dealt_num = pyxel.rndi(1,36)
            if dealt_num not in self.dealt_cards:
                self.dealt_cards.append(dealt_num)
                info = CardInfo(dealt_num)
                self.cards.append(Card(info.suit,info.rank,hand_x,100))
                hand_x += 10
        self.num_in_hand = 5
        self.discard_x = 10
        self.discard_y = 30

        self.game_over = False
        # pyxel.load("card.pyxres")

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def new_hand(self):
        hand_x = 20
        new_num_in_hand = 0
        while new_num_in_hand < 5:
            dealt_num = pyxel.rndi(1,36)
            if dealt_num not in self.dealt_cards:
                self.dealt_cards.append(dealt_num)
                info = CardInfo(dealt_num)
                self.cards.append(Card(info.suit,info.rank,hand_x,100))
                hand_x += 10
                new_num_in_hand += 1
        self.num_in_hand = 5

    def update(self):
        for sq in self.board:
            if self.card_clicked and sq.in_square() and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                for card in self.cards:
                    if card.clicked:
                        card.x = sq.x
                        card.y = sq.y
                        card.bg_color = 13
                        card.clicked = False
                        if card.in_hand:
                            card.in_hand = False
                            self.num_in_hand -= 1
                        self.card_clicked = False
                        return
        
        for card in self.cards:
            if card.can_move and not self.card_clicked and card.in_card() and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                card.clicked = True
                self.card_clicked = True
        if self.num_in_hand == 1:
            for card in self.cards:
                if card.in_hand:
                    card.in_hand = False
                    card.x = self.discard_x
                    card.y = self.discard_y
                    self.discard_y += 10
                    self.num_in_hand -= 1
                card.bg_color = 0
                card.can_move = False
            if len(self.dealt_cards) < 20:
                self.new_hand()
            else:
                self.game_over = True

            


    def draw(self):
        pyxel.cls(0)

        for sq in self.board:
            sq.draw()

        for card in self.cards:
            card.draw()

        if self.game_over:
            pyxel.text(20,100,'GAME OVER',7)
        # pyxel.blt(0,0,pyxel.images[0],2,34,22-2+1,64-34+1)

PileUpPoker()