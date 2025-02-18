
window.onload = function () {
    if (!sessionStorage.getItem("logged_in")) {
        window.location.href = "/login";
    }
};
// Sidebar toggle functionality for small screens
const sidebar = document.querySelector('.sidebar');
const toggleButton = document.createElement('button');
toggleButton.innerText = '☰';
toggleButton.classList.add('sidebar-toggle-btn');
document.body.appendChild(toggleButton);

toggleButton.addEventListener('click', () => {
    sidebar.classList.toggle('active');
    toggleButton.classList.toggle('active');
});
