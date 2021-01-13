from Scripts import utils
import random, os

class Mastermind:
    def __init__(self):
        # Setup colors if on windows
        if os.name == "nt": os.system("color")
        self.u = utils.Utils("Mastermind")
        self.colors = [
            "\u001b[41;1m {} \u001b[0m", # red
            "\u001b[44;1m {} \u001b[0m", # blue
            "\u001b[43;1m {} \u001b[0m", # yellow
            "\u001b[42;1m {} \u001b[0m", # green
            "\u001b[47;1m {} \u001b[0m", # white
            "\u001b[40;1m {} \u001b[0m", # black
        ]
        self.check_colors = [
            "\u001b[47;1m {} \u001b[0m", # white - right color, wrong position
            "\u001b[40;1m {} \u001b[0m", # black - right color, right position
        ]
        self.num_pegs = 4
        self.sequence = []
        self.max_guesses = 0 # 0 = unlimited, anything above sets a max
        self.show_answer = False

    def generate_sequence(self):
        self.sequence = [random.randint(1,len(self.colors)) for x in range(self.num_pegs)]
        return self.sequence

    def get_sequence(self,sequence,blank=False):
        # Walks a list of ints and returns the color codes based on index - sequence is 1-based, list is 0-based
        return "".join([self.colors[-1].format("?") if blank else self.colors[x-1].format(x) for x in sequence])

    def get_right_wrong(self,guess,sequence=None):
        right_wrong,right_right = self.check_guess(guess,sequence)
        return "{}{}".format(
            self.check_colors[0].format(len(right_wrong)),
            self.check_colors[1].format(len(right_right))
        )

    def get_pretty_guess(self,guess,sequence=None):
        return "{}   ||   {}".format(
            self.get_right_wrong(guess,sequence),
            self.get_sequence(guess)
        )

    def get_blank_sequence(self,sequence=None):
        if sequence == None: sequence = self.generate_sequence()
        return self.get_sequence(sequence,True)

    def check_guess(self,guess,sequence = None):
        if sequence == None: sequence = self.generate_sequence()
        # Compares the guess against the sequence
        right_right = [x for x in range(len(guess)) if guess[x] == sequence[x]]
        right_wrong = []
        for x in range(len(guess)):
            if x in right_right: continue # Skip correct guess indexes
            # Get a list of indexes that match our guess
            temp_check = [y for y in range(len(sequence)) if sequence[y] == guess[x] and not y in right_right]
            for y in temp_check:
                if y in right_wrong: continue # Already added, skip
                right_wrong.append(y)
                break # Leave here so we only add it once
        return (right_wrong,right_right)

    def print_progress(self,prior_guesses,sequence):
        print("Attempts:")
        for index,guess in enumerate(prior_guesses):
            print("{}. {}".format(str(index+1).rjust(4),self.get_pretty_guess(guess,sequence)))
        print("")

    def new_game(self):
        # Set up our new sequence - and let the player choose
        prior_guesses = []
        sequence = self.generate_sequence()
        valid_guesses = [str(x) for x in range(1,len(self.colors)+1)]
        while True:
            self.u.head()
            print("")
            print("Current Sequence Placeholder:  {}".format(self.get_sequence(sequence,not self.show_answer)))
            print("")
            if len(prior_guesses):
                self.print_progress(prior_guesses,sequence)
            print("Attempts Left: {}".format(self.max_guesses-len(prior_guesses) if self.max_guesses > 0 else "Unlimited"))
            print("Color Legend:  {}".format(self.get_sequence([x+1 for x in range(len(self.colors))])))
            print("{} = Right Color, Wrong Place".format(self.check_colors[0].format("#")))
            print("{} = Right Color, Right Place".format(self.check_colors[1].format("#")))
            print("")
            check = self.u.grab("Please type the {} number sequence you'd like to guess:  ".format(self.num_pegs)).lower()
            # Verify we got *something* tangible
            if not len(check): continue
            if check in ("q","m"): return
            if check == "corpnewt":
                self.show_answer ^= True
                continue
            valid = [int(x) for x in check if x in valid_guesses]
            if not len(valid) == len(sequence):
                self.u.head("Uh Oh")
                print("")
                print("Not the right amount of numbers pressed!")
                print("")
                self.u.grab("Press [enter] to return...",timeout=5)
                continue
            # Let's gather the results
            prior_guesses.append(valid)
            right_wrong,right_right = self.check_guess(valid,sequence)
            if len(right_right) == len(sequence):
                self.u.head("YOU WON!")
                print("")
                self.print_progress(prior_guesses,sequence)
                print("The Winning Sequence:")
                print("      "+self.get_pretty_guess(sequence,sequence))
                print("")
                print("You took {:,} guess{}!".format(len(prior_guesses),"" if len(prior_guesses)==1 else "es"))
                print("")
                return self.u.grab("Press [enter] to return to the main menu...")
            if self.max_guesses > 0 and len(prior_guesses) >= self.max_guesses:
                self.u.head("YOU LOST!")
                print("")
                self.print_progress(prior_guesses,sequence)
                print("The Winning Sequence:")
                print("      "+self.get_pretty_guess(sequence,sequence))
                print("")
                print("You took {:,} guess{}!".format(len(prior_guesses),"" if len(prior_guesses)==1 else "es"))
                print("")
                return self.u.grab("Press [enter] to return to the main menu...")

    def main(self):
        self.u.head()
        print("")
        print("Difficulty Options:")
        print("  1. Easy Game   (4 pegs, unlimited tries)")
        print("  2. Medium Game (4 pegs, 10 tries)")
        print("  3. Hard Game   (6 pegs, 10 tries)")
        print("")
        print("Q. Quit")
        print("")
        menu = self.u.grab("Please choose an option:  ").lower()
        if not len(menu): return
        if menu == "q": self.u.custom_quit()
        if not menu in ("1","2","3"): return
        self.show_answer = False
        self.max_guesses = 0 if menu == "1" else 10
        self.num_pegs = 6 if menu == "3" else 4
        self.new_game()

if __name__ == '__main__':
    m = Mastermind()
    while True:
        m.main()