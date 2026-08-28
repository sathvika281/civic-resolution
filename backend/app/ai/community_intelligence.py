from app.ai.fallback.rules import cluster_related_fallback
from app.models.domain import ClusterResult


def cluster_related(similar_count: int) -> ClusterResult:
    return cluster_related_fallback(similar_count)
