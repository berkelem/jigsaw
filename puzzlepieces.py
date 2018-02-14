# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 20:45:52 2017

@author: Matthew Berkeley
"""
import numpy as np


class Piece():
    
    def __init__(self, id_num, A, B, C, D):
        self.id, self.A, self.B, self.C, self.D = id_num, A, B, C, D
        self.rot = 0
        self.up = True
        self.pos = False
        
    def rotate90ccw(self):
        self.A, self.B, self.C, self.D = self.B, self.C, self.D, self.A
        self.rot -= 90
    
    def rotate90cw(self):
        self.A, self.B, self.C, self.D = self.D, self.A, self.B, self.C
        self.rot += 90
        
    def flip(self):
        self.A, self.B, self.C, self.D = self.A, self.D, self.C, self.B
        self.up = not self.up
        
        
class Puzzle():
    
    def __init__(self):
        self.innies = ['oa', 'ia', 'c', 'x']
        self.outies = ['OA', 'IA', 'C', 'X']
        self.p0 = Piece(0, 'X', 'C', 'c', 'ia')
        self.p1 = Piece(1, 'oa', 'OA', 'X', 'c')
        self.p2 = Piece(2, 'c', 'C', 'OA', 'oa')
        self.p3 = Piece(3, 'IA', 'C', 'x', 'c')
        self.p4 = Piece(4, 'C', 'ia', 'x', 'IA')
        self.p5 = Piece(5, 'x', 'oa', 'IA', 'IA')
        self.p6 = Piece(6, 'oa', 'c', 'IA', 'OA')
        self.p7 = Piece(7, 'X', 'oa', 'oa', 'C')
        self.p8 = Piece(8, 'X', 'ia', 'x', 'OA')
        self.p9 = Piece(9, 'ia', 'oa', 'X', 'IA')
        self.p10 = Piece(10,'ia', 'c', 'OA', 'OA')
        self.p11 = Piece(11, 'OA', 'x', 'c', 'C')
        self.p12 = Piece(12, 'X', 'C', 'c', 'x')
        self.p13 = Piece(13, 'x', 'IA', 'IA', 'c')
        self.p14 = Piece(14, 'oa', 'C', 'IA', 'ia')
        self.p15 = Piece(15, 'C', 'C', 'oa', 'c')
        self.cursor = 0
        self.pos_sides = {
                    0: [0,1,1,0], 1: [0,1,1,1], 2: [0,1,1,1], 3: [0,0,1,1], 
                    4: [1,1,1,0], 5: [1,1,1,1], 6: [1,1,1,1], 7: [1,0,1,1], 
                    8: [1,1,1,0], 9: [1,1,1,1], 10: [1,1,1,1], 11: [1,0,1,1], 
                    12: [1,1,0,0], 13: [1,1,0,1], 14: [1,1,0,1], 15: [1,0,0,1]
                    }
        self.pos_nbs = {
                    0: [1,4], 1: [0,2,5], 2: [1,3,6], 3: [2,7],
                    4: [0,5,8], 5: [1,4,6,9], 6: [2,5,7,10], 7: [3,6,11],
                    8: [4,9,12], 9: [5,8,10,13], 10: [6,9,11,14], 11: [7,10,15],
                    12: [8,13], 13: [9,12,14], 14: [10,13,15], 15: [11,14]
                    }
        #self.filled = np.array(([0]*16)).astype(bool)
        self.config = [None]*16

    def check_match(self, side1, side2):
        if side1 in self.innies:
            ind = self.innies.index(side1)
            if self.outies[ind] == side2:
                return True
            else:
                return False
        elif side1 in self.outies:
            ind = self.outies.index(side1)
            if self.innies[ind] == side2:
                return True
            else:
                return False
        else:
            raise ValueError('Side code does not match stored values.')
            
    def check_piece(self, piece):
        nbs = self.pos_nbs[self.cursor]
        ind = 0
        while ind < len(nbs) and piece.rot < 360:
            i = nbs[ind]
            if i < self.cursor:
                piece_fx = self.config[i]
                print 'Fixed piece', (piece_fx.id, piece_fx.A, piece_fx.B, piece_fx.C, piece_fx.D)                
                
                side_ok = False
                while piece.rot < 360 and not side_ok:
                    print 'Test piece', (piece.id, piece.A, piece.B, piece.C, piece.D)
                    if i == self.cursor - 1:
                        side_fx = piece_fx.B
                        side_new = piece.D
                    elif i == self.cursor - 4:
                        side_fx = piece_fx.C
                        side_new = piece.A
                    side_ok = self.check_match(side_fx, side_new)
                    if side_ok:
                        ind += 1
                        continue
                    else:
                        piece.rotate90cw()
                        ind = 0
                        break
                    if piece.rot >= 360 and not side_ok:
                        if piece.up:
                            piece.flip()
                            piece.rot = 0
                        ind = 0
                        break
            else:
                ind += 1
                
        if ind > 0:           
            piece_ok=True
            #print 'Piece {0} goes in place {1}!'.format(piece.id, self.cursor)
        else:
            piece_ok = False
            #print 'Piece {0} does not fit in place {1}.'.format(piece.id, self.cursor)
            if not piece.up:
                piece.flip()
                piece.rot = 0
        return piece_ok
    
    def fill_position(self, piece_no):
        while self.cursor < 16 and piece_no < 16:
            
            piece = self.pieces[piece_no]
            if piece.pos:
                piece_no += 1
                
            elif self.check_piece(piece):
                self.config[self.cursor] = piece
                piece.pos = True
                self.cursor += 1
                piece_no = 0
            
            else:
                piece_no += 1
        
            yield piece_no

    def fill_grid(self,order):
        self.pieces = [self.p0, self.p1, self.p2, self.p3, 
                  self.p4, self.p5, self.p6, self.p7, 
                  self.p8, self.p9, self.p10, self.p11, 
                  self.p12, self.p13, self.p14, self.p15]
        self.pieces = [self.pieces[i] for i in order]
        pieces_order = [p.id for p in self.pieces]
        #print 'order', pieces_order
                  
        piece_no = 0
        
        complete = False
        while not complete:
            filled = all([p.pos for p in self.pieces])
            #print self.cursor, piece_no
            #print 'filled?', filled
            fill_pos = self.fill_position(piece_no)
            if piece_no < 16 and not filled:
                piece_no = next(fill_pos)
            #print 'active piece no', piece_no
            if piece_no > 15 and not filled:
                #print 'config wrong', self.config
                #print self.cursor
                
                last_piece = self.config[self.cursor-1]
                last_piece.pos = False
                self.config[self.cursor-1] = None
                piece_no = pieces_order.index(last_piece.id) + 1
                self.cursor -= 1
                #print 'Removed piece {0} from position {1}'.format(last_piece.id, self.cursor)
                #print 'updated config', self.config
                #print 'updated cursor', self.cursor
                #print 'updated piece no', piece_no
                
            elif filled:
                complete = True

            
        
            
        return
            
        
        
        

if __name__ == '__main__':
    
    order = range(16)
    orders = []
    for i in xrange(1):#len(ord)):
        order = order[-1:] + order[:-1]  
        puzzle = Puzzle()
        puzzle.fill_grid(order)
        final_config = []
        orient = []
        for item in puzzle.config:
            
            try:
                final_config.append(item.id)
                orient.append((item.rot,item.up))
                
            except AttributeError:
                final_config.append(None)
                orient.append(None)
        
        soln = zip(final_config, orient)
        print 'solution', soln