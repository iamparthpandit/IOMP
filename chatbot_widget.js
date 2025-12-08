(function() {
    // HTML Template
    const chatHTML = `
    <!-- Bottom-right hover button -->
    <div id="chatTrigger" class="fixed bottom-5 right-5 w-14 h-14 bg-blue-600 text-white rounded-full flex items-center justify-center cursor-pointer shadow-lg hover:bg-blue-700 transition z-50">
      <i class="fas fa-comment"></i>
    </div>

    <!-- Chat panel -->
    <div id="chatPanel" class="fixed bottom-20 right-5 w-80 h-96 bg-white rounded-lg shadow-2xl hidden flex flex-col z-50 border border-gray-200">
      <div class="flex justify-between items-center p-3 border-b bg-blue-600 text-white rounded-t-lg">
        <span class="font-semibold text-sm">IOMP Assistant</span>
        <button id="closeChatBtn" class="text-white hover:text-gray-200 text-xl">&times;</button>
      </div>

      <div id="chatBox" class="flex-1 overflow-y-auto p-3 space-y-2 text-sm bg-gray-50"></div>

      <form id="chatForm" class="p-3 border-t flex gap-2 bg-white rounded-b-lg">
        <input id="chatInput" required class="flex-1 px-2 py-1 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Ask anything…">
        <button type="submit" class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition">Send</button>
      </form>
    </div>
    `;

    // Inject HTML
    const div = document.createElement('div');
    div.innerHTML = chatHTML;
    document.body.appendChild(div);

    // Logic
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const token = localStorage.getItem('token');
    let visible = false;

    const chatTrigger = document.getElementById('chatTrigger');
    const chatPanel = document.getElementById('chatPanel');
    const closeChatBtn = document.getElementById('closeChatBtn');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatBox = document.getElementById('chatBox');

    function toggleChat() {
        visible = !visible;
        chatPanel.classList.toggle('hidden', !visible);
        chatPanel.classList.toggle('flex', visible);
    }

    chatTrigger.onclick = toggleChat;
    closeChatBtn.onclick = toggleChat;

    function addBubble(text, sender) {
        const div = document.createElement('div');
        div.className = sender === 'user' ? 'text-right' : 'text-left';
        div.innerHTML = `<span class="inline-block px-3 py-2 rounded-lg max-w-[80%] ${sender === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-black'}">${text}</span>`;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    chatForm.onsubmit = async (e) => {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (!msg) return;

        addBubble(msg, 'user');
        chatInput.value = '';

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    message: msg, 
                    role: user.role || 'student', 
                    name: user.name || 'User'
                })
            });
            
            if (res.status === 401) {
                addBubble("Please log in to use the chat.", 'bot');
                return;
            }

            const data = await res.json();
            addBubble(data.reply || "No response received.", 'bot');
        } catch (err) {
            console.error(err);
            addBubble("Error connecting to server.", 'bot');
        }
    };
})();
