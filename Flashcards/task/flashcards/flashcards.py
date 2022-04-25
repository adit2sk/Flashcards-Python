# Write your code here
import argparse
from os.path import exists
from random import choice
from json import dumps


def add_card(card_dict_, error_dict_):
    output = []
    print("The card:")
    output.append("The card:")
    while True:
        term = input()
        if term in card_dict_.keys():
            print("The term \"" + term + "\" already exists. Try again:")
            output.append("The term \"" + term + "\" already exists. Try again:")
        else:
            break
    print("The definition of the card:")
    output.append("The definition of the card:")
    while True:
        definition = input()
        if definition in card_dict_.values():
            print("The definition \"" + definition + "\" already exists. Try again:")
            output.append("The definition \"" + definition + "\" already exists. Try again:")
        else:
            card_dict_[term] = definition
            error_dict_[term] = 0
            print("The pair (" + term + " : " + definition + ") has been added.")
            output.append("The pair (" + term + " : " + definition + ") has been added.")
            break
    return [card_dict_, error_dict_, output]


card_dict = {}
output_list = []
error_dict = {}

parser = argparse.ArgumentParser(description="Importing and Exporting files in command line")
parser.add_argument("--import_from")
parser.add_argument("--export_to")
args = parser.parse_args()

if args.import_from:
    file_name = args.import_from
    if exists(file_name):
        with open(file_name, "r") as f:
            import_list = f.readlines()
            for i in import_list:
                import_line = i.split(":")
                if import_line[0] in card_dict:
                    del card_dict[import_line[0]]
                card_dict[import_line[0]] = import_line[1].strip('\n')
                error_dict[import_line[0]] = 0
            print(len(import_list), "cards have been loaded.")
            output_list.append(str(len(import_list)) + " cards have been loaded.")

while True:
    print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
    output_list.append("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
    action = input()
    if action == "add":
        add = add_card(card_dict, error_dict)
        card_dict = add[0]
        error_dict = add[1]
        output_list = output_list + add[2]
    elif action == "remove":
        print("Which card?")
        output_list.append("Which card?")
        del_card = input()
        if del_card in card_dict:
            del card_dict[del_card]
            print("The card has been removed.")
            output_list.append("The card has been removed.")
        else:
            print("Can't remove " + del_card + ": there is no such card.")
            output_list.append("Can't remove " + del_card + ": there is no such card.")
    elif action == "import":
        print("File name:")
        output_list.append("File name:")
        file_name = input()
        if exists(file_name):
            with open(file_name, "r") as f:
                import_list = f.readlines()
                for i in import_list:
                    import_line = i.split(":")
                    if import_line[0] in card_dict:
                        del card_dict[import_line[0]]
                    card_dict[import_line[0]] = import_line[1].strip('\n')
                    if import_line[0] not in error_dict:
                        error_dict[import_line[0]] = 0
                print(len(import_list), "cards have been loaded.")
                output_list.append(str(len(import_list)) + " cards have been loaded.")
        else:
            print("File not found.")
            output_list.append("File not found.")
    elif action == "export":
        print("File name:")
        output_list.append("File name:")
        file_name = input()
        export_list = []
        for i in card_dict:
            export_line = i + ":" + card_dict[i]
            export_list.append(export_line)
        with open(file_name, "w") as f:
            for i in export_list:
                f.write(i+'\n')
            print(len(export_list), "cards have been saved.")
            output_list.append(str(len(export_list)) + " cards have been saved.")
    elif action == "ask":
        print("How many times to ask?")
        output_list.append("How many times to ask?")
        ask = int(input())
        for i in range(ask):
            ask_term = choice(list(card_dict.keys()))
            print("Print the definition of \"" + ask_term + "\":")
            output_list.append("Print the definition of \"" + ask_term + "\":")
            answer = input()
            if answer == str(card_dict[ask_term]):
                print("Correct!")
                output_list.append("Correct!")
            elif answer in card_dict.values():
                key = [k for k, v in card_dict.items() if v == answer][0]
                print("Wrong. The right answer is \"" + str(card_dict[ask_term]) + "\", but your definition is correct for \"" + str(key) + "\".")
                error_dict[ask_term] += 1
                output_list.append("Wrong. The right answer is \"" + str(card_dict[ask_term]) + "\", but your definition is correct for \"" + str(key) + "\".")
            else:
                print("Wrong. The right answer is \"" + str(card_dict[ask_term]) + "\".")
                error_dict[ask_term] += 1
                output_list.append("Wrong. The right answer is \"" + str(card_dict[ask_term]) + "\".")
    elif action == "log":
        print("File name:")
        file_name = input()
        with open(file_name, "w") as f:
            for i in output_list:
                f.write(i)
            print("The log has been saved.")
    elif action == "hardest card":
        with open("testing.txt", "a") as t:
            t.write(dumps(error_dict) )
        errors = list(error_dict.values())
        errors.sort(reverse=True)
        error_terms = [k for k, v in error_dict.items() if v == errors[0]]
        if len(error_terms) == 0 or errors[0] == 0:
            print("There are no cards with errors.")
            output_list.append("There are no cards with errors.")
        elif len(error_terms) == 1:
            print("The hardest card is " + error_terms[0] + ". You have " + str(errors[0]) + " errors answering it")
            output_list.append("The hardest card is " + error_terms[0] + ". You have " + str(errors[0]) + " errors answering it")
        else:
            error_string = ""
            for i in error_terms:
                error_string = error_string + " \"" + i + "\","
            print("The hardest cards are " + error_string.rstrip(error_string[-1]))
            output_list.append("The hardest cards are " + error_string.rstrip(error_string[-1]))
    elif action == "reset stats":
        for i in error_dict:
            error_dict[i] = 0
        print("Card statistics have been reset.")
    elif action == "exit":
        if args.export_to:
            file_name = args.export_to
            export_list = []
            for i in card_dict:
                export_line = i + ":" + card_dict[i]
                export_list.append(export_line)
            with open(file_name, "w") as f:
                for i in export_list:
                    f.write(i+'\n')
                print(len(export_list), "cards have been saved.")
                output_list.append(str(len(export_list)) + " cards have been saved.")
        else:
            print("Bye bye!")
        exit()
