from cli_parser import parser
from gensim import corpora, models, similarities
from nltk import word_tokenize
from nltk.corpus import stopwords
from itertools import chain
import os
import glob
import os
import warnings
warnings.filterwarnings("ignore")
from gensim import corpora
import gensim
from itertools import chain
import pandas as pd
import re
from nltk.corpus import stopwords
from pathlib2 import Path
import shutil

from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words('english')) 

# create clustered topic directories 
def create_output_dir(old_path,doc_names,num):
    output_path = os.path.join(old_path,"output")
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    topic_name = "topic%d"%(num+1)
    for doc_name in doc_names:
        doc_name = '/'+doc_name
        dest_path = os.path.join(output_path,topic_name)
        if not os.path.isdir(dest_path):
            os.mkdir(dest_path)
        shutil.copyfile(old_path+doc_name, dest_path+doc_name)
        
def topic_model_build(path):

    os.chdir(path)
    documents = []
    for filename in glob.glob("*.txt"):
        data = Path(filename).read_text()
        documents.append(filename + data)

    ls = documents
    ls = [re.sub(r'(citation)','',x, flags=re.I) for x in ls]

    # remove common words and tokenize
    texts = []
    for i in range(len(ls)):

        raw = str(ls[i]).lower()
        tokens = word_tokenize(raw)
        stopped_tokens = [i for i in tokens if not i in stop_words]
        greaterone_tokens = [i for i in stopped_tokens if len(i) > 1]
        stemmed_tokens = [WordNetLemmatizer().lemmatize(i) for i in greaterone_tokens]
        texts.append(stemmed_tokens)

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    num_topics = 5
    lda = gensim.models.ldamodel.LdaModel(corpus,num_topics=num_topics,id2word=dictionary,chunksize=500,passes=50,
                                              iterations = 10,update_every = 1,minimum_probability = 0)

    topics_ls = []
    # Prints the topics.
    for top in lda.print_topics():
        topics_ls.append(re.findall(r'"(.*?)"',str(top)))
    
    # Writing topics to text file
    topics_file = open('Topics_List.txt', 'w')
    for item in topics_ls:
        topics_file.write("%s\n" % item)
    
    # Assigns the topics to the documents in corpus
    lda_corpus = lda[corpus]

    # Find the threshold, let's set the threshold to be 1/#clusters,
    # To prove that the threshold is sane, we average the sum of all probabilities:
    scores = list(chain(*[[score for topic_id,score in topic] \
                          for topic in [doc for doc in lda_corpus]]))
    threshold = sum(scores)/len(scores)
    
    cluster_ls = []
    for z in range(0,num_topics):
        cluster = [j for i,j in zip(lda_corpus,documents) if i[z][1] > threshold]
        cluster_ls.append(cluster)
    
    cluster_doc_keys = []
    for each_cluster in cluster_ls:
        cluster_doc_keys.append([re.search(r'.*?\.txt',x).group() for x in each_cluster])
    
    # create clustered topic directories 
    for num,each in enumerate(cluster_doc_keys):
        create_output_dir(path,each,num)




def main():

    # parse all the command line arguments
    args = parser.parse_args()

    # validate the path passed in the argument
    if(not os.path.isdir(args.path)):
        raise NotADirectoryError(args.path);

    # create the requried directories
    topic_model_build(args.path)

if __name__ == '__main__':
  main()
