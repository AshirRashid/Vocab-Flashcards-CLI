import os, json
def update():
    from notion.client import NotionClient
    import os
    import json

    token = os.environ['notion_token']
    url = 'https://www.notion.so/4f0880b990674088ac92d44da6f143f3?v=f31e764d63aa47ee858c0940e220d75c'
    client = NotionClient(token_v2=token)
    page = client.get_block(url)

    words = []
    meanings = []
    sentences = []

    for row in page.collection.get_rows():
        sentence = ' '.join(row.Usage.split('\n'))
        meaning = ' '.join(row.Meaning.split('\n'))
        word = ' '.join(row.Word.split('\n'))
        if not word:
            word = 'No Entry Found'
        if not sentence:
            sentence = 'No Entry Found'
        if not meaning:
            meaning = 'No Entry Found'
        words.append(word)
        meanings.append(meaning)
        sentences.append(sentence)

    if len(words) != len(meanings) or len(meanings) != len(sentences):
        print('**THERE ARE UNEQUAL AMOUNT OF WORDS, MEANING, AND SENTENCE.**')
    else:
        print('number of words:', len(words))

        with open('vocab', 'wt') as file:
            to_store = dict(
                            zip( words, zip(meanings, sentences) )
                            )
            json.dump(to_store, file)



if __name__ == '__main__':
    update()
