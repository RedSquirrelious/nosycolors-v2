lexicon = dict()

for line in open('exportedwords.csv'):
	word = line.split(';')[1].strip('"')
	word_id = line.split(';')[0]

	lexicon[word] = word_id

for line in open('word_emotion_score.csv'):
	line = line.strip()
	word = line.split(' ')[0]
	col2 = line.split(' ')[1]
	col3 = line.split(' ')[2]
	print(lexicon[word], col2, col3)


#MAKING THE WORD EMOTION JOIN TABLE, ADDS WORD ID TO WORD AND SCORE
cat csvtxt-NRC-Emotion-Lexicon-v0.92-Annotator-and-Sense-Level.txt | sed 's/-/ /g' | sed 's/, //g' | awk '{print $2, 5, $5; print $2, 6, $7; print $2, 4, $9; print $2, 1, $11; print $2, 8, $13; print $2,3, $15; print $2,7, $17; print $2,2, $19;}'| awk '{sum[$1" "$2] += $3}END{for(k in sum){print k, sum[k]}}' > word_emotion_score.csv

#MAKES THE WORD TABLE (WITH COUNTER)
cat csvtxt-NRC-Emotion-Lexicon-v0.92-Annotator-and-Sense-Level.txt | awk '{print $2}' | awk -F'--' '{print $1}' | sort | uniq -c 