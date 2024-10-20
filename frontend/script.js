document.getElementById('create-rule-btn').addEventListener('click', createRule);
document.getElementById('combine-rules-btn').addEventListener('click', combineRules);
document.getElementById('evaluate-btn').addEventListener('click', evaluateRule);

async function createRule() {
    const rule = document.getElementById('rule-input').value;
    if (!rule) return alert('Please enter a rule.');
    console.log(rule,"rulerulerule")
    const response = await fetch('http://127.0.0.1:5000/create-rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "rule_string":rule }),
    });

    const result = await response.json();
    document.getElementById('rule-output').textContent = JSON.stringify(result, null, 2);
}

async function combineRules() {
    const rules = document.getElementById('combine-rules-input').value.split(',').map(rule => rule.trim());
    if (rules.length === 0) return alert('Please enter some rules.');

    const response = await fetch('http://127.0.0.1:5000/combine-rules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rules }),
    });

    const result = await response.json();
    document.getElementById('combined-output').textContent = JSON.stringify(result, null, 2);
}

async function evaluateRule() {
    const userData = document.getElementById('evaluate-input').value;
    if (!userData) return alert('Please enter user data.');

    try {
        const userJson = JSON.parse(userData);
        const response = await fetch('http://127.0.0.1:5000/evaluate-rule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user: userJson }),
        });

        const result = await response.json();
        document.getElementById('evaluate-output').textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        alert('Invalid user data format.');
    }
}
