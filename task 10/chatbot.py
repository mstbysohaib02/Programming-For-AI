def get_response(user_input, last_topic=None):
    user_input = user_input.lower()
    topic = None

    keywords = {
        "rooms": ["room", "rooms", "single", "double", "triple"],
        "fees": ["fee", "fees", "charges", "cost"],
        "facilities": ["facility", "facilities", "service", "services"],
        "rules": ["rule", "rules", "regulations"],
        "location": ["location", "address", "where"],
        "contact": ["contact", "phone", "email", "number"]
    }

    responses = {
        "rooms": "We offer single, double, and triple rooms with attached bathrooms, study tables, and Wi-Fi.",
        "fees": "Fees: Single - Rs. 8000/month, Double - Rs. 6500/month, Triple - Rs. 5000/month. Security: Rs. 5000.",
        "facilities": "Facilities include 24/7 security, mess, Wi-Fi, laundry, study rooms, and a common lounge.",
        "rules": "Rules: No smoking or loud music. Visitors allowed 10 AM - 6 PM. Entry after 10 PM requires approval.",
        "location": "We're located at Sector 12, near XYZ University, Sher Shah Town.",
        "contact": "Contact us at 0300-1234567 or email info@hostelhub.com."
    }

    for key, word_list in keywords.items():
        if any(word in user_input for word in word_list):
            topic = key
            break

    if not topic and last_topic:
        topic = last_topic 

    if topic:
        return responses[topic], topic
    else:
        return (
            "Sorry, I didn't understand. You can ask about rooms, fees, facilities, rules, location, or contact info.",
            None
        )
