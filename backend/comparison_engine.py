import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CANONICAL_SKILL_MAP = {
    # Core web technologies
    'html5': 'html',
    'html 5': 'html',
    'css3': 'css',
    'css 3': 'css',
    
    # JavaScript ecosystem
    'javascript': 'javascript',
    'js': 'javascript',
    'typescript': 'typescript',
    'ts': 'typescript',
    'typescript js': 'typescript',
    
    # React family
    'react js': 'react',
    'react.js': 'react',
    'reactjs': 'react',
    'react native': 'react native',
    'next js': 'next.js',
    'next.js': 'next.js',
    'nextjs': 'next.js',
    'gatsby': 'gatsby',
    'gatsby js': 'gatsby',
    
    # Vue ecosystem
    'vue js': 'vue',
    'vue.js': 'vue',
    'vuejs': 'vue',
    'nuxt': 'nuxt.js',
    'nuxt js': 'nuxt.js',
    'nuxt.js': 'nuxt.js',
    
    # Angular
    'angular': 'angular',
    'angular js': 'angular',
    'angularjs': 'angular',
    
    # Node.js
    'node js': 'node.js',
    'node.js': 'node.js',
    'nodejs': 'node.js',
    'node': 'node.js',
    
    # Express
    'express js': 'express',
    'expressjs': 'express',
    'express.js': 'express',
    
    # CSS frameworks
    'tailwindcss': 'tailwind',
    'tailwind css': 'tailwind',
    'bootstrap': 'bootstrap',
    'material ui': 'material-ui',
    'mui': 'material-ui',
    'sass': 'sass',
    'scss': 'sass',
    'less': 'less',
    
    # Version control
    'git hub': 'git',
    'github': 'git',
    'gitlab': 'git',
    'bitbucket': 'git',
    
    # Databases
    'mongo db': 'mongodb',
    'mongo': 'mongodb',
    'postgresql': 'postgresql',
    'postgres': 'postgresql',
    'mysql': 'mysql',
    'sql': 'sql',
    'nosql': 'nosql',
    
    # APIs
    'rest api': 'rest',
    'restful': 'rest',
    'restful api': 'rest',
    'graphql': 'graphql',
    
    # DevOps
    'docker': 'docker',
    'kubernetes': 'kubernetes',
    'k8s': 'kubernetes',
    'ci/cd': 'ci/cd',
    'cicd': 'ci/cd',
    
    # Cloud platforms
    'aws': 'aws',
    'amazon web services': 'aws',
    'azure': 'azure',
    'microsoft azure': 'azure',
    'gcp': 'gcp',
    'google cloud': 'gcp',
    'google cloud platform': 'gcp',
    
    # Design tools
    'figma': 'figma',
    'figma design': 'figma',
    'sketch': 'sketch',
    'adobe xd': 'adobe xd',
    'xd': 'adobe xd',
    
    # Build tools
    'webpack': 'webpack',
    'vite': 'vite',
    'parcel': 'parcel',
    'rollup': 'rollup',
    
    # State management
    'redux': 'redux',
    'mobx': 'mobx',
    'vuex': 'vuex',
    
    # Backend frameworks
    'django': 'django',
    'flask': 'flask',
    'fastapi': 'fastapi',
    'fast api': 'fastapi',
    'spring boot': 'spring boot',
    'spring': 'spring boot',
    'laravel': 'laravel',
    
    # Programming languages
    'python': 'python',
    'java': 'java',
    'c++': 'c++',
    'cpp': 'c++',
    'c#': 'c#',
    'csharp': 'c#',
    'c sharp': 'c#',
    'go': 'go',
    'golang': 'go',
    'rust': 'rust',
    'ruby': 'ruby',
    'php': 'php',
    'swift': 'swift',
    'kotlin': 'kotlin',
    
    # Libraries
    'jquery': 'jquery',
    'axios': 'axios',
    'lodash': 'lodash'
}

SKILL_TAXONOMY = {
    'languages': {
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 
        'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'c', 
        'html', 'css', 'sql'
    },
    'frameworks': {
        'react', 'angular', 'vue', 'svelte', 'next.js', 'gatsby',
        'django', 'flask', 'fastapi', 'spring boot', 'express',
        'laravel', 'nest.js', 'nuxt.js', 'ember', 'backbone'
    },
    'tools': {
        'docker', 'kubernetes', 'git', 'jenkins', 'aws', 'azure', 'gcp',
        'terraform', 'ansible', 'webpack', 'vite', 'babel', 'npm', 'yarn',
        'postman', 'swagger', 'jira', 'figma', 'sketch', 'adobe xd',
        'vscode', 'intellij'
    },
    'databases': {
        'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra',
        'dynamodb', 'oracle', 'sqlite', 'elasticsearch', 'firebase'
    },
    'libraries': {
        'redux', 'mobx', 'tensorflow', 'pytorch', 'keras', 'pandas',
        'numpy', 'scikit-learn', 'jquery', 'bootstrap', 'material-ui',
        'tailwind', 'sass', 'axios', 'lodash'
    },
    'concepts': {
        # API patterns (excluded from scoring)
        'rest', 'graphql', 'microservices', 'oauth', 'websocket',
        # Methodologies (excluded from scoring)
        'agile', 'scrum', 'tdd', 'devops', 'ci/cd',
        # Design patterns (excluded from scoring)
        'oop', 'mvc', 'mvvm', 'solid',
        # Soft skills & descriptive terms (excluded from scoring)
        'responsive design', 'responsive', 'ui/ux', 'ux', 'ui',
        'performance optimization', 'optimization', 'performance',
        'problem solving', 'problem-solving', 'communication',
        'teamwork', 'collaboration', 'leadership',
        'analytical', 'critical thinking', 'creativity',
        # Generic descriptive terms (excluded from scoring)
        'frontend', 'backend', 'fullstack', 'full-stack',
        'web development', 'mobile development',
        'software development', 'software engineering',
        'best practices', 'clean code', 'code review',
        'debugging', 'testing', 'deployment'
    }
}

def canonicalize_skill(skill):
    if not skill:
        return None
    skill_lower = skill.lower().strip()
    return CANONICAL_SKILL_MAP.get(skill_lower, skill_lower)

def normalize_text(text):
    if not text:
        return ""
    return text.lower().strip()

def normalize_list(items):
    if not items:
        return []
    return [normalize_text(item) for item in items if item]

def normalize_and_canonicalize_skills(skills):
    canonical_skills = []
    for skill in skills:
        if skill:
            canonical = canonicalize_skill(skill)
            if canonical:
                canonical_skills.append(canonical)
    return list(set(canonical_skills))

def classify_skill(skill):
    canonical = canonicalize_skill(skill)
    if not canonical:
        return None
    
    for category in ['languages', 'frameworks', 'tools', 'databases']:
        if canonical in SKILL_TAXONOMY[category]:
            return category
    
    if canonical in SKILL_TAXONOMY.get('libraries', set()):
        return 'libraries'
    
    if canonical in SKILL_TAXONOMY.get('concepts', set()):
        return 'concepts'
    
    return 'other'

def classify_skills_by_taxonomy(skills):
    classified = {
        'languages': [],
        'frameworks': [],
        'tools': [],
        'databases': [],
        'libraries': [],
        'concepts': [],
        'other': []
    }
    
    # Filter out junk terms that should never be considered technical skills
    junk_terms = {'general', 'dev', 'development', 'programming', 'coding', 'scripting', 
                  'software', 'web', 'application', 'system', 'technology'}
    
    for skill in skills:
        # Skip junk terms
        if skill.lower() in junk_terms:
            continue
            
        canonical = canonicalize_skill(skill)
        if canonical:
            # Double-check canonical form isn't junk
            if canonical.lower() in junk_terms:
                continue
                
            category = classify_skill(skill)
            if category and category in classified:
                if canonical not in classified[category]:
                    classified[category].append(canonical)
    
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
    """
    UNIFIED SKILL SET MATCHING - Compares single canonical skill sets, not category-wise.
    Uses pure skill intersection/difference without weighted category scoring.
    """
    
    # STEP 1: Build Canonical Resume Core Skill Set
    # Collect all resume skills from various fields
    resume_skills_raw = []
    resume_skills_raw.extend(resume_profile.get('technical_skills', []))
    resume_skills_raw.extend(resume_profile.get('programming_languages', []))
    resume_skills_raw.extend(resume_profile.get('frameworks', []))
    resume_skills_raw.extend(resume_profile.get('tools', []))
    resume_skills_raw.extend(resume_profile.get('databases', []))
    
    # Canonicalize and classify
    resume_skills_canonical = normalize_and_canonicalize_skills(resume_skills_raw)
    resume_classified = classify_skills_by_taxonomy(resume_skills_canonical)
    
    # Build unified resume core skill set (languages ∪ frameworks ∪ tools ∪ databases)
    resume_core_skills = set()
    resume_core_skills.update(resume_classified['languages'])
    resume_core_skills.update(resume_classified['frameworks'])
    resume_core_skills.update(resume_classified['tools'])
    resume_core_skills.update(resume_classified['databases'])
    
    # STEP 2: Build Canonical JD Required Skill Set
    # Collect all JD required skills
    jd_skills_raw = []
    jd_skills_raw.extend(job_profile.get('required_skills', []))
    jd_skills_raw.extend(job_profile.get('required_languages', []))
    jd_skills_raw.extend(job_profile.get('required_frameworks', []))
    jd_skills_raw.extend(job_profile.get('required_tools', []))
    jd_skills_raw.extend(job_profile.get('required_databases', []))
    
    # Canonicalize and classify
    jd_skills_canonical = normalize_and_canonicalize_skills(jd_skills_raw)
    jd_classified = classify_skills_by_taxonomy(jd_skills_canonical)
    
    # Build unified JD core required set (exclude non-technical concepts)
    jd_core_required = set()
    jd_core_required.update(jd_classified['languages'])
    jd_core_required.update(jd_classified['frameworks'])
    jd_core_required.update(jd_classified['tools'])
    jd_core_required.update(jd_classified['databases'])
    # NOTE: Concepts are automatically excluded (they're not added to this set)
    
    # STEP 3: Unified Matching Logic (Simple Set Operations)
    matched = resume_core_skills.intersection(jd_core_required)
    missing = jd_core_required - resume_core_skills
    additional = resume_core_skills - jd_core_required  # Bonus skills
    
    # STEP 4: Pure Skill Match Score (No weighted categories)
    skill_match_ratio = len(matched) / len(jd_core_required) if len(jd_core_required) > 0 else 0.0
    final_score = round(skill_match_ratio * 100, 2)
    
    # Category breakdowns (for display only, not used in scoring)
    matched_by_category = {}
    missing_by_category = {}
    for category in ['languages', 'frameworks', 'tools', 'databases']:
        resume_cat = set(resume_classified[category])
        jd_cat = set(jd_classified[category])
        matched_by_category[category] = list(resume_cat.intersection(jd_cat))
        missing_by_category[category] = list(jd_cat - resume_cat)
    
    # Category-specific ratios (for detailed display only)
    language_ratio = len(matched_by_category['languages']) / len(jd_classified['languages']) if jd_classified['languages'] else 1.0
    framework_ratio = len(matched_by_category['frameworks']) / len(jd_classified['frameworks']) if jd_classified['frameworks'] else 1.0
    tool_ratio = len(matched_by_category['tools']) / len(jd_classified['tools']) if jd_classified['tools'] else 1.0
    database_ratio = len(matched_by_category['databases']) / len(jd_classified['databases']) if jd_classified['databases'] else 1.0
    
    # STEP 5: Experience Handling (Does NOT affect skill score)
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
    
    experience_gap_years = jd_experience - resume_experience if jd_experience > 0 else 0
    experience_gap = experience_gap_years > 0
    
    experience_gap_warning = None
    if experience_gap:
        experience_gap_warning = f"Candidate has {resume_experience} years but role requires {jd_experience}+ years (gap: {experience_gap_years} years)"
    
    # Education check (informational only)
    resume_degrees = set(normalize_list(resume_profile.get('education_degrees', [])))
    jd_education = set(normalize_list(job_profile.get('required_education', [])))
    
    education_match = True
    if jd_education:
        if 'bachelor' in ' '.join(jd_education).lower() or 'bsc' in ' '.join(jd_education).lower() or 'btech' in ' '.join(jd_education).lower():
            education_match = any('bachelor' in deg.lower() or 'bsc' in deg.lower() or 'btech' in deg.lower() or 'master' in deg.lower() or 'phd' in deg.lower() for deg in resume_degrees)
        elif 'master' in ' '.join(jd_education).lower():
            education_match = any('master' in deg.lower() or 'phd' in deg.lower() for deg in resume_degrees)
    
    # STEP 6: Recommendation Thresholds
    # ≥80% → Strong Fit | 60-79% → Good Skill Match | 40-59% → Partial Match | <40% → Weak Match
    if final_score >= 80:
        if experience_gap:
            recommendation = "Strong Fit (Experience Gap)"
            decision_summary = f"Excellent skill match ({round(final_score)}%). {experience_gap_warning}"
        else:
            recommendation = "Strong Fit"
            decision_summary = f"Highly recommended. Core skills match {round(final_score)}% with adequate experience."
    
    elif final_score >= 60:
        if experience_gap:
            recommendation = "Good Skill Match (Needs Experience)"
            decision_summary = f"Strong technical foundation ({round(final_score)}%). {experience_gap_warning}"
        else:
            recommendation = "Good Skill Match"
            decision_summary = f"Good candidate. Core skills match {round(final_score)}% with suitable experience."
    
    elif final_score >= 40:
        recommendation = "Partial Match"
        if experience_gap:
            decision_summary = f"Partial skill match ({round(final_score)}%). {experience_gap_warning}"
        else:
            decision_summary = f"Partial match ({round(final_score)}%). Missing some critical requirements."
    
    else:
        recommendation = "Weak Match"
        decision_summary = f"Insufficient match ({round(final_score)}%). Missing most core technical requirements."
    
    # STEP 7: Build simplified output (no large category-wise missing lists)
    top_strengths = []
    if len(matched) > 0:
        matched_list = sorted(list(matched))
        if len(matched_list) <= 5:
            top_strengths.append(f"Matched core skills: {', '.join(matched_list)}")
        else:
            top_strengths.append(f"Matched {len(matched_list)} core skills: {', '.join(matched_list[:5])}...")
    
    if matched_by_category['frameworks']:
        top_strengths.append(f"Framework match: {', '.join(matched_by_category['frameworks'][:3])}")
    if matched_by_category['languages']:
        top_strengths.append(f"Language match: {', '.join(matched_by_category['languages'][:3])}")
    
    if not top_strengths:
        top_strengths.append("Limited matching skills found")
    
    major_gaps = []
    if len(missing) > 0:
        missing_list = sorted(list(missing))
        if len(missing_list) <= 5:
            major_gaps.append(f"Missing core skills: {', '.join(missing_list)}")
        else:
            major_gaps.append(f"Missing {len(missing_list)} core skills: {', '.join(missing_list[:5])}...")
    
    if not major_gaps:
        major_gaps.append("No critical skill gaps identified")
    
    experience_analysis = f"Candidate has {resume_experience} years of experience. "
    if experience_gap:
        experience_analysis += f"Role requires {jd_experience}+ years."
    else:
        experience_analysis += f"Meets or exceeds the {jd_experience} years requirement."
    
    explanation = {
        'decision_summary': decision_summary,
        'top_strengths': top_strengths[:3],
        'major_gaps': major_gaps[:3],
        'experience_relevance': experience_analysis,
        'experience_gap_warning': experience_gap_warning,
        'additional_skills': sorted(list(additional))[:10]
    }
    
    # STEP 8: Simplified Output Structure
    return {
        # Core unified skill matching
        'matched_skills': sorted(list(matched)),
        'missing_skills': sorted(list(missing)),
        'additional_skills': sorted(list(additional)),
        
        # Category-level breakdowns (for display only)
        'matched_languages': matched_by_category['languages'],
        'missing_languages': missing_by_category['languages'],
        'matched_frameworks': matched_by_category['frameworks'],
        'missing_frameworks': missing_by_category['frameworks'],
        'matched_tools': matched_by_category['tools'],
        'missing_tools': missing_by_category['tools'],
        'matched_databases': matched_by_category['databases'],
        'missing_databases': missing_by_category['databases'],
        
        # Experience and education
        'experience_match': not experience_gap,
        'experience_gap_warning': experience_gap_warning,
        'experience_gap': experience_gap,
        'education_match': education_match,
        'resume_experience_years': resume_experience,
        'required_experience_years': jd_experience,
        
        # Scoring
        'match_percentage': final_score,
        'skill_match_ratio': round(skill_match_ratio * 100, 2),
        'language_ratio': round(language_ratio * 100, 2),
        'framework_ratio': round(framework_ratio * 100, 2),
        'tool_ratio': round(tool_ratio * 100, 2),
        'database_ratio': round(database_ratio * 100, 2),
        
        # Recommendation
        'recommendation': recommendation,
        'explanation': explanation,
        
        # Scoring details
        'weighted_scores': {
            'skill_match_score': round(skill_match_ratio * 100, 2),
            'matched_count': len(matched),
            'required_count': len(jd_core_required),
            'framework_match': round(framework_ratio * 100, 2),
            'tool_match': round(tool_ratio * 100, 2),
            'language_match': round(language_ratio * 100, 2),
            'database_match': round(database_ratio * 100, 2)
        }
    }

