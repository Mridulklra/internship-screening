const { dbAll, dbGet } = require('../config/database');

const getStatistics = async (req, res) => {
  try {
    const stats = await Promise.all([
      dbGet('SELECT COUNT(*) as total FROM candidates'),
      dbGet('SELECT COUNT(*) as count FROM candidates WHERE status = "shortlisted"'),
      dbGet('SELECT COUNT(*) as count FROM candidates WHERE status = "pending"'),
      dbGet('SELECT AVG(ai_score) as avg FROM candidates'),
      dbGet('SELECT AVG(cgpa) as avg FROM candidates WHERE cgpa > 0')
    ]);

    res.json({
      success: true,
      data: {
        total: stats[0].total,
        shortlisted: stats[1].count,
        pending: stats[2].count,
        averageScore: Math.round(stats[3].avg * 10) / 10,
        averageCgpa: Math.round(stats[4].avg * 10) / 10
      }
    });
  } catch (error) {
    console.error('Error fetching statistics:', error);
    res.status(500).json({ success: false, error: error.message });
  }
};

const getReferralNetwork = async (req, res) => {
  try {
    const referrals = await dbAll('SELECT * FROM referrals');
    const candidates = await dbAll(`
      SELECT id, name, status, referred_by, ai_score 
      FROM candidates 
      WHERE referred_by IS NOT NULL
    `);

    const nodes = [];
    const links = [];

    referrals.forEach(referral => {
      nodes.push({
        id: referral.referrer_name,
        type: 'referrer',
        email: referral.referrer_email,
        totalReferrals: referral.total_referrals,
        successfulHires: referral.successful_hires,
        conversionRate: referral.conversion_rate,
        value: referral.conversion_rate * 100
      });
    });

    candidates.forEach(candidate => {
      const candidateNode = {
        id: `candidate_${candidate.id}`,
        type: 'candidate',
        name: candidate.name,
        status: candidate.status,
        score: candidate.ai_score
      };
      
      nodes.push(candidateNode);

      links.push({
        source: candidate.referred_by,
        target: `candidate_${candidate.id}`,
        value: candidate.ai_score
      });
    });

    res.json({
      success: true,
      data: { nodes, links }
    });
  } catch (error) {
    console.error('Error fetching referral network:', error);
    res.status(500).json({ success: false, error: error.message });
  }
};

module.exports = { getStatistics, getReferralNetwork };