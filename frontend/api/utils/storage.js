// Simple file-based storage for Vercel
import fs from 'fs';
import path from 'path';

const STORAGE_DIR = '/tmp';
const USERS_FILE = path.join(STORAGE_DIR, 'users.json');

// Ensure storage directory exists
if (!fs.existsSync(STORAGE_DIR)) {
  fs.mkdirSync(STORAGE_DIR, { recursive: true });
}

export function getUsers() {
  try {
    if (fs.existsSync(USERS_FILE)) {
      const data = fs.readFileSync(USERS_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('Error reading users file:', error);
  }
  return [];
}

export function saveUsers(users) {
  try {
    fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2));
    return true;
  } catch (error) {
    console.error('Error saving users file:', error);
    return false;
  }
}

export function addUser(userData) {
  const users = getUsers();
  users.push(userData);
  return saveUsers(users);
}

export function findUser(email) {
  const users = getUsers();
  return users.find(user => user.email === email);
}