import matplotlib.pyplot as plt
from wordcloud import WordCloud

with open('topics_trace_backup') as f:
	lines = f.readlines()

def terms_to_wordcounts(terms, multiplier=100000):
    return  " ".join([" ".join(int(multiplier*i[1]) * [i[0]]) for i in terms])

def make_image(terms, image_name):

    freqs = []
    for score, word in terms:
        freqs.append((word.split('/')[0], score))

    text = terms_to_wordcounts(freqs)

    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")

    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(image_name)

for i, line in list(enumerate(lines))[::2]:
	words = line.split(' ')[3::2]
	words = [tuple(word.split('*')) for word in words]
	words = [(float(score), word.split('/')[0]) for score, word in words]
	name = 'topic' + str(i) + '.png'
	print name
	make_image(words, name)

