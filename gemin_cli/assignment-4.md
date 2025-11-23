# 📘 Assignment Detail

## 🧠 1. Review Presentation on AI Driven & AI Native Development
- AI Driven & AI Native Development : [https://docs.google.com/presentation/d/1UGvCUk1-O8m5i-aTWQNxzg8EXoKzPa8fgcwfNh8vRjQ/edit](https://docs.google.com/presentation/d/1UGvCUk1-O8m5i-aTWQNxzg8EXoKzPa8fgcwfNh8vRjQ/edit)

## 📂 2. Read Following
- Learn the part 1 : [https://ai-native.panaversity.org/docs/Introducing-AI-Driven-Development](https://ai-native.panaversity.org/docs/Introducing-AI-Driven-Development)
- Learn the part 2 : [https://ai-native.panaversity.org/docs/AI-Tool-Landscape](https://ai-native.panaversity.org/docs/AI-Tool-Landscape)

## 📂 3. Watch the following video
- 🔗 Agentic AI: The Revolution - English : [https://www.youtube.com/watch?v=gvdrOrHHVYg&t=2s](https://www.youtube.com/watch?v=gvdrOrHHVYg&t=2s)
- 🔗 Agentic AI: The Revolution - Urdu : [https://www.youtube.com/watch?v=rFFyItAFddY&t=1s](https://www.youtube.com/watch?v=rFFyItAFddY&t=1s)

## 📂 4. Read Following Article
- 🔗 Review the Article : [https://medium.com/google-cloud/gemini-cli-tutorial-series-77da7d494718](https://medium.com/google-cloud/gemini-cli-tutorial-series-77da7d494718)

# 📝 **5. Assignment: Build a Cricket Live-Scores Web App using Gemini CLI + Python Flask**

### **Overview**

In this assignment, you will build a **Python Flask web application** that displays **live cricket match scores**.
You will retrieve live match data using the **RSS feed** provided by ESPN Cricinfo:

➡️ **RSS Feed URL:**
`https://static.cricinfo.com/rss/livescores.xml`

Your goal is to iteratively improve the application using **Gemini CLI** prompts. You can begin with a minimal working version and then continue enhancing or beautifying the project using the Gemini CLI.

---

# 🎯 **Learning Objectives**

By completing this assignment, you will learn to:

* Use **Gemini CLI** to assist in iterative development.
* Build a **Flask web application**.
* Fetch and parse **RSS feed data** in Python.
* Render data on an HTML page using a Flask template.
* Add styling, features, and improvements based on CLI-generated suggestions.

---

# 📌 **Part 1 — Starter Prompt (Required)**

You must begin with this prompt to Gemini CLI:

> **I would like to create a Python Flask Application that shows me a list of live scores of cricket matches. There is a RSS Feed for this that is available over here: [https://static.cricinfo.com/rss/livescores.xml](https://static.cricinfo.com/rss/livescores.xml). Let's use that.**

Gemini CLI should help you generate the basic structure and code.

---

# 📁 **Part 2 — Minimum Requirements**

Your application **must**:

### ✔ 1. Use Flask

Create a Flask server that runs on localhost.

### ✔ 2. Fetch the RSS feed

Use Python to request and parse:

```
https://static.cricinfo.com/rss/livescores.xml
```

### ✔ 3. Parse data from the feed

Extract at least:

* Match title
* Description (which often includes score updates)
* Link to full match page

### ✔ 4. Display matches

Render all live matches in a **clean HTML page**.

### ✔ 5. Use Gemini CLI at least 3 times

Examples:

* Generate starter Flask code
* Improve HTML UI
* Add CSS styles
* Add periodic refresh
* Add searching or filtering
* Add match detail loading
* Add reusable components or improved architecture

---

# ⭐ **Part 3 — Optional Enhancements (Choose Any)**

You may add as many improvements as you want. Here are some ideas:

### 🎨 **UI Improvements**

* Better styling (Bulma, Tailwind, Bootstrap, custom CSS, etc.)
* Card-style match display
* Add match status badges

### 🔄 **Functionality Enhancements**

* Auto-refresh the live scores every 30–60 seconds
* AJAX/Fetch-API refresh without reloading page
* Manual refresh button

### 🔍 **Search**

* Search matches by team name

# 📦 **Part 5 — Deliverables**

Submit the following:

1. **Zip Project folder** containing:

   * app.py
   * templates/ (if any)
   * static/ (if any CSS/JS)
   * requirements.txt

2. **A short 1–2 page report** including:

   * Steps you followed
   * Prompts used
   * What you added or changed manually
   * Screenshots
