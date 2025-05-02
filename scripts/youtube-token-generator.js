const generateToken = require('youtube-po-token-generator');

(async () => {
  try {
    const token = await generateToken();
    console.log(JSON.stringify(token));
  } catch (err) {
    console.error("Token error:", err);
    process.exit(1);
  }
})();
