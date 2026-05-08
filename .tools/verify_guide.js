// Round-trip sanity check: extract salt/iv/ct from built guide and decrypt with creds.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const html = fs.readFileSync(path.join(__dirname, '..', 'guide', 'index.html'), 'utf8');

function pick(name) {
  const m = html.match(new RegExp("const " + name + " = '([^']+)'"));
  if (!m) throw new Error('missing ' + name);
  return m[1];
}
function pickNum(name) {
  const m = html.match(new RegExp("const " + name + " = (\\d+)"));
  return parseInt(m[1], 10);
}

const salt = Buffer.from(pick('SALT_B64'), 'base64');
const iv = Buffer.from(pick('IV_B64'), 'base64');
const ct = Buffer.from(pick('CT_B64'), 'base64');
const iter = pickNum('ITER');

const tests = [
  { user: 'yhstella', pass: 'wjddbs!0531', expect: 'pass' },
  { user: 'yhstella', pass: 'wrong', expect: 'fail' },
  { user: 'wrong', pass: 'wjddbs!0531', expect: 'fail' },
];

for (const t of tests) {
  try {
    const key = crypto.pbkdf2Sync(`${t.user}:${t.pass}`, salt, iter, 32, 'sha256');
    const tag = ct.slice(ct.length - 16);
    const body = ct.slice(0, ct.length - 16);
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(tag);
    const plain = Buffer.concat([decipher.update(body), decipher.final()]).toString('utf8');
    const ok = plain.startsWith('OK\n');
    console.log(`[${t.expect === 'pass' ? 'OK' : 'FAIL'}] ${t.user}/${t.pass}: decrypted=${ok}, len=${plain.length}`);
    if (t.expect === 'fail') console.log('  ❌ should have failed');
  } catch (e) {
    console.log(`[${t.expect === 'fail' ? 'OK' : 'FAIL'}] ${t.user}/${t.pass}: ${e.message}`);
    if (t.expect === 'pass') console.log('  ❌ should have passed');
  }
}
