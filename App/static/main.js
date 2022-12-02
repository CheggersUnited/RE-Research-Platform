const form = document.getElementById("authors_form");
let i = 1;

function test(){
    let node = document.createElement('div');
    let html = "<div>This is real <h1>BIG</h1> a test</div>";
    let node2 = document.createTextNode("<div>This is a test</div>");
    node.innerHTML = html;
    form.appendChild(node);
    form.appendChild(node2);
};

function add_author(){
    i += 1;
    let row = document.createElement('div');
    row.classList.add('row');
    row.classList.add('collection-item');
    row.classList.add('valign-wrapper');
    let html = `
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
    `;
    row.innerHTML = html;
    form.appendChild(row);
};

function remove_author(){
    i -= 1;
    form.removeChild(form.lastElementChild);
};

