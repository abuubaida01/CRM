# CRM Project with Django 🚀

## Overview

Welcome to the CRM project built with Django! This project serves as a comprehensive Customer Relationship Management (CRM) system. It's designed to facilitate team collaboration, lead and client management, and more.

### Apps Breakdown

1. **CRM (Main) 🌐**
   - Central module with critical configurations in `settings.py` for static and media files.
   - Customized context processors for enhanced functionality.

2. **UserProfile 👤**
   - Utilizes and customizes methods/forms from `contrib.auth.models` for user account creation, sign-in, and sign-out.
   - Userprofile functionality to track users with active team details.

3. **Client 🤝**
   - Three models: `Client` for creating team-specific clients, `ClientFile` for file tracking, and `Comment` for client comments.

4. **Lead 🎯**
   - Three models: `Lead` for managing team-specific leads with priorities and statuses, `LeadFile` for file tracking, and `Comment` for lead comments.

5. **Team 🏢**
   - Two models: `Plan` for defining team usage of Clients and leads, and `Team` for creating teams with specific plans.

6. **Core 🔧**
   - Basic app for rendering index, about, and base HTML files.

7. **Dashboard 📊**
   - Basic app for rendering a dashboard with team-specific client and lead information.

---

## Project Functionality

- Users can create teams, add members, and collaboratively manage leads and clients.
- Flexibility to switch clients to leads and vice versa.
- Editing and deleting capabilities for clients and leads.
- User-friendly dashboard displaying team-specific information.
- and many other...

---

## Project Purpose 🎓

This project was created for learning purposes, following a comprehensive tutorial playlist available at [YouTube Playlist](youtube.com/playlist?list=PLpyspNLjzwBka94O3ABYcRYk8IaBR8hXZ). The code has been independently crafted without copy-pasting.

---

## Future Vision 🔮

1. **Team Management 🤝**
   - Define roles and permissions within teams.

2. **Team Creation 🚀**
   - Allow users to create and remove teams.

3. **Communication Features 💬**
   - Integrate real-time chat for seamless team communication.

4. **Payment Integration 💳**
   - Implement payment methods and plan extensions.

---

## Contribution

Contributions are welcome! Feel free to explore, contribute, and make this CRM project your own! Happy coding! 🚀🌐

---

