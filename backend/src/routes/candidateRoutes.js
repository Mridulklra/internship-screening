const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');
const {
  getAllCandidates,
  getCandidateById,
  updateCandidateStatus
} = require('../controllers/candidateController');

router.use(authenticateToken);

router.get('/', getAllCandidates);
router.get('/:id', getCandidateById);
router.patch('/:id/status', updateCandidateStatus);

module.exports = router;