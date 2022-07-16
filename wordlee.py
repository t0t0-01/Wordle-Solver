import string
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import random






def load_words():
    f = open("./data/used.txt", "r")
    words = {e.strip().lower() for e in f.readlines()}
    f.close()
    return words
                

def filter_words(words, incorrect, false_loc, correct_loc, duplicates):
    """
    

    Parameters
    ----------
    words : TYPE
        DESCRIPTION.
    incorrect : TYPE
        DESCRIPTION.
    false_loc : TYPE
        DESCRIPTION.
    correct_loc : TYPE
        DESCRIPTION.
    duplicates : TYPE
        DESCRIPTION.

    Returns
    -------
    updated_words : TYPE
        DESCRIPTION.

    """
    updated_words = words.copy()
    for word in words:
        removed = False
        for wrong_letter in incorrect:
            if wrong_letter in word:
                updated_words.remove(word)
                removed = True
                break
                
                
        if not removed:
            for letter, pos in false_loc:
                    if word[pos] == letter or letter not in word:
                        updated_words.remove(word)
                        removed = True
                        break
                    
                
                        
            if not removed:
                for letter, pos in correct_loc:
                    if word[pos] != letter:
                        updated_words.remove(word)
                        removed = True
                        break
            
            if not removed:
                    for letter in duplicates:
                        if letter[1] != word.count(letter[0]):
                            updated_words.remove(word)
                            removed = True
                            break

        
                    
    return updated_words
    

def generate_probabilities(words):
    """
    Takes as input a list of words, and outputs a probability distribution for
    the words based on the frequency of occurence of the letters
    

    Parameters
    ----------
    words : list
        list of words to generate a probability distribution from.

    Returns
    -------
    word_probs : dict
        {'word': (prob, nb_of_unique_letters)}

    """
    
    
    letters = {e: 0 for e in list(string.ascii_lowercase)}
    for word in words:
        for char in word:
            letters[char] += 1
            
            
    letter_probs = {e: letters[e] / len(words) for e in letters}
    
    word_probs = {"test": (0,0)}
    m = "test"
    for word in words:
        word_prob = 1
        for char in word:
            word_prob *= letter_probs[char]
        word_probs[word] = (word_prob, len(set(word)))
        if word_prob > word_probs[m][0]:
            m = word

    updated = {}
    for e in word_probs:
        if word_probs[e][1] == 5:
            updated[e] = word_probs[e]

    j = "test"
    for e in updated:
        if word_probs[e][0] > word_probs[j][0]:
            j = e
        
    return word_probs


def get_max_probability(pd, words):
    """
    Takes a list of words and probability distribution, and outputs the word
    with the highest probability of occurence

    Parameters
    ----------
    pd : dict
        Probability distribution of words
    words : list
        List of words

    Returns
    -------
    max_prob : float
        The highest probability of occurence
    max_word : string
        The word that has the highes probability of occurence

    """
    
    max_prob = 0
    max_word = ""
    for w in words:
        if pd[w][0] > max_prob:
            max_prob = pd[w][0]
            max_word = w
            
    return max_word, max_prob
    
    
def run_iters(answer, pd_function, threshold=6):
    probs = generate_probabilities(load_words())
    
    ##add the first one to the iters list
    iters = []
    word = "alert"
    set1 = load_words()
    prob = 1
    prev_word = ""
    messages = []
    


    while len(iters) <= 5 and prev_word != word:
        iters.append((word, prob))
        prev_word = word
        
        result = get_result(word,answer)
        messages.append(result[-1])
        
        set1 = filter_words(set1, *result[:-1])
        
        if pd_function == "max":
            word, prob = get_max_probability(probs, set1)
        elif pd_function == "max_unique":
            if len(iters) < threshold:
                word, prob = get_max_probability_uniqueness(probs, set1)
            else:
                word, prob = get_max_probability(probs, set1)
                                                 
        
    if prev_word != word:
        iters.append("WRONG")
        iters.append(answer)
        iters.append(answer in pd_function)
        
    output_message = f"Wordle {wordle_id} {len(messages)}/6\n\n"
    for m in messages:
        output_message += m + "\n"

    return iters, output_message
    
    
def get_result(guess, correct_word):
    incorrect = []
    false_loc = []
    correct_loc = []
    duplicates = []
    color_message = ""
    
    to_be_checked = {}
    
    for pos, char in enumerate(guess):
        if char not in correct_word:
            incorrect.append(char)
            color_message += "⬜"
            
        elif guess.count(char) == correct_word.count(char):
            if correct_word[pos] == char:
                correct_loc.append((char, pos))
                color_message += "🟩"
            else:
                false_loc.append((char, pos))
                color_message += "🟨"
        else:
            if char not in to_be_checked:
                to_be_checked[char] = [pos]
            else:
                to_be_checked[char].append(pos)
            
            
            

    for char in to_be_checked:
        correct_count = 0
        left = []
        has_duplicates = False
        for pos in to_be_checked[char]:
            
            if correct_word[pos] == char:
                correct_loc.append((char, pos))
                color_message = color_message[:pos] + "🟩" + color_message[pos:]
                correct_count += 1
            else:
                left.append(pos)

        for other in left:
            if correct_count != correct_word.count(char):
                false_loc.append((char, other))
                color_message = color_message[:pos] + "🟨" + color_message[pos:]
                correct_count += 1
            else:
                has_duplicates = True
                
            
        if has_duplicates:
           duplicates.append((char, correct_count))
           color_message += "⬜"
           
    
        

    return incorrect, false_loc, correct_loc, duplicates, color_message


def get_max_probability_uniqueness(pd, words):
    """
    Takes a list of words and probability distribution, and outputs the word
    with the highest probability of occurence that also has highest uniqye

    Parameters
    ----------
    pd : dict
        Probability distribution of words
    words : list
        List of words

    Returns
    -------
    max_prob : float
        The highest probability of occurence
    max_word : string
        The word that has the highes probability of occurence
    """

    max_unique = max([pd[e][1] for e in pd if e in words])
    subset = {e: pd[e] for e in pd if pd[e][1] == max_unique}
    
    
    # if len(words) < 15 and len(words) > 2:
    #     smaller_list = generate_probabilities(words)
    #     equal = True
    #     choice = random.choice(list(smaller_list))
    #     for e in smaller_list:
    #         if smaller_list[choice] != smaller_list[e]:
    #             equal = False
    #             break
    #     if equal:
    #         letters = []
    #         for e in smaller_list:
    #             for pos, char in enumerate(choice):
    #                 if smaller_list[e][pos] != char:
    #                     letters.append(char)
                        
            
            
    
    max_prob = 0
    max_word = ""
    for w in words:
        if w in subset and subset[w][0] > max_prob:
            max_prob = subset[w][0]
            max_word = w
            
    return max_word, max_prob
    


def generate_weighted_probabilities(words, factor):
    """
    Takes as input a list of words, and outputs a probability distribution for
    the words based on the frequency of occurence of the letters. Also downweights
    
    

    Parameters
    ----------
    words : list
        list of words to generate a probability distribution from.
    
    factor: int
        

    Returns
    -------
    word_probs : dict
        {'word': (prob, nb_of_unique_letters)}

    """
    
    
    letters = {e: 0 for e in list(string.ascii_lowercase)}
    for word in words:
        for char in word:
            letters[char] += 1
            
            
    letter_probs = {e: letters[e] / len(words) for e in letters}
    
    word_probs = {"test": (0,0)}
    m = "test"
    for word in words:
        word_prob = 1
        
        
        
        for char in word:
            word_prob *= letter_probs[char]
        word_probs[word] = (word_prob, len(set(word)))
        
        
        
        if word_prob > word_probs[m][0]:
            m = word

    updated = {}
    for e in word_probs:
        if word_probs[e][1] == 5:
            updated[e] = word_probs[e]

    j = "test"
    for e in updated:
        if word_probs[e][0] > word_probs[j][0]:
            j = e
        
    return word_probs

# prev = ['field', 'sever', 'lilac', 'egret', 'pinto', 'hutch', 'gawky', 'droll', 'retro', 'rusty', 'beady', 'smite', 'brink', 'awful', 'gloat', 'input', 'loser', 'cacao', 'blown', 'apron', 'primo', 'atone', 'donor', 'float', 'goose', 'piety', 'girth', 'trait', 'flood', 'gloom', 'depth', 'froth', 'phase', 'showy', 'creak', 'manor', 'atoll', 'bayou', 'crept', 'tiara', 'asset', 'vouch', 'album', 'hinge', 'money', 'scrap', 'gamer', 'glass', 'scour', 'being', 'delve', 'yield', 'metal', 'tipsy', 'slung', 'farce', 'gecko', 'shine', 'canny', 'midst', 'badge', 'homer', 'train', 'story', 'hairy', 'forgo', 'larva', 'trash', 'zesty', 'shown', 'heist', 'askew', 'inert', 'olive', 'plant', 'oxide', 'cargo', 'foyer', 'flair', 'ample', 'cheek', 'shame', 'mince', 'chunk', 'royal', 'squad', 'black', 'stair', 'scare', 'foray', 'comma', 'natal', 'shawl', 'fewer', 'trope', 'snout', 'lowly', 'stove', 'shall', 'found', 'nymph', 'epoxy', 'depot', 'chest', 'purge', 'slosh', 'their', 'renew', 'allow', 'saute', 'movie', 'cater', 'tease', 'smelt', 'focus', 'today', 'watch', 'lapse', 'month', 'sweet', 'hoard', 'cloth', 'brine', 'ahead', 'mourn', 'nasty', 'rupee', 'choke', 'chant', 'spill', 'vivid', 'bloke', 'trove', 'thorn', 'other', 'tacit', 'swill', 'dodge', 'shake', 'caulk', 'aroma', 'cynic', 'robin', 'ultra', 'ulcer', 'pause', 'humor', 'frame', 'elder', 'skill', 'aloft', 'pleat', 'shard', 'moist', 'those', 'light', 'wrung', 'could', 'perky', 'mount', 'whack', 'sugar', 'knoll', 'crimp', 'wince', 'prick', 'robot', 'point', 'proxy', 'shire', 'solar', 'panic', 'tangy', 'abbey', 'favor', 'drink', 'query', 'gorge', 'crank', 'slump', 'banal', 'tiger', 'siege', 'truss', 'boost', 'rebus', 'unify', 'troll', 'tapir', 'aside', 'ferry', 'acute', 'picky', 'weary', 'gripe', 'craze', 'pluck', 'brake', 'baton', 'champ', 'peach', 'using', 'trace', 'vital', 'sonic', 'masse', 'conic', 'viral', 'rhino', 'break', 'triad', 'epoch', 'usher', 'exult', 'grime', 'cheat', 'solve', 'bring', 'prove', 'store', 'tilde', 'clock', 'wrote', 'retch', 'perch', 'rouge', 'radio', 'surer', 'finer', 'vodka', 'heron', 'chill', 'gaudy', 'pithy', 'smart', 'badly', 'rogue', 'group', 'fixer', 'groin', 'duchy', 'coast', 'blurt', 'pulpy', 'altar', 'great', 'briar', 'click', 'gouge', 'world', 'erode', 'boozy', 'dozen', 'fling', 'growl', 'abyss', 'steed', 'enema', 'jaunt', 'comet', 'tweed', 'pilot', 'dutch', 'belch', 'ought', 'dowry', 'thumb', 'hyper', 'hatch', 'alone', 'motor', 'aback', 'guild', 'kebab', 'spend', 'fjord', 'essay', 'spray', 'spicy', 'agate', 'salad', 'basic', 'moult', 'corny', 'forge', 'civic', 'islet', 'labor', 'gamma', 'lying', 'audit', 'round', 'loopy', 'lusty', 'golem', 'goner', 'greet', 'start', 'lapel', 'biome', 'parry', 'shrub', 'front', 'wooer', 'totem', 'flick', 'delta', 'bleed', 'argue', 'swirl', 'error', 'agree', 'offal', 'flume', 'crass', 'panel', 'stout', 'bribe', 'drain', 'yearn', 'print', 'seedy', 'ivory', 'belly', 'stand', 'first', 'forth', 'booby', 'flesh', 'unmet', 'linen', 'maxim', 'pound', 'mimic', 'spike', 'cluck', 'crate', 'digit', 'repay', 'sower', 'crazy', 'adobe', 'outdo', 'trawl', 'whelp', 'unfed', 'paper', 'staff', 'croak', 'helix', 'floss', 'pride', 'batty', 'react', 'marry', 'abase', 'colon', 'stool', 'crust', 'fresh', 'death', 'major', 'feign', 'abate', 'bench', 'quiet', 'grade', 'stink', 'karma', 'model', 'dwarf', 'heath', 'serve', 'naval', 'evade', 'focal', 'blush', 'awake', 'humph', 'sissy', 'rebut', 'cigar']
# wordss = [e for e in load_words() if e not in prev]


# s = []
# count = 0
# without_wrong = []
# overall = []
# wrong = 0
# words = load_words()
# wrongs = []

# for word in words:
#     count += 1
    
#     if count % 100 == 0:
#         print(count / len(words) * 100, "% done")
        
#     l = run_iters(word, "max")
#     if "WRONG" in l:
#         wrong += 1
#         count -= 1
#         wrongs.append(l)
#     else:
#         without_wrong.append(len(l))
    
#     s.append(len(l))
    
#     overall.append(l)
    
# plt.bar(list(set(s)), [s.count(e) for e in list(set(s))])
# plt.show()

# plt.boxplot(without_wrong)
# plt.show()

# converted = np.array(s)
    
# print("Min: ", np.min(converted))
# print("Max: ", np.max(converted))
# print("Mean: ", np.mean(converted))
# print("Std: ", np.std(converted))
# print("Median: ", np.median(converted))




# for i in range(1,5):
#     print(f"Nb of iterations = {i}:\n")
    
#     s = []
#     count = 0
#     without_wrong = []
#     overall = []
#     wrong = 0
#     words = load_words()
#     wrongs = []

#     for word in words:
#         count += 1

#         if count % 500 == 0:
#             print(count / len(words) * 100, "% done")


#         l = run_iters(word, "max_unique", i)
#         if "WRONG" in l:
#             wrong += 1
#             count -= 1
#             wrongs.append(l)
#         else:
#             without_wrong.append(len(l))

#         s.append(len(l))

#         overall.append(l)

#     plt.bar(list(set(s)), [s.count(e) for e in list(set(s))])
#     plt.title(f"Statistics with max uniqueness applied on {i} iterations")
#     plt.show()

#     plt.boxplot(without_wrong)
#     plt.title(f"Statistics with max uniqueness applied on {i} iterations")
#     plt.show()

#     converted = np.array(s)

#     print("Min: ", np.min(converted))
#     print("Max: ", np.max(converted))
#     print("Mean: ", np.mean(converted))
#     print("Std: ", np.std(converted))
#     print("Median: ", np.median(converted), "\n\n")

def run_daily():
    
    wordle_id = (date.today() - date(2022, 7, 17)).days + 393
    
    f = open("./data/list.txt", "r")
    words = [e.strip() for e in f.readlines()]
    f.close()
    return run_iters(words[wordle_id], "max_unique", 4)

#print(run_daily())