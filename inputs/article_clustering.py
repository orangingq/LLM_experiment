from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, DBSCAN
import numpy as np
import json
from sklearn.metrics import pairwise_distances_argmin_min
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from gensim.models import Word2Vec as WV
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Korean Text Preprocess
def preprocess(texts):
    okt = Okt()
    stop_words = "등 탓 것 이미 의 에서 이 얼마나 했다 말 해야 한다 . 관련 앞서 통해 현재 좀 약 경우 중 별도 고 이번 처음 전 현 초 로 모두 무엇 인지 크게 뒤 오늘 날 정도 것일 및 위해 답 첫날 위 면서 다음 포함 며 대한 먼저 대상"
    stop_words += " 더 시작 영향 의견 내용 매우 번 뜻 를 우리 후 도 때문 지난 또 대해 그 직후 우려 지난해 단지 내 나 차 수 따라서 곧바로 불 안 순간 그냥 점 통한 최고 주요 모든 동안 수년 최근 지난달 문제 설명 속 건 년 이하 이상"
    stop_words += " 밤 기간 데 가장 제 보도 연합뉴스 서울신문 미만 부터 까지 확인 지적 마지막 개 동시 향후 라며 곳 다른 밑 지속 기여 과정 올해 첫 진행 상황 바로 상대로 photo 명 애초 하니 생각 앞 여 때마침 저 과"
    stop_words = set(stop_words.split(' '))
    word_tokens = [okt.nouns(text) for text in texts]
    result = [(word for word in text if not word in stop_words) for text in word_tokens]
    return [[str(word) for word in text] for text in result]



# Text Vectorization, Normalization
def vectorize(texts):
    vectorizer = TfidfVectorizer(min_df=3, max_features=50000, ngram_range=(1,2))
    return vectorizer.fit_transform(texts)
    # print(len(texts), len(texts[0]))
    # model = WV(sentences = texts, size = 100, window = 5, min_count = 1, workers = 4)#, sg = 0
    # model.save("word2vec.model")
    # # model = WV.load("word2vec.model")
    
    # print(model.wv.vectors.shape)
    # print(model.wv.most_similar("카카오"))
        
    # features = []
    # for text in texts:
    #     zero_vector = np.zeros(model.vector_size)
    #     vectors = []
    #     for token in text:
    #         if token in model.wv:
    #             try:
    #                 vectors.append(model.wv[token])
    #             except KeyError:
    #                 continue
        
    #     if vectors:
    #         vectors = np.asarray(vectors)
    #         avg_vec = vectors.mean(axis=0)
    #         features.append(avg_vec)
    #     else:
    #         features.append(zero_vector)
        
    #     # print(np.array(features).shape)
    # scaler = StandardScaler() #MinMaxScaler()
    # features [:] = scaler.fit_transform(features)
    # return features


# Extract Central Article
def get_central_sentences(vectors, kmeans):
    centroids = kmeans.cluster_centers_
    closest_points, _ = pairwise_distances_argmin_min(centroids, vectors)
    return closest_points
    # central_sentences = [original_texts[index] for index in closest_points]
    # return central_sentences


# Visualization
def visualize_clusters(vectors, labels):
    # 1. Dimensionality reduction
    reduced_data = PCA(n_components=2).fit_transform(vectors.toarray())
    
    # 2. Visualization
    k = len(set(labels))
    length = vectors.shape[0]#len(vectors) #vectors.shape[0]
    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=labels, cmap='rainbow')
    plt.colorbar(ticks=range(len(set(labels))))
    plt.title(f"K-means Clustering of {length} Articles (k={k})")
    plt.savefig('./inputs/article_clusters.png')

def kmeans_clustering(vectors, k=-1):
    
    # print(np.array(vectors).shape)
    if k < 0:
        length = len(vectors) # vectors.shape[0]
        k = int(length / 25) # k: cluster 수
    print(f"total: {length}, kmeans clustering: k = {k}")
        
    # kmeans clustering
    kmeans = KMeans(init='k-means++', n_clusters=k, n_init=100)
    kmeans.fit(vectors)
    labels = kmeans.labels_

    # extract main articles
    central_indices = get_central_sentences(vectors, kmeans)
    
    return labels, central_indices

def DBSCAN_clustering(vectors):
    model = DBSCAN(eps=0.5, min_samples=4, metric = "cosine") #eps=0.3,
    # 거리 계산 식으로는 Cosine distance를 이용
    result = model.fit_predict(vectors)
    # print(result)
    result[result == 0] = -1
    return result


def article_clustering(k=-1):    
    files = [
        'inputs/articles/articles_297to981.json',
        'inputs/articles/articles_982to2979.json',
        'inputs/articles/articles_2980to19991.json'
    ]
    total_articles = []
    outliers = []
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i, article in enumerate(data):
                if article['text_rank'][0] == "":
                    outliers += [i]
                else:
                    total_articles += [article['text_rank'][0]]#[' '.join(article['article'])]#[article['text_rank'][0]]
    
    
    
    # preprocess
    preprocessed = preprocess(total_articles)
    preprocessed_texts = []
    preprocessed_indices = []
    for i, t in enumerate(preprocessed):
        if t == '':
            outliers += [i]
        else:
            preprocessed_texts += [' '.join(t)]
            preprocessed_indices += [i]

    print(f"preprocessed texts ({len(preprocessed_texts)}): {preprocessed_texts[40]}")
    print(f"\noutliers ({len(outliers)}): {outliers}")
    
    
    # vectorize
    text_vectors = vectorize(preprocessed_texts)
        
    # print(text_vectors)
    
    # clustering
    # result, central_indices = kmeans_clustering(text_vectors)
    result = DBSCAN_clustering(text_vectors)
    print(result)
    # visualize
    visualize_clusters(text_vectors, result)
        
    noise_cnt = 0
    for cluster_num in set(result):
        # -1,0은 노이즈 판별이 났거나 클러스터링이 안된 경우
        if cluster_num == -1: 
            for i, label in enumerate(result):
                if label == cluster_num:
                    noise_cnt += 1
            continue
        else:
            # print(cluster_num, central_indices[cluster_num], preprocessed_indices[central_indices[cluster_num]], total_articles[preprocessed_indices[central_indices[cluster_num]]])
            print(f"\ncluster num : {cluster_num}")# - {total_articles[preprocessed_indices[central_indices[cluster_num]]]}")
            for i, label in enumerate(result):
                if label == cluster_num:
                    print(f"Text {i}: {total_articles[i][:70]}")
    print("\nnoise count: " , noise_cnt)
    
    # print(central_indices)
    
article_clustering()