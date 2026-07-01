import re
from app.utils.constants import (
    TECH,
    ACCOUNTING,
    BANKING,
    CUSTOMER_SERVICE,
    SALES,
    MANAGEMENT,
    PERSONALITY
)

class RelevanceFilter:
    def __init__(self):
        # Bind from centralized constants file
        self.categories = {
            "TECH": TECH,
            "ACCOUNTING": ACCOUNTING,
            "BANKING": BANKING,
            "CUSTOMER_SERVICE": CUSTOMER_SERVICE,
            "SALES": SALES,
            "MANAGEMENT": MANAGEMENT,
            "PERSONALITY": PERSONALITY
        }

    def detect_category(self, query: str) -> str | None:
        query_lower = query.lower()
        tokens = set(re.findall(r"[a-zA-Z0-9]+", query_lower))
        
        best_category = None
        max_matches = 0
        
        for category, keywords in self.categories.items():
            matches = 0
            for kw in keywords:
                if " " in kw:
                    if kw in query_lower:
                        matches += 2
                else:
                    if kw in tokens:
                        matches += 1
            if matches > max_matches:
                max_matches = matches
                best_category = category
                
        return best_category

    def filter(self, query: str, ranked_items: list[dict], max_results: int = 15) -> list[dict]:
        query_lower = query.lower()
        
        # 1. Exact skill list to validate in user query
        exact_skills = [
            "java", "python", "javascript", "sql", "react", "angular",
            "aws", "cloud", "devops", "selenium", "automation", "frontend"
        ]
        
        active_skills = []
        for skill in exact_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', query_lower):
                active_skills.append(skill)
                
        # 2. Strict allowed term mappings per skill
        allowed_mappings = {
            "java": ["java", "automata", "programming", "coding"],
            "devops": ["devops", "aws", "cloud", "linux", "docker", "kubernetes", "automation"],
            "python": ["python", "automata", "data science", "machine learning", "programming"],
            "javascript": ["frontend", "front end", "html", "css", "javascript", "react", "angular", "automata front end"],
            "react": ["frontend", "front end", "html", "css", "javascript", "react", "angular", "automata front end"],
            "angular": ["frontend", "front end", "html", "css", "javascript", "react", "angular", "automata front end"],
            "frontend": ["frontend", "front end", "html", "css", "javascript", "react", "angular", "automata front end"],
            "sql": ["sql", "database", "data"],
            "aws": ["aws", "cloud", "devops", "linux", "docker", "kubernetes", "automation"],
            "cloud": ["aws", "cloud", "devops", "linux", "docker", "kubernetes", "automation"],
            "selenium": ["selenium", "automation", "test automation", "coding", "programming"],
            "automation": ["selenium", "automation", "test automation", "coding", "programming"]
        }

        category = self.detect_category(query)
        filtered = []

        for item in ranked_items:
            item_text = self._create_searchable_text(item)
            name_lower = item.get("name", "").lower()
            desc_lower = item.get("description", "").lower()
            skills_lower = " ".join(item.get("skills", [])).lower()
            keywords_lower = " ".join(item.get("keywords", [])).lower()
            
            # Standardize url/link field
            if "link" in item and "url" not in item:
                item["url"] = item["link"]
                
            # 3. Relaxed Skill Verification Check
            if active_skills:
                matched_skills = 0
                for active_skill in active_skills:
                    allowed_terms = allowed_mappings.get(active_skill)
                    if allowed_terms:
                        for term in allowed_terms:
                            if (term in name_lower or
                                term in desc_lower or
                                term in skills_lower or
                                term in keywords_lower):
                                matched_skills += 1
                                break
                if matched_skills == 0 and not any(ind in name_lower for ind in ["automata", "coding", "programming", "software", "developer", "engineer", "frontend", "backend", "qa", "test"]):
                    continue

            # 4. General personality/ability test requested or matched (always keep)
            if "opq" in name_lower or "personality" in name_lower or "skills development" in name_lower:
                filtered.append(item)
                continue

            if not category:
                filtered.append(item)
                continue

            # 5. Keep if matches detected category keywords
            item_tokens = set(re.findall(r"[a-zA-Z0-9]+", item_text))
            cat_keywords = self.categories[category]
            
            has_cat_match = False
            for kw in cat_keywords:
                if " " in kw:
                    if kw in item_text:
                        has_cat_match = True
                        break
                else:
                    if kw in item_tokens:
                        has_cat_match = True
                        break
                        
            # Apply category filtering rules
            if category == "TECH":
                # Remove accounting/banking/customer service
                if any(self._matches_category(item_text, c) for c in ["ACCOUNTING", "BANKING", "CUSTOMER_SERVICE"]):
                    if not any(t in name_lower for t in ["net", "mvc", "mvvm", "xaml", "ado"]):
                        continue
                if has_cat_match or any(ind in name_lower for ind in ["automata", "coding", "programming", "software", "developer"]):
                    filtered.append(item)
                    
            elif category == "ACCOUNTING":
                if any(self._matches_category(item_text, c) for c in ["TECH", "BANKING", "CUSTOMER_SERVICE"]):
                    continue
                if has_cat_match:
                    filtered.append(item)
                    
            elif category == "BANKING":
                if self._matches_category(item_text, "TECH"):
                    query_words = set(re.findall(r"[a-zA-Z0-9]+", query.lower()))
                    has_finance = any(w in query_words for w in ["finance", "accounting", "accountant"])
                    if not has_finance:
                        continue
                if has_cat_match:
                    filtered.append(item)
                    
            else:
                if has_cat_match:
                    filtered.append(item)
                    
        # Fallback if filtered list is completely empty
        if not filtered:
            filtered = ranked_items[:max_results]
            
        return filtered[:max_results]

    def _matches_category(self, item_text: str, category: str) -> bool:
        item_tokens = set(re.findall(r"[a-zA-Z0-9]+", item_text))
        for kw in self.categories[category]:
            if " " in kw:
                if kw in item_text:
                    return True
            else:
                if kw in item_tokens:
                    return True
        return False

    def _create_searchable_text(self, item: dict) -> str:
        parts = []
        for field in ["name", "description", "test_type"]:
            val = item.get(field)
            if val:
                parts.append(str(val))
        for field in ["skills", "keywords", "keys", "job_levels"]:
            val = item.get(field)
            if isinstance(val, list):
                parts.extend([str(x) for x in val if x])
            elif val:
                parts.append(str(val))
        return " ".join(parts).lower()
