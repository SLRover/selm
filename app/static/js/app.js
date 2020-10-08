$(document).foundation();

// Setup form
let dbAlert = document.createElement('p');
dbAlert.className = 'help-text red';
dbAlert.innerHTML = 'SQLite is NOT recommended for production environment';
let databaseSelector = $('#database-select');

function showHideSetupFields() {
    if (databaseSelector.val() === 'sqlite') {
        $('.pg-field').hide();
        databaseSelector.after(dbAlert);
    } else {
        $('.pg-field').show();
        dbAlert.remove();
    }
}

$(document).ready(function () {
    showHideSetupFields();
});

databaseSelector.change(function () {
    showHideSetupFields();
});