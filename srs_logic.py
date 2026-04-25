import random

class FSISystem:
    def __init__(self):
         
        # 初始語塊資料庫 - 西班牙語版
        self.boxes = {
            "box1": [
                {
                    "phrase": "Quisiera saber si...", 
                    "ipa": "/kiˈsjeɾa saˈβeɾ si/",
                    "prompts": ["puedo entrar", "hay una mesa", "abre hoy"] # <-- 加入提示詞清單
                },
                {
                    "phrase": "Es necesario que...", 
                    "ipa": "/es neθeˈsaɾjo ke/",
                    "prompts": ["estudiemos más", "lo hagas ahora", "venga pronto"] # <-- 加入提示詞清單
                }
            ],
            "box2": [], "box3": []
        }
        self.correct_count = {} 

    def get_next_chunk(self):
        """根據 SRS 邏輯選擇下一個練習語塊"""
        rand = random.random()
        if rand < 0.8 or not self.boxes["box2"]:
            return random.choice(self.boxes["box1"]) if self.boxes["box1"] else None
        else:
            return random.choice(self.boxes["box2"])

    def update_progress(self, phrase, is_correct):
        """更新箱子狀態"""
        if is_correct:
            self.correct_count[phrase] = self.correct_count.get(phrase, 0) + 1
            if self.correct_count[phrase] >= 5:
                self._move_box(phrase, "box1", "box2")
        else:
            self.correct_count[phrase] = 0
            self._move_box(phrase, "box2", "box1")

    def _move_box(self, phrase, from_box, to_box):
        item = next((x for x in self.boxes[from_box] if x["phrase"] == phrase), None)
        if item:
            self.boxes[from_box].remove(item)
            self.boxes[to_box].append(item)

fsi_coach = FSISystem()