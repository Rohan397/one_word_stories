import random
import nltk
import string
import os
# from gtts import gTTS
import pyttsx3
import speech_recognition as sr
r = sr.Recognizer()

space = " "
engine = pyttsx3.init()
def give_introduction():
    """
    inputs:  none
    returns: start (int) - whether player or program starts game
    purpose: gives introduction to game and allows user to decide who starts
             story
    """
    engine.say("Hi! I am a program to help you develop your improv skills")
    print("Hi! I am a program to help you develop your improv skills")
    engine.say("I will play one word stories with you! Here are the rules: ")
    print("I will play one word stories with you! Here are the rules: ")
    engine.say("1) Each of us can only say one word at a time.")
    print("1) Each of us can only say one word at a time.")
    engine.say("2) To start a new story, say 'NEW STORY'.")
    print("2) To start a new story, say 'NEW STORY'.")
    engine.say("3) To stop the game say 'EXIT GAME'.")
    print("3) To stop the game say 'EXIT GAME'.")
    engine.say("4) You start every story!")
    print("4) You start every story!")
    engine.runAndWait()




def get_corpus(file):
    """reads file and returns the corpus in form of list with pos_tag for each word"""

    f = open(file, "r")
    corpus = f.read()
    tokens = nltk.word_tokenize(corpus)
    tags = nltk.pos_tag(tokens)
    return tags

def generateTagDict(tags, tag_dict):
    """generates a dict mapping post_tags to words with that pos_tag"""

    for tuple in tags:
        if tuple[1] not in tag_dict:
            tag_dict[tuple[1]] = [tuple[0]]
        else:
            tag_dict[tuple[1]].append(tuple[0])


def process_corpus(tags, order, wordOrTag):
    """
    inputs:  tags - the list of words and associated tags
             order - the order of the ngram to build
             wordOrTag - flag saying whether to build ngram word (0) or tag(1)
    returns: tag_gram (dict) - contains ngrams for sentence structure
             tag_dict (dict) - a dictionary mapping tags to words with the tag
             next_words (dict) - maps tuple of prev word and next tag to next word
    purpose: processes the corpus to have a list of ngrams ready before game begins
    """
    ngrams = {}

    for i in range(len(tags) - order):
        gram = []

        for j in range(order):
            gram.append(tags[i+j][wordOrTag])

        gram_string = space.join(gram)
        if gram_string not in ngrams:
            ngrams[gram_string] = [tags[i+order][wordOrTag]]
        else:
            ngrams[gram_string].append(tags[i+order][wordOrTag])

    return ngrams

def markovIt(ngrams, story, order, wordOrTag):
    """goes through ngrams and picks the next state to generate"""
    tokens = nltk.word_tokenize(story)
    tags = nltk.pos_tag(tokens)
    currGram= tags[len(tags)-order:len(tags)]
    text_lst = []
    for i in range(order):
        text_lst.append(currGram[i][wordOrTag])

    currGram = space.join(text_lst)
    possibilities = ngrams[currGram]
    next = random.choice(possibilities)
    return next


def main():
    target_order = 4
    backup_order = 1
    give_introduction()

    #processing corpus
    tags_dict = {}
    corpus = "corpora/Cinderella.txt"
    tags = get_corpus(corpus)
    generateTagDict(tags, tags_dict)
    word_ngrams   = process_corpus(tags, target_order, 0)
    target_ngrams = process_corpus(tags, target_order, 1)
    backup_ngrams = process_corpus(tags, backup_order, 1)

    #game loop
    story = ""
    game_over = False
    with sr.Microphone() as source:
        while game_over == False:
            new_story = False
            try:
                print("say your word")
                audio = r.listen(source, timeout = 3)
                print("time over.")
                user_word = r.recognize_google(audio)
                print("TEXT: " + user_word)
            except:
                engine.say("You ran out of time - we'll restart a new story")
                engine.runAndWait()
                story = ""
                new_story = True

            if new_story == False:
                if user_word == "exit game":
                    game_over = True

                elif user_word ==  "new story":
                    story = ""

                else:
                    story += user_word + space
                    try:
                         next_word = markovIt(word_ngrams, story, target_order,0)
                    except:
                        try:
                            next_tag = markovIt(target_ngrams, story, target_order, 1)
                            next_word = random.choice(tags_dict[next_tag])
                        except:
                            next_tag = markovIt(backup_ngrams, story, backup_order,1)
                            next_word = random.choice(tags_dict[next_tag])


                    engine.say(next_word)
                    engine.runAndWait()
                    engine.stop()
                    story += next_word + space
                    print(story)

    engine.say("thanks for playing with me. I hope it was a fun story!")
    engine.runAndWait()
    engine.stop()
main()
