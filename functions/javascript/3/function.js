//function/javascript/3/function.js

function handler(event) {
    const name = event.name || "world";
    return `Hi there, ${name}!`;
}

module.exports = { handler };
