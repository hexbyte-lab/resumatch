from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.utils.text_processor import clean_text, extract_keywords
from src.config import Config


class ResumeMatcher:
    """
    Matches resume against job description and provides scoring
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def calculate_match_score(self, resume_text, job_description):
        """
        Calculate similarity score between resume and job description

        Args:
            resume_text (str): Resume content
            job_description (str): Job posting content

        Returns:
            float: Match score between 0-100
        """
        # Clean texts
        resume_clean = clean_text(resume_text)
        job_clean = clean_text(job_description)

        # Vectorize and calculate cosine similarity
        tfidf_matrix = self.vectorizer.fit_transform([resume_clean, job_clean])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

        # Convert to percentage (0-100)
        score = round(similarity * 100, 2)

        return score

    def find_missing_keywords(self, resume_text, job_description):
        """
        Find keywords in job description that are missing from resume

        Args:
            resume_text (str): Resume content
            job_description (str): Job posting content

        Returns:
            list: Missing keywords
        """
        resume_keywords = set(extract_keywords(resume_text, max_keywords=50))
        job_keywords = set(extract_keywords(job_description, max_keywords=50))

        missing = job_keywords - resume_keywords

        return sorted(list(missing))

    def analyze(self, resume_text, job_description):
        """
        Full analysis: score + missing keywords

        Args:
            resume_text (str): Resume content
            job_description (str): Job posting content

        Returns:
            dict: Analysis results
        """
        score = self.calculate_match_score(resume_text, job_description)
        missing_keywords = self.find_missing_keywords(resume_text, job_description)

        return {
            "match_score": score,
            "missing_keywords": missing_keywords,
            "total_missing": len(missing_keywords),
        }


if __name__ == "__main__":
    matcher = ResumeMatcher()

    resume = "Python developer with experience in Flask and REST APIs"
    job = "Looking for Python developer skilled in Django, Flask, and Docker"

    result = matcher.analyze(resume, job)
    print("Match Score:", result["match_score"])
    print("Missing Keywords:", result["missing_keywords"])
