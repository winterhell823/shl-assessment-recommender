import re
from app.utils.logger import get_logger

logger = get_logger("Ranker")

class Ranker:
    def rank(self, keyword_items: list[dict], vector_items: list[dict], query: str) -> list[dict]:
        query_lower = query.lower()
        
        ignore_tokens = {
            "hiring", "hire", "need", "want", "assessment", "test",
            "candidate", "role", "looking", "for", "with",
            "and", "the", "a", "an", "to", "developer", "skills", "technical"
        }
        
        raw_query_words = re.findall(r"[a-zA-Z0-9]+", query_lower)
        query_words = [w for w in raw_query_words if w not in ignore_tokens]
        if not query_words:
            query_words = raw_query_words

        # Merge keyword and vector items with deduplication
        seen_urls = set()
        merged = []
        
        for item in keyword_items:
            url = item.get("url") or item.get("link")
            if not url:
                continue
            if url not in seen_urls:
                seen_urls.add(url)
                merged.append((item, 10))

        for item in vector_items:
            url = item.get("url") or item.get("link")
            if not url:
                continue
            if url not in seen_urls:
                seen_urls.add(url)
                merged.append((item, 5))
            else:
                for idx, (existing_item, base_score) in enumerate(merged):
                    existing_url = existing_item.get("url") or existing_item.get("link")
                    if existing_url == url:
                        merged[idx] = (existing_item, base_score + 15)
                        break

        # Important skills list
        IMPORTANT_SKILLS = [
            "java", "python", "javascript", "sql", "react", "angular", "node",
            "aws", "cloud", "devops", "selenium", "automation", "frontend",
            "backend", "data", "machine learning"
        ]

        scored_items = []
        for item, base_score in merged:
            score = base_score
            name_lower = item.get("name", "").lower()
            desc_lower = item.get("description", "").lower()
            skills_lower = " ".join(item.get("skills", [])).lower()
            keywords_lower = " ".join(item.get("keywords", [])).lower()
            all_text_lower = f"{name_lower} {desc_lower} {skills_lower} {keywords_lower}"

            # Standardize url/link field
            if "link" in item and "url" not in item:
                item["url"] = item["link"]

            # Skill Boost rules
            for skill in IMPORTANT_SKILLS:
                if re.search(r'\b' + re.escape(skill) + r'\b', query_lower):
                    # Exact skill in assessment name
                    if re.search(r'\b' + re.escape(skill) + r'\b', name_lower):
                        score += 300
                    # Exact skill in description/skills/keywords
                    elif (re.search(r'\b' + re.escape(skill) + r'\b', desc_lower) or
                          re.search(r'\b' + re.escape(skill) + r'\b', skills_lower) or
                          re.search(r'\b' + re.escape(skill) + r'\b', keywords_lower)):
                        score += 120

            # Developer / software query boost
            dev_keywords = ["developer", "software", "programming", "coding"]
            has_dev_indicator = any(re.search(r'\b' + re.escape(dk) + r'\b', query_lower) for dk in dev_keywords)
            if has_dev_indicator:
                boost_indicators = ["programming", "coding", "automata", "software", "developer"]
                if any(re.search(r'\b' + re.escape(bi) + r'\b', name_lower) for bi in boost_indicators):
                    score += 100
                elif any(re.search(r'\b' + re.escape(bi) + r'\b', all_text_lower) for bi in boost_indicators):
                    score += 50

            # Penalization rules
            # 1. Java query penalization
            if re.search(r'\bjava\b', query_lower):
                if not re.search(r'\bjava\b', name_lower):
                    net_keywords = [".net", "c#", "asp.net", "ado.net", "wpf", "wcf", "mvvm", "mvc", "visual studio"]
                    if any(nk in name_lower for nk in net_keywords):
                        score -= 200

            # 2. DevOps query penalization
            if re.search(r'\bdevops\b', query_lower):
                devops_terms = ["devops", "aws", "cloud", "linux", "docker", "kubernetes", "automation"]
                if not any(term in all_text_lower for term in devops_terms):
                    score -= 200

            # 3. Python query penalization
            if re.search(r'\bpython\b', query_lower):
                if not re.search(r'\bpython\b', name_lower):
                    is_allowed_python = ("automata" in name_lower or 
                                         "data science" in all_text_lower or 
                                         "machine learning" in all_text_lower)
                    if not is_allowed_python:
                        score -= 150

            scored_items.append((score, item))

        scored_items.sort(key=lambda x: x[0], reverse=True)

        return [item for _, item in scored_items]