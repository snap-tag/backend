from spellchecker import SpellChecker


spell = SpellChecker()

def generate_tags(nlp, texts: str):
    # print(corrected_text)
    entities = None
    print(texts)
    corrected_text = []
    for word in texts.split(" "):
        try:
            corrected_word = spell.correction(word)
            if corrected_word is not None and corrected_word not in corrected_text:
                corrected_text.append(str(corrected_word))
        except ValueError:
            continue
    corrected_text = ' '.join(corrected_text)
   
    # doc = nlp(corrected_text)

    # entities = [ent.text for ent in doc.ents]

    return entities if entities is not None else corrected_text.split(" ")