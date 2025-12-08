const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'Please provide a name'],
        trim: true
    },
    email: {
        type: String,
        required: [true, 'Please provide an email'],
        unique: true,
        lowercase: true,
        match: [/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/, 'Please provide a valid email']
    },
    password: {
        type: String,
        required: [true, 'Please provide a password'],
        minlength: 6,
        select: false
    },
    role: {
        type: String,
        enum: ['student', 'teacher', 'admin'],
        default: 'student'
    },
    profilePicture: {
        type: String,
        default: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDJ7alwZ4VtU9QjSG7VKafpieuWwNgPDgp2Y4KxAjlKwzhLF9QwtgPuE_RxEueIXjzAiJU3DrN2mg8myDX5Rfxgw2ifFs1p5OCij9LY2ZGhTKIh0kYMHHC3Mtg1ufz4cR_l1c73jMMIalIAWIrN_SQWZVBn-C9kHQB0yE-qHi9Fo1cK2mGRyJk9nbq4IFvGPJGk4WnaxiN08atgc4Ee_rrBwEKGkl90Fub5d2GJsgmGbs3F0VpIEi4oxFCGFJO761a2Q4R5x811WzyZ'
    },
    createdAt: {
        type: Date,
        default: Date.now
    }
});

// Hash password before saving
userSchema.pre('save', async function(next) {
    if (!this.isModified('password')) {
        return next();
    }
    
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
});

// Compare password method
userSchema.methods.comparePassword = async function(candidatePassword) {
    return await bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
