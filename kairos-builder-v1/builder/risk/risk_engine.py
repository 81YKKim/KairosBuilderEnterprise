class RiskEngine:

    def __init__(self):

        self.max_position_count = 10

        # 🔥 핵심 완화 (진짜 트레이딩 활성화)
        self.min_score = 30

        self.max_allocation_ratio = 0.25

    def filter_positions(self, ranked_list):

        filtered = []

        for item in ranked_list:

            score = item.get("score", 0)

            if score < self.min_score:
                continue

            filtered.append(item)

            if len(filtered) >= self.max_position_count:
                break

        return filtered

    def adjust_allocation(self, capital, positions):

        results = []

        total_score = sum(p["score"] for p in positions) or 1

        for p in positions:

            weight = p["score"] / total_score

            weight = min(weight, self.max_allocation_ratio)

            results.append({
                "ticker": p["ticker"],
                "score": p["score"],
                "signal": p["signal"],
                "allocation": capital * weight
            })

        return results