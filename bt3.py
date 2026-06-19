from abc import ABC, abstractmethod

# ==========================================
# 1. ĐỊNH NGHĨA CÁC LỚP ĐỐI TƯỢNG (OOP)
# ==========================================

class Champion(ABC):
    """
    Lớp cơ sở trừu tượng làm khuôn mẫu cho toàn bộ quân cờ trong game.
    """
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int):
        # Bẫy dữ liệu 2: Xử lý chỉ số âm hoặc bằng 0
        if base_hp <= 0:
            base_hp = 100
        if base_atk <= 0:
            base_atk = 100
            
        self.champion_id = champion_id
        self.name = name
        self.base_hp = base_hp
        self.base_atk = base_atk

    @abstractmethod
    def calculate_skill_damage(self) -> float:
        """Tính lượng sát thương kỹ năng đặc thù của từng hệ tộc."""
        pass

    def get_combat_power(self) -> float:
        """Tính điểm chiến lực tổng hợp của quân cờ: HP + (Sát thương kỹ năng * 1.5)"""
        return self.base_hp + (self.calculate_skill_damage() * 1.5)

    def __add__(self, other):
        """Nạp chồng toán tử + để cộng dồn điểm chiến lực."""
        if isinstance(other, Champion):
            return self.get_combat_power() + other.get_combat_power()
        elif isinstance(other, (int, float)):
            return self.get_combat_power() + other
        return NotImplemented

    def __radd__(self, other):
        """Hỗ trợ phép cộng đảo chiều khi giá trị khởi đầu là số 0 (ví dụ trong hàm sum)."""
        return self.__add__(other)

    def __gt__(self, other):
        """Nạp chồng toán tử > để so sánh điểm chiến lực giữa 2 quân cờ."""
        if isinstance(other, Champion):
            return self.get_combat_power() > other.get_combat_power()
        return NotImplemented


class Warrior(Champion):
    """
    Lớp cụ thể biểu diễn hệ Chiến binh (Warrior).
    """
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, shield_bonus: int):
        super().__init__(champion_id, name, base_hp, base_atk)
        if shield_bonus < 0:
            shield_bonus = 0
        self.shield_bonus = shield_bonus

    def calculate_skill_damage(self) -> float:
        """Công thức hệ Chiến binh: ATK * 2 + Giáp cộng thêm"""
        return self.base_atk * 2 + self.shield_bonus


class Mage(Champion):
    """
    Lớp cụ thể biểu diễn hệ Pháp sư (Mage).
    """
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, ability_power: float):
        super().__init__(champion_id, name, base_hp, base_atk)
        if ability_power <= 0:
            ability_power = 1.0
        self.ability_power = ability_power

    def calculate_skill_damage(self) -> float:
        """Công thức hệ Pháp sư: ATK * Hệ số SMPT"""
        return self.base_atk * self.ability_power


# ==========================================
# 2. LOGIC HỆ THỐNG QUẢN LÝ (BACKEND GAME)
# ==========================================

class AutoBattlerManager:
    """
    Hệ thống điều khiển trung tâm quản lý bể tướng và tương tác người dùng.
    """
    def __init__(self):
        # Khởi tạo sẵn danh sách tướng ban đầu
        self.champion_pool = {
            "WAR01": Warrior("WAR01", "Rikkei Knight", 1200, 300, 150),
            "WAR02": Warrior("WAR02", "Steel Guardian", 1500, 250, 200),
            "MAG01": Mage("MAG01", "Rikkei Wizard", 800, 500, 1.5) # ATK 500 * AP 1.5 = 750 sát thương
        }

    def display_pool(self):
        """Chức năng 1: Hiển thị bể tướng hiện tại dưới dạng bảng bảng chuẩn"""
        print("\n--- DANH SÁCH QUÂN CỜ TRONG BỂ TƯỚNG ---")
        print(f"{'Mã':<7} | {'Tên tướng':<18} | {'Hệ':<8} | {'HP':<5} | {'ATK':<5} | {'Chỉ số riêng':<17} | {'Chiến lực'}")
        print("-" * 85)
        for c in self.champion_pool.values():
            he_toc = "Warrior" if isinstance(c, Warrior) else "Mage"
            chi_so_rieng = f"Armor: {c.shield_bonus}" if isinstance(c, Warrior) else f"AP: {c.ability_power}"
            print(f"{c.champion_id:<7} | {c.name:<18} | {he_toc:<8} | {c.base_hp:<5} | {c.base_atk:<5} | {chi_so_rieng:<17} | {c.get_combat_power():.0f}")
        print("-" * 85)

    def add_champion(self):
        """Chức năng 2: Thêm quân cờ mới từ input kèm xử lý ngoại lệ và trùng lặp"""
        print("\n--- THÊM QUÂN CỜ MỚI ---")
        print("Chọn Hệ: 1 - Warrior | 2 - Mage")
        choice = input("Nhập lựa chọn của bạn: ").strip()
        if choice not in ["1", "2"]:
            print("Lựa chọn hệ không hợp lệ!")
            return

        c_id = input("Nhập mã tướng: ").strip().upper()
        # Bẫy dữ liệu 4: Trùng mã tướng
        if c_id in self.champion_pool:
            print(f"Lỗi: Mã tướng [{c_id}] đã tồn tại trong bể tướng!")
            return

        name = input("Nhập tên tướng: ").strip()

        try:
            hp = int(input("Nhập HP: "))
            atk = int(input("Nhập ATK: "))

            if choice == "1":
                armor = int(input("Nhập Armor: "))
                new_champ = Warrior(c_id, name, hp, atk, armor)
                self.champion_pool[c_id] = new_champ
                print(f"\nThêm tướng Warrior thành công!")
            else:
                ap = float(input("Nhập Hệ số SMPT (ví dụ 1.5): "))
                new_champ = Mage(c_id, name, hp, atk, ap)
                self.champion_pool[c_id] = new_champ
                print(f"\nThêm tướng Mage thành công!")

            print(f"Mã: {new_champ.champion_id} | Tên: {new_champ.name} | Chiến lực: {new_champ.get_combat_power():.0f}")

        except ValueError:
            print("Lỗi: Nhập sai định dạng số! Thao tác tạo tướng thất bại.")

    def compare_champions(self):
        """Chức năng 3: So sánh sức mạnh 2 tướng sử dụng nạp chồng toán tử '>'"""
        print("\n--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---")
        id1 = input("Nhập mã tướng thứ nhất: ").strip().upper()
        id2 = input("Nhập mã tướng thứ hai: ").strip().upper()

        # Bẫy dữ liệu 3: Mã tướng không tồn tại
        if id1 not in self.champion_pool or id2 not in self.champion_pool:
            print("Lỗi: Một hoặc cả hai mã tướng không tồn tại trong hệ thống!")
            return

        c1 = self.champion_pool[id1]
        c2 = self.champion_pool[id2]

        type1 = "Warrior" if isinstance(c1, Warrior) else "Mage"
        type2 = "Warrior" if isinstance(c2, Warrior) else "Mage"

        print("\nThông tin so sánh:")
        print(f"{c1.champion_id} - {c1.name} | Hệ: {type1} | Chiến lực: {c1.get_combat_power():.0f}")
        print(f"{c2.champion_id} - {c2.name} | Hệ: {type2} | Chiến lực: {c2.get_combat_power():.0f}")

        # Sử dụng toán tử nạp chồng '>'
        if c1 > c2:
            print(f"Kết quả: {c1.champion_id} - {c1.name} mạnh hơn {c2.champion_id} - {c2.name}.")
        elif c2 > c1:
            print(f"Kết quả: {c2.champion_id} - {c2.name} mạnh hơn {c1.champion_id} - {c1.name}.")
        else:
            print(f"Kết quả: Cả hai quân cờ có chiến lực ngang nhau!")

    def calculate_team_power(self):
        """Chức năng 4: Tính tổng chiến lực đội hình sử dụng nạp chồng toán tử '+'"""
        print("\n--- TÍNH TỔNG CHIẾN LỰC ĐỘI HÌNH RA SÂN ---")
        raw_input = input("Nhập danh sách mã tướng, cách nhau bằng dấu phẩy: ")
        
        # Tách chuỗi và chuẩn hóa dữ liệu đầu vào
        input_ids = [i.strip().upper() for i in raw_input.split(",") if i.strip()]
        
        if not input_ids:
            print("Đội hình trống!")
            return

        team_champions = []
        print("\nDanh sách đội hình:")
        stt = 1
        
        for c_id in input_ids:
            # Bẫy dữ liệu 3: Mã không tồn tại thì thông báo, bỏ qua và chạy tiếp
            if c_id not in self.champion_pool:
                print(f"⚠️ Mã tướng [{c_id}] không hợp lệ, bỏ qua!")
                continue
            
            champ = self.champion_pool[c_id]
            team_champions.append(champ)
            print(f"{stt}. {champ.champion_id} - {champ.name} | Chiến lực: {champ.get_combat_power():.0f}")
            stt += 1

        if not team_champions:
            print("Không có tướng hợp lệ nào trong đội hình để tính toán.")
            return

        # Sử dụng nạp chồng toán tử + thông qua hàm sum() tích hợp sẵn của Python
        total_power = sum(team_champions)
        print(f"Tổng chiến lực đội hình: {total_power:.0f}")

    def run(self):
        """Vòng lặp menu điều hướng chương trình chính"""
        while True:
            print("\n================ RIKKEI RPG AUTO-BATTLER ================")
            print("1. Hiển thị bể tướng hiện có")
            print("2. Thêm quân cờ mới")
            print("3. So sánh 2 quân cờ")
            print("4. Tính tổng chiến lực Đội Hình Ra Sân")
            print("5. Thoát chương trình")
            print("=========================================================")
            
            choice = input("Chọn chức năng (1-5): ").strip()
            if choice == "1":
                self.display_pool()
            elif choice == "2":
                self.add_champion()
            elif choice == "3":
                self.compare_champions()
            elif choice == "4":
                self.calculate_team_power()
            elif choice == "5":
                print("\nCảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!")
                break
            else:
                print("Lựa chọn không hợp lệ, vui lòng chọn từ 1 đến 5.")

# Khởi chạy chương trình
if __name__ == "__main__":
    # Minh chứng Bẫy dữ liệu 1: Thử khởi tạo trực tiếp lớp Champion -> Sẽ ném ra TypeError lỗi ngay lập tức
    try:
        instance_loi = Champion("ERROR", "Tướng Lỗi", 100, 100)
    except TypeError as e:
        print(f"[HỆ THỐNG BẢO VỆ]: Đã ngăn chặn khởi tạo trực tiếp lớp Champion! Chi tiết lỗi: {e}")
        
    manager = AutoBattlerManager()
    manager.run()