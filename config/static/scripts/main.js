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

const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const appendAlert = (message, type) => {
const wrapper = document.createElement('div')
wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
].join('')

alertPlaceholder.append(wrapper)
}

const alertTrigger = document.getElementById('liveAlertBtn')
if (alertTrigger) {
alertTrigger.addEventListener('click', () => {
    appendAlert('You have logged out successfully!', 'success')
})
}

let newText = 'Log In'
let newIconClass = 'bi-box-arrow-in-right'


let saveIcon = document.querySelector('#logouticon')
let saveText = document.querySelector('#logouttext')

let logoutbtn = document.querySelector('#logoutbtn')
let confirmBtn = document.querySelector('#liveAlertBtn')

confirmBtn.addEventListener('click', function(){
    saveText.textContent = newText
    saveIcon.className = newIconClass
})
