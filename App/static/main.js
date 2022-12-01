M.AutoInit();

let i = 1;
function add_author(){
    let form = document.getElementById("authors_form");
    i += 1;
    form.innerHTML += `
        <div class="row">
            <div class="col s6">${i}</div>
            <div class="col s12 input-field">
                <label for="fname">First Name</label>
                <input class="input-field col s12" type="text" name="fname">
            </div>

            <div class="col s12 input-field">
                <label for="lname">Last Name</label>
                <input class="input-field col s12" type="text" name="lname">
            </div>

            <div class="col s12 input-field">
                <label for="email">Email</label>
                <input class="input-field col s12" type="text" name="email">
            </div>
        </div>
    `;
};

