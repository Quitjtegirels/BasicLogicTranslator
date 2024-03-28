# Library
import re

# Tokenizer
def logic_proposition_tokenizer(sentence):
    pattern = "([&↔\*→]|[Pp]rovided that|[Gg]iven that|[Jj]ust in case|[Oo]n the condition that|[aA]ssuming that|[Oo]nly if|providedthat|onlyif)"
    tokenized_logical_sentences = re.split(pattern, sentence)
    return tokenized_logical_sentences

# Negation translation
def negator(tokenized_logical_sentences): #the algorithm makes uses of tokenizer, negator negates each proposition separately
    negations = ["don't", "doesn't", "not", "does not", "do not", "didn't", "did not","no"]
    Intct = "[Ii]t is not the case that"
    negated_sentences = []
    for atom in tokenized_logical_sentences:
        negated_sentence = atom
        for negs in negations:
            if negs in atom:
                prenegated_sentence = re.sub(negs, "", atom.strip())
                very_negated_sentence = re.sub("  ", " ", prenegated_sentence)
                negated_sentence = "¬" + very_negated_sentence
        negated_sentences.append(negated_sentence)
    negator_string = "".join(negated_sentences)

    return negator_string
# Provided that translation
def prov_that(no_space_prop): 
  prov_pattern1 = "(?<=^providedthat¬[p-z][&↔\*→]¬[p-z])"
  prov_pattern2 = "(?<=^providedthat[p-z][&↔\*→]¬[p-z])"
  prov_pattern3 = "(?<=^providedthat¬[p-z][&↔\*→][p-z])"
  prov_pattern4 = "(?<=^providedthat[p-z][&↔\*→][p-z])"
  prov_pattern5 = "(?<=^providedthat[p-z])"
  prov_pattern6 = "(?<=^providedthat¬[p-z])"
  prov_process1 =re.sub(prov_pattern1,"→",no_space_prop)
  prov_process2 =re.sub(prov_pattern2,"→",prov_process1)
  prov_process3 =re.sub(prov_pattern3,"→",prov_process2)
  prov_process4 =re.sub(prov_pattern4,"→",prov_process3)
  prov_process5 =re.sub(prov_pattern6,"→",prov_process4)
  prov_process6 =re.sub(prov_pattern5,"→",prov_process5)
  prov_process7 =re.sub("(?<!^)providedthat","↓",prov_process6)  
  prov_del =re.sub("providedthat","",prov_process7)
  return prov_del


# Only if translator
def only_if(prov_del):
  only_pattern1="(?<=^onlynecc¬[p-z][&↔\*→]¬[p-z])"
  only_pattern2="(?<=^onlynecc[p-z][&↔\*→]¬[p-z])"
  only_pattern3="(?<=^onlynecc¬[p-z][&↔\*→][p-z])"
  only_pattern4="(?<=^onlynecc[p-z][&↔\*→]¬[p-z])"
  only_pattern5="(?<=^onlynecc[p-z])"
  only_pattern6="(?<=^onlynecc[p-z])"
  only_process1 =re.sub(only_pattern1,"↓",prov_del)
  only_process2 =re.sub(only_pattern2,"↓",only_process1)
  only_process3 =re.sub(only_pattern3,"↓",only_process2)
  only_process4 =re.sub(only_pattern4,"↓",only_process3)
  only_process5 =re.sub(only_pattern5,"↓",only_process4)
  only_process6 =re.sub(only_pattern6,"↓",only_process5)
  only_process7 =re.sub("(?<!^)onlynecc","→",only_process6)
  only_if_del = re.sub("onlynecc","",only_process7)
  return only_if_del


# The main function in use
def LogicTranslator(sentence):
    sentence = input("Enter your complete sentence: ")
    soa = {}
    n = int(input("How many symbolic letters do you need for your translation? "))
    for i in range(n): 
          soa_proposition = input("Enter the sentence letter, from p to z: ")
          soa_sentence = input("Enter the corresponding English sentence: ")
          soa[soa_proposition] = soa_sentence
    # Basic connective translations starts
    sentence_without_punctuation = re.sub("[!,;]", "", sentence)
    iff_translatedsentence = re.sub("if and only if|just in case", "↔", sentence_without_punctuation)
    and_translate_sentence = re.sub(" and | but |who|which", "&", iff_translatedsentence)
    or_translatedsentence = re.sub(" or |unless| nor ", "*", and_translate_sentence)
    or_translate_sentence_2 = re.sub("^[Ee]ither|\s[Ee]ither", "", or_translatedsentence)
    only_if_pattern_reg = re.sub("[Oo]nly if","onlynecc",or_translate_sentence_2)
    provided_that_translation = re.sub(
        "[Gg]iven that|[Oo]n the condition that|[aA]ssuming that|[Ii]n case|[Pp]rovided that",
        "providedthat", only_if_pattern_reg)
    if_pattern = "[tT]hen"
    if_step1_translatedsentence = re.sub("[Ii]f\s", "", provided_that_translation)
    if_final_pattern = re.sub(if_pattern, "→", if_step1_translatedsentence)
    Intct_neg = re.sub("[Ii]t is not the case that\s*", "¬?", if_final_pattern)
    nnt_neg = re.sub("[Nn]either|[Nn]ot both", "¬??", Intct_neg)
    # tokenization
    tokenized_sentence = logic_proposition_tokenizer(nnt_neg)
    # negation
    negated_sentence = negator(tokenized_sentence)
    # Propositional translation
    propos_trans = negated_sentence
    for symbol, sent in soa.items():
          propos_trans = re.sub(sent, symbol, propos_trans)
    # stylistic variant
    no_space_prop = re.sub(" ","",propos_trans)
    prov_that_trans = prov_that(no_space_prop)
    only_if_trans = only_if(prov_that_trans)
    conc_trans = re.sub("[tT]herefore","∴",only_if_trans)
    return conc_trans

print(LogicTranslator("sentence"))
print("""¬?: denotes an one-place negation(it is not the case), and its scope is not clear \n¬??: denotes a two-place negation(neither, not both) and its scope is not clear \n"↓": denotes "<-" left-hand implication, p↓q is equivalent to q->p) 
""")
