"""
Copyright 2008 Olivier Belanger

This file is part of Ounk.

Ounk is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Ounk is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ounk.  If not, see <http://www.gnu.org/licenses/>.
"""

import random

class Markov:
    def __init__( self, order ):
        """Object's initialization.

--- PARAMETERS ---

order : Order of the Markov chain. Determines how many past values 
        will be used to build the probability table for the next note.
"""
        self.originalList = []
        self.temporaryList = []
        self.playedNotes = []
        self.order = order

    def mkStartPlayback( self ):
        """Sets up a markov chain for playback.

--- PARAMETERS ---

no parameter

"""
        self.playedNotes = []
        
        for val in self.originalList:
        	self.temporaryList.append( val )
        
        for i in range(self.order):
            self.temporaryList.append(self.originalList[i])
            
        self.playedNotes = self.originalList[ len( self.originalList ) - self.order:]

    def next( self ):
        """Calls a new value from the generator objet."""
    	newValue = 0
        condition = False
        self.probTable = []
        
        for i in range(len(self.temporaryList) - self.order):           
            for iord in range(self.order):
                if self.playedNotes[len(self.playedNotes) - (iord + 1)] != self.temporaryList[(self.order - 1) + i - iord]:
                    condition = False
                    break
                else:
                    condition = True

            if condition:
                self.probTable.append(self.temporaryList[i + self.order])

        newValue = self.probTable[random.randint(0, (len(self.probTable) - 1))]	
        self.playedNotes.append( newValue )
        return newValue
        
    def mkStartRecord( self ):
        """Initializes a markov chain to record a new sequence.

--- PARAMETERS ---

no parameter

"""
        self.originalList = []
        self.temporaryList = []
        self.playedNotes = []    

    def mkSetList(self, l):
        """Takes a list as a sequence to be analyzed.

--- PARAMETERS ---

list : New sequence used to determine picked up values.

"""
        self.originalList = l
        self.temporaryList = []
        self.playedNotes = []  
        
    def mkRecord( self, value ):
        """Appends a new value to a sequence to be analyzed.

--- PARAMETERS ---

value : In record mode, the value is added to the list used for the generation.
"""
        self.originalList.append( value )
		
    def	mkChangeOrder( self, value ):
        """Changes the order of the markov chain.

--- PARAMETERS ---

order : Order of the Markov chain. Determines how many past values 
        will be used to build the probability table for the next note.
"""
    	self.order = value
    	self.mkStartPlayback()		
