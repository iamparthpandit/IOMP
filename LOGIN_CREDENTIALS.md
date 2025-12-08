# IOMP Login Credentials

## ✅ Database Updated Successfully!

All users have been imported with new credentials from the CSV file.

---

## 📋 LOGIN CREDENTIALS

### 📌 ADMIN USERS

| Email | Password | Name |
|-------|----------|------|
| principal@techvista.edu | Principal@2025 | Dr. Sarah Johnson |
| director@metrotech.edu | Director@2025 | Dr. James Wilson |
| training.head@futurecorp.com | Training@2025 | Robert Brown |
| head.teacher@globalacademy.edu | HeadTeach@2025 | Mrs. Rachel Green |

### 👨‍🏫 STAFF USERS

| Email | Password | Name |
|-------|----------|------|
| cs.prof@techvista.edu | CsProf@2025 | Prof. Michael Chen |
| math.teacher@techvista.edu | MathTeach@2025 | Mrs. Emily Rodriguez |
| eng.prof@metrotech.edu | EngProf@2025 | Dr. Lisa Park |
| trainer@futurecorp.com | Trainer@2025 | Jennifer Davis |
| primary.teacher@globalacademy.edu | Primary@2025 | Mr. Tom Anderson |

### 🎓 STUDENT USERS

| Email | Password | Name |
|-------|----------|------|
| student001@techvista.edu | Student@2025 | Alex Kumar |
| student002@techvista.edu | Student@2025 | Maria Garcia |
| student003@metrotech.edu | Student@2025 | David Thompson |
| employee001@futurecorp.com | Employee@2025 | Kevin Lee |
| student004@globalacademy.edu | Student@2025 | Sophie White |

---

## 🚀 How to Login

1. Open: http://localhost:5000/login
2. Enter any email from the table above
3. Enter the corresponding password
4. Click "Continue"

---

## 📝 Quick Test Examples

**Test as Admin:**
- Email: `principal@techvista.edu`
- Password: `Principal@2025`

**Test as Staff:**
- Email: `cs.prof@techvista.edu`
- Password: `CsProf@2025`

**Test as Student:**
- Email: `student001@techvista.edu`
- Password: `Student@2025`

---

## ⚙️ Technical Details

- Total Users: 14
- Roles: Admin (4), Staff (5), Student (5)
- All passwords are properly hashed using bcrypt
- JWT tokens valid for 7 days
- Login endpoint: `/api/auth/login`
- Protected dashboard: `/` (requires authentication)

---

## 🔒 Security Features

✅ Passwords hashed with bcrypt
✅ JWT token-based authentication
✅ Protected routes require valid token
✅ Automatic redirect to login if not authenticated
✅ Session persistence with localStorage
✅ Logout clears all session data
