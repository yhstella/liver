// Encrypt guide_content.html with username:password using PBKDF2-SHA256 + AES-256-GCM,
// then wrap with login form + Web Crypto decryption client.
// Usage: node .tools/build_guide.js
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const PLAIN = path.join(ROOT, '.tools', 'guide_content.html');
const TEMPLATE = path.join(ROOT, '.tools', 'guide_template.html');
const OUT = path.join(ROOT, 'guide', 'index.html');

// Credentials are NOT committed to repo — supplied via env or hardcoded here only at build time.
// The OUTPUT (guide/index.html) does not contain plaintext credentials, only the encrypted blob.
const USERNAME = process.env.GUIDE_USER || 'yhstella';
const PASSWORD = process.env.GUIDE_PASS || 'wjddbs!0531';

const PBKDF2_ITERATIONS = 250000;
const SALT_BYTES = 16;
const IV_BYTES = 12;
const KEY_BYTES = 32;

function encrypt(plaintext, user, pass) {
  const salt = crypto.randomBytes(SALT_BYTES);
  const iv = crypto.randomBytes(IV_BYTES);
  const material = `${user}:${pass}`;
  const key = crypto.pbkdf2Sync(material, salt, PBKDF2_ITERATIONS, KEY_BYTES, 'sha256');

  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  // Add a magic prefix so decryption client can verify success even before parsing
  const data = Buffer.concat([Buffer.from('OK\n', 'utf8'), Buffer.from(plaintext, 'utf8')]);
  const ciphertext = Buffer.concat([cipher.update(data), cipher.final()]);
  const authTag = cipher.getAuthTag();

  return {
    salt: salt.toString('base64'),
    iv: iv.toString('base64'),
    ct: Buffer.concat([ciphertext, authTag]).toString('base64'),
    iter: PBKDF2_ITERATIONS,
  };
}

const plaintext = fs.readFileSync(PLAIN, 'utf8');
const blob = encrypt(plaintext, USERNAME, PASSWORD);

const template = fs.readFileSync(TEMPLATE, 'utf8');
const output = template
  .replace('__SALT__', blob.salt)
  .replace('__IV__', blob.iv)
  .replace('__CT__', blob.ct)
  .replace('__ITER__', String(blob.iter));

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, output, 'utf8');
console.log(`Wrote ${OUT}`);
console.log(`Plaintext: ${plaintext.length} bytes → Ciphertext: ${blob.ct.length} bytes (base64)`);
