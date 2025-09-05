from kiwipiepy import Kiwi
from collections import Counter

kiwi = Kiwi()

def extract_top_nouns(text: str) -> str:
    if not text:
        return ""
    
    top_k = 10
    
    # 명사만 추출
    result = kiwi.analyze(text)
    nouns = [m[0] for m in result[0][0] if m[1] == 'NNG' or m[1] == 'NNP']
    
    # 가장 많이 나온 단어 10개 선택
    top_nouns = [word for word, _ in Counter(nouns).most_common(top_k)]
    
    return " ".join(top_nouns)