let currentMonth = new Date();

function renderCalendar() {
  const year = currentMonth.getFullYear();
  const month = currentMonth.getMonth();
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const calendar = document.getElementById('calendar');
  calendar.innerHTML = '';
  
  // Update month display
  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  document.getElementById('currentMonthDisplay').textContent = `${monthNames[month]} ${year}`;

  // Empty cells for days before start of month
  for (let i = 0; i < firstDay; i++) {
    const emptyCell = document.createElement('div');
    emptyCell.className = 'bg-gray-50 border-b border-r border-gray-200';
    calendar.appendChild(emptyCell);
  }

  // Days
  for (let day = 1; day <= daysInMonth; day++) {
    const cell = document.createElement('div');
    cell.className = 'calendar-day bg-white p-2 hover:bg-gray-50 cursor-pointer relative flex flex-col gap-1';
    
    // Check if today
    const today = new Date();
    const isToday = day === today.getDate() && month === today.getMonth() && year === today.getFullYear();
    
    cell.innerHTML = `
      <div class="flex justify-between items-start">
        <span class="text-sm font-semibold ${isToday ? 'bg-iomp-blue-light text-white w-6 h-6 flex items-center justify-center rounded-full' : 'text-gray-700'}">${day}</span>
      </div>
      <div id="day-${year}-${month + 1}-${day}" class="flex flex-col gap-1 overflow-y-auto max-h-[80px]"></div>
    `;
    
    cell.onclick = (e) => {
      // Don't open modal if clicking on an event
      if (e.target.closest('.event-item')) return;
      openModal(`${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`);
    };
    
    calendar.appendChild(cell);
  }

  loadEvents();
}

function changeMonth(offset) {
  currentMonth.setMonth(currentMonth.getMonth() + offset);
  renderCalendar();
}

async function loadEvents() {
  try {
    const token = localStorage.getItem('token');
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    
    const res = await fetch('/api/events', { headers });
    const data = await res.json();
    
    if (data.success) {
      data.events.forEach(e => {
        const date = new Date(e.date);
        // Check if event is in current month view
        if (date.getMonth() === currentMonth.getMonth() && date.getFullYear() === currentMonth.getFullYear()) {
          const dayEl = document.getElementById(`day-${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`);
          if (dayEl) {
            const eventItem = document.createElement('div');
            eventItem.className = 'event-item text-xs p-1 rounded bg-blue-100 text-blue-800 truncate border-l-2 border-blue-500 mb-1';
            eventItem.textContent = e.title;
            eventItem.title = e.title;
            dayEl.appendChild(eventItem);
          }
        }
      });
    }
  } catch (error) {
    console.error('Error loading events:', error);
  }
}

function openModal(date = '') {
  document.getElementById('modal').classList.remove('hidden');
  if (date) document.getElementById('date').value = date;
}

function closeModal() {
  document.getElementById('modal').classList.add('hidden');
}

async function saveEvent() {
  const title = document.getElementById('title').value;
  const dateVal = document.getElementById('date').value;
  const timeVal = document.getElementById('time').value || '00:00';
  const location = document.getElementById('location').value;
  
  if (!title || !dateVal) {
    alert('Please fill in title and date');
    return;
  }

  const dateTime = new Date(`${dateVal}T${timeVal}`).toISOString();

  const data = {
    title: title,
    date: dateTime,
    location: location,
    description: ''
  };

  try {
    const token = localStorage.getItem('token');
    if (!token) {
      alert('Please login to add events');
      return;
    }

    const res = await fetch('/api/events', { 
      method: 'POST', 
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }, 
      body: JSON.stringify(data) 
    });
    
    const result = await res.json();
    
    if (result.success) {
      closeModal();
      renderCalendar();
      // Clear inputs
      document.getElementById('title').value = '';
      document.getElementById('location').value = '';
    } else {
      alert(result.message || 'Failed to save event');
    }
  } catch (error) {
    console.error('Error saving event:', error);
    alert('An error occurred');
  }
}

// Initial render
renderCalendar();