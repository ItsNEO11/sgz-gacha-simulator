import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

# === 概率配置 ===
prob_normal = 0.000582
prob_rare = 0.000291
prob_special = 0.000174

special_cards = ["孙权"]
rare_cards = [
    "曹操", "诸葛亮", "刘备", "张飞", "吕布", "张角", "太史慈", "SP荀彧", "SP诸葛亮", "SP朱儁", "关银屏",
    "SP周瑜", "陆逊", "SP皇甫嵩", "SP袁绍", "周泰", "赵云", "张苞", "典韦", "满宠", "SP关羽", "SP马超",
    "王元姬", "魏延", "SP郭嘉", "SP曹真", "姜维", "SP刘晔", "SP吕蒙"
]
normal_cards = [
    "荀彧", "张昭", "曹植", "曹丕", "蔡文姬", "袁绍", "邓艾", "祝触夫人", "董卓", "夏侯惇", "周瑜", "华佗", "大乔", "小乔",
    "李儒", "马超", "吕玲绮", "马腾", "徐庶", "吕蒙", "王平", "华雄", "黄盖", "高顺", "陈到", "田丰", "钟会", "程昱", "许褚",
    "左慈", "黄忠", "孩坚", "郭嘉", "庞德", "SP庞德", "曹纯", "张让", "夏侯渊", "王双", "颜良", "SP张梁", "袁术", "兀突骨",
    "鞠义", "SP黄月英", "蔡邕", "朵思大王", "沮授", "甘宁", "关兴", "陆抗", "公孙瓒", "董白", "陈群", "于吉", "法正", "于禁",
    "徐晃", "曹仁", "邹氏", "严颜", "孙策", "伊籍", "貂蝉", "荀攸", "SP许褚", "张春华", "司马徽", "诸葛恪", "甄姬", "孟获", "黄月英",
    "高览", "张郃", "文丑", "许攸", "马忠", "王异"
]

card_pool = (
    [(name, "普通", prob_normal) for name in normal_cards] +
    [(name, "稀有", prob_rare) for name in rare_cards] +
    [(name, "特别", prob_special) for name in special_cards]
)

cost_per_draw = 18.96  # 元

# === 抽卡逻辑 ===
def simulate(draws):
    results = []
    orange_history = []
    orange_name_types = []
    normal_streak = 0

    for i in range(draws):
        if (i + 1) % 30 == 0 and not any(r[1] in ["普通", "稀有", "特别"] for r in results[-29:]):
            weights_raw = [p for _, _, p in card_pool]
            total = sum(weights_raw)
            weights = [p / total for p in weights_raw]
            idx = np.random.choice(len(card_pool), p=weights)
            result = card_pool[idx]
        else:
            roll = np.random.rand()
            if roll < 0.055755:
                if normal_streak >= 5:
                    rs_pool = [(name, "稀有", prob_rare) for name in rare_cards] + [(name, "特别", prob_special) for name in special_cards]
                    weights_raw = [p for _, _, p in rs_pool]
                    total = sum(weights_raw)
                    weights = [p / total for p in weights_raw]
                    idx = np.random.choice(len(rs_pool), p=weights)
                    result = rs_pool[idx]
                else:
                    weights_raw = [p for _, _, p in card_pool]
                    total = sum(weights_raw)
                    weights = [p / total for p in weights_raw]
                    idx = np.random.choice(len(card_pool), p=weights)
                    result = card_pool[idx]
            elif roll < 0.055755 + 0.350018:
                result = ("紫卡", "紫")
            else:
                result = ("蓝卡", "蓝")

        results.append((result[0], result[1], i + 1))

        if result[1] in ["普通", "稀有", "特别"]:
            if result[1] == "普通":
                normal_streak += 1
            else:
                normal_streak = 0
            orange_history.append(result[1])
            orange_name_types.append((result[0], result[1]))

    return results, orange_history, orange_name_types

# === 页面 UI ===
st.title("🎲 三国志·战略版 抽卡计算器")
st.markdown("🧮 抽卡成本计算：5 连消耗 948 金珠，1 元 = 10 金珠，每抽约为 **18.96 元**")
st.markdown("🔆 每赛季抽免半，需要 17820 金珠，可抽 360 次；")
st.markdown("🔆 每赛季双月卡，消费 144 元得 20340 金珠，可抽 107.27 次（21.45 次 5 连）；")
st.markdown("🔆 每赛季帝王套，消费 1308 元得 26160 金珠，可抽 137.97 次（27.59 次 5 连）；")
st.markdown("⚠️ 模拟真实抽卡率、30 抽保底、5+1 出核心")

n_draws = st.number_input("请输入抽卡次数：", min_value=1, max_value=100000, value=300, step=1)

if st.button("模拟抽卡"):
    results, orange_history, orange_name_types = simulate(n_draws)
    total_cost = n_draws * cost_per_draw
    orange_count = len(orange_history)
    avg_cost = total_cost / orange_count if orange_count > 0 else 0

    st.subheader(f"💰 总花费：￥{total_cost:,.2f}")
    st.markdown(f"- 抽卡次数：{n_draws}")
    st.markdown(f"- 抽中五星橙卡：{orange_count} 张")
    st.markdown(f"- 其中：普通 {orange_history.count('普通')}，稀有 {orange_history.count('稀有')}，特别 {orange_history.count('特别')}")
    st.markdown(f"- 每张橙卡平均成本：￥{avg_cost:,.2f}")
    if orange_count > 0:
        avg_draws_per_orange = n_draws / orange_count
        st.markdown(f"- 平均出橙概率：每抽 {avg_draws_per_orange:.1f} 次出一张橙卡")

    if orange_name_types:
        st.markdown("### 🎉 恭喜你抽到：")
        counter_by_type = defaultdict(Counter)
        all_draw_count = defaultdict(int)

        for name, level in orange_name_types:
            counter_by_type[level][name] += 1
            all_draw_count[name] += 1

        if counter_by_type["特别"]:
            st.success("💎 特别橙卡：" + "，".join([f"{n} × {c}" for n, c in counter_by_type["特别"].items()]))
        if counter_by_type["稀有"]:
            st.info("⭐️ 稀有橙卡：" + "，".join([f"{n} × {c}" for n, c in counter_by_type["稀有"].items()]))
        if counter_by_type["普通"]:
            st.warning("✅ 普通橙卡：" + "，".join([f"{n} × {c}" for n, c in counter_by_type["普通"].items()]))

        # 🌟 满红展示
        full_red_list = [f"{name}（{count}）" for name, count in all_draw_count.items() if count >= 6]
        if full_red_list:
            st.success("🌟 满红武将：" + "，".join(sorted(full_red_list)))

        # 🕳️ 未抽到橙卡（抽卡数 >= 3000）
        if n_draws >= 3000:
            all_obtained = set(all_draw_count.keys())
            full_pool = set(special_cards + rare_cards + normal_cards)
            unhit = full_pool - all_obtained
            if unhit:
                st.error("💡 还未抽到的橙卡：" + "，".join(sorted(unhit)))
            else:
                st.success("🎉 恭喜！你已抽齐当前所有橙卡！")

        # 🕳️ 未满红橙卡（抽卡数 >= 10000）
        if n_draws >= 10000:
            full_pool = set(special_cards + rare_cards + normal_cards)
            not_full_red = [f"{name}（{all_draw_count.get(name, 0)}）"
                            for name in sorted(full_pool) if all_draw_count.get(name, 0) < 6]
            if not_full_red:
                st.error("💡 还未满红的橙卡有：" + "，".join(not_full_red))
            else:
                st.success("🎉 太棒了！你已满红当前所有橙卡！")
    else:
        st.info("😢 本次未抽中任何五星橙卡。")

    # 饼图
    if orange_count > 0:
        labels = ["Special 5★", "Rare 5★", "Normal 5★"]
        values = [orange_history.count("特别"), orange_history.count("稀有"), orange_history.count("普通")]
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

# === 卡池展示 ===
st.markdown("## 🛡 当前卡池武将列表")
st.success("💎 特别橙卡：" + "，".join(special_cards))
st.info("⭐ 稀有橙卡：" + "，".join(rare_cards))
st.warning("✅ 普通橙卡：" + "，".join(normal_cards))
