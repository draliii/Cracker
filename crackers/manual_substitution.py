import matplotlib.pyplot as plt
from utils.text_analyzer import TextStats
from utils.dictionary import Dictionary


def solve_manually(stats: TextStats, dictionary: Dictionary) -> tuple:
    """
    Console tool with pyplot graphs. Can be used to guess passwords of simple substitution ciphers. The tool was built
    to find substitution tables that start with a password and the rest of the alphabet is intact, however, if the first
    part is skipped, it can be used to guess any monoalphabetic cipher. 
    :param stats: TextStats object of the text to be cracked
    :param dictionary: Dictionary constructed from the language of the plaintext
    :return: solved text, cipher name ("monoalphabetic"), conversion table
    """
    password = []
    solve = True
    swap_password = False
    last_stable_pos = 26
    new_stats = stats
    table = list(range(0, 26))
    # these plt commands allow for changing data in one figure
    plt.ion()
    plt.show()

    # first loop splits the alphabet to password letters (those in the password list) and those that are not in the
    # password. Order is not important for now
    while solve:
        plt.clf()

        # new text and conversion table is computed based on the password
        # since password is usually given in descending alphabetical order, any skipped letters are guaranteed to be in
        #   the message. These are the confirmed_letters. last_stable_pos is used to compute it.
        new_stats, confirmed_letters_message, table = get_new_stats(stats, password, last_stable_pos)

        # draw and annotate the data
        new_scatter = list(new_stats.frequency[i] for i in range(0, 26))
        plt.plot(new_scatter, "r.")
        plt.plot(dictionary.frequency, "b.")
        for i in range(0, 26):
            plt.annotate(chr(i + 65), (i, dictionary.frequency[i]))
            pass
        plt.draw()
        for i in range(0, 26):
            plt.annotate(chr(table[i] + 65), (i, new_scatter[i]))
        plt.draw()
        plt.pause(0.001)

        # ask user what letter to process next
        print("Ciphertext:", stats.text)
        print("Message is:", confirmed_letters_message)
        print("Message is:", new_stats.text)
        print("Password is:", password)
        answer = input("Guess a password letter. Type 0 to stop, type 1 to undo, 2 to go to password switching mode\n")

        # stop solving on input 0, return
        if answer == "0":
            solve = False
            continue
        # undo on input 1 (delete recently added letter)
        if answer == "1":
            if len(password) >= 1:
                password.pop()
                if len(password) >= 1:
                    last_stable_pos = table.index(ord(password[-1]) - 65)
                else:
                    last_stable_pos = 26
            else:
                print("Can't undo any further")
            continue
        # stop adding letters to password, start shuffling
        if answer == "2":
            solve = False
            swap_password = True
            continue
        # TODO: an option to add all letters to the password and go to swapping might be useful - for manual analysis
        if len(answer) != 1:
            print("Invalid input")
            continue
        if not (64 < ord(answer) < 123):
            print("Invalid input")
            continue
        if answer.upper() in password:
            print("This letter already is in the password")
            continue
        password.append(answer.upper())
        last_stable_pos = table.index(ord(password[-1]) - 65)

    # in the second loop, pairs of ciphertext letters are given by the user. Those are swapped in the table to make
    # some adjustments to the previously guessed password
    while swap_password:
        print("Ciphertext:", stats.text)
        print("Message is:", new_stats.text)
        print("Password is:", password)

        input_letters = input("Type two password letters to swap, 0 to quit\n").split(" ")
        if input_letters == ["0"]:
            break
        try:
            a, b = list(map(lambda x: x.upper(), input_letters))
            a_idx = password.index(a)
            b_idx = password.index(b)
            password[a_idx] = b
            password[b_idx] = a
        except:
            print("Invalid input")
            continue

        # again visualise the changes
        plt.clf()
        new_stats, confirmed_letters_message, table = get_new_stats(stats, password)
        new_scatter = list(new_stats.frequency[i] for i in range(0, 26))
        plt.plot(new_scatter, "r.")
        plt.plot(dictionary.frequency, "b.")
        for i in range(0, 26):
            plt.annotate(chr(i + 65), (i, dictionary.frequency[i]))
            pass
        plt.draw()
        for i in range(0, 26):
            plt.annotate(chr(table[i] + 65), (i, new_scatter[i]))
        plt.draw()
        plt.pause(0.001)

    plt.close()

    return new_stats.text, "monoalphabetic", table


def get_new_stats(stats: TextStats, password: list, last_stable_pos: int=-1):
    """
    Construct new conversion table from the given password. Original ciphertext is translated using this table. To make
    it easier to understand which parts of the plaintext are fixed, an additional text is created with dashes on letters
    that are not yet certain. Certain are those characters, that are larger than last_stable_pos.
    :param stats: TextStats object of original ciphertext 
    :param password: list of letters in the password. May be sorted
    :param last_stable_pos: int value. Letters smaller than this value will be hidden from additional output. This has
     no effect on the resulting stats object.
    :return: new TextStats object with translated text, temporary translation with omitted letters, conversion table
    """

    # skip everything if there is no password
    if len(password) == 0:
        return stats, "-" * len(stats.text), list(range(0, 26))
    # if stable pos is not given, consider all letters stable
    if last_stable_pos == -1:
        last_stable_pos = len(password)

    # split letters to password letters and non-password letters
    text = stats.text
    unused_letters = list(range(0, 26))
    table = []
    for char in password:
        char_idx = ord(char) - 65
        table.append(char_idx)
        unused_letters.pop(unused_letters.index(char_idx))
    # the table contains the password first, then all remaining letters follow in alphabetical order
    table.extend(unused_letters)

    # since this table was used to conveniently encrypt the text, using it to decrypt is not effective
    # temporary reversed table is created for faster search
    reversed_table = [0]*26
    for i in range(0, 26):
        reversed_table[table[i]] = i

    # use the table to translate ciphertext
    new_text = ""
    tmp_text = ""
    for char in text:
        char_idx = ord(char) - 65
        new_char_idx = reversed_table[char_idx]
        new_char = chr(new_char_idx + 65)
        new_text += new_char
        if new_char_idx <= last_stable_pos:
            tmp_text += "-"
        else:
            tmp_text += new_char

    new_stats = TextStats(new_text)
    return new_stats, tmp_text, table
