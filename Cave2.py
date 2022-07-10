import random

class Cave:
    '''Cave structure adapted from https://rosettacode.org/wiki/Hunt_The_Wumpus#Python
    '''
    
    def __init__(self):
        self.cave = {1: [2, 6, 7, 8, 9], 2: [1, 3, 6, 7, 10], 3: [2, 4, 5, 6, 10],
                     4: [3, 5, 10, 11, 12], 5: [3, 4, 6, 9, 12], 6 :[1, 2, 3, 5, 9],
                     7: [1, 2, 8, 10, 11], 8: [1, 7, 9, 11, 12], 9: [1, 6, 5, 8, 12],
                     10: [2, 3, 4, 7, 11], 11: [4, 7, 8, 10, 12], 12: [4, 5, 8, 9, 11]}
 
        self.player_pos = 1
        self.rooms_visited = {1}
        self.populate_cave()

    def populate_cave(self):
        ''' Put the threats into random rooms.
        '''
        rooms = random.sample(list(range(2, len(self.cave)+1)), 5)
        threats = ['bats', 'bats', 'pit', 'pit', 'wumpus']
        
        self.threats = dict(zip(rooms, threats))
            
            
    def enter_room(self, room_number):
        ''' Allows a player to visit an adjacent room
            If the player attempts to enter a non-adjacent room they remain
            where they are.
        '''
        
        if room_number in self.cave[self.player_pos]:
            self.player_pos = room_number
            if room_number not in self.rooms_visited:
                self.rooms_visited.add(room_number)

    def adjacent_rooms(self):
        ''' Returns a list of the adjacent room numbers
        '''
        
        return self.cave[self.player_pos]

    def goto_room(self, room_number):
        ''' Allows a player to go to a room they have previously visted
            If the player attempts to enter a room they have not visited
            they remain where they are.
        '''
        
        if room_number in self.rooms_visited:
            self.player_pos = room_number

    def current_pos(self):
        ''' Returns the current room the player is in.
        '''
        
        return self.player_pos

    def current_threat(self):
        ''' Returns the threat in the current room.
            Possible values are: 'bats', 'pit', 'wumpus' and 'empty'
        '''

        return self.threats.get(self.current_pos(), "empty")
