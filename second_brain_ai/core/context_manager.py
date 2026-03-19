from core.logger import build_log

class AIContextManager:
    """Manages AI session limits and safely pauses build loops via READY_FOR_CONTINUATION flag."""
    def __init__(self, token_limit: int = 120000):
        self.total_tokens = 0
        self.token_limit = token_limit
        
    def track_usage(self, token_count: int, completed_tasks: list = None, pending_tasks: list = None):
        self.total_tokens += token_count
        
        # When reaching 90% of the limit
        if self.total_tokens > (self.token_limit * 0.9):
            self.trigger_continuation(completed_tasks or [], pending_tasks or [])
            
    def trigger_continuation(self, completed: list, pending: list):
        """Forces system break and dumps state safely to avoid context window crashes."""
        build_log.info("Context limit approaching. Triggering continuation.")
        print("\nSTATUS: READY_FOR_CONTINUATION")
        print(f"COMPLETED_TASKS: {completed}")
        print(f"NEXT_TASKS: {pending}\n")
        
        # In actual exec this would exit the loop gracefully
        # sys.exit(0)

context_mgr = AIContextManager()
