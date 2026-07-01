class PRGenerator:
    def create_pr(self, diff: str, safe: bool) -> dict:
        if not safe:
            return {
                "status": "rejected",
                "reason": "unsafe change detected"
            }

        return {
            "status": "approved",
            "diff_size": len(diff),
            "message": "Auto-generated PR ready for merge"
        }