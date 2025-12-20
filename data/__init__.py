from .database import (
    init_db, 
    log_search_query, 
    log_shown_movies, 
    get_user_history, 
    get_user_stats
)

__all__ = ["init_db", "log_search_query", "log_shown_movies", "get_user_history", "get_user_stats"]
