// docker/javascript/entrypoint.js

const fs = require("fs");

(async () => {
  const event = JSON.parse(fs.readFileSync("/tmp/input.json", "utf8"));
  const { handler } = require("/function/function.js");
  const output = await handler(event);
  console.log(JSON.stringify(output));
})();
