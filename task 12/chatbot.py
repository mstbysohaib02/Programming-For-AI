from app import app, db, HostelInfo

with app.app_context():
    db.drop_all()
    db.create_all()

    entries = [
        HostelInfo(topic="rooms", response="We offer single, double, and triple rooms with attached bathrooms, study tables, and Wi-Fi."),
        HostelInfo(topic="fees", response="Fees: Single - Rs. 8000/month, Double - Rs. 6500/month, Triple - Rs. 5000/month. Security: Rs. 5000."),
        HostelInfo(topic="facilities", response="Facilities include 24/7 security, mess, Wi-Fi, laundry, study rooms, and a common lounge."),
        HostelInfo(topic="rules", response="Rules: No smoking or loud music. Visitors allowed 10 AM - 6 PM. Entry after 10 PM requires approval."),
        HostelInfo(topic="location", response="We're located near ABC University, Block 5, Main Road, City Center."),
        HostelInfo(topic="contact", response="You can reach us at hostel@example.com or call +923001234567.")
    ]

    db.session.add_all(entries)
    db.session.commit()
    print("✅ Hostel info database added successfully!")
