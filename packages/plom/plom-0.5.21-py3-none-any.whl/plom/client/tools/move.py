# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2018-2020 Andrew Rechnitzer
# Copyright (C) 2020 Colin B. Macdonald
# Copyright (C) 2020 Victoria Schuster

from PyQt5.QtWidgets import QUndoCommand, QGraphicsItem


class CommandMoveItem(QUndoCommand):
    # Moves the graphicsitem. we give it an ID so it can be merged with other
    # commandmoves on the undo-stack.
    # Don't use this for moving text - that gets its own command.
    # Graphicsitems are separate from graphicsTEXTitems
    def __init__(self, xitem, delta):
        super(CommandMoveItem, self).__init__()
        # The item to move
        self.xitem = xitem
        # The delta-position of that item.
        self.delta = delta
        self.setText("Move")

    def id(self):
        # Give it an id number for merging of undo/redo commands
        return 101

    def redo(self):
        # Temporarily disable the item emiting "I've changed" signals
        self.xitem.setFlag(QGraphicsItem.ItemSendsGeometryChanges, False)
        # Move the object
        self.xitem.setPos(self.xitem.pos() + self.delta)
        # Reenable the item emiting "I've changed" signals
        self.xitem.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def undo(self):
        # Temporarily disable the item emiting "I've changed" signals
        self.xitem.setFlag(QGraphicsItem.ItemSendsGeometryChanges, False)
        # Move the object back
        self.xitem.setPos(self.xitem.pos() - self.delta)
        # Reenable the item emiting "I've changed" signals
        self.xitem.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def mergeWith(self, other):
        # Most commands cannot be merged - make sure the moved items are the
        # same - if so then merge things.
        if self.xitem != other.xitem:
            return False
        self.delta = other.delta
        return True
