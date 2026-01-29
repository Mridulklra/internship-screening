const express = require('express');
const router = express.Router();
const { authenticateToken } = require('../middleware/auth');
const {
  getStatistics,
  getReferralNetwork
} = require('../controllers/analyticsController');

router.use(authenticateToken);

router.get('/statistics', getStatistics);
router.get('/referrals', getReferralNetwork);

module.exports = router;