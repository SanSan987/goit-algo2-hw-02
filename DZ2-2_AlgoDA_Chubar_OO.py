# Програмна реалізація Завдання-2
# «Оптимальне розрізання стрижня для максимального прибутку (Rod Cutting Problem)»


from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    memo = {}

    def helper(n):
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]

        max_profit = float('-inf')
        best_cut = []

        for i in range(1, n + 1):
            if i <= len(prices):
                profit, cuts = helper(n - i)
                profit += prices[i - 1]
                if profit > max_profit:
                    max_profit = profit
                    best_cut = cuts + [i]
        memo[n] = (max_profit, best_cut)
        return memo[n]

    max_profit, cuts = helper(length)
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    dp = [0] * (length + 1)
    cut_record = [[] for _ in range(length + 1)]

    for i in range(1, length + 1):
        for j in range(1, i + 1):
            if j <= len(prices):
                if dp[i] < dp[i - j] + prices[j - 1]:
                    dp[i] = dp[i - j] + prices[j - 1]
                    cut_record[i] = cut_record[i - j] + [j]

    cuts = cut_record[length]
    return {
        "max_profit": dp[length],
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1
    }

def run_tests():
    test_cases = [
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print("=" * 50)
        print(f"🧪 Тест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Мемоізація
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\n📌 Мемоізація:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Табуляція
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\n📌 Табуляція:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("✅ Перевірка пройшла успішно!")

if __name__ == "__main__":
    run_tests()
