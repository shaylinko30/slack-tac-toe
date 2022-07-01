import unittest
from game import *

class TestGame(unittest.TestCase):

    def setUp(self):
        self.unfinishedBoard = [
            [untouchedValue, secondPlayerValue, firstPlayerValue],
            [secondPlayerValue, firstPlayerValue, untouchedValue],
            [secondPlayerValue, firstPlayerValue, secondPlayerValue]
        ]
        self.tieBoard = [
            [firstPlayerValue, secondPlayerValue, firstPlayerValue],
            [secondPlayerValue, firstPlayerValue, secondPlayerValue],
            [secondPlayerValue, firstPlayerValue, secondPlayerValue]
        ]
        self.oneRowUntouched = [
            [untouchedValue, untouchedValue, untouchedValue],
            [secondPlayerValue, firstPlayerValue, secondPlayerValue],
            [secondPlayerValue, firstPlayerValue, secondPlayerValue]
        ]

        self.xWinsTopRowBoard = [
            [firstPlayerValue, firstPlayerValue, firstPlayerValue],
            [secondPlayerValue, firstPlayerValue, secondPlayerValue],
            [secondPlayerValue, untouchedValue, secondPlayerValue]
        ]
        self.xWinsMiddleRowBoard = [
            [untouchedValue, untouchedValue, secondPlayerValue],
            [firstPlayerValue, firstPlayerValue, firstPlayerValue],
            [secondPlayerValue, secondPlayerValue, untouchedValue]
        ]
        self.xWinsBottomRowBoard = [
            [secondPlayerValue, secondPlayerValue, firstPlayerValue],
            [secondPlayerValue, firstPlayerValue, secondPlayerValue],
            [firstPlayerValue, firstPlayerValue, firstPlayerValue]
        ]

        self.oWinsLeftColumnBoard = [
            [secondPlayerValue, firstPlayerValue, firstPlayerValue],
            [secondPlayerValue, firstPlayerValue, secondPlayerValue],
            [secondPlayerValue, untouchedValue, firstPlayerValue]
        ]
        self.oWinsMiddleColumnBoard = [
            [untouchedValue, secondPlayerValue, untouchedValue],
            [firstPlayerValue, secondPlayerValue, firstPlayerValue],
            [firstPlayerValue, secondPlayerValue, untouchedValue]
        ]
        self.oWinsRightColumnBoard = [
            [firstPlayerValue, secondPlayerValue, secondPlayerValue],
            [firstPlayerValue, firstPlayerValue, secondPlayerValue],
            [secondPlayerValue, firstPlayerValue, secondPlayerValue]
        ]

        self.xWinsDiagonalBoard = [
            [firstPlayerValue, secondPlayerValue, untouchedValue],
            [secondPlayerValue, firstPlayerValue, firstPlayerValue],
            [secondPlayerValue, secondPlayerValue, firstPlayerValue]
        ]
        self.oWinsDiagonalBoard = [
            [firstPlayerValue, firstPlayerValue, secondPlayerValue],
            [firstPlayerValue, secondPlayerValue, secondPlayerValue],
            [secondPlayerValue, firstPlayerValue, firstPlayerValue]
        ]


    def test_checkTie(self):
        self.assertEqual(checkTie(self.tieBoard), True, 'Should return true on a tie board')
        self.assertEqual(checkTie(self.unfinishedBoard), False, 'Should return false on an unfinished board')

    def test_getOpposite(self):
        self.assertEqual(getOpposite(firstPlayerValue), secondPlayerValue, 'Should return {} when {} is passed in'.format(secondPlayerValue, firstPlayerValue))
        self.assertEqual(getOpposite(secondPlayerValue), firstPlayerValue, 'Should return {} when {} is passed in'.format(firstPlayerValue, secondPlayerValue))

    def test_checkWinner(self):
        self.assertEqual(checkWinner(self.xWinsTopRowBoard), True, 'Should return true when {} wins the top row'.format(firstPlayerValue))
        self.assertEqual(checkWinner(self.xWinsMiddleRowBoard), True, 'Should return true when {} wins the middle row'.format(firstPlayerValue))
        self.assertEqual(checkWinner(self.xWinsBottomRowBoard), True, 'Should return true when {} wins the bottom row'.format(firstPlayerValue))

        self.assertEqual(checkWinner(self.oWinsLeftColumnBoard), True, 'Should return true when {} wins the top column'.format(secondPlayerValue))
        self.assertEqual(checkWinner(self.oWinsMiddleColumnBoard), True, 'Should return true when {} wins the middle column'.format(secondPlayerValue))
        self.assertEqual(checkWinner(self.oWinsRightColumnBoard), True, 'Should return true when {} wins the bottom column'.format(secondPlayerValue))

        self.assertEqual(checkWinner(self.xWinsDiagonalBoard), True, 'Should return true when {} wins the diagonal'.format(firstPlayerValue))
        self.assertEqual(checkWinner(self.oWinsDiagonalBoard), True, 'Should return true when {} wins the diagonal'.format(secondPlayerValue))

        self.assertEqual(checkWinner(getBaseGame()), False, 'Should return false when the board is in the base game state')
        self.assertEqual(checkWinner(self.oneRowUntouched), False, 'Should return false when one row is {}'.format(untouchedValue))
        self.assertEqual(checkWinner(self.tieBoard), False, 'Should return false if the board it in a tie state')

if __name__ == '__main__':
    unittest.main()