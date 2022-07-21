import random


class MasterMind:
    def __init__(self):
        self.chances = self.k = 0
        self.balls_set = list()
        self.__choice = list()
        self.states = list()

    def initialize(self, n, m, k):
        self.k = k
        self.chances = 2 * n
        self.__create_balls_set(n, m)
        self.__generate_choice()
        hint = 0
        guess_list = "_" * self.k
        self.states = list()
        self.states.append((guess_list, hint, self.chances))
        return self.states[0]

    def add_guess(self, guess):
        self.chances -= 1
        self.states.append((guess, self.compare_guess(guess), self.chances))

    def is_final_state(self, guess, hint, chances):
        if self.compare_guess(guess) == self.k and chances > 0:
            return True, "B"
        elif chances <= 0:
            return True, "A"
        return False

    def compare_guess(self, guess):
        count = 0
        for pos in range(0, self.k):
            if self.__choice[pos] == guess[pos]:
                count += 1
        return count

    def __generate_choice(self):
        self.__choice = random.choices(self.balls_set, k=self.k)

    def __create_balls_set(self, n, m):
        for color in range(1, n + 1):
            for _ in range(0, m):
                self.balls_set.append(str(color))

    def print_states(self):
        for state in self.states:
            print(state)

if __name__ == "__main__":
        master_mind = MasterMind()
        init = master_mind.initialize(9, 1, 4)
        while not master_mind.is_final_state(*master_mind.states[-1]):
            guess = [2,3,1,4,5]
            master_mind.add_guess(guess)
            print(master_mind.states[-1])
        master_mind.print_states()
