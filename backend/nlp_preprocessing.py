import re
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        nlp = None
except:
    nlp = None

try:
    import nltk
    try:
        from nltk.corpus import stopwords as nltk_stopwords
        nltk_stop_set = set(nltk_stopwords.words('english'))
    except:
        try:
            nltk.download('stopwords', quiet=True)
            from nltk.corpus import stopwords as nltk_stopwords
            nltk_stop_set = set(nltk_stopwords.words('english'))
        except:
            nltk_stop_set = set()
except:
    nltk_stop_set = set()

spacy_stop_set = set()
if nlp:
    spacy_stop_set = nlp.Defaults.stop_words

combined_stopwords = nltk_stop_set | spacy_stop_set

python_skills = {
    "python", "java", "javascript", "typescript", "c++", "c#", "csharp", "go", "golang",
    "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "perl", "matlab", "sql",
    "react", "angular", "vue", "django", "flask", "fastapi", "spring", "nodejs", "express",
    "tensorflow", "pytorch", "keras", "pandas", "numpy", "sklearn", "scikit", "learn",
    "mysql", "postgresql", "mongodb", "redis", "cassandra", "oracle", "sqlite",
    "aws", "azure", "gcp", "docker", "kubernetes", "k8s", "git", "github", "gitlab",
    "html", "css", "rest", "api", "graphql", "oauth", "jwt", "sass", "tailwind",
    "bootstrap", "hadoop", "spark", "kafka", "airflow", "tableau", "powerbi", "excel",
    "pytest", "jest", "selenium", "cypress", "jira", "figma", "webpack", "vite"
}

tech_specific_ontology = {
    "programming_language": {
        "python", "java", "javascript", "typescript", "c++", "c#", "csharp", "go", "golang",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "perl", "matlab", "sql"
    },
    "framework": {
        "react", "angular", "vue", "svelte", "next", "nextjs", "gatsby", "django", "flask",
        "fastapi", "spring", "rails", "express", "expressjs", "laravel", "symfony"
    },
    "library": {
        "redux", "tensorflow", "pytorch", "keras", "pandas", "numpy", "scipy", "matplotlib",
        "sklearn", "scikit", "xgboost", "lightgbm", "apollo", "prisma", "typeorm", "sqlalchemy"
    },
    "database": {
        "mysql", "postgresql", "postgres", "mongodb", "mongo", "redis", "cassandra",
        "dynamodb", "oracle", "sqlite", "mariadb", "mssql", "elasticsearch", "neo4j"
    },
    "cloud": {
        "aws", "azure", "gcp", "docker", "kubernetes", "k8s", "lambda", "ec2", "s3"
    },
    "tool": {
        "git", "github", "gitlab", "jira", "confluence", "postman", "swagger", "figma",
        "tableau", "powerbi", "excel", "vscode", "intellij", "jenkins", "webpack", "vite"
    }
}

technical_whitelist = set()
for cat in tech_specific_ontology.values():
    technical_whitelist.update(cat)

def normalize_unicode(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    return text

def lowercase_text(text):
    return text.lower()

def cleanup_special_chars(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    return text

def normalize_whitespace(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def segment_sentences(text):
    if not nlp:
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    doc = nlp(text[:1000000])
    return [sent.text.strip() for sent in doc.sents]

def tokenize_text(text):
    if not nlp:
        return text.split()
    doc = nlp(text[:1000000])
    return [token.text for token in doc]

def remove_stopwords(tokens):
    return [token for token in tokens if token.lower() not in combined_stopwords or token.lower() in technical_whitelist]

def lemmatize_tokens(tokens):
    if not nlp:
        return tokens
    doc = nlp(' '.join(tokens)[:1000000])
    return [token.lemma_ for token in doc]

def filter_short_tokens(tokens, min_length=2):
    return [token for token in tokens if len(token) >= min_length]

def filter_numeric_tokens(tokens):
    return [token for token in tokens if not token.isdigit()]

def preprocess_text(text):
    if not text:
        return {
            "clean_tokens": [],
            "lemmatized_tokens": [],
            "reconstructed_clean_text": ""
        }
    
    text = normalize_unicode(text)
    text = lowercase_text(text)
    text = cleanup_special_chars(text)
    text = normalize_whitespace(text)
    
    tokens = tokenize_text(text)
    tokens = remove_stopwords(tokens)
    tokens = filter_short_tokens(tokens)
    tokens = filter_numeric_tokens(tokens)
    
    lemmatized = lemmatize_tokens(tokens)
    
    reconstructed = ' '.join(tokens)
    
    return {
        "clean_tokens": tokens,
        "lemmatized_tokens": lemmatized,
        "reconstructed_clean_text": reconstructed
    }

def extract_skills_hybrid(text):
    if not text:
        return []
    
    processed = preprocess_text(text)
    lemmatized = processed['lemmatized_tokens']
    
    skill_set = set()
    
    for token in lemmatized:
        if token in technical_whitelist:
            skill_set.add(token)
    
    if nlp:
        doc = nlp(text[:1000000])
        for chunk in doc.noun_chunks:
            chunk_lower = chunk.text.lower()
            words = chunk_lower.split()
            if 1 <= len(words) <= 4:
                has_tech = False
                for word in words:
                    if word in technical_whitelist:
                        has_tech = True
                        break
                if has_tech:
                    skill_set.add(chunk_lower)
        
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT']:
                ent_lower = ent.text.lower()
                if ent_lower in technical_whitelist:
                    skill_set.add(ent_lower)
    
    validated_skills = []
    for skill in skill_set:
        words = skill.split()
        has_verb = False
        if nlp:
            skill_doc = nlp(skill)
            for token in skill_doc:
                if token.pos_ == 'VERB':
                    has_verb = True
                    break
        
        stopword_count = sum(1 for w in words if w in combined_stopwords)
        stopword_heavy = len(words) > 0 and (stopword_count / len(words)) > 0.5
        
        if not has_verb and not stopword_heavy:
            validated_skills.append(skill)
    
    return sorted(list(set(validated_skills)))[:30]

def extract_keywords_hybrid(text):
    if not text:
        return []
    
    processed = preprocess_text(text)
    lemmatized = processed['lemmatized_tokens']
    
    keyword_set = set()
    
    for token in lemmatized:
        if token in technical_whitelist:
            keyword_set.add(token)
    
    if nlp:
        doc = nlp(text[:1000000])
        for chunk in doc.noun_chunks:
            chunk_lower = chunk.text.lower()
            words = chunk_lower.split()
            if 1 <= len(words) <= 4:
                has_tech = False
                for word in words:
                    if word in technical_whitelist:
                        has_tech = True
                        break
                if has_tech:
                    keyword_set.add(chunk_lower)
    
    validated_keywords = []
    for keyword in keyword_set:
        words = keyword.split()
        has_verb = False
        if nlp:
            kw_doc = nlp(keyword)
            for token in kw_doc:
                if token.pos_ == 'VERB':
                    has_verb = True
                    break
        
        stopword_count = sum(1 for w in words if w in combined_stopwords)
        stopword_heavy = len(words) > 0 and (stopword_count / len(words)) > 0.5
        
        if not has_verb and not stopword_heavy:
            validated_keywords.append(keyword)
    
    return sorted(list(set(validated_keywords)))[:30]

def generate_tfidf_vectors(resume_text, jd_text):
    if not resume_text and not jd_text:
        return {
            "resume_tfidf_vector": [],
            "jd_tfidf_vector": [],
            "feature_names": []
        }
    
    resume_processed = preprocess_text(resume_text)
    jd_processed = preprocess_text(jd_text)
    
    resume_clean = resume_processed['reconstructed_clean_text']
    jd_clean = jd_processed['reconstructed_clean_text']
    
    corpus = [resume_clean, jd_clean]
    
    try:
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=500,
            lowercase=False,
            token_pattern=r'\b\w+\b'
        )
        
        tfidf_matrix = vectorizer.fit_transform(corpus)
        feature_names = vectorizer.get_feature_names_out().tolist()
        
        resume_vector = tfidf_matrix[0].toarray()[0].tolist()
        jd_vector = tfidf_matrix[1].toarray()[0].tolist()
        
        return {
            "resume_tfidf_vector": resume_vector,
            "jd_tfidf_vector": jd_vector,
            "feature_names": feature_names
        }
    except Exception as e:
        return {
            "resume_tfidf_vector": [],
            "jd_tfidf_vector": [],
            "feature_names": []
        }
