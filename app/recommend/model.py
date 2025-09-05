# app/recommend/models.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.recommend.utils import extract_top_nouns
from app.db.database import SessionLocal
from app.db import models

def recommend_books_by_user_books(book_ids: list[int]):

    top_n = 10

    db = SessionLocal()
    try:
        # 1. 사용자의 책 가져오기
        target_books = db.query(models.Book).filter(models.Book.book_id.in_(book_ids)).all()
        if not target_books:
            raise ValueError(f"No books found for IDs: {book_ids}")

        # 2. 사용자의 책 제외한 책들 가져오기 (추천 후보 책)
        candidate_books = db.query(models.Book).filter(~models.Book.book_id.in_(book_ids)).all()
        if not candidate_books:
            return []

        # 3. 후보 책들 TF-IDF 벡터 생성
        corpus = [(b.keyword or "") + " " + extract_top_nouns(b.review) for b in candidate_books]
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(corpus)

        # 4. 사용자 취향 벡터 생성
        user_texts = [(b.keyword or "") + " " + extract_top_nouns(b.review) for b in target_books]
        user_vecs = vectorizer.transform(user_texts)
        import numpy as np
        user_vec = np.mean(user_vecs, axis=0)

        # 5. 코사인 유사도 계산
        sim_scores = cosine_similarity(user_vec, X).flatten()
        top_indices = sim_scores.argsort()[::-1][:top_n]
        recommended_books = [candidate_books[i] for i in top_indices]

        return recommended_books
    finally:
        db.close()
