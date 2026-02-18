import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILL_TAXONOMY = {
    'programming_languages': {
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'csharp', 'go', 'golang',
        'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'perl', 'matlab', 'sql', 'c'
    },
    'markup_languages': {
        'html', 'html5', 'css', 'css3', 'xml', 'markdown'
    },
    'frameworks': {
        'react', 'reactjs', 'react js', 'angular', 'vue', 'vuejs', 'vue js', 'svelte',
        'next js', 'nextjs', 'gatsby', 'ember', 'backbone', 'django', 'flask', 'fastapi',
        'spring', 'spring boot', 'rails', 'asp net', 'dotnet', 'express', 'expressjs', 'express js',
        'laravel', 'symfony', 'codeigniter', 'nestjs', 'nest js', 'nuxt js', 'nuxtjs'
    },
    'libraries': {
        'redux', 'mobx', 'recoil', 'zustand', 'jotai', 'tensorflow', 'pytorch', 'keras',
        'scikit learn', 'sklearn', 'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn',
        'plotly', 'xgboost', 'lightgbm', 'catboost', 'apollo', 'prisma', 'typeorm',
        'sequelize', 'mongoose', 'sqlalchemy', 'hibernate', 'entity framework', 'jwt',
        'lodash', 'axios', 'jquery', 'bootstrap', 'material ui', 'mui', 'chakra ui', 'ant design',
        'tailwind', 'tailwindcss', 'sass', 'scss', 'less'
    },
    'databases': {
        'mysql', 'postgresql', 'postgres', 'mongodb', 'mongo', 'redis', 'cassandra',
        'dynamodb', 'oracle', 'sqlite', 'mariadb', 'mssql', 'elasticsearch', 'elastic',
        'couchdb', 'neo4j', 'firebase', 'firestore', 'supabase'
    },
    'tools': {
        'docker', 'kubernetes', 'k8s', 'git', 'github', 'gitlab', 'bitbucket', 'jenkins',
        'circleci', 'travis ci', 'aws', 'azure', 'gcp', 'google cloud', 'lambda',
        'terraform', 'ansible', 'chef', 'puppet', 'webpack', 'vite', 'rollup', 'babel',
        'npm', 'yarn', 'postman', 'insomnia', 'swagger', 'jira', 'confluence', 'trello',
        'figma', 'sketch', 'adobe xd', 'vscode', 'intellij', 'pycharm', 'visual studio'
    },
    'concepts': {
        'restful', 'rest api', 'graphql', 'grpc', 'microservices', 'agile', 'scrum',
        'tdd', 'test driven development', 'ci/cd', 'devops', 'oop', 'solid', 'design patterns',
        'mvc', 'mvvm', 'oauth', 'oauth2', 'websocket', 'api', 'soap'
    }
}

def normalize_text(text):
    if not text:
        return ""
    return text.lower().strip()

def normalize_list(items):
    if not items:
        return []
    return [normalize_text(item) for item in items if item]

def classify_skill(skill):
    skill_norm = normalize_text(skill)
    for category, skills in SKILL_TAXONOMY.items():
        if skill_norm in skills:
            return category
    return 'technical_skills'

def classify_skills_by_taxonomy(skills):
    classified = {category: [] for category in SKILL_TAXONOMY.keys()}
    classified['technical_skills'] = []
    
    for skill in skills:
        category = classify_skill(skill)
        classified[category].append(skill)
    
    return classified

def detect_domain(text, roles=None):
    text_lower = normalize_text(text)
    role_text = ' '.join(normalize_list(roles or []))
    combined = text_lower + ' ' + role_text
    
    frontend_keywords = ['frontend', 'front-end', 'front end', 'ui', 'react', 'angular',
                         'vue', 'html', 'css', 'javascript', 'web developer', 'ui developer']
    backend_keywords = ['backend', 'back-end', 'back end', 'api', 'server', 'django',
                        'flask', 'spring', 'node', 'express', 'database', 'sql']
    fullstack_keywords = ['fullstack', 'full-stack', 'full stack', 'mern', 'mean', 'lamp']
    data_keywords = ['data', 'analytics', 'machine learning', 'ml', 'ai', 'data scientist',
                     'data analyst', 'data engineer', 'python', 'pandas', 'numpy', 'tensorflow']
    mobile_keywords = ['mobile', 'android', 'ios', 'react native', 'flutter', 'swift', 'kotlin']
    devops_keywords = ['devops', 'sre', 'cloud', 'aws', 'azure', 'docker', 'kubernetes', 'ci/cd']
    
    scores = {
        'frontend': sum(1 for kw in frontend_keywords if kw in combined),
        'backend': sum(1 for kw in backend_keywords if kw in combined),
        'fullstack': sum(1 for kw in fullstack_keywords if kw in combined),
        'data': sum(1 for kw in data_keywords if kw in combined),
        'mobile': sum(1 for kw in mobile_keywords if kw in combined),
        'devops': sum(1 for kw in devops_keywords if kw in combined)
    }
    
    domain = max(scores, key=scores.get)
    return domain if scores[domain] > 0 else 'general'

def calculate_weighted_score(matched, required, category_weight):
    if not required:
        return 0.0
    match_ratio = len(matched) / len(required)
    return match_ratio * category_weight

def compare_profiles(resume_profile, job_profile):
    resume_skills_all = set()
    resume_skills_all.update(normalize_list(resume_profile.get('technical_skills', [])))
    resume_skills_all.update(normalize_list(resume_profile.get('programming_languages', [])))
    resume_skills_all.update(normalize_list(resume_profile.get('frameworks', [])))
    resume_skills_all.update(normalize_list(resume_profile.get('tools', [])))
    resume_skills_all.update(normalize_list(resume_profile.get('databases', [])))
    
    jd_skills_all = set()
    jd_skills_all.update(normalize_list(job_profile.get('required_skills', [])))
    jd_skills_all.update(normalize_list(job_profile.get('required_languages', [])))
    jd_skills_all.update(normalize_list(job_profile.get('required_frameworks', [])))
    jd_skills_all.update(normalize_list(job_profile.get('required_tools', [])))
    jd_skills_all.update(normalize_list(job_profile.get('required_databases', [])))
    
    resume_classified = classify_skills_by_taxonomy(list(resume_skills_all))
    jd_classified = classify_skills_by_taxonomy(list(jd_skills_all))
    
    matched_by_category = {}
    missing_by_category = {}
    
    for category in SKILL_TAXONOMY.keys():
        resume_cat = set(resume_classified[category])
        jd_cat = set(jd_classified[category])
        matched_by_category[category] = list(resume_cat.intersection(jd_cat))
        missing_by_category[category] = list(jd_cat - resume_cat)
    
    frameworks_score = calculate_weighted_score(
        matched_by_category['frameworks'],
        jd_classified['frameworks'],
        0.35
    )
    
    languages_score = calculate_weighted_score(
        matched_by_category['programming_languages'] + matched_by_category['markup_languages'],
        jd_classified['programming_languages'] + jd_classified['markup_languages'],
        0.25
    )
    
    databases_score = calculate_weighted_score(
        matched_by_category['databases'],
        jd_classified['databases'],
        0.10
    )
    
    tools_score = calculate_weighted_score(
        matched_by_category['tools'],
        jd_classified['tools'],
        0.10
    )
    
    resume_experience = resume_profile.get('experience_years_estimated', 0)
    jd_experience_str = job_profile.get('required_experience_years', '')
    
    if isinstance(resume_experience, str):
        try:
            resume_experience = int(resume_experience)
        except:
            resume_experience = 0
    
    if isinstance(jd_experience_str, str) and jd_experience_str:
        try:
            jd_experience = int(re.search(r'\d+', str(jd_experience_str)).group())
        except:
            jd_experience = 0
    else:
        jd_experience = 0
    
    jd_domain = detect_domain(
        job_profile.get('job_role', ''),
        job_profile.get('required_skills', [])
    )
    
    resume_domain = detect_domain(
        '',
        resume_profile.get('experience_roles', []) + resume_profile.get('project_technologies', [])
    )
    
    domain_match = (jd_domain == resume_domain or resume_domain == 'fullstack' or jd_domain == 'general')
    
    experience_match = resume_experience >= jd_experience if jd_experience > 0 else True
    
    if not experience_match:
        experience_score = 0.05
    elif domain_match:
        experience_score = 0.10
    else:
        experience_score = 0.05
    
    resume_degrees = set(normalize_list(resume_profile.get('education_degrees', [])))
    jd_education = set(normalize_list(job_profile.get('required_education', [])))
    
    education_match = True
    if jd_education:
        if 'bachelor' in ' '.join(jd_education) or 'bsc' in ' '.join(jd_education) or 'btech' in ' '.join(jd_education):
            education_match = any('bachelor' in deg or 'bsc' in deg or 'btech' in deg or 'master' in deg or 'phd' in deg for deg in resume_degrees)
        elif 'master' in ' '.join(jd_education):
            education_match = any('master' in deg or 'phd' in deg for deg in resume_degrees)
    
    education_score = 0.10 if education_match else 0.05
    
    final_score = (
        frameworks_score +
        languages_score +
        databases_score +
        tools_score +
        experience_score +
        education_score
    ) * 100
    
    final_score = min(round(final_score, 2), 100.0)
    
    top_strengths = []
    if matched_by_category['frameworks']:
        top_strengths.append(f"Strong framework match: {', '.join(matched_by_category['frameworks'][:3])}")
    if matched_by_category['programming_languages']:
        top_strengths.append(f"Proficient in required languages: {', '.join(matched_by_category['programming_languages'][:3])}")
    if matched_by_category['databases']:
        top_strengths.append(f"Database experience: {', '.join(matched_by_category['databases'][:2])}")
    if experience_match and domain_match:
        top_strengths.append(f"Relevant {resume_experience}+ years in {resume_domain} domain")
    
    major_gaps = []
    if missing_by_category['frameworks']:
        major_gaps.append(f"Missing critical frameworks: {', '.join(missing_by_category['frameworks'][:3])}")
    if missing_by_category['programming_languages']:
        major_gaps.append(f"Missing required languages: {', '.join(missing_by_category['programming_languages'][:2])}")
    if not experience_match:
        major_gaps.append(f"Experience gap: {resume_experience} years vs {jd_experience} required")
    if not domain_match:
        major_gaps.append(f"Domain mismatch: Resume shows {resume_domain}, but role requires {jd_domain}")
    if not education_match:
        major_gaps.append("Education requirements not met")
    
    if not major_gaps:
        major_gaps.append("No critical gaps identified")
    
    experience_analysis = f"Candidate has {resume_experience} years of experience in {resume_domain} domain. "
    if domain_match:
        experience_analysis += f"Domain aligns well with {jd_domain} role requirements."
    else:
        experience_analysis += f"Domain ({resume_domain}) differs from required {jd_domain}, which may impact role fit."
    
    if final_score >= 75:
        recommendation = "Strong Fit"
        decision_summary = "Highly recommended for interview. Strong technical match with relevant experience."
    elif final_score >= 50:
        recommendation = "Moderate Fit"
        decision_summary = "Consider for interview. Has foundational skills but gaps in critical areas."
    elif final_score >= 30:
        recommendation = "Low Fit"
        decision_summary = "Not recommended. Significant gaps in required technical skills and experience."
    else:
        recommendation = "Not Suitable"
        decision_summary = "Not qualified. Missing most critical requirements."
    
    explanation = {
        'decision_summary': decision_summary,
        'top_strengths': top_strengths[:3],
        'major_gaps': major_gaps[:3],
        'experience_relevance': experience_analysis,
        'domain_match': domain_match,
        'jd_domain': jd_domain,
        'resume_domain': resume_domain
    }
    
    matched_skills = list(resume_skills_all.intersection(jd_skills_all))
    missing_skills = list(jd_skills_all - resume_skills_all)
    
    resume_languages = set(normalize_list(resume_profile.get('programming_languages', [])))
    jd_languages = set(normalize_list(job_profile.get('required_languages', [])))
    matched_languages = list(resume_languages.intersection(jd_languages))
    missing_languages = list(jd_languages - resume_languages)
    
    resume_frameworks = set(normalize_list(resume_profile.get('frameworks', [])))
    jd_frameworks = set(normalize_list(job_profile.get('required_frameworks', [])))
    matched_frameworks = list(resume_frameworks.intersection(jd_frameworks))
    missing_frameworks = list(jd_frameworks - resume_frameworks)
    
    resume_tools = set(normalize_list(resume_profile.get('tools', [])))
    jd_tools = set(normalize_list(job_profile.get('required_tools', [])))
    matched_tools = list(resume_tools.intersection(jd_tools))
    missing_tools = list(jd_tools - resume_tools)
    
    resume_databases = set(normalize_list(resume_profile.get('databases', [])))
    jd_databases = set(normalize_list(job_profile.get('required_databases', [])))
    matched_databases = list(resume_databases.intersection(jd_databases))
    missing_databases = list(jd_databases - resume_databases)
    
    framework_ratio = (len(matched_frameworks) / len(jd_frameworks) * 100) if jd_frameworks else 0
    language_ratio = (len(matched_languages) / len(jd_languages) * 100) if jd_languages else 0
    database_ratio = (len(matched_databases) / len(jd_databases) * 100) if jd_databases else 0
    tool_ratio = (len(matched_tools) / len(jd_tools) * 100) if jd_tools else 0
    
    return {
        'matched_skills': sorted(matched_skills),
        'missing_skills': sorted(missing_skills),
        'matched_languages': sorted(matched_languages),
        'missing_languages': sorted(missing_languages),
        'matched_frameworks': sorted(matched_frameworks),
        'missing_frameworks': sorted(missing_frameworks),
        'matched_tools': sorted(matched_tools),
        'missing_tools': sorted(missing_tools),
        'matched_databases': sorted(matched_databases),
        'missing_databases': sorted(missing_databases),
        'experience_match': experience_match,
        'education_match': education_match,
        'match_percentage': final_score,
        'framework_ratio': round(framework_ratio, 2),
        'language_ratio': round(language_ratio, 2),
        'database_ratio': round(database_ratio, 2),
        'tool_ratio': round(tool_ratio, 2),
        'recommendation': recommendation,
        'resume_experience_years': resume_experience,
        'required_experience_years': jd_experience,
        'explanation': explanation,
        'weighted_scores': {
            'frameworks': round(frameworks_score * 100, 2),
            'languages': round(languages_score * 100, 2),
            'databases': round(databases_score * 100, 2),
            'tools': round(tools_score * 100, 2),
            'experience': round(experience_score * 100, 2),
            'education': round(education_score * 100, 2)
        }
    }
