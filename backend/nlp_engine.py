import re
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        nlp = None
except:
    nlp = None

base_stopwords = set("""
a about above after again against all am an and any are as at be because been before being below between both but by could did do does doing down during each few for from further had has have having he her here hers herself him himself his how i if in into is it its itself just me more most my myself no nor not of off on once only or other our ours ourselves out over own same she should so some such than that the their theirs them themselves then there these they this those through to too under until up very was we were what when where which while who whom why will with you your yours yourself yourselves
""".split())

domain_stopwords = set("""
candidate role responsibility responsibilities required must should will would include includes including looking seeking ideal position work team environment company organization business strong excellent good great ability experience years year level senior junior prefer preferred bonus nice work working company join organization offer summary culture benefits salary competitive package grew growth opportunity opportunities hiring hire apply application
""".split())

stopwords = base_stopwords | domain_stopwords

typed_technical_ontology = {
    "programming_language": {
        "python", "java", "javascript", "typescript", "c++", "c#", "csharp", "go", "golang", 
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "perl", "matlab", "sql"
    },
    "framework": {
        "react", "react js", "reactjs", "angular", "vue", "vue js", "vuejs", "svelte", 
        "next js", "nextjs", "gatsby", "ember", "backbone", "django", "flask", "fastapi", 
        "spring", "spring boot", "rails", "asp net", "dotnet", "express", "express js", "expressjs"
    },
    "library": {
        "redux", "mobx", "recoil", "zustand", "jotai", "tensorflow", "pytorch", "keras", 
        "scikit learn", "sklearn", "pandas", "numpy", "scipy", "matplotlib", "seaborn", 
        "plotly", "xgboost", "lightgbm", "catboost", "apollo", "prisma", "typeorm", 
        "sequelize", "mongoose", "sqlalchemy", "hibernate", "entity framework"
    },
    "database": {
        "mysql", "postgresql", "postgres", "mongodb", "mongo", "redis", "cassandra", 
        "dynamodb", "oracle", "sqlite", "mariadb", "mssql", "elasticsearch", "elastic", 
        "couchdb", "neo4j"
    },
    "cloud_service": {
        "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud", 
        "google cloud platform", "docker", "kubernetes", "k8s", "lambda"
    },
    "analytics_tool": {
        "hadoop", "spark", "apache spark", "kafka", "apache kafka", "airflow", 
        "apache airflow", "beam", "flink"
    },
    "bi_tool": {
        "tableau", "power bi", "powerbi", "looker", "qlik", "qlikview", "excel", 
        "google sheets", "metabase", "superset"
    },
    "dev_tool": {
        "postman", "insomnia", "swagger", "openapi", "chrome devtools", 
        "visual studio code", "vscode", "intellij", "pycharm", "eclipse", "vim", "emacs",
        "figma", "sketch", "adobe xd", "photoshop", "illustrator", "invision", "zeplin",
        "jira", "confluence", "trello", "asana", "monday", "clickup"
    },
    "build_tool": {
        "webpack", "vite", "rollup", "parcel", "babel", "esbuild", "npm", "yarn", 
        "pip", "maven", "gradle", "composer", "bundler", "cargo", "nuget"
    },
    "version_control_tool": {
        "git", "github", "gitlab", "bitbucket", "svn", "mercurial"
    },
    "testing_tool": {
        "jest", "pytest", "junit", "mocha", "chai", "selenium", "cypress", 
        "playwright", "testcafe"
    },
    "ml_method": {
        "machine learning", "deep learning", "neural network", "neural networks", 
        "predictive modeling", "data mining"
    },
    "ai_method": {
        "artificial intelligence", "ai", "ml", "dl", "nlp", "natural language processing", 
        "computer vision", "cv"
    },
    "web_standard": {
        "html", "html5", "css", "css3", "rest api", "restful", "graphql", "grpc", 
        "websocket", "oauth", "oauth2", "jwt", "json web token"
    },
    "css_preprocessor": {
        "sass", "scss", "less", "tailwind", "tailwindcss"
    },
    "rendering_framework": {
        "bootstrap", "material ui", "mui", "chakra ui", "ant design"
    },
    "data_method": {
        "exploratory data analysis", "eda", "data analysis", "data visualization", 
        "data analytics", "etl", "data pipeline"
    }
}

technical_ontology = set()
for skill_type, skills in typed_technical_ontology.items():
    technical_ontology.update(skills)

generic_reject_list = {
    "data", "analysis", "dashboard", "dashboards", "project", "projects", 
    "developer", "engineer", "content", "report", "reports", "visualization",
    "modern", "professional", "collaborative", "fast", "clean", "maintainable",
    "large", "small", "big", "new", "old", "best", "good", "great", "better",
    "quality", "high", "low", "performance", "efficient", "effective",
    "solution", "solutions", "system", "systems", "application", "applications",
    "software", "platform", "service", "services", "product", "products",
    "business", "enterprise", "company", "organization", "team", "user", "users",
    "client", "clients", "customer", "customers", "management", "manager",
    "information", "additional", "various", "across", "processes", "process",
    "collection", "amazon", "prime", "matrix", "issues", "issue", "devices",
    "device", "browser", "compatibility", "enhance", "development", "frameworks",
    "proficiency", "wireframes", "mockups", "pixel", "interactive", "responsive",
    "design", "code", "build", "web", "frontend", "backend", "full", "stack",
    "technologies", "tools", "skills", "knowledge", "experience", "years"
}

tech_action_verbs = {
    "built", "developed", "implemented", "designed", "created", "architected", "engineered",
    "used", "utilized", "worked", "applied", "employed", "leveraged",
    "integrated", "deployed", "configured", "setup", "established", "installed",
    "optimized", "improved", "enhanced", "refactored", "migrated", "upgraded",
    "trained", "analyzed", "tested", "debugged", "troubleshot", "maintained",
    "automated", "scripted", "programmed", "coded", "wrote",
    "managed", "led", "coordinated", "delivered", "launched", "shipped",
    "collaborated", "contributed", "participated", "worked on"
}

normalization_map = {
    "reactjs": "react", "react js": "react",
    "nodejs": "node js", "node": "node js",
    "vuejs": "vue", "vue js": "vue",
    "nextjs": "next js",
    "expressjs": "express", "express js": "express",
    "k8s": "kubernetes",
    "html5": "html",
    "css3": "css",
    "ml": "machine learning", "ai": "artificial intelligence", "dl": "deep learning",
    "nlp": "natural language processing", "cv": "computer vision",
    "sklearn": "scikit learn", "tf": "tensorflow",
    "py": "python", "js": "javascript", "ts": "typescript",
    "mongo": "mongodb", "postgres": "postgresql",
    "powerbi": "power bi", "power bi": "power bi",
    "ms excel": "excel", "microsoft excel": "excel",
    "asp net": "dotnet",
    "csharp": "c#", "golang": "go",
    "elastic": "elasticsearch",
    "eda": "exploratory data analysis",
    "data viz": "data visualization",
    "dataviz": "data visualization"
}

tech_org_whitelist = {
    'github', 'gitlab', 'aws', 'azure', 'google cloud', 'gcp',
    'microsoft', 'oracle', 'ibm', 'docker', 'kubernetes',
    'amazon', 'meta', 'facebook', 'apple', 'netflix'
}

soft_skills = {
    "communication", "leadership", "teamwork", "problem solving", "critical thinking",
    "time management", "adaptability", "creativity", "work ethic", "attention to detail",
    "collaboration", "interpersonal", "organizational", "analytical", "motivated",
    "self starter", "team player", "fast learner", "detail oriented", "results driven"
}

priority_sections = {
    "skills", "technical skills", "tools", "technologies", "tech stack", 
    "frameworks", "programming languages", "languages", "technical competencies"
}

low_priority_sections = {
    "summary", "objective", "profile", "personal", "about", "references",
    "education", "languages", "additional information", "hobbies", "interests",
    "responsibilities", "achievements", "accomplishments", "duties"
}

strict_reject_sections = {
    "summary", "objective", "profile", "responsibilities", "achievements", "accomplishments"
}

junk_patterns = {
    "intern", "internship", "bachelor", "master", "degree", "university", "college",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december", "jan", "feb", "mar", "apr",
    "jun", "jul", "aug", "sep", "oct", "nov", "dec", "present", "current"
}

job_title_indicators = {
    "engineer", "developer", "analyst", "manager", "architect", "specialist",
    "designer", "scientist", "administrator", "lead", "director", "consultant",
    "coordinator", "associate", "intern", "trainee", "junior", "senior", "staff", "principal"
}

source_sites = {
    "arc.dev", "arc dev", "toptal", "roadmap", "linkedin", "indeed", "glassdoor",
    "monster", "dice", "stackoverflow", "github jobs", "remote ok", "weworkremotely",
    "flexjobs", "angel list", "angellist"
}

def detect_sections(text):
    lines = text.split('\n')
    section_map = {}
    current_section = "general"
    
    for i, line in enumerate(lines):
        line_lower = line.strip().lower()
        if len(line_lower) < 30 and len(line_lower) > 0:
            for priority_sec in priority_sections:
                if priority_sec in line_lower:
                    current_section = priority_sec
                    section_map[i] = current_section
                    break
            for low_sec in low_priority_sections:
                if low_sec in line_lower and current_section == "general":
                    current_section = low_sec
                    section_map[i] = current_section
                    break
    
    return section_map

def get_section_priority(text_fragment, section_map):
    text_lower = text_fragment.lower()
    
    for section_name in strict_reject_sections:
        if section_name in text_lower:
            return -1.0
    
    for section_name in priority_sections:
        if section_name in text_lower:
            return 2.0
    
    for section_name in low_priority_sections:
        if section_name in text_lower:
            return 0.3
    
    return 1.0

def sanitize_resume_text(text):
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' ', text)
    text = re.sub(r'\b(?:\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b', ' ', text)
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', text)
    text = re.sub(r'\b(?:github|linkedin|twitter)\.com/[^\s]+', ' ', text)
    text = re.sub(r'\b\d{5}(?:-\d{4})?\b', ' ', text)
    text = re.sub(r'\b[A-Z]{2}\s+\d{5}\b', ' ', text)
    text = re.sub(r'\b\d+\s+[A-Z][a-z]+\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct)\b', ' ', text, flags=re.IGNORECASE)
    
    for pattern in junk_patterns:
        text = re.sub(r'\b' + pattern + r'\b', ' ', text, flags=re.IGNORECASE)
    
    if nlp:
        doc = nlp(text[:100000])
        sanitized_tokens = []
        for token in doc:
            if token.ent_type_ == 'PERSON':
                continue
            if token.ent_type_ in ['GPE', 'LOC'] and token.text.lower() not in technical_ontology:
                continue
            if token.ent_type_ == 'ORG':
                org_lower = token.text.lower()
                is_tech_company = any(tech in org_lower for tech in ['google', 'microsoft', 'amazon', 'meta', 'facebook', 'apple', 'netflix', 'uber', 'airbnb', 'oracle', 'ibm', 'salesforce', 'adobe'])
                is_in_ontology = org_lower in technical_ontology
                if not is_tech_company and not is_in_ontology:
                    continue
            sanitized_tokens.append(token.text)
        text = ' '.join(sanitized_tokens)
    
    text = re.sub(r'\b\d+\b', ' ', text)
    text = re.sub(r'\b[a-zA-Z]\b', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    tokens = [w for w in text.split() if w not in stopwords and len(w) > 1]
    return " ".join(tokens)

def normalize_phrase(phrase):
    phrase = phrase.strip().lower()
    phrase = re.sub(r'\s+', ' ', phrase)
    return normalization_map.get(phrase, phrase)

def is_technical_phrase(phrase):
    phrase_lower = phrase.lower()
    for tech_term in technical_ontology:
        if tech_term in phrase_lower or phrase_lower in tech_term:
            return True
    return False

def is_junk_phrase(phrase):
    phrase_lower = phrase.lower()
    
    if phrase_lower in generic_reject_list:
        return True
    
    if any(junk in phrase_lower for junk in junk_patterns):
        return True
    
    words = phrase_lower.split()
    if len(words) == 1 and words[0] in generic_reject_list:
        return True
    
    stopword_count = sum(1 for w in words if w in stopwords)
    if len(words) > 0 and (stopword_count / len(words)) > 0.5:
        return True
    
    if any(title in phrase_lower for title in job_title_indicators):
        word_count = len(words)
        if word_count >= 2:
            return True
    
    if phrase_lower in soft_skills:
        return True
    
    task_phrases = ['conduct', 'perform', 'prepare', 'write', 'create', 'build', 'develop', 'manage', 'lead', 'coordinate']
    for task in task_phrases:
        if phrase_lower.startswith(task):
            return True
    
    fragment_indicators = ['content', 'information', 'various', 'across', 'processes', 'issues', 'quality', 'multiple', 'support', 'focus']
    if len(words) >= 2:
        for indicator in fragment_indicators:
            if indicator in words and phrase_lower not in technical_ontology:
                return True
    
    adjectives = ['additional', 'various', 'multiple', 'high', 'low', 'best', 'better', 'clean', 'maintainable', 'interactive', 'responsive']
    if words and words[0] in adjectives:
        return True
    
    return False

def extract_noun_phrases(text):
    phrases = set()
    
    if nlp:
        doc = nlp(text[:100000])
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.strip()
            word_count = len(chunk_text.split())
            if 1 <= word_count <= 4:
                has_technical = False
                for token in chunk:
                    if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 1:
                        if is_technical_phrase(token.text):
                            has_technical = True
                            break
                if has_technical:
                    phrases.add(chunk_text.lower())
    
    pattern = r'\b([a-z]+(?:\s+[a-z]+){0,3})\b'
    matches = re.findall(pattern, text.lower())
    for match in matches:
        if 1 <= len(match.split()) <= 4:
            if is_technical_phrase(match):
                phrases.add(match)
    
    return list(phrases)

def appears_near_action_verb(phrase, text, window=10):
    text_lower = text.lower()
    phrase_lower = phrase.lower()
    
    words = text_lower.split()
    for i, word in enumerate(words):
        if word in tech_action_verbs:
            start = max(0, i - window)
            end = min(len(words), i + window)
            context = ' '.join(words[start:end])
            if phrase_lower in context:
                return True
    return False

def contains_verb(phrase):
    if nlp:
        doc = nlp(phrase)
        for token in doc:
            if token.pos_ == 'VERB':
                return True
    
    verb_indicators = ['ing', 'ed', 'en']
    words = phrase.lower().split()
    for word in words:
        if word in tech_action_verbs:
            return True
        if any(word.endswith(suffix) for suffix in verb_indicators) and len(word) > 4:
            return True
    return False

def validate_phrase_structure(phrase):
    words = phrase.strip().split()
    if len(words) > 3:
        return False
    
    if contains_verb(phrase):
        return False
    
    stopword_count = sum(1 for w in words if w.lower() in stopwords)
    if len(words) > 0 and (stopword_count / len(words)) > 0.4:
        return False
    
    phrase_lower = phrase.lower()
    action_starters = ['built', 'developed', 'created', 'designed', 'performed', 'implemented', 'managed', 'led', 'worked', 'used', 'analyzed', 'prepared', 'write', 'conduct']
    for starter in action_starters:
        if phrase_lower.startswith(starter):
            return False
    
    time_words = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'present', 'current', 'year', 'month']
    for time_word in time_words:
        if time_word in phrase_lower:
            return False
    
    section_titles = ['summary', 'experience', 'education', 'skills', 'projects', 'certifications', 'objective', 'profile']
    for title in section_titles:
        if phrase_lower == title:
            return False
    
    return True

def get_skill_type(phrase):
    phrase_lower = phrase.lower()
    normalized = normalize_phrase(phrase_lower)
    
    for skill_type, skills in typed_technical_ontology.items():
        if normalized in skills:
            return skill_type
        for skill in skills:
            if skill in normalized or normalized in skill:
                return skill_type
    
    words = phrase_lower.split()
    for word in words:
        for skill_type, skills in typed_technical_ontology.items():
            if word in skills:
                return skill_type
    
    return None

def is_valid_technical_skill(phrase):
    phrase = phrase.strip()
    if not phrase or len(phrase) <= 1:
        return False
    
    phrase_lower = phrase.lower()
    normalized_phrase = normalize_phrase(phrase_lower)
    
    if normalized_phrase in generic_reject_list:
        return False
    
    words = phrase_lower.split()
    if len(words) == 1 and words[0] in generic_reject_list:
        return False
    
    if len(words) == 1 and len(phrase) <= 2:
        if phrase_lower not in technical_ontology:
            return False
    
    if not validate_phrase_structure(phrase):
        return False
    
    if nlp:
        doc = nlp(phrase)
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                return False
            if ent.label_ in ['GPE', 'LOC', 'FAC']:
                person_lower = phrase.lower()
                if person_lower not in technical_ontology:
                    return False
            if ent.label_ == 'ORG':
                org_lower = ent.text.lower()
                if org_lower not in tech_org_whitelist and org_lower not in technical_ontology:
                    return False
            if ent.label_ == 'DATE':
                return False
            if ent.label_ == 'CARDINAL':
                cardinal_text = ent.text.lower()
                if not any(tech in cardinal_text for tech in ['3d', '2d', 'c++', 'c#']):
                    return False
    
    skill_type = get_skill_type(phrase)
    if skill_type is not None:
        return True
    
    if is_technical_phrase(phrase):
        return True
    
    return False

def extract_skills(text):
    section_map = detect_sections(text)
    sanitized = sanitize_resume_text(text)
    text_lower = sanitized.lower()
    
    skill_scores = {}
    skill_metadata = {}
    
    for tech_term in technical_ontology:
        pattern = r'\b' + re.escape(tech_term) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            normalized = normalize_phrase(tech_term)
            count = len(matches)
            section_priority = get_section_priority(text_lower, section_map)
            skill_scores[normalized] = skill_scores.get(normalized, 0) + (count * section_priority)
            skill_metadata[normalized] = {'frequency': count, 'tfidf': 0, 'context': False, 'section_priority': section_priority}
    
    noun_phrases = extract_noun_phrases(sanitized)
    for phrase in noun_phrases:
        if is_junk_phrase(phrase):
            continue
        
        normalized = normalize_phrase(phrase)
        if normalized.lower() in soft_skills:
            continue
        if len(phrase.split()) > 4:
            continue
        if is_technical_phrase(phrase):
            section_priority = get_section_priority(phrase, section_map)
            if normalized not in skill_scores:
                skill_scores[normalized] = section_priority
                skill_metadata[normalized] = {'frequency': 1, 'tfidf': 0, 'context': False, 'section_priority': section_priority}
            else:
                skill_scores[normalized] += section_priority
                skill_metadata[normalized]['frequency'] += 1
    
    for skill in list(skill_scores.keys()):
        if appears_near_action_verb(skill, sanitized, window=10):
            skill_scores[skill] += 3
            skill_metadata[skill]['context'] = True
    
    cleaned = clean_text(sanitized)
    if cleaned:
        try:
            vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 4), min_df=1)
            tfidf_matrix = vectorizer.fit_transform([cleaned])
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            for term, tfidf_score in zip(feature_names, tfidf_scores):
                if is_technical_phrase(term) and not is_junk_phrase(term):
                    normalized = normalize_phrase(term)
                    if normalized not in skill_scores:
                        skill_scores[normalized] = 0
                        skill_metadata[normalized] = {'frequency': 0, 'tfidf': tfidf_score, 'context': False, 'section_priority': 1.0}
                    
                    skill_metadata[normalized]['tfidf'] = max(skill_metadata[normalized]['tfidf'], tfidf_score)
                    
                    if tfidf_score > 0.15:
                        skill_scores[normalized] += 5
                    elif tfidf_score > 0.08:
                        skill_scores[normalized] += 3
                    elif tfidf_score > 0.04:
                        skill_scores[normalized] += 1
        except:
            pass
    
    filtered_skills = {}
    for skill, score in skill_scores.items():
        if score <= 0:
            continue
        if skill in soft_skills:
            continue
        if skill.lower() in generic_reject_list:
            continue
        skill_words = skill.split()
        if len(skill_words) == 1 and skill_words[0].lower() in generic_reject_list:
            continue
        if len(skill.split()) > 3:
            continue
        if not is_technical_phrase(skill):
            continue
        if is_junk_phrase(skill):
            continue
        if re.search(r'[0-9]{3,}', skill):
            continue
        if re.search(r'@|\.com|http|www', skill):
            continue
        
        section_priority = skill_metadata.get(skill, {}).get('section_priority', 1.0)
        if section_priority < 0:
            continue
        
        filtered_skills[skill] = score
    
    def rank_key(item):
        skill, score = item
        metadata = skill_metadata.get(skill, {'frequency': 0, 'tfidf': 0, 'context': False, 'section_priority': 1.0})
        freq_score = metadata['frequency']
        tfidf_score = metadata['tfidf']
        context_bonus = 2 if metadata['context'] else 0
        length_bonus = len(skill.split()) * 0.5
        section_bonus = metadata.get('section_priority', 1.0)
        
        return (score + freq_score + tfidf_score * 10 + context_bonus + length_bonus + section_bonus)
    
    ranked_skills = sorted(filtered_skills.items(), key=rank_key, reverse=True)
    
    final_validated_skills = []
    for skill, score in ranked_skills:
        if is_valid_technical_skill(skill):
            final_validated_skills.append(skill)
        if len(final_validated_skills) >= 15:
            break
    
    return final_validated_skills if final_validated_skills else ["general"]

def extract_keywords(docs):
    if not docs or not docs[0]:
        return []
    
    text = docs[0]
    
    boilerplate_patterns = [
        r'(?i)job title:.*?(?:\n|$)',
        r'(?i)location:.*?(?:\n|$)',
        r'(?i)employment type:.*?(?:\n|$)',
        r'(?i)salary range:.*?(?:\n|$)',
        r'(?i)compensation:.*?(?:\n|$)',
        r'(?i)(?:we offer|benefits include|competitive salary|compensation package).*?(?:\n\n|\Z)',
        r'(?i)(?:equal opportunity employer|eeo statement|diversity statement).*?(?:\n\n|\Z)',
        r'(?i)(?:to apply|how to apply|application process|submit your|send resume).*?(?:\n\n|\Z)',
        r'\[.*?\]',
        r'\{.*?\}'
    ]
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, ' ', text)
    
    for site in source_sites:
        text = text.replace(site, ' ')
    
    text_lower = text.lower()
    keyword_scores = {}
    
    if nlp:
        doc = nlp(text[:100000])
        for token in doc:
            if token.pos_ not in ['NOUN', 'PROPN']:
                continue
            if len(token.text) <= 2:
                continue
            if token.text.lower() in stopwords:
                continue
            if is_technical_phrase(token.text):
                normalized = normalize_phrase(token.text)
                keyword_scores[normalized] = keyword_scores.get(normalized, 0) + 1
        
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.strip()
            word_count = len(chunk_text.split())
            if 1 <= word_count <= 5:
                if is_technical_phrase(chunk_text):
                    normalized = normalize_phrase(chunk_text)
                    keyword_scores[normalized] = keyword_scores.get(normalized, 0) + 2
    
    phrase_pattern = r'\b([a-z]+(?:\s+[a-z]+){0,4})\b'
    phrases = re.findall(phrase_pattern, text_lower)
    for phrase in phrases:
        phrase = phrase.strip()
        word_count = len(phrase.split())
        if 1 <= word_count <= 5:
            if is_technical_phrase(phrase):
                normalized = normalize_phrase(phrase)
                keyword_scores[normalized] = keyword_scores.get(normalized, 0) + 1
    
    for tech_term in technical_ontology:
        if tech_term in text_lower:
            normalized = normalize_phrase(tech_term)
            keyword_scores[normalized] = keyword_scores.get(normalized, 0) + 3
    
    cleaned = clean_text(text)
    if cleaned:
        try:
            vectorizer = TfidfVectorizer(max_features=80, ngram_range=(1, 5), min_df=1)
            tfidf_matrix = vectorizer.fit_transform([cleaned])
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            for term, tfidf_score in zip(feature_names, tfidf_scores):
                if is_technical_phrase(term):
                    normalized = normalize_phrase(term)
                    if normalized not in keyword_scores:
                        keyword_scores[normalized] = 0
                    
                    if tfidf_score > 0.1:
                        keyword_scores[normalized] += 8
                    elif tfidf_score > 0.05:
                        keyword_scores[normalized] += 5
                    elif tfidf_score > 0.02:
                        keyword_scores[normalized] += 2
        except:
            pass
    
    hr_noise = {
        'candidate', 'candidates', 'team', 'teams', 'environment', 'company', 'organization', 'business',
        'position', 'positions', 'role', 'roles', 'work', 'working', 'worker', 'workers',
        'year', 'years', 'experience', 'experiences', 'strong', 'excellent', 'good', 'great', 'ability', 'abilities',
        'along', 'building', 'active', 'looking', 'seeking', 'ideal', 'required', 'must', 'will', 'would', 'should',
        'responsibility', 'responsibilities', 'include', 'includes', 'including', 'join', 'joining',
        'prefer', 'preferred', 'preference', 'bonus', 'nice', 'level', 'senior', 'junior', 'mid',
        'offer', 'offers', 'summary', 'culture', 'cultural', 'benefit', 'benefits', 'salary', 'compensation',
        'competitive', 'package', 'grew', 'growth', 'grow', 'opportunity', 'opportunities',
        'hiring', 'hire', 'apply', 'application', 'qualified', 'qualification', 'qualifications',
        'code', 'build', 'work', 'skill', 'skills', 'knowledge', 'familiar', 'familiarity',
        'tool', 'tools', 'tech', 'technology', 'technologies', 'framework', 'frameworks',
        'use', 'using', 'used', 'develop', 'developing', 'developed',
        'collaborate', 'collaboration', 'participate', 'participation'
    }
    
    filtered_keywords = {}
    for keyword, score in keyword_scores.items():
        if score <= 0:
            continue
        if keyword in hr_noise:
            continue
        if keyword in soft_skills:
            continue
        if keyword.lower() in generic_reject_list:
            continue
        keyword_words = keyword.split()
        if len(keyword_words) == 1 and keyword_words[0].lower() in generic_reject_list:
            continue
        if len(keyword.split()) > 3:
            continue
        if not is_technical_phrase(keyword):
            continue
        if is_junk_phrase(keyword):
            continue
        if contains_verb(keyword):
            continue
        if re.search(r'[0-9]{3,}', keyword):
            continue
        if any(noise in keyword for noise in ['http', '@', '.com', 'www', 'email', 'phone']):
            continue
        if any(site in keyword for site in source_sites):
            continue
        
        filtered_keywords[keyword] = score
    
    def rank_jd_key(item):
        keyword, score = item
        word_count = len(keyword.split())
        length_bonus = word_count * 1.5
        return score + length_bonus
    
    ranked_keywords = sorted(filtered_keywords.items(), key=rank_jd_key, reverse=True)
    
    final_validated_keywords = []
    for kw, score in ranked_keywords:
        if is_valid_technical_skill(kw):
            final_validated_keywords.append(kw)
        if len(final_validated_keywords) >= 25:
            break
    
    return final_validated_keywords if final_validated_keywords else ["general"]

def extract_email(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else ""

def extract_phone(text):
    phone_pattern = r'\b(?:\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b'
    phones = re.findall(phone_pattern, text)
    if phones:
        digits = re.sub(r'[^0-9]', '', phones[0])
        return digits[-10:] if len(digits) >= 10 else phones[0]
    return ""

def extract_location(text):
    if not nlp:
        return ""
    
    doc = nlp(text[:50000])
    locations = []
    for ent in doc.ents:
        if ent.label_ in ['GPE', 'LOC']:
            loc_lower = ent.text.lower()
            if loc_lower not in technical_ontology and len(ent.text.split()) <= 3:
                locations.append(ent.text)
    
    return locations[0] if locations else ""

def extract_name(text):
    if not nlp:
        lines = text.split('\n')
        for line in lines[:5]:
            line_clean = line.strip()
            if 2 <= len(line_clean.split()) <= 4 and len(line_clean) < 50:
                if not re.search(r'@|http|www|\d{3}', line_clean):
                    return line_clean
        return ""
    
    doc = nlp(text[:5000])
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    
    lines = text.split('\n')
    for line in lines[:5]:
        line_clean = line.strip()
        if 2 <= len(line_clean.split()) <= 4 and len(line_clean) < 50:
            if not re.search(r'@|http|www|\d{3}', line_clean):
                return line_clean
    
    return ""

def extract_education_degrees(text):
    degree_keywords = {
        'bachelor', 'bachelors', 'b.e', 'b.e.', 'btech', 'b.tech', 'bs', 'b.s', 'ba', 'b.a',
        'master', 'masters', 'm.e', 'm.e.', 'mtech', 'm.tech', 'ms', 'm.s', 'ma', 'm.a', 'mba',
        'phd', 'ph.d', 'doctorate', 'bsc', 'b.sc', 'msc', 'm.sc'
    }
    
    degrees = []
    text_lower = text.lower()
    
    for keyword in degree_keywords:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text_lower):
            if keyword not in degrees:
                degrees.append(keyword)
    
    return degrees[:5]

def extract_education_fields(text):
    field_keywords = {
        'computer science', 'information technology', 'engineering', 'software engineering',
        'data science', 'information systems', 'electronics', 'electrical', 'mechanical',
        'civil', 'mathematics', 'statistics', 'business', 'management', 'finance'
    }
    
    fields = []
    text_lower = text.lower()
    
    for field in field_keywords:
        if field in text_lower:
            fields.append(field)
    
    return list(set(fields))

def extract_institutions(text):
    if not nlp:
        return []
    
    education_keywords = ['university', 'college', 'institute', 'school', 'academy']
    
    institutions = []
    doc = nlp(text[:50000])
    
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            org_lower = ent.text.lower()
            if any(edu_word in org_lower for edu_word in education_keywords):
                if org_lower not in technical_ontology:
                    institutions.append(ent.text)
    
    return list(set(institutions))

def extract_experience_roles(text):
    role_indicators = {
        'engineer', 'developer', 'analyst', 'scientist', 'manager', 'architect',
        'designer', 'administrator', 'lead', 'specialist', 'consultant', 'coordinator',
        'associate', 'intern', 'trainee'
    }
    
    education_excludes = ['college', 'university', 'institute', 'school', 'academy']
    
    roles = []
    text_lower = text.lower()
    
    lines = text.split('\n')
    for line in lines:
        line_lower = line.lower()
        line_clean = line.strip()
        
        if any(edu in line_lower for edu in education_excludes):
            continue
        
        if re.search(r'@|http|www|education|degree', line_lower):
            continue
        
        words = line_lower.split()
        if 2 <= len(words) <= 6:
            if any(indicator in line_lower for indicator in role_indicators):
                if len(line_clean) < 60 and not re.search(r'[0-9]{4}', line_clean):
                    if line_clean not in roles:
                        roles.append(line_clean)
    
    return roles[:5]

def extract_experience_companies(text):
    if not nlp:
        return []
    
    companies = []
    doc = nlp(text[:50000])
    
    education_keywords = ['university', 'college', 'institute', 'school', 'academy']
    tech_keywords = ['python', 'java', 'react', 'sql', 'aws', 'azure', 'excel', 'tableau']
    
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            org_lower = ent.text.lower()
            org_text = ent.text.strip()
            
            if any(edu in org_lower for edu in education_keywords):
                continue
            
            if org_lower in tech_org_whitelist:
                continue
            
            if org_lower in technical_ontology:
                continue
            
            if any(tech in org_lower for tech in tech_keywords):
                continue
            
            if len(org_text.split()) <= 5 and org_text not in companies:
                companies.append(org_text)
    
    return companies[:10]

def extract_experience_duration(text):
    duration_patterns = [
        r'(\d+)\s*(?:years?|yrs?)',
        r'(\d+)\s*(?:months?|mos?)',
        r'\b(\d{4})\s*-\s*(\d{4}|present|current)\b'
    ]
    
    durations = []
    text_lower = text.lower()
    
    for pattern in duration_patterns:
        matches = re.findall(pattern, text_lower)
        durations.extend([str(m) if isinstance(m, str) else '-'.join(m) for m in matches])
    
    return durations[:5]

def estimate_experience_years(text):
    year_pattern = r'(\d+)\s*\+?\s*(?:years?|yrs?)'
    years_found = re.findall(year_pattern, text.lower())
    
    if years_found:
        return str(max([int(y) for y in years_found]))
    
    date_ranges = re.findall(r'\b(\d{4})\s*-\s*(\d{4}|present|current)\b', text.lower())
    if date_ranges:
        total_years = 0
        for start, end in date_ranges:
            start_year = int(start)
            end_year = 2026 if end in ['present', 'current'] else int(end)
            total_years += max(0, end_year - start_year)
        return str(total_years) if total_years > 0 else ""
    
    return ""

def extract_projects(text):
    project_indicators = ['project', 'projects']
    
    project_titles = []
    lines = text.split('\n')
    
    in_project_section = False
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        if any(indicator in line_lower for indicator in project_indicators):
            if len(line_lower.split()) <= 3:
                in_project_section = True
                continue
        
        if in_project_section and line.strip():
            line_clean = line.strip()
            words = line_clean.split()
            
            if 3 <= len(words) <= 12:
                if not re.search(r'@|http|www', line_clean):
                    if not any(tech in line_lower for tech in ['python', 'java', 'react', 'sql']):
                        if line_clean not in project_titles:
                            project_titles.append(line_clean)
            
            if len(project_titles) >= 5:
                break
    
    return project_titles[:5]

def extract_certifications(text):
    cert_keywords = ['certified', 'certification', 'certificate', 'credential', 'comptia', 'aws certified', 'azure certified', 'cisco']
    
    certifications = []
    lines = text.split('\n')
    
    for line in lines:
        line_lower = line.lower()
        line_clean = line.strip()
        
        if any(cert in line_lower for cert in cert_keywords):
            if 3 <= len(line_clean.split()) <= 12:
                if not re.search(r'@|http|www', line_clean):
                    if line_clean not in certifications:
                        certifications.append(line_clean)
    
    return certifications[:5]

def split_compound_phrases(phrases):
    expanded = set()
    
    for phrase in phrases:
        phrase = phrase.strip()
        if not phrase:
            continue
        
        if ' and ' in phrase or ' or ' in phrase or '/' in phrase or ',' in phrase:
            parts = re.split(r'\s+(?:and|or|,|/)\s+', phrase)
            for part in parts:
                part = part.strip()
                if part and len(part) > 1:
                    expanded.add(part)
        else:
            expanded.add(phrase)
    
    return list(expanded)

def classify_by_ontology_type(phrases):
    classified = {
        'technical_skills': [],
        'tools': [],
        'frameworks': [],
        'languages': [],
        'databases': []
    }
    
    phrases = split_compound_phrases(phrases)
    
    for phrase in phrases:
        phrase = phrase.strip()
        if not phrase or len(phrase) <= 1:
            continue
        
        if not is_valid_technical_skill(phrase):
            continue
        
        if is_junk_phrase(phrase):
            continue
        
        skill_type = get_skill_type(phrase)
        if skill_type is None:
            continue
        
        if skill_type == 'programming_language':
            classified['languages'].append(phrase)
        elif skill_type == 'database':
            classified['databases'].append(phrase)
        elif skill_type == 'framework':
            classified['frameworks'].append(phrase)
        elif skill_type in ['dev_tool', 'build_tool', 'version_control_tool', 'testing_tool', 'bi_tool', 'analytics_tool']:
            classified['tools'].append(phrase)
        elif skill_type in ['library', 'cloud_service', 'ml_method', 'ai_method', 'web_standard', 'css_preprocessor', 'rendering_framework', 'data_method']:
            classified['technical_skills'].append(phrase)
    
    for key in classified:
        classified[key] = list(dict.fromkeys(classified[key]))
    
    return classified

def clean_extracted_list(items, max_items=10):
    cleaned = []
    for item in items:
        if not item or not isinstance(item, str):
            continue
        
        item_clean = item.strip()
        
        if len(item_clean) <= 1:
            continue
        
        if item_clean.startswith('¢') or item_clean.startswith('•') or item_clean.startswith('-'):
            item_clean = item_clean[1:].strip()
        
        if re.search(r'@|http|www', item_clean):
            continue
        
        if len(item_clean) > 100:
            continue
        
        if item_clean not in cleaned:
            cleaned.append(item_clean)
    
    return cleaned[:max_items]

def parse_resume_structured(text):
    sanitized = sanitize_resume_text(text)
    
    all_skills = extract_skills(text)
    
    classified = classify_by_ontology_type(all_skills)
    
    candidate_soft_skills = []
    text_lower = text.lower()
    for soft_skill in soft_skills:
        if soft_skill in text_lower:
            candidate_soft_skills.append(soft_skill)
    
    raw_degrees = extract_education_degrees(text)
    raw_fields = extract_education_fields(text)
    raw_institutions = extract_institutions(text)
    raw_roles = extract_experience_roles(text)
    raw_companies = extract_experience_companies(text)
    raw_projects = extract_projects(text)
    raw_certs = extract_certifications(text)
    
    resume_data = {
        'candidate_name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'location': extract_location(text),
        'technical_skills': classified['technical_skills'][:15],
        'programming_languages': classified['languages'][:10],
        'frameworks': classified['frameworks'][:10],
        'tools': classified['tools'][:10],
        'databases': classified['databases'][:10],
        'education_degrees': clean_extracted_list(raw_degrees, 5),
        'education_fields': clean_extracted_list(raw_fields, 5),
        'education_institutions': clean_extracted_list(raw_institutions, 5),
        'experience_roles': clean_extracted_list(raw_roles, 5),
        'experience_companies': clean_extracted_list(raw_companies, 5),
        'experience_date_ranges': extract_experience_duration(text),
        'experience_years_estimated': estimate_experience_years(text),
        'project_titles': clean_extracted_list(raw_projects, 5),
        'project_technologies': [],
        'certifications': clean_extracted_list(raw_certs, 5),
        'soft_skills': candidate_soft_skills[:10]
    }
    
    project_section_match = re.search(r'(?i)projects?.*?(?=\n[A-Z]|\Z)', text, re.DOTALL)
    if project_section_match:
        project_section = project_section_match.group()
        project_skills = extract_skills(project_section)
        project_classified = classify_by_ontology_type(project_skills)
        all_project_tech = (
            project_classified['technical_skills'] +
            project_classified['frameworks'] +
            project_classified['tools'] +
            project_classified['languages'] +
            project_classified['databases']
        )
        resume_data['project_technologies'] = all_project_tech[:15]
    
    return resume_data

def parse_jd_structured(text):
    all_keywords = extract_keywords([text])
    
    classified = classify_by_ontology_type(all_keywords)
    
    experience_years = []
    exp_patterns = [
        r'(\d+)\s*\+?\s*years?',
        r'minimum\s+(\d+)\s*years?',
        r'at least\s+(\d+)\s*years?'
    ]
    for pattern in exp_patterns:
        matches = re.findall(pattern, text.lower())
        experience_years.extend(matches)
    
    required_education = extract_education_degrees(text)
    
    role_match = re.search(r'(?i)(?:position|role|title)[:|\s]+([^\n]{5,50})', text)
    job_role = role_match.group(1).strip() if role_match else ""
    
    if not job_role:
        lines = text.split('\n')
        for line in lines[:10]:
            line_clean = line.strip()
            if 2 <= len(line_clean.split()) <= 6 and len(line_clean) < 60:
                role_indicators = ['engineer', 'developer', 'analyst', 'manager', 'designer', 'architect']
                if any(indicator in line_clean.lower() for indicator in role_indicators):
                    job_role = line_clean
                    break
    
    responsibilities_section = re.search(r'(?i)responsibilit(?:ies|y).*?(?=\n[A-Z]|\Z)', text, re.DOTALL)
    responsibility_tech_terms = []
    if responsibilities_section:
        resp_text = responsibilities_section.group()
        resp_skills = extract_keywords([resp_text])
        resp_classified = classify_by_ontology_type(resp_skills)
        responsibility_tech_terms = (
            resp_classified['technical_skills'] +
            resp_classified['frameworks'] +
            resp_classified['tools'] +
            resp_classified['languages']
        )[:10]
    
    nice_to_have_section = re.search(r'(?i)(?:nice to have|preferred|bonus).*?(?=\n[A-Z]|\Z)', text, re.DOTALL)
    nice_to_have_skills = []
    if nice_to_have_section:
        nice_section_text = nice_to_have_section.group()
        nice_skills = extract_keywords([nice_section_text])
        nice_classified = classify_by_ontology_type(nice_skills)
        nice_to_have_skills = (
            nice_classified['technical_skills'] +
            nice_classified['frameworks'] +
            nice_classified['tools'] +
            nice_classified['languages']
        )[:10]
    
    jd_data = {
        'job_role': job_role[:100] if job_role else "",
        'required_skills': classified['technical_skills'][:15],
        'required_languages': classified['languages'][:10],
        'required_frameworks': classified['frameworks'][:10],
        'required_tools': classified['tools'][:10],
        'required_databases': classified['databases'][:10],
        'required_experience_years': experience_years[0] if experience_years else "",
        'required_education': clean_extracted_list(required_education, 5),
        'nice_to_have_skills': nice_to_have_skills,
        'responsibility_tech_terms': responsibility_tech_terms
    }
    
    return jd_data
