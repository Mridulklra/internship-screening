const { dbAll, dbGet, dbRun } = require('../config/database');
const axios = require('axios');

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:5001';

const getAllCandidates = async (req, res) => {
  try {
    const { status, minScore, sortBy = 'ai_score', order = 'DESC' } = req.query;

    let query = 'SELECT * FROM candidates WHERE 1=1';
    const params = [];

    if (status) {
      query += ' AND status = ?';
      params.push(status);
    }

    if (minScore) {
      query += ' AND ai_score >= ?';
      params.push(parseFloat(minScore));
    }

    const validSortColumns = ['ai_score', 'cgpa', 'created_at', 'name'];
    const sortColumn = validSortColumns.includes(sortBy) ? sortBy : 'ai_score';
    const sortOrder = order.toUpperCase() === 'ASC' ? 'ASC' : 'DESC';

    query += ` ORDER BY ${sortColumn} ${sortOrder}`;

    const candidates = await dbAll(query, params);

    const formattedCandidates = candidates.map(candidate => ({
      ...candidate,
      skills: JSON.parse(candidate.skills || '[]'),
      projects: JSON.parse(candidate.projects || '[]'),
      experience: JSON.parse(candidate.experience || '[]')
    }));

    res.json({
      success: true,
      count: formattedCandidates.length,
      data: formattedCandidates
    });
  } catch (error) {
    console.error('Error fetching candidates:', error);
    res.status(500).json({ success: false, error: error.message });
  }
};

const getCandidateById = async (req, res) => {
  try {
    const { id } = req.params;
    const candidate = await dbGet('SELECT * FROM candidates WHERE id = ?', [id]);

    if (!candidate) {
      return res.status(404).json({ success: false, error: 'Candidate not found' });
    }

    const formattedCandidate = {
      ...candidate,
      skills: JSON.parse(candidate.skills || '[]'),
      projects: JSON.parse(candidate.projects || '[]'),
      experience: JSON.parse(candidate.experience || '[]')
    };

    res.json({ success: true, data: formattedCandidate });
  } catch (error) {
    console.error('Error fetching candidate:', error);
    res.status(500).json({ success: false, error: error.message });
  }
};

const updateCandidateStatus = async (req, res) => {
  try {
    const { id } = req.params;
    const { status } = req.body;

    const validStatuses = ['pending', 'shortlisted', 'rejected', 'interview', 'hired'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({ success: false, error: 'Invalid status' });
    }

    await dbRun(
      'UPDATE candidates SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
      [status, id]
    );

    const updatedCandidate = await dbGet('SELECT * FROM candidates WHERE id = ?', [id]);

    res.json({
      success: true,
      message: 'Candidate status updated',
      data: updatedCandidate
    });
  } catch (error) {
    console.error('Error updating candidate:', error);
    res.status(500).json({ success: false, error: error.message });
  }
};

module.exports = {
  getAllCandidates,
  getCandidateById,
  updateCandidateStatus
};