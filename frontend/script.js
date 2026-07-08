class Calculator {
    constructor(previousOperandTextElement, currentOperandTextElement) {
        this.previousOperandTextElement = previousOperandTextElement;
        this.currentOperandTextElement = currentOperandTextElement;
        this.clear();
    }

    clear() {
        this.currentOperand = '0';
        this.previousOperand = '';
        this.operation = undefined;
    }

    delete() {
        this.currentOperand = this.currentOperand.toString().slice(0, -1);
        if (this.currentOperand === '') {
            this.currentOperand = '0';
        }
    }

    appendNumber(number) {
        if (number === '.' && this.currentOperand.includes('.')) return;
        if (this.currentOperand === '0' && number !== '.') {
            this.currentOperand = number;
        } else {
            this.currentOperand = this.currentOperand.toString() + number.toString();
        }
    }

    chooseOperation(operation) {
        if (this.currentOperand === '0' && this.previousOperand === '') return;
        if (this.previousOperand !== '') {
            this.compute();
        }
        this.operation = operation;
        this.previousOperand = this.currentOperand;
        this.currentOperand = '0';
    }

    compute() {
        let computation;
        const prev = parseFloat(this.previousOperand);
        const current = parseFloat(this.currentOperand);

        if (isNaN(prev)) return;
        const expression = `${this.previousOperand} ${this.operation} ${this.currentOperand}`;

        switch (this.operation) {
            case '+':
                computation = prev + current;
                break;
            case '-':
                computation = prev - current;
                break;
            case '×':
                computation = prev * current;
                break;
            case '÷':
                computation = current === 0 ? NaN : prev / current;
                break;
            case '%':
                computation = prev % current;
                break;
            default:
                return;
        }
        saveCalculation(expression, computation);
        this.currentOperand = computation.toString();
        this.operation = undefined;
        this.previousOperand = '';
    }

    calculatePercentage() {
        const current = parseFloat(this.currentOperand);
        if (isNaN(current)) return;
        this.currentOperand = (current / 100).toString();
    }

    updateDisplay() {
        this.currentOperandTextElement.innerText = this.currentOperand;
        if (this.operation != null) {
            this.previousOperandTextElement.innerText =
                `${this.previousOperand} ${this.operation}`;
        } else {
            this.previousOperandTextElement.innerText = '';
        }
    }
}

const previousOperandTextElement = document.querySelector('[data-previous-operand]');
const currentOperandTextElement = document.querySelector('[data-current-operand]');
const calculator = new Calculator(previousOperandTextElement, currentOperandTextElement);

document.querySelectorAll('[data-number]').forEach(button => {
    button.addEventListener('click', () => {
        calculator.appendNumber(button.innerText);
        calculator.updateDisplay();
    });
});

document.querySelectorAll('[data-operation]').forEach(button => {
    button.addEventListener('click', () => {
        calculator.chooseOperation(button.innerText);
        calculator.updateDisplay();
    });
});

document.querySelector('[data-equals]').addEventListener('click', async () => {
    calculator.compute();
    calculator.updateDisplay();
    await history_data();
});

document.querySelector('[data-all-clear]').addEventListener('click', () => {
    calculator.clear();
    calculator.updateDisplay();
});

document.querySelector('[data-delete]').addEventListener('click', () => {
    calculator.delete();
    calculator.updateDisplay();
});

document.querySelector('[data-percent]').addEventListener('click', () => {
    calculator.calculatePercentage();
    calculator.updateDisplay();
});

document.addEventListener('keydown', event => {
    if (/[0-9]/.test(event.key)) {
        event.preventDefault();
        calculator.appendNumber(event.key);
        calculator.updateDisplay();
    } else if (event.key === '.') {
        event.preventDefault();
        calculator.appendNumber('.');
        calculator.updateDisplay();
    } else if (event.key === '+' || event.key === '-' || event.key === '*') {
        event.preventDefault();
        let op = event.key;
        if (event.key === '*') op = '×';
        calculator.chooseOperation(op);
        calculator.updateDisplay();
    } else if (event.key === '/') {
        event.preventDefault();
        calculator.chooseOperation('÷');
        calculator.updateDisplay();
    } else if (event.key === '%') {
        event.preventDefault();
        calculator.calculatePercentage();
        calculator.updateDisplay();
    } else if (event.key === 'Enter' || event.key === '=') {
        event.preventDefault();
        calculator.compute();
        calculator.updateDisplay();
    } else if (event.key === 'Escape') {
        event.preventDefault();
        calculator.clear();
        calculator.updateDisplay();
    } else if (event.key === 'Backspace') {
        event.preventDefault();
        calculator.delete();
        calculator.updateDisplay();
    }
});

async function history_data() {
    // Load history from the backend and render it into the history panel.
    try {
        const response = await fetch("http://127.0.0.1:8000/history");
        const history = await response.json();
        const historyContainer = document.getElementById("history");
        historyContainer.innerHTML = "";
        history.forEach(item => {
            historyContainer.innerHTML += `
<div class="history-item">
    <span>${item.expression} = ${item.result}</span>
    <button onclick="delete_history(${item.id})">🗑</button>
</div>`;
        });
    } catch (error) {
        console.error("Could not load history:", error);
    }
}

async function delete_history(id) {
    try {
        await fetch(`http://127.0.0.1:8000/history/${id}`, {
            method: "DELETE"
        });
        await history_data();
    } catch (error) {
        console.error("Could not delete history item:", error);
    }
}

async function saveCalculation(expression, result) {
    try {
        const response = await fetch("http://127.0.0.1:8000/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                expression: expression,
                result: result
            })
        });

        await response.json();
        await history_data();
    } catch (error) {
        console.error("Could not save calculation:", error);
    }
}

// fetch() sends an HTTP request and returns a promise (a receipt, not the data itself).
// async/await let this code pause at each request until the backend responds.

// Load any existing history as soon as the page opens.
window.addEventListener('load', () => {
    history_data();
});