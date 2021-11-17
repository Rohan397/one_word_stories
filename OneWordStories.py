"""
This is a game where the user plays a game of one word stories with the program
"""
import random
import nltk
import string
import os
# from gtts import gTTS
# import pyttsx3
target_order = 3
order = 1
space = " "

"""
outline:

intro - explain rules of the game

choose corpus

process the corpus to get ngrams of sentence structure and words (and tokens)

Begin game loop:
 - Computer starts with one word (order = 1)
 - User responds with one word (order = 2)
 - reprocess n-grams to be 2
 - try 2-gram on the two words
 - catch exception and try 2-gram with 2 position tags
 - if another exception ("NEXT STORY")
 - else respond and n becomes Three
 -reprocess and repeat until game ends
"""

def main():
    global order
    # pause = input("Text should come after this")
    # engine = pyttsx3.init()
    # engine.say("I will speak this text")
    # engine.runAndWait()
    # engine.stop()
    # sentence = "hello my name is Rohan."
    #tokens = nltk.word_tokenize(sentence)
    # tagged = nltk.pos_tag(tokens)
    # print(tagged)
    intro()
    corpus = "corpora/sherlockHolmes.txt"
    

    game_over = False
    while game_over == False:
        story_over = False
        story = ""
        order = 1
        tag_ngrams,word_ngrams, corpus_lst, tags_dict = process_corpus(corpus)
        while story_over == False:
            user_word = input("Enter your word: ")
            story += " " + user_word
            try:
                next_word = generateTagGram(tag_ngrams, tags_dict, story)
                print("NEXT WORD", next_word)
                # my_obj = gTTS(text=next_word, lang='en', slow = False)
                # my_obj.save("next_word.mp3")
                # os.system("mpg321 welcome.mp3")
                story += " " + next_word
                print(story)
            except:
                try:
                    print("EXCEPTION CAUGHT")
                    next_word = markovIt(word_ngrams, story)
                    # if next_word in string.punctuation:
                    #     raise KeyError
                    print("NEXT WORD", next_word)
                    story += " " + next_word
                    print(story)
                except:
                    print("NEW STORY")
                    break
            # try:
            #     next_word = markovIt(word_ngrams, story)
            #     if next_word in string.punctuation:
            #         raise KeyError
            #     print("NEXT WORD", next_word)
            #     story += " " + next_word
            #     print(story)
            # except KeyError as error:
            #     try:
            #         next_word = generateTagGram(tag_ngrams, tags_dict, story)
            #         print("NEXT WORD", next_word)
            #         story += " " + next_word
            #         print(story)
            #     except:
            #         print("NEW STORY")
            #         break

            if order != target_order:
                order += 1
                tag_ngrams,word_ngrams, corpus_lst, tags_dict = process_corpus(corpus)


def generateTagGram(ngrams, tags_dict, story):

    text_lst = nltk.word_tokenize(story)
    text_lst = nltk.pos_tag(text_lst)
    currGram= text_lst[len(text_lst)-order:len(text_lst)]
    tags_currGram = ""
    for i in range(len(currGram)):
        if i != len(currGram) - 1:
            tags_currGram += currGram[i][1] + " "
        else:
            tags_currGram += currGram[i][1]
    print(tags_currGram)
    # currGram = space.join(currGram)
    # result = currGram.split()
    possibilities = ngrams[tags_currGram]
    print(possibilities)
    next_tag = random.choice(possibilities)
    possible_words = tags_dict[next_tag]
    next_word = random.choice(possible_words)
    return next_word



def process_corpus(file_name):
    print("ORDER:", order)
    f = open(file_name, "r")

    #reading file and storing tokenized and tagged word info
    corpus = f.read()
    tokens = nltk.word_tokenize(corpus)
    tags = nltk.pos_tag(tokens)

    #initializing dicts of words and tags
    word_ngrams = {}
    tag_ngrams = {}

    #iterating through text to generate ngrams
    for i in range(len(tags) -(order)):

        word_gram = []
        tag_gram = []

        #create the string of ngrams
        for j in range(order):
            word_gram.append(tags[i+j][0])
            tag_gram.append(tags[i+j][1])

        #create string out of list
        word_gram_string = space.join(word_gram)
        tag_gram_string = space.join(tag_gram)

        #create key-word pair in word_ngrams
        if word_gram_string not in word_ngrams.keys():
            word_ngrams[word_gram_string] = [tags[i+order][0]]
        else:
            word_ngrams[word_gram_string].append(tags[i+order][0])

        #create key-tag pair in tag_grams
        if tag_gram_string not in tag_ngrams.keys():
            tag_ngrams[tag_gram_string] = [tags[i+order][1]]
        else:
            tag_ngrams[tag_gram_string].append(tags[i+order][1])

    tags_dict = generateTagDict(tags)
    return tag_ngrams, word_ngrams, tokens, tags_dict

def generateTagDict(tags):
    tags_dict = {}
    for item in tags:
        if item[1] not in tags_dict:
            tags_dict[item[1]] = [item[0]]
        else:
            tags_dict[item[1]].append(item[0])
    return tags_dict


def markovIt(ngrams, story):

    text_lst = story.split()
    currGram= text_lst[len(text_lst)-order:len(text_lst)]
    currGram = space.join(currGram)
    result = currGram.split()
    possibilities = ngrams[currGram]
    next = random.choice(possibilities)
    return next


def  intro():
    print("Welcome to One Word Stories - you type a word, the program responds with  another and you make a story together!")
    print("Type END to quit whenever")

main()
