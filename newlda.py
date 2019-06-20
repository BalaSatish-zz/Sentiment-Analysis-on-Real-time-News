from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

def lda(paralist):
    tokenizer = RegexpTokenizer(r'\w+')
    # create English stop words list
    en_stop = get_stop_words('en')

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    # create sample documents
    # doc_a = 'washington the united states and india on wednesday agreed to strengthen security and civil nuclear cooperation including building six us nuclear power plants in india the two countries said in a joint statementthe agreement came after two days of talks in washington the united states under president donald trump has been looking to sell more energy products to india the worlds third biggest buyer of oilthe talks involved indian foreign secretary vijay gokhale and andrea thompson the us undersecretary of state for arms control and international securitythey committed to strengthen bilateral security and civil nuclear cooperation including the establishment of six us nuclear power plants in india the joint statement saidit gave no further details of the nuclear plant projectthe two countries have been discussing the supply of us nuclear reactors to energy hungry india for more than a decade but a longstanding obstacle has been the need to bring indian liability rules in line with international norms which require the costs of any accident to be channelled to the operator rather than the maker of a nuclear power stationpittsburgh based westinghouse has been negotiating to build reactors in india for years but progress has been slow partly because of indias nuclear liability legislation and the project was thrown into doubt when westinghouse filed for bankruptcy in  after cost overruns on us reactorscanadas brookfield asset management bought westinghouse from toshiba in august  last april westinghouse received strong support from us energy secretary rick perry for its india project which envisaged the building of six ap reactors in the state of andhra pradeshthe agreement to build the reactors announced in  followed on from a us india civil nuclear agreement signed in india plans to triple its nuclear capacity by  to wean asias third largest economy off polluting fossil fuelslast october india and russia signed a pact to build six more nuclear reactors at a new site in india following summit talks between their leaders in new delhi'
    # doc_b = 'the us has agreed to build six atomic power plants in india to strengthen bilateral security and civil nuclear cooperation and expressed its strong support to indias early membership in the nsg  the two countries said this in a joint statement issued at the conclusion of the th round of india us strategic security dialogue co chaired by foreign secretary vijay gokhale and andrea thompson the us under secretary of state for arms control and international security on wednesday  they committed to strengthen bilateral security and civil nuclear cooperation including the establishment of six us nuclear power plants in india the joint statement said without giving details of the sites  india and the us signed a historic agreement to cooperate in civil nuclear energy sector in october  the deal gave a fillip to bilateral ties which have been on an upswing since  a major aspect of the deal was the nuclear suppliers group nsg that gave a special waiver to india enabling it to sign cooperation agreements with a dozen countries  post waiver india signed civil nuclear cooperation agreements with the us france russia canada argentina australia sri lanka the uk japan vietnam bangladesh kazakhstan and south korea  on wednesday the united states also reaffirmed its strong support to indias early membership in the  member the nsg china has blocked indias pending membership to the elite grouping that seeks to prevent proliferation of nuclear weapons  during the meeting the two sides exchanged views on a wide range of global security and non proliferation challenges and reaffirmed their commitment to work together to prevent the proliferation of weapons of mass destruction and their delivery systems and to deny access to such weapons by terrorists and non state actors  on march  indra mani pandey indias additional secretary for disarmament and international security affairs and yleem ds poblete us assistant secretary of state for arms control verification and compliance co chaired the third round of india us space dialogue  the two delegations discussed trends in space threats respective national space priorities and opportunities for cooperation bilaterally and in multilateral fora'
    # doc_c = "new delhi and washington have agreed on a proposal to build six nuclear power plants in indiathis was stated in a joint statement issued on march  at the conclusion of the th round of india us strategic security dialogue in washington co chaired by foreign secretary vijay gokhale and under secretary of state for arms control and international security andrea thompsonthey committed to strengthen bilateral security and civil nuclear cooperation including the establishment of six us nuclear power plants in india the joint statement saidindia and the us signed a historic agreement to cooperate in civil nuclear energy in october  the deal gave a fillip to bilateral ties which have been on an upswing sincea major aspect of the deal was the nuclear suppliers group nsg that gave a special waiver to india enabling it to sign cooperation agreements with a dozen countriesagreements signed with many nationspost waiver india signed civil nuclear cooperation agreements with the us france russia canada argentina australia sri lanka the uk japan vietnam bangladesh kazakhstan and south koreaon march  the us reaffirmed its strong support to indias early membership in the  member nsg notably china has blocked indias pending membership to the elite grouping that seeks to prevent proliferation of nuclear weaponsduring the meeting the two sides exchanged views on a wide range of global security and non proliferation challenges and reaffirmed their commitment to work together to prevent proliferation of weapons of mass destruction and their delivery systems and to deny access to such weapons by terrorists and non state actorson march  indra mani pandey indias additional secretary for disarmament and international security affairs and yleem d s poblete us assistant secretary of state for arms control verification and compliance co chaired the third round of india us space dialoguethe two delegations discussed trends in space threats respective national space priorities and opportunities for cooperation bilaterally and in multilateral fora"
    # doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
    # doc_e = "Health professionals say that brocolli is good for your health."
    #
    # compile sample documents into a list
    #doc_set = [doc_a, doc_b, doc_c]
    doc_set = paralist
    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]

        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        # add tokens to list
        texts.append(stemmed_tokens)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=40)
    ldaresult = ldamodel.print_topics(num_topics=2, num_words=4)
    print(ldaresult)
    topicslist=[]
    for tuple in ldaresult:
        topics = str(tuple[1]).split('"')
        i=0
        print(topics)
        for i in range(len(topics)):
            if i%2==1:
                if topics[i] not in topicslist:
                    topicslist.append(topics[i])
    print(topicslist)
    return topicslist
