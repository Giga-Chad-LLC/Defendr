export function getFormData(formSelector, callback) {
    document.querySelector(formSelector).addEventListener("submit", function(e) {
        e.preventDefault();

        const formData = new FormData(this);

        // convert form data to a plain JavaScript object
        const formDataObject = {};
        formData.forEach((value, key) => {
            formDataObject[key] = value;
        });

        callback(formDataObject)
    });
}

export function createTable({form, containerSelector, headers, rows, onRowClick = null }) {
    const container = form.querySelector(containerSelector);

    // removing previous content
    container.innerHTML = '';

    const table = document.createElement("table");
    table.border = "1";

    // create the table headers
    const headerRow = table.insertRow(0);
    for (let i = 0; i < headers.length; ++i) {
        const header = document.createElement("th");
        header.innerText = headers[i];
        headerRow.appendChild(header);
    }

    // create table rows and populate data
    for (let i = 0; i < rows.length; i++) {
        const row = table.insertRow();
        const rowData = rows[i];

        for (let j = 0; j < rowData.length; j++) {
            const cell = row.insertCell(j);
            cell.innerHTML = rowData[j];
        }

        // setting on row click
        if (onRowClick != null) {
            row.classList.add('clickable-table-row');
            row.addEventListener('click', e => onRowClick(row));
        }
    }

    container.appendChild(table);
    container.style.visibility = 'visible';
}

export function createTableFromInfoboxes({ form, containerSelector, infoboxes }) {
    const headers = [
        'infobox_id',
        'infobox_user_id',
        'infobox_directory_id',
        'infobox_title',
        'infobox_icon',
        'infobox_layout',
        'field_id',
        'field_label',
        'field_type',
        'text_field_value',
        'selection_field_id',
        'option_label',
        'option_selected',
    ]

    const infoboxRows = infoboxes.map(infobox => [
        infobox.infobox_id,
        infobox.infobox_user_id,
        infobox.infobox_directory_id,
        infobox.infobox_title,
        infobox.infobox_icon,
        infobox.infobox_layout,
        infobox.field_id,
        infobox.field_label,
        infobox.field_type,
        infobox.text_field_value,
        infobox.selection_field_id,
        infobox.option_label,
        infobox.option_selected,
    ]);
    createTable({ form, containerSelector, headers, rows: infoboxRows });
}

export function showNotificationError(detail) {
    let msg = "Something went wrong. Adjust your query to achieve correct results"

    if (detail != null && typeof(detail) == 'string') {
        msg = detail;
    }
    else if (detail != null && Array.isArray(detail) && detail.length > 0) {
        msg = detail[0].msg ?? msg;
    }

    swal({
        title: "Error occured",
        text: msg,
        icon: "error"
    });
}

export function showNotificationInfo(detail) {
    swal({
        title: "Information",
        text: detail,
        icon: "info"
    });
}


export function displayFramesBySelectOptions({
    selectSelector,
    optionsToFrameSelectorsMapping,
    unhideClass,
}) {
    const select = document.querySelector(selectSelector)
    select.addEventListener('change', e => {
        for (const option of select.options) {
            const { selected, value } = option;

            const frameSelector = optionsToFrameSelectorsMapping[value]
            const frame = document.querySelector(frameSelector)

            if (selected) {
                frame.classList.toggle(unhideClass)
            }
            else {
                frame.classList.remove(unhideClass)
            }
        }
    });
}


export function populateSelectsWithOptions({ selectSelector, options }) {
    const selects = document.querySelectorAll(selectSelector);

    for(const select of selects) {
        for (const {value, label} of options) {
            const option = document.createElement('option');
            option.value = value;
            option.innerText = label;

            select.add(option);
        }
    }
}


/**
 * Creates and shows a modal with a form with email and password
 */
export function requestAuth(callback = null) {
    const modalContent = document.querySelector('#modal-1-content');
    modalContent.innerHTML = `
        <form id="auth-form" class="auth-form">
            <h2>Authorize</h2>
            <div class="auth-form__block mt-20">
                <label for="email">Email:</label>
                <input type="email" name="email" required="true" placeholder="example@gmail.com"/>
            </div>
            <div class="auth-form__block mt-20">
                <label for="password">Password:</label>
                <input type="password" name="password" required="true"/>
            </div>

            <button class="button mt-30" type="submit">Submit</button>
        </form>
    `;

    // receive data on submit
    getFormData('#auth-form', data => {
        const { email, password } = data;

        if (!email || !password) {
            showNotificationError('Either email or password was not provided. Please, fill all fields.')
        }
        else {
            localStorage.setItem('email', email);
            localStorage.setItem('password', password);

            showNotificationInfo("Authentication data saved successfully");

            if (callback != null) {
                callback({ email, password });
            }
        }

        MicroModal.close('modal-1');
    });

    MicroModal.show('modal-1');
}


export function withAuth(callback, useCached = true) {
    let email    = useCached ? localStorage.getItem("email")    : null;
    let password = useCached ? localStorage.getItem("password") : null;

    if (!email || !password) {
        requestAuth(({email, password}) => {
            console.log(email, password);
            callback({ email, password });
        });
    }
    else {
        console.log(email, password);
        callback({ email, password });
    }
}