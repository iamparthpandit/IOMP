# 🚀 IOMP - Dynamic Homepage Guide

## ✅ What's New - Dynamic Features

### 1. **Personalized Greeting System**
- **Time-based greetings**: "Good Morning", "Good Afternoon", "Good Evening"
- **Personalized welcome**: Uses first name from user account
- **Role-specific messages**:
  - Students: "Ready to learn something new today?"
  - Staff: "Hope you have a productive day teaching!"
  - Admin: "Here's your dashboard overview"

### 2. **Events Page**
- Click "View all →" in Upcoming Events section
- Redirects to `/events` page
- Shows all 6 upcoming events with:
  - Event images
  - Date and time
  - Location
  - Registration buttons

### 3. **Dynamic User Data**
- User name displayed in sidebar
- User role badge (Student/Staff/Admin)
- Profile picture loaded from database
- User email stored and accessible

### 4. **Navigation**
- **Home** → Dashboard (/)
- **Profile** → User Profile (/profile)
- **Events** → All Events (/events)
- **Logout** → Returns to login with session cleared

---

## 🎯 How to Start the Server

### Step 1: Navigate to Project Folder
```powershell
cd C:\Users\VINIT\Desktop\IOMP_1.1\IOMP
```

### Step 2: Start the Server
```powershell
python app.py
```

### Step 3: Access the Application
Open browser and go to: **http://localhost:5000**

---

## 👥 Test Accounts (18 Users Available)

### Quick Test Users:

**Student Account:**
- Email: `john.doe@techvista.edu`
- Password: `Student@2025`
- Greeting: "Good [Time], John! 👋"

**Staff Account:**
- Email: `cs.prof@techvista.edu`
- Password: `CsProf@2025`
- Greeting: "Good [Time], Prof.! 👋"

**Admin Account:**
- Email: `admin@techvista.edu`
- Password: `Admin@2025`
- Greeting: "Good [Time], System! 👋"

### All Students:
1. Alex Kumar - `student001@techvista.edu` - Student@2025
2. Maria Garcia - `student002@techvista.edu` - Student@2025
3. David Thompson - `student003@metrotech.edu` - Student@2025
4. Sophie White - `student004@globalacademy.edu` - Student@2025
5. John Doe - `john.doe@techvista.edu` - Student@2025
6. Emma Watson - `emma.watson@techvista.edu` - Student@2025

---

## 🎨 Dynamic Features in Action

### On Login:
1. User credentials validated against database
2. JWT token generated and stored
3. User data saved to localStorage
4. Redirect to dashboard with personalized greeting

### On Dashboard:
1. **Greeting updates** based on time of day
2. **First name extracted** from full name
3. **Role-specific message** displayed
4. **User avatar** loaded from database
5. **Last login time** tracked

### On Events Click:
1. "View all →" redirects to `/events`
2. All events loaded dynamically
3. Registration buttons functional
4. Back button returns to dashboard

### On Profile Click:
1. Navigate to `/profile`
2. User data pre-filled
3. Logout button available
4. Back to dashboard option

---

## 📊 Database Updates

**Total Users**: 18
- **Admins**: 5
- **Staff**: 6
- **Students**: 7

All users have:
- Unique emails
- Hashed passwords (bcrypt)
- Profile pictures
- Role assignments
- Creation timestamps

---

## 🔧 Technical Implementation

### JavaScript Features:
- **Time-based greeting logic**
- **Dynamic DOM manipulation**
- **LocalStorage management**
- **Session persistence**
- **Role-based content**
- **Event routing**

### Pages:
- `/` - Dashboard (Dynamic Homepage)
- `/login` - Authentication
- `/profile` - User Profile
- `/events` - All Events
- `/api/auth/login` - Login API
- `/api/auth/me` - User Info API

---

## 🎬 User Flow

```
Login → Credentials Check → Token Generated → Dashboard
  ↓
Personalized Greeting Based on Time + Role
  ↓
View Events → Events Page → Register for Event
  ↓
View Profile → User Details → Logout
  ↓
Back to Login
```

---

## 🛑 Stop Server

Press **Ctrl + C** in the terminal running the server

---

## 📝 Notes

- All passwords are securely hashed with bcrypt
- Sessions persist until logout
- Real-time greeting updates on page load
- Mobile-responsive design
- Events page fully dynamic
- Database automatically created on first run

**Server Status**: ✅ Running on http://localhost:5000
