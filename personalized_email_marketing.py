"""
پروژه ۲: سامانه‌ی تولید محتوای شخصی‌سازی‌شده برای ایمیل مارکتینگ
با استفاده از RAG پایه، Self-Consistency و مهندسی پرامپت
"""

import json
import random
from typing import Dict, List, Any

# ============================================
# ۱. داده‌های کاربران
# ============================================

USERS = [
    {
        "id": 1,
        "name": "علی رضایی",
        "interests": ["برنامه‌نویسی", "پایتون", "هوش مصنوعی"],
        "purchased_courses": ["مبانی پایتون", "یادگیری ماشین مقدماتی"],
        "level": "متوسط",
        "last_activity": "۲ روز پیش"
    },
    {
        "id": 2,
        "name": "مریم حسینی",
        "interests": ["بازاریابی دیجیتال", "سئو", "تولید محتوا"],
        "purchased_courses": ["سئو مقدماتی", "بازاریابی محتوا"],
        "level": "پیشرفته",
        "last_activity": "۱ هفته پیش"
    },
    {
        "id": 3,
        "name": "رضا کریمی",
        "interests": ["طراحی", "UI/UX", "فتوشاپ"],
        "purchased_courses": ["مبانی طراحی", "فیگما مقدماتی"],
        "level": "مبتدی",
        "last_activity": "۳ روز پیش"
    },
    {
        "id": 4,
        "name": "سارا محمدی",
        "interests": ["برنامه‌نویسی", "جاوااسکریپت", "ری‌اکت"],
        "purchased_courses": ["جاوااسکریپت پیشرفته"],
        "level": "پیشرفته",
        "last_activity": "امروز"
    },
    {
        "id": 5,
        "name": "محمد حسینی",
        "interests": ["بازاریابی دیجیتال", "تبلیغات", "تحلیل داده"],
        "purchased_courses": ["تحلیل داده با پایتون", "بازاریابی محتوا"],
        "level": "متوسط",
        "last_activity": "۵ روز پیش"
    }
]

# ============================================
# ۲. داده‌های دوره‌ها
# ============================================

COURSES = [
    {"id": "c1", "title": "برنامه‌نویسی پایتون پیشرفته", "category": "برنامه‌نویسی", "difficulty": "پیشرفته"},
    {"id": "c2", "title": "یادگیری ماشین با پایتون", "category": "برنامه‌نویسی", "difficulty": "پیشرفته"},
    {"id": "c3", "title": "سئو حرفه‌ای", "category": "بازاریابی", "difficulty": "پیشرفته"},
    {"id": "c4", "title": "بازاریابی شبکه‌های اجتماعی", "category": "بازاریابی", "difficulty": "متوسط"},
    {"id": "c5", "title": "طراحی UI/UX پیشرفته", "category": "طراحی", "difficulty": "پیشرفته"},
    {"id": "c6", "title": "فتوشاپ از صفر تا صد", "category": "طراحی", "difficulty": "مبتدی"},
    {"id": "c7", "title": "جاوااسکریپت برای مبتدیان", "category": "برنامه‌نویسی", "difficulty": "مبتدی"},
    {"id": "c8", "title": "ری‌اکت و Next.js", "category": "برنامه‌نویسی", "difficulty": "پیشرفته"},
    {"id": "c9", "title": "تحلیل داده با پایتون", "category": "برنامه‌نویسی", "difficulty": "متوسط"},
]


# ============================================
# ۳. تابع RAG
# ============================================

def retrieve_user_context(user_id: int) -> Dict[str, Any]:
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        return {}

    recommended_courses = []
    for course in COURSES:
        if course["category"] in user["interests"]:
            recommended_courses.append(course["title"])

    return {
        "name": user["name"],
        "interests": ", ".join(user["interests"]),
        "purchased_courses": ", ".join(user["purchased_courses"]),
        "level": user["level"],
        "last_activity": user["last_activity"],
        "recommended_courses": ", ".join(recommended_courses[:3]) or "دوره‌های تخصصی"
    }


# ============================================
# ۴. تولید ایمیل (شبیه‌سازی)
# ============================================

def generate_email(user_id: int, num_samples: int = 3) -> Dict[str, Any]:
    user_context = retrieve_user_context(user_id)
    if not user_context:
        return {"error": "User not found"}

    samples = []
    for i in range(num_samples):
        sample = simulate_email(user_context, i)
        samples.append(sample)

    best = select_best_email(samples, user_context)

    return {
        "user_id": user_id,
        "user_name": user_context["name"],
        "user_context": user_context,
        "best_email": best
    }


# ============================================
# ۵. شبیه‌سازی ایمیل
# ============================================

def simulate_email(user_context: Dict[str, Any], seed: int) -> Dict[str, Any]:
    random.seed(seed + user_context.get("id", 0))

    name = user_context["name"]
    interests = user_context["interests"].split(", ")
    level = user_context["level"]
    recommended = user_context["recommended_courses"].split(", ")

    course = random.choice(recommended) if recommended else "دوره‌های تخصصی"
    discount = random.randint(15, 30)

    subjects = [
        f"{name} جان، وقتشه {course} رو شروع کنی! 🚀",
        f"{name} جان، {course} رو با تخفیف {discount}٪ بگیر! 🎯"
    ]
    subject = subjects[seed % len(subjects)]

    body = f"""
سلام {name} جان،
با توجه به علاقه‌ات به {interests[0]} و سطح {level}، دوره‌ی {course} رو برات انتخاب کردیم. 
این دوره مخصوص افرادی مثل تو طراحی شده که می‌خوان تخصصشون رو به سطح بعدی ببرن.
تا {discount}٪ تخفیف ویژه منتظرته!
"""

    cta = f"✅ برای ثبت‌نام و استفاده از تخفیف {discount}٪، همین الان کلیک کن!"

    full_email = f"موضوع: {subject}\n\n{body}\n\n{cta}"

    score = len(full_email) / 10 + random.uniform(0, 5)
    if "تخفیف" in full_email: score += 3
    if name in full_email: score += 5
    if interests[0] in full_email: score += 3

    return {
        "subject": subject,
        "body": body,
        "cta": cta,
        "full_email": full_email,
        "score": round(score, 2)
    }


# ============================================
# ۶. انتخاب بهترین ایمیل
# ============================================

def select_best_email(samples: List[Dict], user_context: Dict) -> Dict:
    for sample in samples:
        score = sample["score"]
        if user_context["name"] in sample["full_email"]: score += 5
        if "تخفیف" in sample["full_email"]: score += 3
        if user_context["interests"].split(", ")[0] in sample["full_email"]: score += 3
        sample["final_score"] = score

    return sorted(samples, key=lambda x: x["final_score"], reverse=True)[0]


# ============================================
# ۷. اجرای اصلی
# ============================================

def main():
    print("=" * 70)
    print("پروژه ۲: سامانه‌ی تولید محتوای شخصی‌سازی‌شده")
    print("=" * 70)

    results = []
    for user in USERS:
        result = generate_email(user["id"])
        results.append(result)

    for r in results:
        print(f"\n{'=' * 60}")
        print(f"👤 کاربر: {r['user_name']}")
        print(f"📊 علایق: {r['user_context']['interests']}")
        print(f"📈 سطح: {r['user_context']['level']}")
        print(f"\n✨ بهترین ایمیل:")
        print("-" * 60)
        print(r['best_email']['full_email'])
        print("-" * 60)

    output = []
    for r in results:
        output.append({
            "user_id": r["user_id"],
            "user_name": r["user_name"],
            "user_context": r["user_context"],
            "best_email": r["best_email"]["full_email"]
        })

    with open("personalized_emails.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ نتایج در 'personalized_emails.json' ذخیره شد.")
    print("=" * 70)


if __name__ == "__main__":
    main()