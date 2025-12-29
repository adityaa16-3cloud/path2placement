def chatbot_response(user_message, performance_prediction=None, placement_prediction=None):
    message = user_message.lower()

    # ---------------- GREETINGS ----------------
    if any(word in message for word in ["hi", "hello", "hey"]):
        return (
            "👋 **Hello! I’m your AI Student Assistant**\n\n"
            "**I can help you with:**\n"
            "• Academic performance analysis\n"
            "• Placement readiness evaluation\n"
            "• Personalized improvement tips\n\n"
            "👉 Try asking:\n"
            "• Will I pass?\n"
            "• Will I get placed?\n"
            "• How can I improve?"
        )

    # ---------------- PERFORMANCE ----------------
    if "pass" in message or "performance" in message:
        if performance_prediction is None:
            return (
                "⚠️ **No performance prediction found**\n\n"
                "Please predict your academic performance first to get insights."
            )

        if performance_prediction == 1:
            return (
                "✅ **Academic Performance: PASS**\n\n"
                "**Confidence Level:** 🟢 High\n\n"
                "**Key Observations:**\n"
                "• Good attendance\n"
                "• Consistent study hours\n"
                "• Strong internal & assignment scores\n\n"
                "**Keep doing:**\n"
                "• Maintain attendance above 75%\n"
                "• Study consistently every day"
            )
        else:
            return (
                "❌ **Academic Performance: FAIL**\n\n"
                "**Confidence Level:** 🟡 Medium\n\n"
                "**Areas to Improve:**\n"
                "• Attendance\n"
                "• Study consistency\n"
                "• Internal marks\n\n"
                "**Action Plan:**\n"
                "• Increase daily study hours\n"
                "• Focus on weak subjects\n"
                "• Improve assignment scores"
            )

    # ---------------- PLACEMENT ----------------
    if any(word in message for word in ["place", "placement", "job"]):
        if placement_prediction is None:
            return (
                "⚠️ **Placement data not found**\n\n"
                "Please predict your placement first to receive personalized advice."
            )

        if placement_prediction == 1:
            return (
                "🎉 **Placement Prediction: LIKELY PLACED**\n\n"
                "**Confidence Level:** 🟢 High\n\n"
                "**Positive Indicators:**\n"
                "• Strong CGPA\n"
                "• Relevant internships & projects\n"
                "• Good aptitude & communication skills\n\n"
                "**Suggestions to stay ahead:**\n"
                "• Continue building projects\n"
                "• Practice mock interviews\n"
                "• Apply early to companies"
            )
        else:
            return (
                "⚠️ **Placement Prediction: AT RISK**\n\n"
                "**Confidence Level:** 🔴 Low to Medium\n\n"
                "**Main Gaps Identified:**\n"
                "• Limited internships\n"
                "• Lower technical skills\n"
                "• Backlogs affecting profile\n\n"
                "**Improvement Roadmap:**\n"
                "• Work on 2–3 strong projects\n"
                "• Improve aptitude & coding\n"
                "• Reduce backlogs if any"
            )

    # ---------------- IMPROVEMENT ----------------
    if any(word in message for word in ["improve", "suggest", "advice"]):
        return (
            "📌 **Personalized Improvement Suggestions**\n\n"
            "**Academics:**\n"
            "• Maintain attendance above 75%\n"
            "• Study at least 2–3 hours daily\n\n"
            "**Placement:**\n"
            "• Do internships or certifications\n"
            "• Build real-world projects\n"
            "• Practice aptitude weekly\n"
            "• Improve communication skills"
        )

    # ---------------- DEFAULT ----------------
    return (
        "🤖 **I didn’t fully understand that**\n\n"
        "**You can ask me:**\n"
        "• Will I pass?\n"
        "• Will I get placed?\n"
        "• How can I improve placement?\n\n"
        "💡 Tip: Ask short, clear questions like ChatGPT 😊"
    )
