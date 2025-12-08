# Profile Dropdown Menu - Implementation Guide

## Overview
A dynamic profile dropdown menu has been added to all pages (index.html, profile.html, events.html) that appears when users click on their profile picture in the header.

## Features Implemented

### 1. **Visual Design**
- Dark theme (#2d3748 background) matching Chrome's profile menu
- Smooth slide-down animation with opacity transition
- Rounded corners and professional shadow effects
- Responsive design that works on all screen sizes

### 2. **User Information Display**
- **Large Profile Avatar** (80px circular image)
- **User Name** (dynamically loaded from localStorage)
- **Email Address** (dynamically loaded from localStorage)

### 3. **Menu Options**

#### Main Section
- 🔑 **Profile Settings** - Navigates to /profile page
- 🌐 **Manage your Account** - Placeholder for account management
- ✏️ **Customise Profile** - Navigates to /profile page
- 🔄 **Sync is on** - Shows sync status (green icon)

#### Other Profiles Section
- Lists other available profiles (Admin, Staff, etc.)
- Each profile shows name, email, and avatar
- Click to switch profiles (coming soon functionality)
- **Add Profile** button - Placeholder for adding new profiles
- **Open Guest Profile** button - Placeholder for guest mode

#### Sign Out Section
- 🚪 **Sign out** button (red color for emphasis)
- Confirmation dialog before logout
- Clears all localStorage data (token, user, lastLoginTime)
- Redirects to /login page

## Technical Implementation

### CSS Classes
```css
.profile-dropdown - Main dropdown container
.profile-dropdown.active - Visible state
.profile-dropdown-header - Top section with avatar and user info
.profile-dropdown-section - Grouped menu items
.profile-dropdown-item - Individual menu option
.profile-avatar-large - 80px circular avatar
```

### JavaScript Functions

#### Toggle Dropdown
```javascript
headerAvatar.addEventListener('click', (e) => {
  e.stopPropagation();
  profileDropdown.classList.toggle('active');
  // Populate with user data from localStorage
});
```

#### Close on Outside Click
```javascript
document.addEventListener('click', (e) => {
  if (!profileDropdown.contains(e.target) && e.target !== headerAvatar) {
    profileDropdown.classList.remove('active');
  }
});
```

#### Load Other Profiles
```javascript
function loadOtherProfiles(currentUser) {
  // Fetches profiles excluding current user
  // Displays with avatar, name, and email
}
```

#### Logout Functionality
```javascript
dropdownLogout.addEventListener('click', () => {
  if (confirm('Are you sure you want to sign out?')) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('lastLoginTime');
    window.location.href = '/login';
  }
});
```

## Data Flow

### 1. User Data Loading
```javascript
const userData = localStorage.getItem('user');
const user = JSON.parse(userData);
```

### 2. Dropdown Population
- Avatar: `user.profile_picture`
- Name: `user.name`
- Email: `user.email`

### 3. Other Profiles
- Hardcoded sample data (Admin, Staff)
- Filtered to exclude current user
- Can be replaced with API call for real data

## Files Modified

### 1. `index.html`
- Added profile dropdown CSS styles
- Wrapped header avatar in relative div
- Added dropdown HTML structure
- Added JavaScript for dropdown functionality

### 2. `profile.html`
- Same dropdown implementation as index.html
- Integrated with existing profile page
- Font Awesome icons added for consistency

### 3. `events.html`
- Same dropdown implementation
- Seamless integration with events page
- Consistent user experience across all pages

## User Experience

### Opening Dropdown
1. User clicks profile picture in top-right corner
2. Dropdown slides down with smooth animation
3. User data automatically loads from localStorage
4. Other profiles section populates dynamically

### Closing Dropdown
1. Click outside dropdown area
2. Click profile picture again
3. Click any navigation option
4. Click Sign out

### Navigation Flow
```
Profile Picture Click → Dropdown Opens
├── Profile Settings → /profile page
├── Customise Profile → /profile page
├── Other Profile → Switch profile (coming soon)
└── Sign out → Confirmation → /login
```

## Customization Options

### Change Colors
```css
.profile-dropdown {
  background: #2d3748; /* Change background color */
  color: white; /* Change text color */
}
```

### Modify Animation Speed
```css
.profile-dropdown {
  transition: all 0.3s ease; /* Change 0.3s to desired duration */
}
```

### Add More Menu Items
```html
<div class="profile-dropdown-item" onclick="yourFunction()">
  <i class="fas fa-icon text-gray-300 text-lg"></i>
  <span>Menu Item Name</span>
</div>
```

## Future Enhancements

### Planned Features
1. **Profile Switching** - Actually switch between different user accounts
2. **Account Management** - Full account settings page
3. **Guest Mode** - Anonymous browsing capability
4. **API Integration** - Fetch other profiles from database
5. **User Preferences** - Save dropdown preferences
6. **Keyboard Navigation** - Arrow keys and Enter support
7. **Notifications** - Show unread notifications count

### API Integration Example
```javascript
async function loadOtherProfiles(currentUser) {
  const response = await fetch('/api/users/profiles');
  const profiles = await response.json();
  // Filter and display profiles
}
```

## Browser Compatibility
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Testing Checklist
- [ ] Dropdown opens on avatar click
- [ ] Dropdown closes on outside click
- [ ] User data loads correctly
- [ ] Navigation links work
- [ ] Logout confirmation works
- [ ] Mobile responsiveness
- [ ] Animation is smooth
- [ ] Icons display properly
- [ ] Other profiles section loads
- [ ] Dropdown closes after navigation

## Troubleshooting

### Dropdown Not Opening
- Check if Font Awesome is loaded
- Verify JavaScript console for errors
- Ensure localStorage has user data

### User Data Not Showing
- Check if user data exists in localStorage
- Verify JSON parsing is successful
- Check avatar URL validity

### Styling Issues
- Ensure CSS is properly loaded
- Check for conflicting styles
- Verify z-index is high enough (1000)

## Credits
Inspired by Chrome browser's profile menu design
Implemented with Tailwind CSS and vanilla JavaScript
Icons from Font Awesome 6.5.1
