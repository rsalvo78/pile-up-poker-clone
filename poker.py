
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
        self.clicked = False
        self.in_hand = True
        self.bg_color = 7
        self.can_move = True

    def rank_text(self):
        rank_text = ''
        if self.rank <= 10:
            rank_text = str(self.rank)
        elif self.rank == 11:
            rank_text = 'J'
        elif self.rank == 12:
            rank_text = 'Q'
        elif self.rank == 13:
            rank_text = 'K'
        elif self.rank == 14:
            rank_text = 'A'
        return rank_text 
    
    def draw(self,sq,hasBorder=False):
        if self.clicked:
            shift_height = 0.2*sq.h
        else:
            shift_height = 0
        if hasBorder:
            pyxel.rect(sq.x,sq.y,sq.w,sq.h,self.color)
            pyxel.rect(sq.x+1,sq.y-shift_height+1,sq.w-2,sq.h-2,self.bg_color)
        else:
            pyxel.rect(sq.x,sq.y-shift_height,sq.w,sq.h,self.bg_color)
        rank_text = self.rank_text()
        pyxel.text(sq.x+sq.w/4,sq.y+sq.h/4-shift_height,rank_text,self.color)

class Square:
    def __init__(self,x=0,y=0,w=20,h=28,margin=1,col=1):
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
                   self.w-2*self.margin,self.h-2*self.margin,1)
        if self.has_card:
            self.card.draw(self)

class PileUpPoker:
    def __init__(self):
        pixel_scale = 20
        phone_width = 9
        phone_height = 19.5
        pyxel.init(int(pixel_scale*phone_width),int(pixel_scale*phone_height))
        self.board = []
        self.card_clicked = False
        self.clicked_square = Square()
        self.hand_squares = []
        self.num_in_hand = 5
        self.score = {}

        self.discard_x = 0.1*pyxel.width
        self.discard_y = 0.3*pyxel.height
        self.discard_squares = []

        self.game_over = False
        self.to_next_hand = False

        self.next_hand_button_w = 57
        self.next_hand_button_h = 13
        self.next_hand_button_x = 0.5*pyxel.width - self.next_hand_button_w/2
        self.next_hand_button_y = 0.85*pyxel.height - self.next_hand_button_h/2

        self.final_score_w = 93
        self.final_score_h = 26
        self.final_score_x = 0.5*pyxel.width - self.final_score_w/2
        self.final_score_y = 0.15*pyxel.height - self.final_score_h/2

        self.game_over_x = self.next_hand_button_x
        self.game_over_y = self.next_hand_button_y

        self.new_game()

        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def new_game(self):
        self.board = []
        self.card_clicked = False
        self.clicked_square = Square()
        self.score = {}

        square_width = self.clicked_square.w
        square_height = self.clicked_square.h
        square_margin = self.clicked_square.margin
        num_rows = 4
        num_cols = 4

        board_width = square_margin*(num_rows-1) + square_width*num_rows
        board_height = square_margin*(num_cols-1) + square_height*num_cols
        self.board.append(Square(0.5*pyxel.width - board_width/2,0.5*pyxel.height - board_height/2))

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

        self.hand_squares = []
        hand_width = square_margin*(5-1) + square_width*5
        hand_height = square_height
        hand_x = 0.5*pyxel.width - hand_width/2
        hand_y = pyxel.height - hand_height
        num_hand_squares = 0
        self.dealt_cards = []
        while num_hand_squares < 5:
            self.hand_squares.append(Square(hand_x,hand_y))
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
            hand_x += self.hand_squares[-1].w + 1

        self.num_in_hand = 5

        self.discard_squares = []

        self.game_over = False
        self.to_next_hand = False

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

    def hand_score(self,hand):
        ranks = []
        suits = []
        for sq in hand:
            card = sq.card
            if sq.has_card:
                ranks.append(card.rank)
                suits.append(card.suit)
        ranks.sort()
        suits.sort()
        
        if len(ranks) == 4:
            isFourOfAKind = all(ii == ranks[0] for ii in ranks)
            isFlush = all(ii == suits[0] for ii in suits)
            isStraight = all(ranks[ii]+1 == ranks[ii+1] for ii in range(len(ranks)-1))
            isStraightFlush = isFlush and isStraight
            if isStraightFlush:
                return ('staight\nflush',450)
            elif isFourOfAKind:
                return ('4 of\na kind',325)
            elif isStraight:
                return ('straight',180)
            elif isFlush:
                return ('flush',80)
            else:
                ofAKind1 = 0
                ofAKind2 = 0
                ofAKind3 = 0
                for r in ranks:
                    if r == ranks[0]:
                        ofAKind1 += 1
                    if r == ranks[1]:
                        ofAKind2 += 1
                    if r == ranks[2]:
                        ofAKind3 += 1
                ofAKinds = [ofAKind1,ofAKind2,ofAKind3]
                isPair = any(2 == k for k in ofAKinds)
                isTwoPair = ranks[0] == ranks[1] and ranks[2] == ranks[3]
                isThreeOfAKind = any(3 == k for k in ofAKinds)
                if isThreeOfAKind:
                    return ('3 of\na kind',125)
                elif isTwoPair:
                    return ('2 pair',60)
                elif isPair:
                    return ('pair',5)
        elif len(ranks) == 3:
            ofAKind1 = 0
            ofAKind2 = 0
            for r in ranks:
                if r == ranks[0]:
                    ofAKind1 += 1
                if r == ranks[1]:
                    ofAKind2 += 1
            ofAKinds = [ofAKind1,ofAKind2]
            isPair = any(2 == k for k in ofAKinds)
            isThreeOfAKind = any(3 == k for k in ofAKinds)
            if isThreeOfAKind:
                return ('3 of\na kind',125)
            elif isPair:
                return ('pair',5)
        elif len(ranks) == 2:
            isPair = ranks[0] == ranks[1]
            if isPair:
                return ('pair',5)
        
        return ('no hand',0)
            
    def update_score(self):
        indices = {
            "row1": [0,1,2,3],
            "row2": [4,5,6,7],
            "row3": [8,9,10,11],
            "row4": [12,13,14,15],
            "col1": [0,4,8,12],
            "col2": [1,5,9,13],
            "col3": [2,6,10,14],
            "col4": [3,7,11,15],
            "corners": [0,3,12,15]
        }
        for name in indices:
            ii = indices[name]
            hand = [self.board[ii[0]],self.board[ii[1]],self.board[ii[2]],self.board[ii[3]]]
            x = self.board[ii[3]].x
            y = self.board[ii[3]].y
            if name.startswith('r'):
                x += self.board[ii[3]].w + 1
            elif name.startswith('col'):
                y += self.board[ii[3]].h + 1
            else: # corners
                x = self.board[ii[0]].x - 20
                y = self.board[ii[0]].y - 20
            self.score[name] = (self.hand_score(hand),[x,y])

        self.score['discard'] = (self.hand_score(self.discard_squares),[self.discard_x,self.discard_y])

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

        self.update_score()

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
                        self.discard_y += sq.h+1
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
        if self.game_over:
            next_button = (pyxel.mouse_x >= self.next_hand_button_x
                and pyxel.mouse_x <= self.next_hand_button_x + self.next_hand_button_w
                and pyxel.mouse_y >= self.next_hand_button_y
                and pyxel.mouse_y <= self.next_hand_button_y + self.next_hand_button_h)
            if next_button and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.new_game()

    def draw(self):
        pyxel.cls(0)

        for sq in self.board + self.hand_squares + self.discard_squares:
            sq.draw()

        for name in self.score:
            score_info = self.score[name]
            x = score_info[1][0]
            y = score_info[1][1]
            hand_type = score_info[0][0]
            score = score_info[0][1]
            if score > 0:
                pyxel.text(x,y,hand_type + '\n$' + str(score),7)

        for sq in self.board:
            if sq.has_card and sq.card.can_move and not sq.card.clicked:
                sq.card.draw(sq,hasBorder=True)
        for sq in self.board + self.hand_squares:
            if sq.card.clicked:
                sq.draw()

        if not self.game_over:
            if self.num_in_hand == 1:
                next_hand_color = 7
                pyxel.rect(self.next_hand_button_x,
                            self.next_hand_button_y,
                            self.next_hand_button_w,
                            self.next_hand_button_h,
                            next_hand_color)
                pyxel.rect(self.next_hand_button_x+1,
                            self.next_hand_button_y+1,
                            self.next_hand_button_w-2,
                            self.next_hand_button_h-2,
                            1)
                discard_card_text = ''
                for sq in self.hand_squares:
                    if sq.has_card:
                        discard_card_text = sq.card.rank_text() + sq.card.suit
                pyxel.text(self.next_hand_button_x+1,self.next_hand_button_y+1,
                            'END ROUND\n' + discard_card_text + ' --> Discard',next_hand_color)
        else:
            total_winnings = 0
            discard_score = 0
            num_hands = 0
            for name in self.score:
                if name == 'discard':
                    continue
                score_info = self.score[name]
                score = score_info[0][1]
                if name == 'corners':
                    score *= 2
                if score > 0:
                    total_winnings += score
                    num_hands += 1
            score_info = self.score['discard']
            discard_score = score_info[0][1]
            if num_hands == 9 and discard_score > 0:
                num_hands += 1
            
            hand_mult = 1
            if num_hands > 1 and num_hands <= 3:
                hand_mult = 2
            elif num_hands <= 5:
                hand_mult = 3
            elif num_hands <= 7:
                hand_mult = 4
            elif num_hands <= 9:
                hand_mult = 5
            elif num_hands == 10:
                hand_mult = 6
            
            winnings_text = 'Winnings $' + str(total_winnings)
            discard_hand_text = 'Discard hand ' + str(discard_score) + ' x 3'
            multiplier_text = 'Multiplier ' + str(num_hands) + ' hands x ' + str(hand_mult)
            total_score_text = 'Total score $' + str((total_winnings + discard_score)*hand_mult)
            score_text = winnings_text + '\n' + discard_hand_text + '\n' + multiplier_text + '\n' + total_score_text
            pyxel.rect(self.final_score_x,
                       self.final_score_y,
                       self.final_score_w,
                       self.final_score_h,
                       7)
            pyxel.rect(self.final_score_x+1,
                       self.final_score_y+1,
                       self.final_score_w-2,
                       self.final_score_h-2,
                       0)
            if num_hands == 10:
                pyxel.text(self.final_score_x+1,self.final_score_y+1,score_text,7)
            else:
                pyxel.text(self.final_score_x+1,self.final_score_y+1,score_text,1)
                score_text = winnings_text + '\n\n' + multiplier_text + '\n' + total_score_text
                pyxel.text(self.final_score_x+1,self.final_score_y+1,score_text,7)
            
            pyxel.rect(self.next_hand_button_x,
                        self.next_hand_button_y,
                        self.next_hand_button_w,
                        self.next_hand_button_h,
                        7)
            pyxel.rect(self.next_hand_button_x+1,
                        self.next_hand_button_y+1,
                        self.next_hand_button_w-2,
                        self.next_hand_button_h-2,
                        1)
            pyxel.text(self.game_over_x+1,self.game_over_y+1,'PLAY AGAIN?',7)

PileUpPoker()