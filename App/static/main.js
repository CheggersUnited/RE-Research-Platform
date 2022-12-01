const form = document.getElementById("authors_form");
let i = 1;

function add_author(){
    i += 1;
    let html = `
        <div class="row collection-item valign-wrapper">
            <div style="height: 100%;" class="col s1">${i}</div>
            <div class="col s3 input-field">
                <label for="fname">First Name</label>
                <input class="input-field col s12" type="text" name="fname">
            </div>

            <div class="col s4 input-field">
                <label for="lname">Last Name</label>
                <input class="input-field col s12" type="text" name="lname">
            </div>

            <div class="col s4 input-field">
                <label for="email">Email</label>
                <input class="input-field col s12" type="text" name="email">
            </div>
        </div>
    `;
    form.appendChild(html);
};

function remove_author(){
    i -= 1;
    // let node = form.lastElementChild;
    form.removeChild(form.lastElementChild);
};

