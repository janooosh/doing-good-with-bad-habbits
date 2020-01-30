const clearinformations = document.getElementById('clearinformation');
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const loginbtn = document.getElementById('login_btn');
const rgstr_btn = document.getElementById('rgstr_btn');
var submit_btn = document.getElementById('btt');
const transatcion_tbl = document.getElementById('transatcion_tbl');

rgstr_btn.addEventListener('click', () => {
    register();
});

rgstr_btn.addEventListener('click', () =>{
    validchecker();
});

loginbtn.addEventListener ('click', () => {
    logsin();
});

signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

submit_btn.addEventListener('click', () => {
    alert("i am pressed");
    transatcion_tbl.classList.remove('hide_table');
});


signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});

var attempt = 3;
var un = document.getElementById('un');
var userpw = document.getElementById('pw');
var email = document.getElementById('emailstore');
var congratsmsg = pconfirm;

function validchecker() {
    try {
        if (un.value.length <= 3 || userpw.value.length <= 3) {
            throw "The username or the password you have entered is too low";
        }
        if (un.value.length > 15 || userpw.value.length > 15) {
            throw "The username or the password you have entered is too long";
        }

        if (email.value.length > 25 || userpw.value.length < 0) {
            throw "You have not entered a password or your email is too long!";
        }
    }
    catch(e) {
        window.alert('Oops ERROR:' + ' '+ e);
        localStorage.clear();
        congratsmsg.innerHTML = "";
    }
}

// storing input from register-form
function register() {
    localStorage.setItem('un', un.value);
    localStorage.setItem('pw', userpw.value);
    localStorage.setItem('email', email.value)
    if (register) {
        congratsmsg.innerHTML = "Congrats you've made your account!";
    }
}

function logsin() {
    // here we store the data
    var storedName = localStorage.getItem('un');
    var storedPw = localStorage.getItem('pw');
    var storedEmail = localStorage.getItem('email');
    // we collect the id's from the form
    var userName = document.getElementById('userName');
    var pw = document.getElementById('userPw');
    var email = document.getElementById('emaillogin');
    // here we check if stored data from register-form is equal to data from login form
    if(userName.value === storedName && pw.value === storedPw && email.value === storedEmail) {
        alert('You will now be logged in');
        return location.href = 'mainPage.html', clearinformation();
    } else if (email.value != storedEmail) {
        congratsmsg.innerHTML = "The entered details is incorrect";
        attempt--;
    } else if (userName.value != storedName) {
        congratsmsg.innerHTML = "The entered details is incorrect";
        attempt--;
    } else if (pw.value != storedPw) {
        attempt--;
        congratsmsg.innerHTML = "The entered details is incorrect";
    } else {
        alert('Remember to sign up');
    }

    if (attempt === 0) {
        loginbtn.disabled = true;
        rgstr_btn.disabled = true;
        congratsmsg.innerHTML="An Admin has now disabled the login, because you have used too many tries!";
    }
}
function clearinformation() {
    localStorage.clear();
}

