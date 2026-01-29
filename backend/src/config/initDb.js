const { initDatabase, dbRun } = require('./database');

const sampleCandidates = [
  {
    name: 'Rahul Sharma',
    email: 'rahul.sharma@example.com',
    phone: '+91-9876543210',
    college: 'IIT Delhi',
    degree: 'B.Tech Computer Science',
    graduation_year: 2025,
    cgpa: 8.7,
    skills: JSON.stringify(['React', 'Node.js', 'Python', 'MongoDB', 'Docker']),
    projects: JSON.stringify(['E-commerce Platform', 'ML Chatbot']),
    experience: JSON.stringify(['SDE Intern at Flipkart - 3 months']),
    ai_score: 92,
    status: 'shortlisted',
    referred_by: 'Amit Kumar'
  },
  {
    name: 'Priya Patel',
    email: 'priya.patel@example.com',
    phone: '+91-9876543211',
    college: 'BITS Pilani',
    degree: 'B.Tech Electronics',
    graduation_year: 2025,
    cgpa: 9.1,
    skills: JSON.stringify(['JavaScript', 'React', 'TypeScript', 'PostgreSQL', 'AWS']),
    projects: JSON.stringify(['Social Analytics Dashboard', 'IoT Automation']),
    experience: JSON.stringify(['Frontend Intern at Zomato - 6 months']),
    ai_score: 95,
    status: 'shortlisted',
    referred_by: 'Sneha Reddy'
  },
  {
    name: 'Arjun Mehta',
    email: 'arjun.mehta@example.com',
    phone: '+91-9876543212',
    college: 'NIT Trichy',
    degree: 'B.Tech Computer Science',
    graduation_year: 2025,
    cgpa: 7.8,
    skills: JSON.stringify(['Java', 'Spring Boot', 'MySQL', 'Git']),
    projects: JSON.stringify(['Library Management System']),
    experience: JSON.stringify([]),
    ai_score: 78,
    status: 'pending',
    referred_by: null
  }
];

const sampleReferrals = [
  {
    referrer_name: 'Amit Kumar',
    referrer_email: 'amit.kumar@company.com',
    total_referrals: 5,
    successful_hires: 2,
    conversion_rate: 0.4
  },
  {
    referrer_name: 'Sneha Reddy',
    referrer_email: 'sneha.reddy@company.com',
    total_referrals: 3,
    successful_hires: 2,
    conversion_rate: 0.67
  }
];

async function seedDatabase() {
  try {
    console.log('🌱 Initializing database...');
    await initDatabase();

    console.log('🌱 Seeding candidates...');
    for (const candidate of sampleCandidates) {
      await dbRun(`
        INSERT INTO candidates (name, email, phone, college, degree, graduation_year, cgpa, skills, projects, experience, ai_score, status, referred_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `, [
        candidate.name, candidate.email, candidate.phone, candidate.college,
        candidate.degree, candidate.graduation_year, candidate.cgpa,
        candidate.skills, candidate.projects, candidate.experience,
        candidate.ai_score, candidate.status, candidate.referred_by
      ]);
    }

    console.log('🌱 Seeding referrals...');
    for (const referral of sampleReferrals) {
      await dbRun(`
        INSERT INTO referrals (referrer_name, referrer_email, total_referrals, successful_hires, conversion_rate)
        VALUES (?, ?, ?, ?, ?)
      `, [
        referral.referrer_name, referral.referrer_email,
        referral.total_referrals, referral.successful_hires,
        referral.conversion_rate
      ]);
    }

    console.log('✅ Database seeded successfully!');
    console.log('📊 Added:', sampleCandidates.length, 'candidates');
    console.log('🔗 Added:', sampleReferrals.length, 'referrers');
    process.exit(0);
  } catch (error) {
    console.error('❌ Error seeding database:', error);
    process.exit(1);
  }
}

seedDatabase();