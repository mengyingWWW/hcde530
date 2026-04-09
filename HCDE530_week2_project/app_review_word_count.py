def count_words(text):
    """Return number of words in a review string."""
    return len(text.split())


# 50 made-up app review responses
reviews = [
    "The app is super easy to use and helped me organize my weekly tasks.",
    "I like the design, but syncing across devices takes too long sometimes.",
    "Great for reminders, though the notification sound options are limited.",
    "I found the onboarding clear and finished setup in under two minutes.",
    "Search works well, but filters for old notes could be better.",
    "This app keeps crashing when I upload large images from my gallery.",
    "I appreciate the dark mode because I use it mostly at night.",
    "The calendar integration is useful and saves me from duplicate entries.",
    "I wish the free version allowed more than three custom categories.",
    "The interface feels clean and simple, which makes daily use enjoyable.",
    "Loading time improved a lot after the latest update on my phone.",
    "I struggled to reset my password because the email arrived very late.",
    "The tutorial tooltips were actually helpful and not too overwhelming.",
    "I love how fast I can add a new task with one tap.",
    "Sometimes completed tasks reappear after refresh, which is frustrating.",
    "The app helped me stay consistent with my study schedule this month.",
    "Widgets on the home screen are nice but customization is minimal.",
    "I can share lists with friends easily and collaboration feels smooth.",
    "The premium plan is a bit expensive for the features offered.",
    "Overall it is reliable, but offline mode still needs major work.",
    "I use this every day and it has replaced my paper planner.",
    "Color coding is nice, yet I cannot choose enough shades for projects.",
    "The app logs me out randomly and I need to sign in again.",
    "I enjoy the weekly summary emails because they keep me accountable.",
    "Customer support responded quickly and solved my sync issue in one day.",
    "The update changed button locations and now my workflow feels slower.",
    "Voice input works better than expected and captures most words correctly.",
    "I wish there were templates for recurring workflows and meeting notes.",
    "The app drains battery faster than other productivity tools I have used.",
    "Cross-platform support is good and data transfer from web is seamless.",
    "I had trouble finding archived items until I discovered the hidden menu.",
    "The progress charts are motivating and easy to understand at a glance.",
    "It would be helpful to export reports directly to PDF from mobile.",
    "I like the minimal layout but font size options are too limited.",
    "Backup and restore worked perfectly when I switched to a new phone.",
    "The app is useful for personal planning but less strong for team use.",
    "I accidentally deleted a list and could not recover it afterward.",
    "Tagging features make it easier to sort notes by topic quickly.",
    "The reminders are reliable, though snooze options are missing useful presets.",
    "I enjoy using it, but startup speed is slower on older devices.",
    "The free tier is decent and enough for basic personal productivity.",
    "I found a bug where recurring reminders duplicate after timezone changes.",
    "The design feels modern and I can navigate without thinking much.",
    "It is good for habit tracking, especially with streak indicators.",
    "I want better keyboard shortcuts on desktop to speed up my workflow.",
    "Sharing to other apps is convenient and works most of the time.",
    "Some icons are hard to interpret and could use clearer labels.",
    "After the recent patch, syncing reliability has improved noticeably for me.",
    "I value the privacy settings, but explanations are too technical.",
    "Overall this app saves me time and keeps my week organized.",
]


print(f"{'Review #':<10} {'Words':<6} {'Preview'}")
print("-" * 72)

word_counts = []

for i, review in enumerate(reviews, start=1):
    words = count_words(review)
    word_counts.append(words)
    preview = review if len(review) <= 60 else review[:60] + "..."
    print(f"{i:<10} {words:<6} {preview}")

print()
print("Summary")
print("-" * 20)
print(f"Total reviews : {len(word_counts)}")
print(f"Shortest      : {min(word_counts)} words")
print(f"Longest       : {max(word_counts)} words")
print(f"Average       : {sum(word_counts) / len(word_counts):.1f} words")
