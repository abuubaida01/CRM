/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'backend/core/templates/core/*.html',
    'backend/client/templates/client/*.html',
    'backend/dashboard/templates/dashboard/*.html',
    'backend/lead/templates/lead/*.html',
    'backend/team/templates/team/*.html',
    'backend/userprofile/templates/userprofile/*.html',
  ],
  
  theme: {
    extend: {},
  },
  plugins: [],
}

