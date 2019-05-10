import matplotlib.pyplot as plt
import pickle as pkl
from utils.text_analyzer import TextStats
from utils.dictionary import Dictionary


def solve_manually(stats: TextStats, dictionary: Dictionary):
    password = []
    solve = True
    swap_password = False
    last_stable_pos = 26
    plt.ion()
    plt.show()
    while solve:
        plt.clf()
        new_stats, tmp, table = get_new_stats(stats, password, last_stable_pos)
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
        print("Ciphertext:", stats.text)
        print("Message is:", tmp)
        print("Message is:", new_stats.text)
        answer = input("Guess a password letter. Type 0 to stop, type 1 to undo, 2 to go to password switching mode\n")
        if answer == "0":
            solve = False
            continue
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
        if answer == "2":
            solve = False
            swap_password = True
            continue
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

    while swap_password:
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

        plt.clf()
        new_stats, tmp, table = get_new_stats(stats, password)
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
        print("Ciphertext:", stats.text)
        print("Message is:", new_stats.text)
        print("Password is:", password)

    return new_stats.text


def get_new_stats(stats: TextStats, password: list, last_stable_pos: int=-1):
    if len(password) == 0:
        return stats, "-", list(range(0, 26))
    if last_stable_pos == -1:
        last_stable_pos = len(password)
    text = stats.text
    unused_letters = list(range(0, 26))
    table = []
    for p in password:
        P = ord(p) - 65
        table.append(P)
        unused_letters.pop(unused_letters.index(P))
    table.extend(unused_letters)

    new_text = ""
    tmp_text = ""
    for c in text:
        p = ord(c) - 65
        np = table.index(p)
        nc = chr(np + 65)
        new_text += nc
        if np <= last_stable_pos:
            tmp_text += "-"
        else:
            tmp_text += nc

    new_stats = TextStats(new_text)
    return new_stats, tmp_text, table


def swap(a: str, b: str, text: str):
    text = text.replace(a, b.lower())
    text = text.replace(b, a)
    text = text.replace(b.lower(), b)
    return text


def make_table(t1: list, t2: list):
    table = [-1] * 26
    for c1, c2 in zip(t1, t2):
        l1 = ord(c1) - 65
        l2 = ord(c2) - 65
        table[l1] = l2
    return table
