// =========================
// Show Current Time
// =========================

function getCurrentTime() {

    const now = new Date();

    return now.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

}

document.getElementById("welcome-time").innerText = getCurrentTime();


// =========================
// Suggested Question
// =========================

function askSuggestion(question) {

    document.getElementById("user-input").value = question;

    sendMessage();

}


// =========================
// Send Message
// =========================

async function sendMessage() {

    const input = document.getElementById("user-input");

    const chatBox = document.getElementById("chat-box");

    const message = input.value.trim();

    if (message === "") return;

    // ----------------------
    // User Message
    // ----------------------

    chatBox.innerHTML += `
    
    <div class="user-message">

        <div class="bubble">

            ${message}

            <div class="time">${getCurrentTime()}</div>

        </div>

    </div>

    `;

    input.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;


    // ----------------------
    // Typing Animation
    // ----------------------

    chatBox.innerHTML += `

    <div class="bot-message typing-message" id="typing">

        <div class="avatar">
            🤖
        </div>

        <div class="typing-bubble">

            <div class="typing">

                <span></span>
                <span></span>
                <span></span>

            </div>

        </div>

    </div>

    `;

    chatBox.scrollTop = chatBox.scrollHeight;


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        // Keep typing animation visible

        await new Promise(resolve => setTimeout(resolve, 900));

        document.getElementById("typing").remove();

        // ----------------------
        // Bot Message
        // ----------------------

        chatBox.innerHTML += `

        <div class="bot-message">

            <div class="avatar">
                🤖
            </div>

            <div class="bubble">

                ${data.reply}

                <div class="time">${getCurrentTime()}</div>

            </div>

        </div>

        `;

    }

    catch (error) {

        document.getElementById("typing").remove();

        chatBox.innerHTML += `

        <div class="bot-message">

            <div class="avatar">
                🤖
            </div>

            <div class="bubble">

                Something went wrong.

                <div class="time">${getCurrentTime()}</div>

            </div>

        </div>

        `;

    }

    chatBox.scrollTop = chatBox.scrollHeight;

}


// =========================
// Enter Key
// =========================

document.getElementById("user-input").addEventListener("keypress", function (event) {

    if (event.key === "Enter") {

        sendMessage();

    }

});