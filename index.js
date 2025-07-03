const https = require("https");
const secret = "X7k9PqLm2vNxZwYa4jRtUv8sBcDeFgHi";
const payload = JSON.stringify({
  ref: "refs/heads/main",
  before: "ab2b5e260b5e46661f75bd76027863f10efa9b57",
  after: "5695e1359ea87ad456c54eb3ce36a2ae403a59fe",
  repository: { name: "action-webhook-repo", owner: { login: "ShovitDutta" } },
  pusher: { name: "ShovitDutta" },
  head_commit: {
    id: "5695e1359ea87ad456c54eb3ce36a2ae403a59fe",
    message: "Test commit",
    timestamp: "2025-07-03T07:16:00Z",
  },
});
const signature =
  "sha256=" +
  require("crypto").createHmac("sha256", secret).update(payload).digest("hex");
const options = {
  hostname: "webhook-repo-iipe.onrender.com",
  path: "/webhook",
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-GitHub-Event": "push",
    "X-Hub-Signature-256": signature,
    "User-Agent": "Node.js-Webhook-Test",
  },
};
const req = https.request(options, (res) => {
  console.log(`Status: ${res.statusCode}`);
  res.on("data", (d) => {
    process.stdout.write(d);
  });
});
req.on("error", (e) => {
  console.error(`Problem with request: ${e.message}`);
});
req.write(payload);
req.end();
