"""
레포트 생성 관련 RAG 설정 및 유틸리티
"""
import openai
import redis
import uuid
import pickle
from typing import NewType
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.config import settings
from src.database.session import DATABASE_URL
# from src.api.report.report_constnats import 
import logging


_logger = logging.getLogger(__name__)
openai.api_key = settings.general.OPENAI_API_KEY




# 객체 생성 전 config 객체 생성하고 생성자에 embed_obj, llm_obj 넣기

class RaptorClustering:
    def __init__(self, embed_obj, llm_obj):
        self.random_seed = 42
        self.embed_obj = embed_obj
        self.llm_obj = llm_obj
        logger.info(f'[RAPTOR] RaptorClustering 초기화')

    def global_cluster_embeddings(
        self, embeddings: np.ndarray, dim: int, n_neighbors: Optional[int] = None, metric: str = "cosine",
    ) -> np.ndarray:
        """
        임베딩 값에 대해 UMAP을 사용하여 전역 차원에서의 축소 수행
        차원을 'dim'으로 축소하여 클러스터링을 더 쉽게 만듬.
        """
        if n_neighbors is None:
            n_neighbors = int((len(embeddings) - 1) ** 0.5)
        logger.info(f"[RAPTOR] 글로벌 UMAP 차원 축소 수행 - dim={dim}, n_neighbors={n_neighbors}, metric={metric}")
        return umap.UMAP(
            n_neighbors=n_neighbors, n_components=dim, metric=metric
        ).fit_transform(embeddings)
    
    def local_cluster_embeddings(
        self, embeddings: np.ndarray, dim: int, num_neighbors: int = 10, metric: str = "cosine"
    ) -> np.ndarray:
        """
        임베딩에 대해 UMAP을 사용하여 지역 차원 축소를 수행. 
        일반적으로 전역 클러스터링 이후에 사용됨.
        """
        logger.info(f"[RAPTOR] 로컬 UMAP 차원 축소 수행 - dim={dim}, num_neighbors={num_neighbors}, metric={metric}")
        return umap.UMAP(
            n_neighbors=num_neighbors, n_components=dim, metric=metric
        ).fit_transform(embeddings)

    def get_optimal_clusters(
        self, embeddings: np.ndarray, max_clusters: int = 50
    ) -> int:
        """
        가우시안 혼합 모델(Gaussian Mixture Model)과 베이지안 정보 기준(BIC)을 사용하여 최적의 클러스터 수를 결정.
        """
        max_clusters = min(max_clusters, len(embeddings))  # 최대 클러스터 수와 임베딩의 길이 중 작은 값을 최대 클러스터 수로 설정
        n_clusters = np.arange(1, max_clusters)            # 1부터 최대 클러스터 수까지의 범위를 생성
        bics = []                                          # BIC 점수를 저장할 리스트
        
        logger.info("[RAPTOR] Gaussian Mixture Model(GMM)을 사용하여 최적의 클러스터 수 결정 중")
        for n in n_clusters: # 각 클러스터 수에 대해 반복
            gm = GaussianMixture(n_components=n, random_state=self.random_seed) # 가우시안 혼합 모델 초기화
            gm.fit(embeddings)              # 임베딩에 대해 모델 학습
            bic = gm.bic(embeddings)        # 학습된 bic 점수 추가
            bics.append(bic)
            logger.debug(f"[RAPTOR] {n}개의 클러스터에 대한 BIC: {bic}")
        
        optimal_clusters = n_clusters[np.argmin(bics)] # BIC 점수가 가장 낮은 클러스터 수를 반환
        logger.info(f"[RAPTOR] 결정된 최적의 클러스터 수: {optimal_clusters}")
        return optimal_clusters  

    def GMM_cluster(
        self, embeddings: np.ndarray, threshold: float
    ) -> Tuple[List[np.ndarray], int]:
        """
        임베딩을 GMM을 사용해 클러스터링합니다. 주어진 확률 임계값을 기준으로 클러스터링 실행
        """
        logger.info("[RAPTOR] GMM을 사용하여 임베딩 클러스터링 중")
        n_clusters = self.get_optimal_clusters(embeddings)  # 최적의 클러스터 수를 구합니다.
        gm = GaussianMixture(n_components=n_clusters, random_state=self.random_seed) # 가우시안 혼합 모델을 초기화합니다.
        gm.fit(embeddings)                                         # 임베딩에 대해 모델을 학습합니다.
        probs = gm.predict_proba(embeddings)                       # 임베딩이 각 클러스터에 속할 확률을 예측합니다.
        labels = [np.where(prob > threshold)[0] for prob in probs] # 임계값을 초과하는 확률을 가진 클러스터를 레이블로 선택합니다.
        logger.info(f"[RAPTOR] 임계값 {threshold}을 기준으로 클러스터 레이블 생성 완료")
        return labels, n_clusters                                  # 레이블과 클러스터 수(튜플)를 반환합니다.

    def perform_clustering(
        self, embeddings: np.ndarray, dim: int, threshold: float,
    ) -> List[np.ndarray]:
        """
        차원 축소 -> GMM을 사용한 클러스터링 -> 각 글로벌 클러스터 내에서의 로컬 클러스터링을 순서대로 수행
        """
        logger.info("[RAPTOR] 계층적 클러스터링 과정 시작")
        if len(embeddings) <= dim + 1:
            logger.warning("[RAPTOR] 데이터가 충분하지 않음 - 모든 데이터 포인트에 대해 단일 클러스터 반환")
            return [np.array([0]) for _ in range(len(embeddings))]

        # 글로벌 차원 축소
        reduced_embeddings_global = self.global_cluster_embeddings(embeddings, dim)
        # 글로벌 클러스터링
        global_clusters, n_global_clusters = self.GMM_cluster(
            reduced_embeddings_global, threshold
        )

        all_local_clusters = [np.array([]) for _ in range(len(embeddings))]
        total_clusters = 0

        # 각 글로벌 클러스터를 순회하며 로컬 클러스터링 수행
        for i in range(n_global_clusters):
            # 현재 글로벌 클러스터에 속하는 임베딩 추출
            global_cluster_embeddings_ = embeddings[
                np.array([i in gc for gc in global_clusters])
            ]

            if len(global_cluster_embeddings_) == 0:
                continue
            if len(global_cluster_embeddings_) <= dim + 1:
                # 작은 클러스터는 직접 할당으로 처리
                local_clusters = [np.array([0]) for _ in global_cluster_embeddings_]
                n_local_clusters = 1
            else:
                # 로컬 차원 축소 및 클러스터링
                reduced_embeddings_local = self.local_cluster_embeddings(
                    global_cluster_embeddings_, dim
                )
                local_clusters, n_local_clusters = self.GMM_cluster(
                    reduced_embeddings_local, threshold
                )

            # 로컬 클러스터 ID 할당, 이미 처리된 총 클러스터 수를 조정
            for j in range(n_local_clusters):
                local_cluster_embeddings_ = global_cluster_embeddings_[
                    np.array([j in lc for lc in local_clusters])
                ]
                indices = np.where(
                    (embeddings == local_cluster_embeddings_[:, None]).all(-1)
                )[1]
                for idx in indices:
                    all_local_clusters[idx] = np.append(
                        all_local_clusters[idx], j + total_clusters
                    )

            total_clusters += n_local_clusters
            logger.info(f"[RAPTOR] 글로벌 클러스터 {i} 처리 후 총 클러스터 수: {total_clusters}")

        return all_local_clusters


    def embed(self, texts: List[str]) -> np.ndarray:
        """
        텍스트 문서 목록에 대한 임베딩을 생성.
        embd 객체는 텍스트 목록을 받아 그 임베딩을 반환하는 `embed_documents` 메소드를 가지고 있음.
        """        
        text_embeddings = self.embed_obj.embed_documents(texts)  # 텍스트 문서들의 임베딩을 생성합니다.
        text_embeddings_np = np.array(text_embeddings)  # 임베딩을 numpy 배열로 변환합니다.
        return text_embeddings_np                       # 임베딩된 numpy 배열을 반환합니다.


    def embed_cluster_texts(self, texts: List[str]) -> pd.DataFrame:
        """
        텍스트 목록을 임베딩하고 클러스터링하여, 텍스트, 임베딩, 그리고 클러스터 라벨이 포함된 DataFrame을 반환합니다.
        이 함수는 임베딩 생성과 클러스터링을 단일 단계로 결합합니다.
        """
        logger.info("[RAPTOR] 텍스트 임베딩 및 클러스터링 시작")
        text_embeddings_np = self.embed(texts) # 임베딩 생성
        cluster_labels = self.perform_clustering(
            text_embeddings_np, 10, 0.1
        )  # 임베딩에 대해 클러스터링 수행
        df = pd.DataFrame()                   # 결과를 저장할 DataFrame 초기화
        df["text"] = texts                    # 원본 텍스트 저장
        df["embd"] = list(text_embeddings_np) # DataFrame에 리스트로 임베딩 저장
        df["cluster"] = cluster_labels        # 클러스터 라벨 저장
        logger.info("[RAPTOR] 클러스터링 완료 - 클러스터가 포함된 DataFrame 생성 완료")
        return df


    def fmt_txt(self, df: pd.DataFrame) -> str:
        """
        DataFrame에 있는 텍스트 문서를 단일 문자열로 포맷합니다.
        """
        logger.info("[RAPTOR] DataFrame의 텍스트를 단일 문자열로 포맷하는 중")
        unique_txt = df["text"].tolist()
        return "--- --- \n --- --- ".join(unique_txt)  # 텍스트 문서들을 특정 구분자로 결합하여 반환


    def embed_cluster_summarize_texts(
        self, texts: List[str], level: int
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        텍스트 목록에 대해 임베딩, 클러스터링 및 요약을 수행합니다. 
        """
        # 텍스트를 임베딩하고 클러스터링하여 'text', 'embd', 'cluster' 열이 있는 데이터프레임을 생성합니다.
        logger.info(f"[RAPTOR] 텍스트 요약 시작 - 레벨 {level}")
        df_clusters = self.embed_cluster_texts(texts)
        expanded_list = []

        # 데이터프레임 항목을 문서-클러스터 쌍으로 확장하여 처리를 간단하게 합니다.
        for index, row in df_clusters.iterrows():
            for cluster in row["cluster"]:
                expanded_list.append(
                    {"text": row["text"], "embd": row["embd"], "cluster": cluster}
                )

            # 확장된 목록에서 새 데이터프레임을 생성합니다.
        expanded_df = pd.DataFrame(expanded_list)

        # 처리를 위해 고유한 클러스터 식별자를 검색합니다.
        all_clusters = expanded_df["cluster"].unique()

        logger.info(f"--Generated {len(all_clusters)} clusters--")

        # 요약
        template = """
        여기 중앙정부 재정 정보와 관련된 문서의 하위 집합이 있습니다.
        재정 보고서, 예산 설명자료, 기획재정부 보도자료 등 다양한 재정 관련 데이터가 주어집니다.
        
        제공된 문서의 자세한 요약을 제공하십시오.
        
        문서:
        {context}
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm_obj | StrOutputParser()

        # LLM을 사용하여 요약문을 생성합니다.       
        # 각 클러스터를 처리하고 요약을 생성합니다.
        summaries = []
        for i in all_clusters:
            df_cluster = expanded_df[expanded_df["cluster"] == i]
            formatted_txt = self.fmt_txt(df_cluster)
            summaries.append(chain.invoke({"context": formatted_txt}))
            
        # 요약, 해당 클러스터 및 레벨을 저장할 데이터프레임을 생성합니다.
        df_summary = pd.DataFrame(
            {
                "summaries": summaries,
                "level": [level] * len(summaries),
                "cluster": list(all_clusters),
            }
        )
        logger.info(f'클러스터링 및 요약 결과 : \ndf_clusters : \n{df_clusters}\n\n\ndf_summary\n{df_summary}')
        return df_clusters, df_summary

    def recursive_embed_cluster_summarize(
        self, texts: List[str], level: int = 1, n_levels: int = 3
    ) -> Dict[int, Tuple[pd.DataFrame, pd.DataFrame]]:
        """
        지정된 레벨까지 또는 고유 클러스터의 수가 1이 될 때까지 텍스트를 재귀적으로 임베딩, 클러스터링, 요약하고 각 레벨에서의 결과를 저장.
        """
        results = {}

        # 현재 레벨에 대해 임베딩, 클러스터링, 요약 수행
        logger.info(f"[RAPTOR] 레벨 {level}에서 임베딩, 클러스터링 및 요약 시작")
        df_clusters, df_summary = self.embed_cluster_summarize_texts(texts, level)

        # 현재 레벨의 결과 저장
        results[level] = (df_clusters, df_summary)

        # 추가 재귀가 가능하고 의미가 있는지 결정
        unique_clusters = df_summary["cluster"].nunique()
        if level < n_levels and unique_clusters > 1:
            logger.info(f"[RAPTOR] 재귀 조건 만족 - 다음 레벨 {level + 1}로 이동")
            new_texts = df_summary["summaries"].tolist()
            next_level_results = self.recursive_embed_cluster_summarize(
                new_texts, level + 1, n_levels
            )

            # 다음 레벨의 결과를 현재 결과 사전에 병합
            results.update(next_level_results)
        
        logger.info(f'results : \n{results}')
        return results