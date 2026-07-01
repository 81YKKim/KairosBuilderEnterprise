import time


class LiveEngine:

    def __init__(self, service):

        self.service = service
        self.running = False
        self.paused = False
        self.interval_sec = 60

    # -----------------------------
    # START LIVE
    # -----------------------------
    def start(self, capital=10000):

        self.running = True

        print("🚀 LIVE ENGINE STARTED")

        while self.running:

            try:

                if self.paused:
                    print("⏸ PAUSED...")
                    time.sleep(5)
                    continue

                print("\n📊 SCANNING MARKET...")

                result = self.service.execute_top_scan(capital)

                print("💰 EXECUTION RESULT:")
                print(result)

                print(f"⏳ WAIT {self.interval_sec}s...\n")

                time.sleep(self.interval_sec)

            except Exception as e:
                print("❌ ERROR:", e)
                time.sleep(5)

    # -----------------------------
    # STOP
    # -----------------------------
    def stop(self):

        self.running = False
        print("🛑 LIVE STOPPED")

    # -----------------------------
    # PAUSE
    # -----------------------------
    def pause(self):

        self.paused = True
        print("⏸ PAUSED")

    # -----------------------------
    # RESUME
    # -----------------------------
    def resume(self):

        self.paused = False
        print("▶ RESUMED")