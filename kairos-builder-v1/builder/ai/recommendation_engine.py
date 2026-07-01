class RecommendationEngine:
    def suggest(self, tracker_stats: dict) -> list[str]:
        if not tracker_stats:
            return ["verify", "list", "doctor"]

        sorted_cmds = sorted(tracker_stats.items(), key=lambda x: x[1], reverse=True)

        return [cmd for cmd, _ in sorted_cmds[:3]]