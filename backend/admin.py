from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import Counter
import re

def get_analytics_summary(
    users_collection,
    submissions_collection,
    analysis_results_collection
) -> Dict:
    
    total_users = users_collection.count_documents({})
    total_submissions = submissions_collection.count_documents({})
    total_analyses = analysis_results_collection.count_documents({})
    
    recent_analyses = list(analysis_results_collection.find().sort("created_at", -1).limit(100))
    
    avg_match_score = 0
    if recent_analyses:
        scores = [a.get('match_percentage', 0) for a in recent_analyses]
        avg_match_score = sum(scores) / len(scores)
    
    return {
        'total_users': total_users,
        'total_submissions': total_submissions,
        'total_analyses': total_analyses,
        'average_match_score': round(avg_match_score, 2),
        'last_updated': datetime.utcnow().isoformat()
    }

def get_top_missing_skills(analysis_results_collection, limit: int = 20) -> List[Dict]:
    
    analyses = list(analysis_results_collection.find({}, {'comparison': 1}))
    
    all_missing_skills = []
    for analysis in analyses:
        comparison = analysis.get('comparison', {})
        missing_skills = comparison.get('missing_skills', [])
        all_missing_skills.extend(missing_skills)
    
    skill_counts = Counter(all_missing_skills)
    
    top_skills = []
    for skill, count in skill_counts.most_common(limit):
        top_skills.append({
            'skill': skill,
            'count': count,
            'percentage': round((count / len(analyses) * 100), 2) if analyses else 0
        })
    
    return top_skills

def get_top_job_roles(submissions_collection, limit: int = 15) -> List[Dict]:
    
    submissions = list(submissions_collection.find({}, {'parsed_jd_fields': 1}))
    
    job_roles = []
    for submission in submissions:
        parsed_jd = submission.get('parsed_jd_fields', {})
        if isinstance(parsed_jd, dict):
            role = parsed_jd.get('job_role', '')
            if role and role != 'Not specified':
                job_roles.append(role.lower().strip())
    
    role_counts = Counter(job_roles)
    
    top_roles = []
    for role, count in role_counts.most_common(limit):
        top_roles.append({
            'role': role.title(),
            'count': count
        })
    
    return top_roles

def get_skill_category_distribution(analysis_results_collection) -> Dict:
    
    analyses = list(analysis_results_collection.find({}, {'comparison': 1}))
    
    category_stats = {
        'languages': {'matched': 0, 'missing': 0},
        'frameworks': {'matched': 0, 'missing': 0},
        'tools': {'matched': 0, 'missing': 0},
        'databases': {'matched': 0, 'missing': 0}
    }
    
    for analysis in analyses:
        comparison = analysis.get('comparison', {})
        
        for category in category_stats.keys():
            matched_key = f'matched_{category}'
            missing_key = f'missing_{category}'
            
            matched = comparison.get(matched_key, [])
            missing = comparison.get(missing_key, [])
            
            category_stats[category]['matched'] += len(matched)
            category_stats[category]['missing'] += len(missing)
    
    return category_stats

def get_recommendation_distribution(analysis_results_collection) -> Dict:
    
    analyses = list(analysis_results_collection.find({}, {'comparison.recommendation': 1}))
    
    recommendations = [
        a.get('comparison', {}).get('recommendation', 'Unknown')
        for a in analyses
    ]
    
    rec_counts = Counter(recommendations)
    
    return {
        'strong_fit': rec_counts.get('Strong Fit', 0),
        'moderate_fit': rec_counts.get('Moderate Fit', 0),
        'low_fit': rec_counts.get('Low Fit', 0),
        'not_suitable': rec_counts.get('Not Suitable', 0),
        'total': len(analyses)
    }

def get_recent_analyses(analysis_results_collection, limit: int = 10) -> List[Dict]:
    
    analyses = list(
        analysis_results_collection
        .find({}, {
            'user_id': 1,
            'match_percentage': 1,
            'comparison.recommendation': 1,
            'created_at': 1
        })
        .sort("created_at", -1)
        .limit(limit)
    )
    
    results = []
    for analysis in analyses:
        results.append({
            'user_id': analysis.get('user_id'),
            'match_percentage': analysis.get('match_percentage', 0),
            'recommendation': analysis.get('comparison', {}).get('recommendation', 'Unknown'),
            'created_at': analysis.get('created_at', datetime.utcnow()).isoformat()
        })
    
    return results

def get_trending_skills(analysis_results_collection, days: int = 30) -> Dict:
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    analyses = list(
        analysis_results_collection.find(
            {'created_at': {'$gte': cutoff_date}},
            {'comparison': 1}
        )
    )
    
    matched_skills = []
    missing_skills = []
    
    for analysis in analyses:
        comparison = analysis.get('comparison', {})
        matched_skills.extend(comparison.get('matched_skills', []))
        missing_skills.extend(comparison.get('missing_skills', []))
    
    return {
        'most_matched': [
            {'skill': skill, 'count': count}
            for skill, count in Counter(matched_skills).most_common(10)
        ],
        'most_missing': [
            {'skill': skill, 'count': count}
            for skill, count in Counter(missing_skills).most_common(10)
        ]
    }

def add_skill_to_taxonomy(skill_taxonomy_collection, skill_data: Dict) -> bool:
    
    existing = skill_taxonomy_collection.find_one({'skill_name': skill_data['skill_name'].lower()})
    
    if existing:
        return False
    
    skill_doc = {
        'skill_name': skill_data['skill_name'].lower(),
        'category': skill_data['category'],
        'weight': skill_data.get('weight', 1.0),
        'aliases': skill_data.get('aliases', []),
        'created_at': datetime.utcnow()
    }
    
    skill_taxonomy_collection.insert_one(skill_doc)
    return True

def update_skill_category(skill_taxonomy_collection, skill_name: str, new_category: str) -> bool:
    
    result = skill_taxonomy_collection.update_one(
        {'skill_name': skill_name.lower()},
        {'$set': {'category': new_category, 'updated_at': datetime.utcnow()}}
    )
    
    return result.modified_count > 0

def delete_skill_from_taxonomy(skill_taxonomy_collection, skill_name: str) -> bool:
    
    result = skill_taxonomy_collection.delete_one({'skill_name': skill_name.lower()})
    return result.deleted_count > 0

def get_all_skills_taxonomy(skill_taxonomy_collection) -> List[Dict]:
    
    skills = list(skill_taxonomy_collection.find({}, {'_id': 0}).sort('category', 1))
    return skills

def get_user_activity_stats(submissions_collection, analysis_results_collection) -> List[Dict]:
    
    pipeline = [
        {
            '$group': {
                '_id': '$user_id',
                'submission_count': {'$sum': 1}
            }
        },
        {'$sort': {'submission_count': -1}},
        {'$limit': 20}
    ]
    
    user_stats = list(submissions_collection.aggregate(pipeline))
    
    results = []
    for stat in user_stats:
        user_id = stat['_id']
        analysis_count = analysis_results_collection.count_documents({'user_id': user_id})
        
        results.append({
            'user_id': user_id,
            'submissions': stat['submission_count'],
            'analyses': analysis_count
        })
    
    return results

def validate_admin_role(users_collection, user_id: int) -> bool:
    
    user = users_collection.find_one({'user_id': user_id})
    
    if not user:
        return False
    
    return user.get('role', 'user') == 'admin'

def promote_user_to_admin(users_collection, user_id: int) -> bool:
    
    result = users_collection.update_one(
        {'user_id': user_id},
        {'$set': {'role': 'admin', 'updated_at': datetime.utcnow()}}
    )
    
    return result.modified_count > 0
