"""
PsychBuddy Database Migration & Sample Data Seeder
=================================================
Provides functions to create all MySQL tables and seed realistic sample data
for all features (psychiatrists, sound therapy, yoga, meditation, books,
video sessions, personalized tips, user logs, community forum, and admin).
"""

import os
import pymysql
import pymysql.cursors
from datetime import datetime, date
from pathlib import Path
from dotenv import load_dotenv

# Ensure environment variables are loaded
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'psychbuddy')
DB_PORT = int(os.getenv('DB_PORT', 3306))


def get_mysql_connection(include_database=True):
    """Establish and return a PyMySQL connection."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        database=DB_NAME if include_database else None,
        cursorclass=pymysql.cursors.DictCursor
    )


# Table Schemas
TABLE_SCHEMAS = {
    'users': """
        CREATE TABLE IF NOT EXISTS users (
            fullname VARCHAR(255) NOT NULL,
            gender VARCHAR(50),
            dob VARCHAR(50),
            age VARCHAR(50),
            mobileno VARCHAR(50),
            email VARCHAR(255) PRIMARY KEY,
            address TEXT,
            password VARCHAR(255) NOT NULL,
            login_status INT DEFAULT 0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'otp_verification': """
        CREATE TABLE IF NOT EXISTS otp_verification (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mobileno VARCHAR(50),
            email VARCHAR(255),
            otp VARCHAR(50),
            date VARCHAR(50),
            time VARCHAR(50)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'admin_credentials': """
        CREATE TABLE IF NOT EXISTS admin_credentials (
            adminname VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'psychiatrist_dir': """
        CREATE TABLE IF NOT EXISTS psychiatrist_dir (
            id INT AUTO_INCREMENT PRIMARY KEY,
            psychname VARCHAR(255) NOT NULL,
            picture VARCHAR(255) NOT NULL,
            location VARCHAR(255),
            education VARCHAR(255),
            description TEXT,
            experience VARCHAR(100),
            `g-rating` VARCHAR(50),
            contact VARCHAR(100),
            email VARCHAR(255)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'sound_therapy': """
        CREATE TABLE IF NOT EXISTS sound_therapy (
            therapy_name VARCHAR(255) NOT NULL,
            therapy_img VARCHAR(255) NOT NULL,
            therapy_path VARCHAR(255) NOT NULL,
            therapy_desc TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'meditation': """
        CREATE TABLE IF NOT EXISTS meditation (
            mname VARCHAR(255) NOT NULL,
            description TEXT NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'reading_resources': """
        CREATE TABLE IF NOT EXISTS reading_resources (
            bookname VARCHAR(255) NOT NULL,
            bookcover VARCHAR(255) NOT NULL,
            bookauthor VARCHAR(255) NOT NULL,
            bestfor VARCHAR(255),
            bookpyear VARCHAR(50),
            bookpath VARCHAR(255) NOT NULL,
            bookdesc TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'sessions': """
        CREATE TABLE IF NOT EXISTS sessions (
            sess_name VARCHAR(255) NOT NULL,
            sess_category VARCHAR(255) NOT NULL,
            sess_path VARCHAR(255) NOT NULL,
            sess_desc TEXT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'community_forum': """
        CREATE TABLE IF NOT EXISTS community_forum (
            id INT AUTO_INCREMENT PRIMARY KEY,
            msg TEXT NOT NULL,
            email VARCHAR(255) NOT NULL,
            date VARCHAR(50) NOT NULL,
            time VARCHAR(50) NOT NULL,
            administrator VARCHAR(255) NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'feedback': """
        CREATE TABLE IF NOT EXISTS feedback (
            user VARCHAR(255) NOT NULL,
            contact VARCHAR(100),
            msg TEXT NOT NULL,
            datetime VARCHAR(100)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'admintips': """
        CREATE TABLE IF NOT EXISTS admintips (
            tips TEXT NOT NULL,
            datetime VARCHAR(100)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'wellnesslog': """
        CREATE TABLE IF NOT EXISTS wellnesslog (
            email VARCHAR(255) NOT NULL,
            log TEXT NOT NULL,
            time VARCHAR(50) NOT NULL,
            date VARCHAR(50) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'yoga': """
        CREATE TABLE IF NOT EXISTS yoga (
            yname VARCHAR(255) NOT NULL,
            steps TEXT NOT NULL,
            benefits TEXT NOT NULL,
            img VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    'tips': """
        CREATE TABLE IF NOT EXISTS tips (
            id INT AUTO_INCREMENT PRIMARY KEY,
            emotion VARCHAR(50) NOT NULL,
            suggestion TEXT NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
}


def migrate_database(drop_existing=False):
    """Create database and all required tables."""
    print("=" * 60)
    print("🚀 PsychBuddy Database Migration")
    print("=" * 60)
    
    # Step 1: Ensure database exists
    conn_server = get_mysql_connection(include_database=False)
    try:
        with conn_server.cursor() as cr:
            cr.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"✔ Database `{DB_NAME}` verified / created.")
    finally:
        conn_server.close()

    # Step 2: Create all tables
    conn = get_mysql_connection(include_database=True)
    try:
        with conn.cursor() as cr:
            for table_name, ddl in TABLE_SCHEMAS.items():
                if drop_existing:
                    cr.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
                    print(f"  - Dropped old `{table_name}` table.")
                cr.execute(ddl)
                print(f"  ✔ Table `{table_name}` ready.")
            conn.commit()
        print("✔ All 14 database tables migrated successfully.\n")
    finally:
        conn.close()


def seed_sample_data(clear_existing=False):
    """Seed comprehensive sample data for all tables."""
    print("=" * 60)
    print("🌱 Seeding Sample Data for Frontend")
    print("=" * 60)

    conn = get_mysql_connection(include_database=True)
    try:
        with conn.cursor() as cr:
            # 1. Admin Credentials (admin / admin encoded in hex)
            admin_hex = "admin".encode().hex()  # '61646d696e'
            cr.execute("INSERT IGNORE INTO admin_credentials VALUES (%s, %s)", (admin_hex, admin_hex))
            print("  ✔ Admin credentials seeded (`admin` / `admin`).")

            # 2. Users (Seed active demo user so user-specific views work immediately)
            user_data = [
                (
                    "Sakshi Naravankar", "Female", "2001-05-14", "23",
                    "+91 9876543210", "sakshi@psychbuddy.com", "Mumbai, Maharashtra",
                    "sakshi123", 1  # login_status = 1 (Active User)
                ),
                (
                    "Ganesh Telore", "Male", "2000-08-20", "24",
                    "+91 9123456780", "ganesh@psychbuddy.com", "Pune, Maharashtra",
                    "ganesh123", 0
                ),
                (
                    "Bhaskar Telore", "Male", "1998-11-03", "26",
                    "+91 9822334455", "bhaskar@psychbuddy.com", "Nashik, Maharashtra",
                    "bhaskar123", 0
                )
            ]
            for u in user_data:
                cr.execute(
                    "INSERT IGNORE INTO users (fullname, gender, dob, age, mobileno, email, address, password, login_status) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", u
                )
            # Ensure at least one user is logged in
            cr.execute("UPDATE users SET login_status = 1 WHERE email = %s", ("sakshi@psychbuddy.com",))
            print("  ✔ Sample users seeded (active session: `sakshi@psychbuddy.com`).")

            # 3. Psychiatrists Directory
            psychiatrists = [
                ("Dr. Harish Shetty", "img/psychiatrist/Harish Shetty.jpg", "Mumbai, India", "MD - Psychiatry",
                 "Renowned social psychiatrist dedicated to community mental health, cognitive therapies, and youth wellbeing.",
                 "25+ Years", "4.9", "+91 98200 00001", "dr.shetty@psychbuddy.com"),
                ("Dr. Samir Parikh", "img/psychiatrist/Samir Parikh.jpg", "New Delhi, India", "DPM, MD - Psychiatry",
                 "Eminent psychiatrist and director of mental health initiatives focused on emotional resilience and school mental health.",
                 "20+ Years", "4.8", "+91 98100 00002", "dr.parikh@psychbuddy.com"),
                ("Dr. Anjali Chhabria", "img/psychiatrist/Anjali Chhabria.jpg", "Mumbai, India", "MD - Psychiatry",
                 "Leading psychiatrist, author, and founder of Mindtemple clinic with a specialty in holistic wellness and counseling.",
                 "22+ Years", "4.9", "+91 98210 00003", "dr.anjali@psychbuddy.com"),
                ("Dr. Jitendra Nagpal", "img/psychiatrist/Jitendra Nagpal.jpg", "New Delhi, India", "MD - Psychiatry",
                 "Senior consultant psychiatrist specializing in child, adolescent, and family mental healthcare.",
                 "24+ Years", "4.7", "+91 98110 00004", "dr.nagpal@psychbuddy.com"),
                ("Dr. Kersi Chavda", "img/psychiatrist/Kersi Chavda.jpg", "Mumbai, India", "MD, DPM - Psychiatry",
                 "Expert in neurodevelopmental conditions, depression management, and behavioral wellness therapy.",
                 "30+ Years", "4.9", "+91 98200 00005", "dr.chavda@psychbuddy.com"),
                ("Dr. Nimesh Desai", "img/psychiatrist/Nimesh Desai.jpg", "New Delhi, India", "MD - Psychiatry",
                 "Distinguished professor and public mental health advocate specializing in adult psychiatry and rehabilitation.",
                 "28+ Years", "4.8", "+91 98100 00006", "dr.desai@psychbuddy.com"),
                ("Dr. Sameer Malhotra", "img/psychiatrist/Sameer Malhotra.jpg", "New Delhi, India", "MD - Psychiatry",
                 "Head of mental health department specializing in substance de-addiction and mood disorders.",
                 "21+ Years", "4.8", "+91 98100 00007", "dr.malhotra@psychbuddy.com"),
                ("Dr. Shyam Bhat", "img/psychiatrist/Shyam Bhat.jpg", "Bangalore, India", "MD - Psychiatry, ABPN",
                 "Integrative medicine physician and psychiatrist blending Eastern mindfulness with modern neuroscience.",
                 "18+ Years", "4.9", "+91 98800 00008", "dr.bhat@psychbuddy.com"),
                ("Dr. Vikram Patel", "img/psychiatrist/Vikram Patel.jpg", "Goa, India", "PhD, FRCPsych",
                 "World-renowned Harvard professor of global mental health and advocate for accessible mental care.",
                 "30+ Years", "5.0", "+91 98300 00009", "dr.patel@psychbuddy.com"),
                ("Dr. Amit Malik", "img/psychiatrist/Amit Malik.jpg", "Pune, India", "MRCPsych - UK",
                 "Global digital health psychiatrist with clinical expertise in anxiety, burnout, and adult ADHD.",
                 "19+ Years", "4.8", "+91 98220 00010", "dr.malik@psychbuddy.com")
            ]
            if clear_existing:
                cr.execute("DELETE FROM psychiatrist_dir;")
            for p in psychiatrists:
                cr.execute(
                    "INSERT IGNORE INTO psychiatrist_dir (psychname, picture, location, education, description, experience, `g-rating`, contact, email) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", p
                )
            print(f"  ✔ {len(psychiatrists)} Psychiatrist profiles seeded.")

            # 4. Sound Therapy (Audio tracks)
            sounds = [
                ("Ocean Waves", "img/sound_img/ocean wave.jpg", "audio/Ocean Wave Sound.mp3",
                 "Calming rhythmic ocean waves to quiet racing thoughts and induce deep, restorative sleep."),
                ("Rain & Thunderstorm", "img/sound_img/rain.jpg", "audio/Rain.mp3",
                 "Gentle rainfall on leaves creating natural white noise to soothe anxiety and promote focus."),
                ("Forest Nightingale", "img/sound_img/nightingale.jpg", "audio/Forest Nightingle Song.mp3",
                 "Sweet natural bird song recorded in a peaceful woodland for stress relief and meditation."),
                ("Running River", "img/sound_img/running river.jpg", "audio/Running River Sound.mp3",
                 "Steady streaming water cascading over smooth river stones to wash away mental fatigue."),
                ("Night Sky & Stars", "img/sound_img/night star.jpg", "audio/Night Stars Sound.mp3",
                 "Deep atmospheric ambient nocturnal tones designed for evening relaxation and unwinding."),
                ("Birds Singing & Chirping", "img/sound_img/nightingale.jpg", "audio/Birds Singing Sound.mp3",
                 "Uplifting morning woodland melodies to brighten your mood and start your day energized."),
                ("Peaceful Water Stream", "img/sound_img/river stream.jpg", "audio/Peaceful Water Sound.mp3",
                 "Gentle, clear creek waters flowing through nature for background focus and study."),
                ("Krishna Divine Flute", "img/sound_img/steady river.jpg", "audio/Krishna Flute 1.mp3",
                 "Soulful classical Indian flute melodies that nurture inner peace and spiritual grounding.")
            ]
            if clear_existing:
                cr.execute("DELETE FROM sound_therapy;")
            for s in sounds:
                cr.execute("INSERT IGNORE INTO sound_therapy VALUES (%s, %s, %s, %s)", s)
            print(f"  ✔ {len(sounds)} Sound therapy audio tracks seeded.")

            # 5. Reading Resources (Books)
            books = [
                ("Hope and Help for Your Nerves", "img/books_poster/Hope and Help for Your Nerves.jpg",
                 "Dr. Claire Weekes", "Anxiety & Panic Relief", "1969",
                 "books/Hope and Help for Your Nerves.pdf",
                 "The timeless masterwork explaining the nervous system, fear-adrenalin cycles, and true recovery through acceptance."),
                ("The Body Keeps The Score", "img/books_poster/The Body Keeps The Score.jpg",
                 "Bessel van der Kolk, M.D.", "Trauma Healing", "2014",
                 "books/The Body Keeps The Score.pdf",
                 "Groundbreaking perspective on how psychological trauma literally reshapes both body and brain, with innovative healing paths."),
                ("Emotional First Aid", "img/books_poster/Emotional First Aid.jpg",
                 "Guy Winch, Ph.D.", "Everyday Resilience", "2013",
                 "books/Emotional First Aid.pdf",
                 "Practical, science-backed treatments for everyday psychological injuries like rejection, guilt, failure, and loneliness."),
                ("Attached - The Science of Adult Attachment", "img/books_poster/Attached.png",
                 "Amir Levine & Rachel Heller", "Relationships & Love", "2010",
                 "books/Attached - The New Science of Adult Attachment.pdf",
                 "A revolutionary guide to understanding adult attachment styles (Anxious, Avoidant, and Secure) to build healthier bonds."),
                ("The 7 Habits of Highly Effective People", "img/books_poster/The 7 Habits of Highly Effective People.jpg",
                 "Stephen R. Covey", "Personal Development", "1989",
                 "books/The 7 Habits of Highly Effective People.pdf",
                 "Foundational principles for self-mastery, proactive living, emotional maturity, and mutual interdependence."),
                ("Breaking Free of Addiction", "img/books_poster/Breaking Free of Addiction.jpg",
                 "Recovery Clinical Group", "Addiction & Habits", "2018",
                 "books/Breaking Free of Addiction.pdf",
                 "Compassionate, evidence-based roadmap for rewiring reward loops and overcoming compulsive behavioral patterns."),
                ("Healing The Trauma of Domestic Violence", "img/books_poster/Healing The Trauma of Domestic Violence.jpg",
                 "Mari McCaig", "Recovery & Safety", "2016",
                 "books/Healing The Trauma of Domestic Violence.pdf",
                 "A gentle workbook providing tools for rebuilding boundary safety, self-esteem, and post-traumatic growth."),
                ("Loving Bravely", "img/books_poster/Loving Bravely.jpg",
                 "Dr. Alexandra H. Solomon", "Couples & Intimacy", "2017",
                 "books/Loving Bravely.pdf",
                 "Twenty lessons on self-discovery to create the self-compassion and courage needed to cultivate authentic love."),
                ("Maybe You Should Talk to Someone", "img/books_poster/Maybe You Should Talk to Someone.jpg",
                 "Lori Gottlieb", "Therapy Insights", "2019",
                 "books/Maybe You Should Talk to Someone.pdf",
                 "A therapist shares intimate stories of her own patients alongside her journey as a patient, exploring the human condition."),
                ("The Highly Sensitive Person", "img/books_poster/The Highly Sensitive Person.jpg",
                 "Dr. Elaine N. Aron", "Sensitivity & Empathy", "1996",
                 "books/The Highly Sensitive Person.pdf",
                 "Essential insights for recognizing environmental overstimulation and turning high sensitivity into your superpower.")
            ]
            if clear_existing:
                cr.execute("DELETE FROM reading_resources;")
            for b in books:
                cr.execute("INSERT IGNORE INTO reading_resources VALUES (%s, %s, %s, %s, %s, %s, %s)", b)
            print(f"  ✔ {len(books)} Reading resources / e-books seeded.")

            # 6. Yoga Poses
            yoga_poses = [
                ("Balasana (Child Pose)",
                 "1. Kneel comfortably on a mat with big toes touching.\n2. Sit back on your heels and widen knees to hip-width.\n3. Fold forward, resting your torso between your thighs.\n4. Extend arms forward or rest alongside your body.\n5. Breathe slowly and deeply for 1-3 minutes.",
                 "Relieves mental fatigue, releases tension in the lower back and shoulders, and gently calms the autonomic nervous system.",
                 "img/YM/balasan.jpg"),
                ("Bhujangasana (Cobra Pose)",
                 "1. Lie prone on your stomach with tops of feet pressed into the mat.\n2. Place hands beneath shoulders with elbows tucked close.\n3. Inhale and gently lift your chest while keeping hips grounded.\n4. Hold gaze forward without straining the neck for 15-30 seconds.",
                 "Invigorates the heart and lungs, stimulates abdominal organs, counteracts slouching, and helps alleviate feelings of mild depression.",
                 "img/YM/bhujangasana.jpg"),
                ("Sukhasana (Easy Pose)",
                 "1. Sit cross-legged on your mat with spine upright and shoulders relaxed.\n2. Rest hands gently on your knees in Gyan mudra.\n3. Lengthen the crown of your head toward the ceiling.\n4. Close eyes and focus on slow, mindful rhythmic breath.",
                 "Cultivates inner centeredness, eases anxiety, improves spinal alignment, and prepares the mind for restful meditation.",
                 "img/YM/sukhasana.jpg"),
                ("Setu Bandhasana (Bridge Pose)",
                 "1. Lie on your back with knees bent and feet flat on the floor, hip-width apart.\n2. Place arms alongside body, palms down.\n3. Press into feet to lift hips toward ceiling, clasping hands under back.\n4. Hold for 30-60 seconds, then slowly roll spine down.",
                 "Opens the chest, neck, and spine, relieves tired legs, and calms the brain while alleviating stress and mild depression.",
                 "img/YM/setu bandhasana.jpg"),
                ("Shavasana (Corpse Pose)",
                 "1. Lie completely flat on your back with arms and legs naturally apart.\n2. Turn palms upward and allow toes to fall open.\n3. Consciously scan body from feet to scalp, releasing every lingering muscle tension.\n4. Rest quietly for 5-10 minutes.",
                 "Known as the ultimate restorative pose; drops blood pressure, resets the nervous system, and integrates the healing benefits of your practice.",
                 "img/YM/shavasana.jpg"),
                ("Vrikshasana (Tree Pose)",
                 "1. Stand tall in mountain pose with feet rooted into earth.\n2. Shift weight onto left foot and place right sole on inner left thigh or calf.\n3. Bring palms together at heart center or reach them toward the sky.\n4. Fix eyes on a non-moving point for 30 seconds, then switch sides.",
                 "Develops laser focus, improves neuro-muscular balance, and promotes self-confidence and grounding during stressful times.",
                 "img/YM/vrikshasana.jpg")
            ]
            if clear_existing:
                cr.execute("DELETE FROM yoga;")
            for y in yoga_poses:
                cr.execute("INSERT IGNORE INTO yoga VALUES (%s, %s, %s, %s)", y)
            print(f"  ✔ {len(yoga_poses)} Yoga postures seeded.")

            # 7. Meditation Techniques
            meditations = [
                ("Mindful Breath Awareness (Anapana)",
                 "Sit in a relaxed, comfortable posture. Direct gentle, non-judgmental attention to the sensation of breath as it passes your nostrils. Whenever thoughts or worries intrude, simply acknowledge them kindly and return attention to the breath."),
                ("Progressive Muscle Relaxation (PMR)",
                 "Systematically tense and then deeply relax each muscle group, starting from your toes, calves, thighs, through your torso, shoulders, and facial muscles. Notice the sharp contrast between tension and deep physiological relief."),
                ("Loving-Kindness Meditation (Metta)",
                 "Silently repeat heartfelt wishes: 'May I be happy. May I be safe. May I be healthy. May I live with ease.' Gradually expand these sincere wishes outward to loved ones, acquaintances, challenging individuals, and all living beings everywhere."),
                ("Box Breathing Technique (4-4-4-4)",
                 "Inhale deeply through your nose for a count of 4. Hold full lungs for 4. Exhale smoothly through your mouth for 4. Hold empty lungs for 4. Repeat for 4-5 cycles to immediately activate the parasympathetic nervous system."),
                ("5-4-3-2-1 Sensory Grounding",
                 "Anchor yourself during panic or high stress by identifying 5 things you can see, 4 things you can physically feel, 3 distinct sounds you can hear, 2 things you can smell, and 1 positive affirmation you can tell yourself.")
            ]
            if clear_existing:
                cr.execute("DELETE FROM meditation;")
            for m in meditations:
                cr.execute("INSERT IGNORE INTO meditation VALUES (%s, %s)", m)
            print(f"  ✔ {len(meditations)} Guided meditation techniques seeded.")

            # 8. Video Therapy Sessions (all 6 categories)
            sessions = [
                ("Session 1 - Self-Discovery & Reflection", "individual therapy",
                 "sessions/individual therapy/session 1.mp4",
                 "A compassionate one-on-one guided journey exploring inner values, negative core beliefs, and radical self-acceptance."),
                ("Session 2 - Navigating Overwhelm", "individual therapy",
                 "sessions/individual therapy/session 2.mp4",
                 "Practical cognitive re-framing tools to de-escalate workplace burnout and daily emotional overwhelm."),
                ("Session 3 - Finding Your Core Strengths", "individual therapy",
                 "sessions/individual therapy/session 3.mp4",
                 "Identifying natural coping strengths and building healthy, guilt-free boundaries with others."),
                ("Finding Strength in Group Support - Pt. 1", "Group therapy",
                 "sessions/group therapy/session 1.mp4",
                 "Shared vulnerability and peer empathy: realizing you are not alone in navigating life's heavy burdens."),
                ("Cultivating Mutual Listening - Pt. 2", "Group therapy",
                 "sessions/group therapy/session 2.mp4",
                 "Facilitated group practices on reflective listening, non-judgmental feedback, and mutual accountability."),
                ("10 Tips For Good Communication", "Couple Therapy",
                 "sessions/couple therapy/10 Tips For Good Communication.mp4",
                 "Essential conversational habits to communicate unmet needs without triggering defense mechanisms in your partner."),
                ("3 Steps to Happier Relationships", "Couple Therapy",
                 "sessions/couple therapy/3 Steps to Happier Relationships.mp4",
                 "Reigniting intimacy, deep friendship, and emotional security through small everyday bids of connection."),
                ("6 Tips on Addressing Family Tension", "Family Therapy",
                 "sessions/family therapy/6 Tips on Adressing family tension.mp4",
                 "Proven family systems strategies for de-escalating multigenerational conflicts and holiday gatherings."),
                ("Functional Family Therapy Basics", "Family Therapy",
                 "sessions/family therapy/functional family therapy.mp4",
                 "Rebalancing relational roles, establishing collaborative household agreements, and supporting adolescent wellbeing."),
                ("How to Fix a Broken Heart", "Heartbroken Therapy",
                 "sessions/heartbroken therapy/how to fix a broken heart.mp4",
                 "Psychological first aid after heartbreak: breaking the illusion of idealization and healing grief step-by-step."),
                ("Moving on after Toxic Relationships", "Heartbroken Therapy",
                 "sessions/heartbroken therapy/move on after toxic relationship.mp4",
                 "Recovering from emotional manipulation, rediscovering your authentic voice, and rebuilding self-worth."),
                ("Grounding Through Trauma Triggers", "Trauma Therapy",
                 "sessions/individual therapy/session 4.mp4",
                 "Somatic grounding and mindfulness tools for managing sudden trauma triggers and emotional flashbacks.")
            ]
            if clear_existing:
                cr.execute("DELETE FROM sessions;")
            for s in sessions:
                cr.execute("INSERT IGNORE INTO sessions VALUES (%s, %s, %s, %s)", s)
            print(f"  ✔ {len(sessions)} Therapy video sessions seeded across all categories.")

            # 9. Emotion Detection Personalized Tips
            emotion_tips = [
                ("happy",
                 "Celebrate your joyful state! Take a moment to write down 3 things you are grateful for today. Sharing a smile or kind word with someone can make your positive energy ripple outward."),
                ("sad",
                 "It is okay not to be okay. Treat yourself with the gentle kindness you would offer a dear friend. Drink warm water, wrap up comfortably, listen to gentle ambient rain sounds, and rest."),
                ("angry",
                 "Your anger is a signal, not a mandate. Try the 4-7-8 breathing method: inhale for 4s, hold for 7s, exhale slowly for 8s. Take a brisk walk outside before responding to any message."),
                ("neutral",
                 "A calm, balanced state is fertile ground for growth! Use this stillness to practice a short 10-minute mindfulness meditation or enjoy a chapter of an inspiring book."),
                ("fear",
                 "Anxiety is often future-focused thinking. Re-anchor into the present physical reality with 5-4-3-2-1 sensory grounding. Remind yourself: 'Right now, in this moment, I am safe.'"),
                ("surprise",
                 "Take a breath and pause. Allow your sensory nervous system time to process recent news or unexpected events before making any sudden decisions."),
                ("disgust",
                 "Notice where you feel aversion in your body. Step back from toxic environments or conversations, wash your face with cool water, and reaffirm your personal boundaries.")
            ]
            if clear_existing:
                cr.execute("DELETE FROM tips;")
            for e, tip in emotion_tips:
                cr.execute("INSERT IGNORE INTO tips (emotion, suggestion) VALUES (%s, %s)", (e, tip))
            print(f"  ✔ Personalized tips seeded for {len(emotion_tips)} emotional states.")

            # 10. Community Forum Posts
            forum_posts = [
                ("Welcome to the PsychBuddy Community Forum! This is a judgment-free sanctuary to share your thoughts, support peers, and celebrate wellness milestones.",
                 "sakshi@psychbuddy.com", str(date.today()), "09:30:00", None),
                ("I started listening to the Ocean Waves sound therapy before sleeping and it has significantly reduced my night anxiety. Highly recommend it to anyone struggling with insomnia!",
                 "ganesh@psychbuddy.com", str(date.today()), "10:15:00", None),
                ("Remember to take intentional 5-minute pauses during your workday. Your mental well-being is every bit as important as any deadline.",
                 "admin@psychbuddy.com", str(date.today()), "11:00:00", "Admin Team")
            ]
            if clear_existing:
                cr.execute("DELETE FROM community_forum;")
            for post in forum_posts:
                cr.execute("INSERT IGNORE INTO community_forum (msg, email, date, time, administrator) VALUES (%s, %s, %s, %s, %s)", post)
            print("  ✔ Community Forum sample discussions seeded.")

            # 11. Wellness Progress Logs
            wellness_logs = [
                ("sakshi@psychbuddy.com", "Completed 20 minutes of morning Sukhasana and mindful breathing. Felt calm, focused, and ready for work.", "08:30:00", str(date.today())),
                ("sakshi@psychbuddy.com", "Listened to Forest Nightingale audio track during my lunch break to decompress from meetings.", "13:15:00", str(date.today())),
                ("ganesh@psychbuddy.com", "Read Chapter 3 of Hope and Help for Your Nerves. Practiced letting nervous sensations pass through without fear.", "21:00:00", str(date.today()))
            ]
            if clear_existing:
                cr.execute("DELETE FROM wellnesslog;")
            for log in wellness_logs:
                cr.execute("INSERT IGNORE INTO wellnesslog VALUES (%s, %s, %s, %s)", log)
            print("  ✔ Daily Mental Wellness progress logs seeded.")

            # 12. Feedback & Admin Tips
            feedbacks = [
                ("Sakshi Naravankar", "+91 9876543210", "PsychBuddy's audio relaxation sessions helped me manage my exam stress wonderfully! The interface is so warm and welcoming.", str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
                ("Ganesh Telore", "+91 9123456780", "The book collection has fantastic titles. The PDFs open instantly and the tips for couples therapy are very practical.", str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            ]
            if clear_existing:
                cr.execute("DELETE FROM feedback;")
            for fb in feedbacks:
                cr.execute("INSERT IGNORE INTO feedback VALUES (%s, %s, %s, %s)", fb)

            admin_tips = [
                ("Hydration and slow breathing: Drink a glass of water and take 5 conscious breaths whenever you feel overwhelmed.", str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
                ("Digital Sunset: Avoid blue light screens 45 minutes before sleep to facilitate restorative melatonin production.", str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            ]
            if clear_existing:
                cr.execute("DELETE FROM admintips;")
            for tip in admin_tips:
                cr.execute("INSERT IGNORE INTO admintips VALUES (%s, %s)", tip)

            print("  ✔ User feedback entries & admin daily tips seeded.")

            conn.commit()
            print("\n" + "=" * 60)
            print("✨ Migration & Sample Data Seeding Completed Successfully!")
            print("   The frontend has full, rich content across all modules.")
            print("=" * 60)
    finally:
        conn.close()


def migrate_and_seed(drop_existing=False, clear_existing=False):
    """Convenience function to run migration and seeding together."""
    migrate_database(drop_existing=drop_existing)
    seed_sample_data(clear_existing=clear_existing)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="PsychBuddy Database Migrator & Seeder")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate all tables from scratch")
    args = parser.parse_args()
    migrate_and_seed(drop_existing=args.reset, clear_existing=args.reset)
