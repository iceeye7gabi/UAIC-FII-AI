import os
import random


class MasterMind:
    def __init__(self):
        self.chances = self.k = self.m = self.n = 0
        self.balls_set = list()
        self.__choice = list()
        self.states = list()

    def initialize(self, n, m, k):
        self.n = n
        self.m = m
        self.k = k
        self.chances = 2 * 3
        self.__create_balls_set(n, m)
        self.__generate_choice()
        hint = 0
        guess_list = "_" * self.k
        self.states = list()
        self.states.append((guess_list, hint, self.chances))
        return self.states[0]

    def add_guess(self, guess):
        if self.is_allowed(guess):
            self.chances -= 1
            self.states.append((guess, self.compare_guess(guess), self.chances))
            return True
        else:
            return False

    def is_final_state(self, guess, hint, chances):
        if hint == self.k and chances > 0:
            return "jucatorB"
        elif chances <= 0:
            return "jucatorA"

    def compare_guess(self, guess):
        count = 0
        for pos in range(0, self.k):
            if self.__choice[pos] == guess[pos]:
                count += 1
        return count

    def is_allowed(self, guess):
        if len(guess) != self.k:
            return False
        for i in range(0, self.k):
            if not 0 < int(guess[i]) <= self.n:
                return False
        for i in range(1, self.n + 1):
            if guess.count(str(i)) > self.m:
                return False
        return True

    def __generate_choice(self):
        self.__choice = random.choices(self.balls_set, k=self.k)
        while len(set(self.__choice)) != 4:
            self.__choice = random.choices(self.balls_set, k=self.k)

    def __create_balls_set(self, n, m):
        for color in range(1, n + 1):
            for _ in range(0, m):
                self.balls_set.append(str(color))

    def print_states(self):
        for state in self.states[::-1]:
            print(state)

    def get_choice(self):
        return str(self.__choice)

    def print_correct_answer(self):
        print(self.__choice)


if __name__ == "__main__":
    master_mind = MasterMind()
    init = master_mind.initialize(9, 1, 4)
    is_final = master_mind.is_final_state(*master_mind.states[-1])
    master_mind.print_states()
    master_mind.print_correct_answer()
    while not is_final:
        if master_mind.add_guess(input("Alegeti o pereche: ")):
            master_mind.print_states()
        else:
            print("Perechea nu este valida")
        is_final = master_mind.is_final_state(*master_mind.states[-1])
    print(is_final + " a castigat!")
    print("Perechea castigatoare: " + master_mind.get_choice())
