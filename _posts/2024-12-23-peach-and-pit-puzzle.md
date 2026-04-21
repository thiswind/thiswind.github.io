---
layout: post
title: "桃子与桃核的趣味题"
title_ar: "مسألة ممتعة عن الخوخ والنوى"
date: 2024-12-23 19:46:00 +0800
tags: ["编程", "数学", "趣味题", "桃子"]
---

{% bilingual %}
这是一道关于桃子和桃核的趣味编程题。题目规则如下：
- 初始有一定数量的钱和桃核。
- 每次可以用 1 元钱购买一个桃子，或者用 3 个桃核兑换一个桃子。
- 每吃掉一个桃子，就会获得 1 个桃核。

最终目标是：尽可能多地吃掉桃子。以下是解决这道题的完整思路和代码。
---
هذه مسألة ممتعة في البرمجة تتعلق بالخوخ والنوى. القواعد كالتالي:
- لديك مبلغ معين من المال وعدد من النوى في البداية.
- يمكنك شراء خوخة مقابل 1 يوان، أو استبدال 3 نوى بخوخة واحدة.
- بعد أكل خوخة، تحصل على نواة واحدة.

الهدف النهائي: أكل أكبر عدد ممكن من الخوخ. فيما يلي الحل الكامل للموضوع مع الكود.
{% endbilingual %}

{% bilingual %}
## 解题思路

本题关键在于充分利用桃核的价值，避免浪费。具体操作步骤如下：
1. 每一步将桃核的价值转换为钱，确保资金最大化。
2. 如果资金足够，买一个桃子并吃掉。
3. 在尝试无法继续购买时，检查是否可以"多兑换一次"，保证资源利用最大化。
---
## منهجية الحل

المفتاح لحل هذه المسألة هو الاستفادة القصوى من قيمة النوى وتجنب الهدر. الخطوات كالتالي:
1. في كل خطوة، تحويل قيمة النوى إلى مال لزيادة الرصيد المالي.
2. إذا كان المال كافيًا، اشتر خوخة وكلها.
3. عند عدم القدرة على المتابعة، تحقق مما إذا كان بالإمكان "إجراء عملية استبدال إضافية" لضمان الاستفادة القصوى من الموارد.
{% endbilingual %}

{% bilingual %}
## 详细推导过程

我们假设初始有 10 元钱，桃核为 0，目标是尽可能多地吃掉桃子。以下是逐步推导的过程：
1. 起始时，用 1 元钱买 1 个桃子，吃掉后剩余 9 元，获得 1 个桃核，总共吃掉了 1 个桃子。
2. 再用 1 元买 1 个桃子，吃掉后剩余 8 元，获得 2 个桃核，总共吃掉了 2 个桃子。
3. 重复此操作，直到花完所有的钱，同时尽可能利用桃核换算为钱。
4. 当钱不足 1 元时，检查桃核是否足够换算为钱（1 桃核等价于 \( \frac{1}{3} \) 元）。若足够，则继续兑换，否则退出循环。
5. 特别是在最后一轮时，尝试"多兑换一次"，确保不会浪费桃核的价值。

推导中发现，这种方法能保证每一轮资源最大化使用，最终可以吃掉 15 个桃子。
---
## التفصيل التدريجي للحل

نفترض أن لديك 10 يوانات وعدد النوى 0، والهدف هو أكل أكبر عدد ممكن من الخوخ. فيما يلي خطوات الحل التدريجي:
1. في البداية، اشترِ خوخة واحدة بـ 1 يوان. بعد أكلها، تبقى لديك 9 يوانات وتحصل على نواة واحدة، وتكون قد أكلت خوخة واحدة.
2. اشترِ خوخة أخرى بـ 1 يوان. بعد أكلها، تبقى لديك 8 يوانات وتحصل على نواتين، وتكون قد أكلت خوختين.
3. كرر هذه العملية حتى تنفق كل المال، مع تحويل النوى إلى مال قدر الإمكان.
4. عندما يصبح المال أقل من 1 يوان، تحقق مما إذا كانت النوى كافية لتحويلها إلى مال (1 نواة = \( \frac{1}{3} \) يوان). إذا كانت كافية، فتابع عملية الشراء، وإلا فتوقف.
5. في الجولة الأخيرة، جرب "إجراء عملية استبدال إضافية" للتأكد من عدم هدر أي قيمة للنوى.

من خلال هذا النهج، يتم ضمان الاستفادة القصوى من كل الموارد، مما يؤدي إلى أكل 15 خوخة في النهاية.
{% endbilingual %}

{% bilingual %}
## 数学表达式

我们用数学形式化地表达问题。假设：
- 初始的钱为 \( M \)，初始的桃核为 \( P_0 \) (这里 \( P_0=0 \) ) 。
- 每吃掉一个桃子，获得 1 个桃核。
- 每 3 个桃核可以兑换 1 个桃子，或者花费 1 元购买 1 个桃子。

**递推关系：**
1. 每吃掉一个桃子，桃核数会增加 1：
   \[
   P_{k+1} = P_k + 1 - 3 \cdot \text{floor}\left(\frac{P_k}{3}\right)
   \]
   其中 \(\text{floor}\left(\frac{P_k}{3}\right)\) 表示可以用 3 个桃核兑换的桃子数量。
2. 若当前的钱 \( M_k \) 不足 1 且 \( P_k < 3 \)，循环停止。
3. 每次操作后：
   \[
   M_{k+1} = M_k - 1 + \frac{\text{floor}(P_k / 3)}{3}
   \]
4. 最终目标：
   \[
   N = \text{最大化的桃子数量}
   \]
---
## التعبير الرياضي

سنعبّر عن المسألة بشكل رياضي. نفترض:
- المال الابتدائي هو \( M \)، وعدد النوى الابتدائي هو \( P_0 \) (حيث \( P_0=0 \)).
- كلما أكلت خوخة، تحصل على نواة واحدة.
- يمكن استبدال 3 نوى بخوخة واحدة، أو شراء خوخة واحدة مقابل 1 يوان.

**العلاقة التكرارية:**
1. عند أكل كل خوخة، يزداد عدد النوى بمقدار 1:
   \[
   P_{k+1} = P_k + 1 - 3 \cdot \text{floor}\left(\frac{P_k}{3}\right)
   \]
   حيث \(\text{floor}\left(\frac{P_k}{3}\right)\) تعني عدد الخوخ الذي يمكن استبداله بالنوى.
2. إذا كان المال الحالي \( M_k \) أقل من 1 و \( P_k < 3 \)، يتوقف التكرار.
3. بعد كل عملية:
   \[
   M_{k+1} = M_k - 1 + \frac{\text{floor}(P_k / 3)}{3}
   \]
4. الهدف النهائي:
   \[
   N = \text{العدد الأقصى للخوخ}
   \]
{% endbilingual %}

{% bilingual %}
## 程序代码

以下是用 Python 实现的完整代码：
---
## الكود البرمجي

فيما يلي الكود الكامل المكتوب بلغة Python:
{% endbilingual %}

```python
from fractions import Fraction

# Initialize global variables
# M_0: Initial money is 10 units
money = Fraction(10)  # Initial money: M = 10 (in fraction to avoid float precision issues)
# P_0: Initial number of peach pits is 0
peach_pits = 0  # Initial number of peach pits: P_0 = 0
# N: Total peaches eaten starts at 0
peaches_eaten = 0  # Total peaches eaten: N = 0

# Simulation begins
while True:
    # Step 1: Convert all peach pits to money equivalent
    # Formula: M_k = M_k + floor(P_k / 3) / 3
    # This step maximizes the value of peach pits by converting them to money.
    money += Fraction(peach_pits, 3)
    peach_pits = 0  # All peach pits are converted to money (P_k = 0)
    
    # Step 2: Check if there is enough money to buy a peach
    # If money is insufficient, check if one more exchange is possible.
    # Formula: If M_k + 1/3 >= 1, convert one pit to money
    # This ensures no peach pit value is wasted.
    if money < 1:
        if money + Fraction(1, 3) >= 1:
            money += Fraction(1, 3)  # Add value of 1 peach pit
            peach_pits -= 1  # Deduct 1 peach pit
        else:
            # Exit condition: when M_k < 1 and P_k < 3, no further peaches can be obtained
            break  # Exit the loop if no further exchange is possible
    
    # Step 3: Buy a peach
    # Formula: M_{k+1} = M_k - 1
    # Subtract 1 unit of money for buying a peach.
    money -= 1
    
    # Step 4: Eat the peach
    # Formula: P_{k+1} = P_k + 1
    # Eating a peach increases the peach pit count by 1.
    peaches_eaten += 1
    peach_pits += 1

# Output the results
# The final state represents the solution to the mathematical problem.
print(f"Remaining money: {money}")  # Remaining money: M_k
print(f"Remaining peach pits: {peach_pits}")  # Remaining peach pits: P_k
print(f"Total peaches eaten: {peaches_eaten}")  # Total peaches eaten: N
```

{% bilingual %}
## 运行结果展示与解释

以下是程序在 Linux 和 Windows 系统中的运行结果和详细解释。
---
## عرض وشرح نتائج التشغيل

فيما يلي نتائج تشغيل البرنامج على نظامي Linux و Windows مع شرح تفصيلي.
{% endbilingual %}
