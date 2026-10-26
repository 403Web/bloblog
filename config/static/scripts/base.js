document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    const body = document.body;

    const savedTheme = localStorage.getItem('theme') || 'light';
    
    body.setAttribute('data-bs-theme', savedTheme);
    body.setAttribute('data-bs-theme', savedTheme);
    toggle.checked = savedTheme === 'dark';

    toggle.addEventListener('change', function () {
        const theme = this.checked ? 'dark' : 'light';
        
        body.setAttribute('data-bs-theme', theme);
        body.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        
        console.log('current theme:', theme);
    });
});
