import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def normalize_text(text):
    if not text:
        return ""
    return text.lower().strip()

def normalize_list(items):
    if not items:
        return []
    return [normalize_text(item) for item in items if item]

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
    
    experience_match = resume_experience >= jd_experience if jd_experience > 0 else True
    experience_match_score = 1.0 if experience_match else 0.0
    
    resume_degrees = set(normalize_list(resume_profile.get('education_degrees', [])))
    jd_education = set(normalize_list(job_profile.get('required_education', [])))
    
    education_match = True
    if jd_education:
        if 'bachelor' in ' '.join(jd_education):
            education_match = any('bachelor' in deg for deg in resume_degrees)
        elif 'master' in ' '.join(jd_education):
            education_match = any('master' in deg or 'phd' in deg for deg in resume_degrees)
    education_match_score = 1.0 if education_match else 0.0
    
    skill_match_ratio = 0.0
    jd_all_skills = set(normalize_list(job_profile.get('required_skills', []))) | set(normalize_list(job_profile.get('required_languages', [])))
    resume_all_skills = set(normalize_list(resume_profile.get('technical_skills', []))) | set(normalize_list(resume_profile.get('programming_languages', [])))
    if len(jd_all_skills) > 0:
        matched_core = resume_all_skills.intersection(jd_all_skills)
        skill_match_ratio = len(matched_core) / len(jd_all_skills)
    
    framework_ratio = 0.0
    if len(jd_frameworks) > 0:
        framework_ratio = len(matched_frameworks) / len(jd_frameworks)
    
    tool_ratio = 0.0
    if len(jd_tools) > 0:
        tool_ratio = len(matched_tools) / len(jd_tools)
    
    final_score = (
        0.5 * skill_match_ratio +
        0.2 * framework_ratio +
        0.1 * tool_ratio +
        0.1 * experience_match_score +
        0.1 * education_match_score
    ) * 100
    
    final_score = round(final_score, 2)
    
    recommendation = "Not Fit"
    if final_score >= 75:
        recommendation = "Good Fit"
    elif final_score >= 50:
        recommendation = "Partial Fit"
    
    match_percentage = 0
    if len(jd_skills_all) > 0:
        match_percentage = round((len(matched_skills) / len(jd_skills_all)) * 100, 2)
    
    resume_text = ' '.join(list(resume_skills_all) + 
                            resume_profile.get('experience_roles', []) +
                            resume_profile.get('education_degrees', []) +
                            resume_profile.get('education_fields', []))
    
    jd_text = ' '.join(list(jd_skills_all) + 
                       [job_profile.get('job_role', '')] +
                       job_profile.get('required_education', []))
    
    similarity_score = 0.0
    if resume_text and jd_text:
        try:
            vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            similarity_score = round(float(similarity[0][0]) * 100, 2)
        except:
            similarity_score = final_score
    
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
        'skill_match_ratio': round(skill_match_ratio * 100, 2),
        'framework_ratio': round(framework_ratio * 100, 2),
        'tool_ratio': round(tool_ratio * 100, 2),
        'similarity_score': similarity_score,
        'recommendation': recommendation,
        'resume_experience_years': resume_experience,
        'required_experience_years': jd_experience
    }
