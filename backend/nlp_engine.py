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

protected_technical_tokens = set()
for skill_type, skills in typed_technical_ontology.items():
    protected_technical_tokens.update(skills)

generic_noun_blacklist = {
    "intelligence", "design", "performance", "structure", "model", "data",
    "analysis", "system", "application", "interactive", "responsive",
    "content", "interface", "execution", "behavior", "insights", "visualization",
    "quality", "solution", "platform", "information", "development", "management",
    "experience", "knowledge", "proficiency", "familiarity", "understanding",
    "ability", "capability", "efficiency", "scalability", "maintainability",
    "accessibility", "compatibility", "security", "reliability", "availability"
}

generic_reject_list = {
    "dashboard", "dashboards", "project", "projects", 
    "developer", "engineer", "report", "reports",
    "modern", "professional", "collaborative", "fast", "clean", "maintainable",
    "large", "small", "big", "new", "old", "best", "good", "great", "better",
    "high", "low", "efficient", "effective",
    "solutions", "systems", "applications",
    "software", "service", "services", "product", "products",
    "business", "enterprise", "company", "organization", "team", "user", "users",
    "client", "clients", "customer", "customers", "manager",
    "additional", "various", "across", "processes", "process",
    "collection", "amazon", "prime", "matrix", "issues", "issue", "devices",
    "device", "browser", "enhance",
    "wireframes", "mockups", "pixel",
    "code", "build", "web", "frontend", "backend", "full", "stack",
    "years", "datasets", "predictable",
    "friendly", "enthusiasts",
    "task", "ensure", "standards", "upwork", "responsible",
    "ids", "st", "me", "be", "to", "and", "or", "of", "in", "less",
    "exploratory", "power", "strong", "responsive", "interactive", "reusable",
    "scalable", "robust", "dynamic", "static", "flexible", "agile",
    "quality", "performance", "optimization", "analysis", "design", "development"
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
    section_boundaries = {}
    lines = text.split('\n')
    
    section_headers = {
        'summary': ['summary', 'profile', 'objective', 'about'],
        'experience': ['experience', 'work experience', 'employment', 'work history'],
        'education': ['education', 'academic', 'qualification'],
        'skills': ['skills', 'technical skills', 'competencies', 'expertise'],
        'projects': ['projects', 'personal projects'],
        'certifications': ['certifications', 'certificates', 'credentials']
    }
    
    for i, line in enumerate(lines):
        line_clean = line.strip()
        line_lower = line_clean.lower()
        
        if len(line_clean) < 40 and len(line_clean) > 2:
            if line_clean.isupper() or (line_clean and line_clean[0].isupper() and ':' not in line_clean):
                for section_type, headers in section_headers.items():
                    for header in headers:
                        if header in line_lower and len(line_lower) < 30:
                            section_boundaries[i] = section_type
                            break
    
    return section_boundaries

def get_section_priority(text_fragment, section_map):
    text_lower = text_fragment.lower()
    
    for section_name in priority_sections:
        if section_name in text_lower:
            return 2.0
    
    for section_name in strict_reject_sections:
        if section_name in text_lower:
            return -1.0
    
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
    tokens = []
    for w in text.split():
        if len(w) <= 1:
            continue
        if w in protected_technical_tokens:
            tokens.append(w)
        elif w not in stopwords:
            tokens.append(w)
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
    
    if phrase_lower in protected_technical_tokens:
        return False
    
    if phrase_lower in technical_ontology:
        return False
    
    words = phrase_lower.split()
    if len(words) == 1 and phrase_lower in generic_noun_blacklist:
        return True
    
    if phrase_lower in generic_reject_list:
        return True
    
    if any(junk in phrase_lower for junk in junk_patterns):
        return True
    
    words = phrase_lower.split()
    if len(words) == 1 and words[0] in generic_reject_list:
        return True
    
    if len(words) > 3:
        return True
    
    stopword_count = sum(1 for w in words if w in stopwords and w not in protected_technical_tokens)
    if len(words) > 0 and (stopword_count / len(words)) > 0.5:
        return True
    
    if any(title in phrase_lower for title in job_title_indicators):
        word_count = len(words)
        if word_count >= 2:
            return True
    
    if phrase_lower in soft_skills:
        return True
    
    if contains_verb(phrase):
        return True
    
    fragment_indicators = ['content', 'information', 'various', 'across', 'processes', 'issues', 'quality', 'multiple', 'support', 'focus', 'datasets', 'collection', 'predictable']
    if len(words) >= 2:
        for indicator in fragment_indicators:
            if indicator in words and phrase_lower not in technical_ontology:
                return True
    
    adjectives = ['additional', 'various', 'multiple', 'high', 'low', 'best', 'better', 'clean', 'maintainable', 'interactive', 'responsive', 'friendly']
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
    
    common_non_tech_words = {'user', 'friendly', 'interface', 'content', 'fire', 'enthusiasts', 'insights', 'execution', 'task', 'wireframes', 'mockups', 'ensure', 'standards', 'accessibility', 'upwork', 'high', 'performance', 'interactive', 'reusable', 'quality'}
    if len(words) >= 2:
        non_tech_count = sum(1 for word in words if word in common_non_tech_words or word in generic_reject_list or word in stopwords)
        if non_tech_count >= len(words) / 2:
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
    
    if normalized_phrase in technical_ontology:
        return True
    
    if is_technical_phrase(phrase):
        tech_word_count = sum(1 for word in words if word in technical_ontology or any(word in tech for tech in technical_ontology))
        if tech_word_count == 0:
            return False
        return True
    
    return False

def extract_skills(text):
    skills_section_match = re.search(r'(?i)(?:skills?|technical\s+skills?|programming\s+languages?|core\s+competencies|technologies).*?(?=\n(?:[A-Z][a-z]+:|\Z))', text, re.DOTALL)
    
    if skills_section_match:
        priority_text = skills_section_match.group()
    else:
        priority_text = text
    
    section_map = detect_sections(text)
    sanitized = text
    text_lower = text.lower()
    
    skill_scores = {}
    skill_metadata = {}
    
    for tech_term in technical_ontology:
        pattern = r'\b' + re.escape(tech_term) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            normalized = normalize_phrase(tech_term)
            count = len(matches)
            section_priority = get_section_priority(text_lower, section_map)
            if skills_section_match:
                section_priority = 5.0
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
        
        skill_lower = skill.lower()
        normalized_skill = normalize_phrase(skill_lower)
        if skill_lower not in protected_technical_tokens and skill_lower not in technical_ontology and normalized_skill not in technical_ontology:
            continue
        
        skill_words = skill_lower.split()
        if len(skill_words) == 1 and skill_lower in generic_noun_blacklist:
            continue
        
        if skill_lower in generic_reject_list:
            continue
        
        skill_words = skill.split()
        if len(skill_words) > 3:
            continue
        
        if len(skill_words) == 1 and skill_words[0].lower() in generic_reject_list:
            continue
        
        if not is_technical_phrase(skill):
            continue
        if is_junk_phrase(skill):
            continue
        if re.search(r'[0-9]{3,}', skill):
            continue
        if re.search(r'@|\.com|http|www', skill):
            continue
        
        if contains_verb(skill):
            continue
        
        if nlp:
            doc = nlp(skill)
            has_bad_entity = False
            for ent in doc.ents:
                if ent.label_ in ['PERSON', 'GPE', 'LOC', 'DATE']:
                    if skill_lower not in protected_technical_tokens:
                        has_bad_entity = True
                        break
            if has_bad_entity:
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
        if len(final_validated_skills) >= 50:
            break
    
    return final_validated_skills if final_validated_skills else ["general"]

def extract_keywords(docs):
    if not docs or not docs[0]:
        return []
    
    text = docs[0]
    
    jd_boilerplate_patterns = [
        r'(?i)arc\.dev.*?(?:\n\n|\Z)',
        r'(?i)toptal.*?(?:\n\n|\Z)',
        r'(?i)roadmap\.sh.*?(?:\n\n|\Z)',
        r'(?i)upwork.*?(?:\n\n|\Z)',
        r'(?i)job title:.*?(?:\n|$)',
        r'(?i)location:.*?(?:\n|$)',
        r'(?i)position type:.*?(?:\n|$)',
        r'(?i)employment type:.*?(?:\n|$)',
        r'(?i)salary range:.*?(?:\n|$)',
        r'(?i)compensation:.*?(?:\n|$)',
        r'(?i)about us:?.*?(?:\n\n|\Z)',
        r'(?i)why join.*?(?:\n\n|\Z)',
        r'(?i)(?:we offer|benefits include|competitive salary|compensation package|flexible work).*?(?:\n\n|\Z)',
        r'(?i)(?:equal opportunity employer|eeo statement|diversity statement).*?(?:\n\n|\Z)',
        r'(?i)(?:to apply|how to apply|application process|submit your|send resume).*?(?:\n\n|\Z)',
        r'(?i)key components to customize.*?(?:\n\n|\Z)',
        r'(?i)(?:tech stack update|experience level adjust|company culture add).*?(?:\n\n|\Z)',
        r'\[.*?\]',
        r'\{.*?\}',
        r'(?i)(?:insert|add|update|adjust|customize).*?(?:here|below)',
        r'(?i)company name',
        r'(?i)brief description',
        r'(?i)city.*?state'
    ]
    
    for pattern in jd_boilerplate_patterns:
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
            keyword_scores[normalized] = keyword_scores.get(normalized, 0) + 5
    
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
        'collaborate', 'collaboration', 'participate', 'participation',
        'saas', 'fast', 'growing', 'dedicated', 'mission', 'creating', 'intuitive', 'financial',
        'believe', 'quality', 'centric', 'fostering', 'innovative', 'talented', 'creative',
        'translating', 'engaging', 'keen', 'eye', 'passion', 'command', 'hybrid', 'remote',
        'full', 'time', 'part', 'contract', 'brief', 'description'
    }
    
    filtered_keywords = {}
    for keyword, score in keyword_scores.items():
        if score <= 0:
            continue
        
        keyword_lower = keyword.lower()
        if keyword_lower not in protected_technical_tokens and keyword_lower not in technical_ontology:
            continue
        
        keyword_words = keyword_lower.split()
        if len(keyword_words) == 1 and keyword_lower in generic_noun_blacklist:
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
    contact_section = text[:800]
    
    location_pattern = re.search(r'(?i)(?:location|address|city|place)\s*[:|\-|–]\s*([^\n]+)', contact_section)
    if location_pattern:
        location_text = location_pattern.group(1).strip()
        location_text = re.sub(r'[\(\)\[\]\{\}]', '', location_text)
        location_text = re.sub(r'\s+', ' ', location_text).strip()
        
        if nlp:
            doc = nlp(location_text)
            person_names = [ent.text.lower() for ent in doc.ents if ent.label_ == 'PERSON']
            if person_names:
                for name in person_names:
                    name_words = name.split()
                    for name_word in name_words:
                        location_text = re.sub(r'\b' + re.escape(name_word) + r'\b', '', location_text, flags=re.IGNORECASE)
        
        words = location_text.split()
        valid_words = []
        
        resume_keywords = ['passionate', 'developer', 'engineer', 'designer', 'analyst', 'architect', 
                          'web', 'mobile', 'software', 'full', 'stack', 'frontend', 'backend',
                          'strong', 'foundation', 'with', 'experience', 'skilled', 'building',
                          'html', 'css', 'javascript', 'python', 'java', 'react', 'angular', 'vue',
                          'summary', 'profile', 'resume', 'cv', 'curriculum', 'vitae']
        
        for word in words:
            word_clean = word.strip(',').lower()
            
            if word_clean in resume_keywords:
                break
            
            if '@' in word or 'http' in word or '.com' in word:
                break
            
            if word.strip():
                valid_words.append(word)
            
            if len(valid_words) >= 6:
                break
        
        location_text = ' '.join(valid_words).strip()
        location_text = re.sub(r'\s+', ' ', location_text).strip()
        
        if location_text and 5 <= len(location_text) <= 80:
            return location_text
    
    if nlp:
        doc = nlp(contact_section)
        gpe_entities = []
        
        for ent in doc.ents:
            if ent.label_ in ['GPE', 'LOC']:
                gpe_lower = ent.text.lower()
                if gpe_lower not in technical_ontology and len(ent.text.split()) <= 3:
                    has_contact_nearby = False
                    for token in doc:
                        if token.i >= ent.start - 20 and token.i <= ent.end + 20:
                            if re.match(r'^\+?\d[\d\-\(\)\s]{7,}$', token.text) or '@' in token.text:
                                has_contact_nearby = True
                                break
                    
                    if has_contact_nearby or ent.start_char < 300:
                        gpe_entities.append(ent.text)
        
        if gpe_entities:
            unique_gpe = []
            for gpe in gpe_entities:
                if gpe not in unique_gpe:
                    unique_gpe.append(gpe)
            return ', '.join(unique_gpe[:3])
    
    return ""

def extract_name(text):
    header_text = text[:500]
    
    if nlp:
        doc = nlp(header_text)
        for ent in doc.ents:
            if ent.label_ == 'PERSON' and ent.start_char < 300:
                words = ent.text.split()
                if 2 <= len(words) <= 5:
                    is_job_title = any(indicator in ent.text.lower() for indicator in job_title_indicators)
                    has_summary_words = any(word in ent.text.lower() for word in ['summary', 'profile', 'passionate', 'enthusiastic'])
                    if not is_job_title and not has_summary_words:
                        return ent.text
    
    lines = header_text.split('\n')
    for line in lines[:3]:
        line_clean = line.strip()
        if 2 <= len(line_clean.split()) <= 5 and len(line_clean) < 50:
            if not re.search(r'@|http|www|\d{3}|engineer|developer|designer|analyst', line_clean.lower()):
                return line_clean
    
    return ""

def extract_education_degrees(text):
    degrees = []
    text_lower = text.lower()
    
    education_section = re.search(r'(?i)education.*?(?=\n(?:experience|projects|skills|certifications|work)|\Z)', text, re.DOTALL)
    search_text = education_section.group() if education_section else text[:3000]
    search_lower = search_text.lower()
    
    degree_mapping = {
        r'(?:bachelor|ba|b\.a|bs|b\.s|bsc|b\.sc|b\.e|be|b\.tech|btech)\s+(?:of\s+)?(?:engineering|science|technology|arts|computer\s+science)': 'Bachelor of Engineering',
        r'(?:master|ma|m\.a|ms|m\.s|msc|m\.sc|m\.e|me|m\.tech|mtech)\s+(?:of\s+)?(?:engineering|science|technology|arts|computer\s+science)': 'Master of Engineering',
        r'(?:phd|ph\.d|doctorate)': 'PhD',
        r'(?:mba|m\.b\.a)': 'MBA',
        r'(?:diploma)': 'Diploma'
    }
    
    for pattern, degree_name in degree_mapping.items():
        if re.search(pattern, search_lower):
            degrees.append(degree_name)
    
    if not degrees:
        simple_patterns = {
            r'\bb\.?\s*e\.?\b': 'Bachelor of Engineering',
            r'\bb\.?\s*tech\b': 'Bachelor of Technology',
            r'\bb\.?\s*s\.?c?\b\s+(?:computer|engineering)': 'Bachelor of Science',
            r'\bm\.?\s*e\.?\b': 'Master of Engineering',
            r'\bm\.?\s*tech\b': 'Master of Technology',
            r'\bm\.?\s*s\.?c?\b\s+(?:computer|engineering)': 'Master of Science'
        }
        
        for pattern, degree_name in simple_patterns.items():
            if re.search(pattern, search_lower):
                degrees.append(degree_name)
                break
    
    return list(dict.fromkeys(degrees))[:3]

def extract_education_fields(text):
    fields = []
    
    education_section = re.search(r'(?i)education.*?(?=\n(?:experience|projects|skills|certifications|work)|\Z)', text, re.DOTALL)
    search_text = education_section.group() if education_section else text[:3000]
    search_lower = search_text.lower()
    
    field_map = {
        r'\bcse\b': 'Computer Science and Engineering',
        r'\bcomputer science(?:\s+and\s+engineering)?\b': 'Computer Science',
        r'\binformation technology\b': 'Information Technology',
        r'\bit\b(?!\s+was)(?!\s+is)(?!\s+has)': 'Information Technology',
        r'\bece\b': 'Electronics and Communication Engineering',
        r'\beee\b': 'Electrical and Electronics Engineering',
        r'\bsoftware engineering\b': 'Software Engineering',
        r'\bdata science\b': 'Data Science',
        r'\bmechanical engineering\b': 'Mechanical Engineering',
        r'\bcivil engineering\b': 'Civil Engineering',
        r'\belectrical engineering\b': 'Electrical Engineering',
        r'\bbusiness administration\b': 'Business Administration',
        r'\bmathematics\b': 'Mathematics',
        r'\bphysics\b': 'Physics',
        r'\bchemistry\b': 'Chemistry'
    }
    
    for pattern, full_name in field_map.items():
        if re.search(pattern, search_lower):
            if full_name not in fields:
                fields.append(full_name)
    
    return fields[:3]

def extract_institutions(text):
    education_section = re.search(r'(?i)education.*?(?=\n(?:experience|projects|skills|certifications|work)|\Z)', text, re.DOTALL)
    search_text = education_section.group() if education_section else text[:3000]
    
    education_keywords = ['university', 'college', 'institute', 'school', 'academy', 'engineering college']
    
    institutions = []
    
    if nlp:
        doc = nlp(search_text[:10000])
        
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                org_lower = ent.text.lower()
                if any(edu_word in org_lower for edu_word in education_keywords):
                    if org_lower not in technical_ontology:
                        institutions.append(ent.text)
    
    if not institutions:
        lines = search_text.split('\n')
        for line in lines:
            line_lower = line.lower()
            line_clean = line.strip()
            
            if any(keyword in line_lower for keyword in education_keywords):
                if 10 <= len(line_clean) <= 100:
                    if not re.search(r'@|http|www|\d{10}', line_clean):
                        institutions.append(line_clean)
    
    return list(dict.fromkeys(institutions))[:3]

def extract_experience_roles(text):
    experience_section = re.search(r'(?i)(?:experience|work\s+experience).*?(?=\n(?:education|projects|skills|certifications)|\Z)', text, re.DOTALL)
    search_text = experience_section.group() if experience_section else text[:3000]
    
    role_indicators = {
        'engineer', 'developer', 'analyst', 'scientist', 'manager', 'architect',
        'designer', 'administrator', 'lead', 'specialist', 'consultant', 'coordinator',
        'associate', 'intern', 'trainee', 'dev', 'programmer'
    }
    
    education_excludes = ['college', 'university', 'institute', 'school', 'academy']
    
    roles = []
    text_lower = search_text.lower()
    
    lines = search_text.split('\n')
    for line in lines:
        line_lower = line.lower()
        line_clean = line.strip()
        
        if any(edu in line_lower for edu in education_excludes):
            continue
        
        if re.search(r'@|http|www|education|degree', line_lower):
            continue
        
        words = line_lower.split()
        if 2 <= len(words) <= 8:
            if any(indicator in line_lower for indicator in role_indicators):
                if len(line_clean) < 80:
                    if line_clean not in roles:
                        roles.append(line_clean)
    
    return roles[:5]

def extract_experience_companies(text):
    if not nlp:
        return []
    
    experience_section = re.search(r'(?i)(?:experience|work\s+experience).*?(?=\n(?:education|projects|skills|certifications)|\Z)', text, re.DOTALL)
    search_text = experience_section.group() if experience_section else text[:3000]
    
    companies = []
    doc = nlp(search_text[:10000])
    
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

def extract_education_entries(text):
    education_section = re.search(r'(?i)education.*?(?=\n(?:experience|projects|skills|certifications|work)|\Z)', text, re.DOTALL)
    if not education_section:
        return []
    
    section_text = education_section.group()
    lines = section_text.split('\n')
    
    entries = []
    current_entry = {'degree': '', 'field': '', 'institution': '', 'year': ''}
    
    degree_patterns = [
        (r'(?i)\b(bachelor|b\.?s\.?|b\.?a\.?|b\.?e\.?|b\.?tech|btech|bsc)\b', 'Bachelor'),
        (r'(?i)\b(master|m\.?s\.?|m\.?a\.?|m\.?e\.?|m\.?tech|mtech|msc)\b', 'Master'),
        (r'(?i)\b(phd|ph\.d|doctorate)\b', 'PhD'),
        (r'(?i)\b(diploma)\b', 'Diploma'),
        (r'(?i)\b(mba|m\.b\.a)\b', 'MBA')
    ]
    
    field_keywords = ['computer science', 'information technology', 'engineering', 'business', 'science', 'arts', 'cse', 'ece', 'eee', 'mechanical', 'civil', 'electrical']
    institution_keywords = ['university', 'college', 'institute', 'school']
    
    for line in lines:
        line_clean = line.strip()
        line_lower = line_clean.lower()
        
        if len(line_clean) < 5:
            continue
        
        degree_found = None
        for pattern, degree_type in degree_patterns:
            if re.search(pattern, line_lower):
                degree_found = degree_type
                break
        
        field_found = None
        for field in field_keywords:
            if field in line_lower:
                field_found = field.title()
                break
        
        institution_found = None
        if any(keyword in line_lower for keyword in institution_keywords):
            institution_found = line_clean
        
        year_match = re.findall(r'\b(19|20)\d{2}\b', line_clean)
        year_found = year_match[-1] if year_match else None
        
        if degree_found or field_found or institution_found or year_found:
            if current_entry['degree'] or current_entry['field'] or current_entry['institution'] or current_entry['year']:
                if degree_found and not current_entry['degree']:
                    current_entry['degree'] = degree_found
                if field_found and not current_entry['field']:
                    current_entry['field'] = field_found
                if institution_found and not current_entry['institution']:
                    current_entry['institution'] = institution_found
                if year_found and not current_entry['year']:
                    current_entry['year'] = year_found
            else:
                if degree_found:
                    current_entry['degree'] = degree_found
                if field_found:
                    current_entry['field'] = field_found
                if institution_found:
                    current_entry['institution'] = institution_found
                if year_found:
                    current_entry['year'] = year_found
            
            if current_entry['degree'] and current_entry['institution']:
                entries.append(current_entry.copy())
                current_entry = {'degree': '', 'field': '', 'institution': '', 'year': ''}
    
    if current_entry['degree'] or current_entry['institution']:
        entries.append(current_entry)
    
    return entries[:3]

def extract_experience_entries(text):
    experience_section = re.search(r'(?i)(?:experience|work\\s+experience).*?(?=\\n(?:education|projects|skills|certifications)|\\Z)', text, re.DOTALL)
    if not experience_section:
        return []
    
    section_text = experience_section.group()
    lines = section_text.split('\\n')
    
    entries = []
    current_entry = {'role': '', 'company': '', 'duration': '', 'responsibilities': [], 'skills': []}
    
    role_indicators = ['engineer', 'developer', 'analyst', 'scientist', 'manager', 'architect', 'designer', 'lead', 'consultant', 'intern']
    
    for i, line in enumerate(lines):
        line_clean = line.strip()
        line_lower = line_clean.lower()
        
        if len(line_clean) < 3:
            if current_entry['role']:
                entries.append(current_entry.copy())
                current_entry = {'role': '', 'company': '', 'duration': '', 'responsibilities': [], 'skills': []}
            continue
        
        is_role = any(indicator in line_lower for indicator in role_indicators) and len(line_clean.split()) <= 8
        year_range = re.search(r'\\b(\\d{4})\\s*-\\s*(\\d{4}|present|current)\\b', line_lower)
        is_bullet = line_clean.startswith('•') or line_clean.startswith('-') or line_clean.startswith('*')
        
        if is_role and not current_entry['role']:
            current_entry['role'] = line_clean
        elif year_range and not current_entry['duration']:
            current_entry['duration'] = year_range.group()
        elif is_bullet and current_entry['role']:
            responsibility = line_clean.lstrip('•-* ').strip()
            current_entry['responsibilities'].append(responsibility)
            
            for tech_term in technical_ontology:
                if tech_term in responsibility.lower():
                    if tech_term not in current_entry['skills']:
                        current_entry['skills'].append(tech_term)
        elif nlp and not current_entry['company'] and current_entry['role']:
            doc = nlp(line_clean)
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                    org_lower = ent.text.lower()
                    if org_lower not in technical_ontology:
                        current_entry['company'] = ent.text
                        break
    
    if current_entry['role']:
        entries.append(current_entry)
    
    return entries[:5]

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
            words = phrase.lower().split()
            if len(words) >= 2:
                tech_count = sum(1 for word in words if word in technical_ontology or any(word in tech for tech in technical_ontology))
                if tech_count >= 2:
                    for word in words:
                        word_clean = word.strip()
                        if word_clean and len(word_clean) > 1 and (word_clean in technical_ontology or any(word_clean in tech for tech in technical_ontology)):
                            expanded.add(word_clean)
                    continue
            
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
    
    expanded_phrases = []
    for phrase in phrases:
        if phrase and phrase.lower() != 'general':
            expanded_phrases.append(phrase)
    phrases = split_compound_phrases(expanded_phrases)
    
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
        
        phrase_normalized = normalize_phrase(phrase.lower())
        phrase_words = phrase_normalized.split()
        
        if len(phrase_words) == 1 and phrase_normalized in generic_noun_blacklist:
            continue
        
        is_in_reject_list = phrase_normalized in generic_reject_list or any(word in generic_reject_list for word in phrase_words if len(phrase_words) == 1)
        if is_in_reject_list:
            continue
        
        exact_match = phrase_normalized in technical_ontology
        if not exact_match:
            has_match = False
            for tech in technical_ontology:
                if tech == phrase_normalized:
                    has_match = True
                    break
            if not has_match and len(phrase_words) > 1:
                continue
        
        if skill_type == 'programming_language':
            if phrase_normalized not in classified['frameworks'] and phrase_normalized not in classified['databases']:
                classified['languages'].append(phrase_normalized)
        elif skill_type == 'web_standard':
            if phrase_normalized in ['html', 'html5', 'css', 'css3']:
                classified['languages'].append(phrase_normalized)
            else:
                classified['technical_skills'].append(phrase_normalized)
        elif skill_type == 'database':
            if phrase_normalized not in classified['languages']:
                classified['databases'].append(phrase_normalized)
        elif skill_type == 'framework':
            if phrase_normalized not in classified['languages']:
                classified['frameworks'].append(phrase_normalized)
        elif skill_type in ['dev_tool', 'build_tool', 'version_control_tool', 'testing_tool', 'bi_tool', 'analytics_tool']:
            if phrase_normalized not in classified['languages'] and phrase_normalized not in classified['frameworks']:
                classified['tools'].append(phrase_normalized)
        elif skill_type in ['library', 'cloud_service', 'ml_method', 'ai_method', 'css_preprocessor', 'rendering_framework', 'data_method']:
            if phrase_normalized not in classified['languages'] and phrase_normalized not in classified['frameworks']:
                classified['technical_skills'].append(phrase_normalized)
    
    for key in classified:
        classified[key] = list(dict.fromkeys(classified[key]))
    
    frameworks_set = set()
    for skill_type, skills in typed_technical_ontology.items():
        if skill_type == 'framework':
            frameworks_set.update(skills)
    
    databases_set = set()
    for skill_type, skills in typed_technical_ontology.items():
        if skill_type == 'database':
            databases_set.update(skills)
    
    languages_corrected = []
    for lang in classified['languages']:
        if lang in frameworks_set:
            if lang not in classified['frameworks']:
                classified['frameworks'].append(lang)
        elif lang in databases_set:
            if lang not in classified['databases']:
                classified['databases'].append(lang)
        else:
            languages_corrected.append(lang)
    
    classified['languages'] = languages_corrected
    
    tools_corrected = []
    for tool in classified['tools']:
        if tool in databases_set:
            if tool not in classified['databases']:
                classified['databases'].append(tool)
        elif tool in frameworks_set:
            if tool not in classified['frameworks']:
                classified['frameworks'].append(tool)
        else:
            tools_corrected.append(tool)
    
    classified['tools'] = tools_corrected
    
    frameworks_corrected = []
    for fw in classified['frameworks']:
        if fw in databases_set:
            if fw not in classified['databases']:
                classified['databases'].append(fw)
        else:
            frameworks_corrected.append(fw)
    
    classified['frameworks'] = frameworks_corrected
    
    return classified

def classify_jd_keywords(phrases, jd_text):
    classified = {
        'technical_skills': [],
        'tools': [],
        'frameworks': [],
        'languages': [],
        'databases': []
    }
    
    jd_lower = jd_text.lower()
    phrases = split_compound_phrases(phrases)
    
    for phrase in phrases:
        phrase = phrase.strip()
        if not phrase or len(phrase) <= 1:
            continue
        
        phrase_lower = phrase.lower()
        phrase_pattern = r'\b' + re.escape(phrase_lower) + r'\b'
        if not re.search(phrase_pattern, jd_lower):
            continue
        
        if not is_valid_technical_skill(phrase):
            continue
        
        if is_junk_phrase(phrase):
            continue
        
        skill_type = get_skill_type(phrase)
        if skill_type is None:
            continue
        
        phrase_normalized = normalize_phrase(phrase_lower)
        phrase_words = phrase_normalized.split()
        
        if len(phrase_words) == 1 and phrase_normalized in generic_noun_blacklist:
            continue
        
        is_in_reject_list = phrase_normalized in generic_reject_list or any(word in generic_reject_list for word in phrase_words if len(phrase_words) == 1)
        if is_in_reject_list:
            continue
        
        exact_match = phrase_normalized in technical_ontology
        if not exact_match:
            has_match = False
            for tech in technical_ontology:
                if tech == phrase_normalized:
                    has_match = True
                    break
            if not has_match and len(phrase_words) > 1:
                continue
        
        if skill_type == 'programming_language':
            if phrase_normalized not in classified['frameworks'] and phrase_normalized not in classified['databases']:
                classified['languages'].append(phrase_normalized)
        elif skill_type == 'database':
            if phrase_normalized not in classified['languages']:
                classified['databases'].append(phrase_normalized)
        elif skill_type == 'framework':
            if phrase_normalized not in classified['languages']:
                classified['frameworks'].append(phrase_normalized)
        elif skill_type in ['library', 'css_preprocessor', 'web_standard', 'rendering_framework']:
            if phrase_normalized not in classified['languages'] and phrase_normalized not in classified['frameworks']:
                classified['technical_skills'].append(phrase_normalized)
        elif skill_type in ['dev_tool', 'build_tool', 'version_control_tool', 'testing_tool', 'bi_tool', 'analytics_tool']:
            if phrase_normalized not in classified['languages'] and phrase_normalized not in classified['frameworks']:
                classified['tools'].append(phrase_normalized)
        elif skill_type in ['cloud_service', 'ml_method', 'ai_method', 'data_method']:
            if phrase_normalized not in classified['languages'] and phrase_normalized not in classified['frameworks']:
                classified['technical_skills'].append(phrase_normalized)
    
    for key in classified:
        classified[key] = list(dict.fromkeys(classified[key]))
    
    prog_langs_set = set()
    for skill_type, skills in typed_technical_ontology.items():
        if skill_type == 'programming_language':
            prog_langs_set.update(skills)
    
    frameworks_set = set()
    for skill_type, skills in typed_technical_ontology.items():
        if skill_type == 'framework':
            frameworks_set.update(skills)
    
    databases_set = set()
    for skill_type, skills in typed_technical_ontology.items():
        if skill_type == 'database':
            databases_set.update(skills)
    
    libraries_set = set()
    for skill_type, skills in typed_technical_ontology.items():
        if skill_type in ['library', 'css_preprocessor']:
            libraries_set.update(skills)
    
    web_standards_set = set()
    for skill_type, skills in typed_technical_ontology.items():
        if skill_type == 'web_standard':
            web_standards_set.update(skills)
    
    languages_corrected = []
    for lang in classified['languages']:
        if lang in frameworks_set:
            if lang not in classified['frameworks']:
                classified['frameworks'].append(lang)
        elif lang in databases_set:
            if lang not in classified['databases']:
                classified['databases'].append(lang)
        elif lang in libraries_set or lang in web_standards_set:
            if lang not in classified['technical_skills']:
                classified['technical_skills'].append(lang)
        elif lang in prog_langs_set:
            languages_corrected.append(lang)
    
    classified['languages'] = languages_corrected
    
    tools_corrected = []
    for tool in classified['tools']:
        if tool in databases_set:
            if tool not in classified['databases']:
                classified['databases'].append(tool)
        elif tool in frameworks_set:
            if tool not in classified['frameworks']:
                classified['frameworks'].append(tool)
        else:
            tools_corrected.append(tool)
    
    classified['tools'] = tools_corrected
    
    frameworks_corrected = []
    for fw in classified['frameworks']:
        if fw in databases_set:
            if fw not in classified['databases']:
                classified['databases'].append(fw)
        else:
            frameworks_corrected.append(fw)
    
    classified['frameworks'] = frameworks_corrected
    
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
    
    junk_terms = {'general', 'dev', 'development', 'programming', 'coding', 'scripting', 'software', 'web', 'application', 
                  'system', 'technology', 'technical', 'digital', 'online', 'virtual', 'remote', 'hybrid',
                  'go', 'excel', 'work', 'job', 'role', 'team', 'company', 'business', 'project',
                  'artificial', 'intelligence', 'chrome', 'edge', 'firefox', 'safari', 'studio', 'visual',
                  'code', 'devtools', 'tools', 'platforms', 'notebook', 'development'}
    
    for category in ['technical_skills', 'languages', 'frameworks', 'tools', 'databases']:
        classified[category] = [skill for skill in classified[category] if skill.lower() not in junk_terms]
    
    total_classified = (
        len(classified['technical_skills']) + 
        len(classified['languages']) + 
        len(classified['frameworks']) + 
        len(classified['tools']) + 
        len(classified['databases'])
    )
    
    clean_extracted_skills = [s for s in all_skills if s.lower() not in junk_terms]
    
    if total_classified == 0 and len(clean_extracted_skills) > 0:
        classified['technical_skills'] = clean_extracted_skills[:15]
    
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
    
    education_entries = extract_education_entries(text)
    experience_entries = extract_experience_entries(text)
    
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
        'soft_skills': candidate_soft_skills[:10],
        'education_entries': education_entries,
        'experience_entries': experience_entries
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
    
    classified = classify_jd_keywords(all_keywords, text)
    
    junk_terms = {'general', 'dev', 'development', 'programming', 'coding', 'scripting', 'software', 'web', 'application',
                  'system', 'technology', 'technical', 'digital', 'online', 'virtual', 'remote', 'hybrid',
                  'go', 'excel', 'work', 'job', 'role', 'team', 'company', 'business', 'project',
                  'artificial', 'intelligence', 'chrome', 'edge', 'firefox', 'safari', 'studio', 'visual',
                  'code', 'devtools', 'tools', 'platforms', 'notebook', 'development'}
    
    for category in ['technical_skills', 'languages', 'frameworks', 'tools', 'databases']:
        classified[category] = [skill for skill in classified[category] if skill.lower() not in junk_terms]
    
    total_classified = (
        len(classified['technical_skills']) + 
        len(classified['languages']) + 
        len(classified['frameworks']) + 
        len(classified['tools']) + 
        len(classified['databases'])
    )
    
    clean_extracted_keywords = [k for k in all_keywords if k.lower() not in junk_terms]
    
    if total_classified == 0 and len(clean_extracted_keywords) > 0:
        classified['technical_skills'] = clean_extracted_keywords[:15]
    
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
        resp_classified = classify_jd_keywords(resp_skills, text)
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
        nice_classified = classify_jd_keywords(nice_skills, text)
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
