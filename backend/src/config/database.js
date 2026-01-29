const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const DB_PATH = path.join(__dirname, '../../database.sqlite');

const db = new sqlite3.Database(DB_PATH, (err) => {
  if (err) {
    console.error('❌ Error connecting to database:', err);
  } else {
    console.log('✅ Connected to SQLite database');
  }
});

// Initialize tables
const initDatabase = () => {
  return new Promise((resolve, reject) => {
    db.serialize(() => {
      // Users table
      db.run(`
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          email TEXT UNIQUE NOT NULL,
          password TEXT NOT NULL,
          name TEXT NOT NULL,
          role TEXT DEFAULT 'recruiter',
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
      `);

      // Candidates table
      db.run(`
        CREATE TABLE IF NOT EXISTS candidates (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT UNIQUE NOT NULL,
          phone TEXT,
          college TEXT,
          degree TEXT,
          graduation_year INTEGER,
          cgpa REAL,
          skills TEXT,
          projects TEXT,
          experience TEXT,
          resume_path TEXT,
          ai_score REAL DEFAULT 0,
          status TEXT DEFAULT 'pending',
          referred_by TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
      `);

      // Referrals table
      db.run(`
        CREATE TABLE IF NOT EXISTS referrals (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          referrer_name TEXT NOT NULL,
          referrer_email TEXT,
          total_referrals INTEGER DEFAULT 1,
          successful_hires INTEGER DEFAULT 0,
          conversion_rate REAL DEFAULT 0,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
      `);

      // Insert demo user (password: demo123)
      db.run(`
        INSERT OR IGNORE INTO users (email, password, name, role)
        VALUES ('recruiter@company.com', '$2a$10$xQJYv0qC5FYr6YO.WdHQDeZNGJgXqHXzKGKkVvN6QYxYnHZKZH7.C', 'Demo Recruiter', 'admin')
      `, (err) => {
        if (err) reject(err);
        else {
          console.log('✅ Database initialized successfully');
          resolve();
        }
      });
    });
  });
};

// Helper functions
const dbAll = (query, params = []) => {
  return new Promise((resolve, reject) => {
    db.all(query, params, (err, rows) => {
      if (err) reject(err);
      else resolve(rows);
    });
  });
};

const dbGet = (query, params = []) => {
  return new Promise((resolve, reject) => {
    db.get(query, params, (err, row) => {
      if (err) reject(err);
      else resolve(row);
    });
  });
};

const dbRun = (query, params = []) => {
  return new Promise((resolve, reject) => {
    db.run(query, params, function(err) {
      if (err) reject(err);
      else resolve({ id: this.lastID, changes: this.changes });
    });
  });
};

module.exports = { db, dbAll, dbGet, dbRun, initDatabase };