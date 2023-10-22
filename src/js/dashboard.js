(() => {
    function getFormData(formSelector, callback) {
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

    function createTable({form, containerSelector, headers, rows}) {
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
        }

        container.appendChild(table);
        container.style.visibility = 'visible';
    }

    // requests
    {
        const host = "http://127.0.0.1:8000";

        // getting all users
        getFormData("#get-users-form", _ => {
            axios.get(`${host}/users`)
                .then(response => createTable({
                        form: document.querySelector("#get-users-form"),
                        containerSelector: ".frames-container__result",
                        headers: ["id", "email"],
                        rows: response.data.users.map(user => [user.id, user.email])
                    }))
                .catch(error => {
                    alert(`Error: ${error.response.data.detail}`)
                    console.error(error);
                });
        })

        // getting user by id
        getFormData('#get-user-by-id-form', data => {
            if (data.id == null) {
                alert("Id field cannot be empty");
                return;
            }

            axios.get(`${host}/users/${data.id}`)
            .then(response => {
                const user = response.data;

                createTable({
                    form: document.querySelector("#get-user-by-id-form"),
                    containerSelector: ".frames-container__result",
                    headers: ["id", "email"],
                    rows: [[user.id, user.email]]
                });
            })
            .catch(error => {
                alert(`Error: ${error.response.data.detail}`)
                console.error(error);
            });
        })

        // creating user
        getFormData('#create-user-form', data => {
            console.log(data)

            axios.post(`${host}/users`, data)
            .then(response => {
                const user = response.data;

                createTable({
                    form: document.querySelector("#create-user-form"),
                    containerSelector: ".frames-container__result",
                    headers: ["id", "email"],
                    rows: [[user.id, user.email]]
                });
            })
            .catch(error => {
                alert(`Error: ${error.response.data.detail}`)
                console.error(error);
            });
        });


        // creating infobox

        // online service infobox
        getFormData('#online-service-infobox-fields', data => {
            console.log(data)
        });

        // international passport infobox
        getFormData('#international-passport-infobox-fields', data => {
            console.log(data)
        });

        // bankcard infobox
        getFormData('#bankcard-infobox-fields', data => {
            data = {
                user_id: data.user_id,
                directory_id: null,
                fields: {
                    number: data.number,
                    pin: data.pin,
                    cvv: data.cvv,
                },
            };

            console.log(data);

            axios.post(`${host}/infoboxes/bankcard`, data)
            .then(response => {
                const infobox = response.data;
                console.log(infobox);

                createTable({
                    form: document.querySelector("#bankcard-infobox-fields"),
                    containerSelector: ".frames-container__result",
                    headers: ["id", "directory_id", "title", "icon", "layout"],
                    rows: [[infobox.id, infobox.directory_id, infobox.title, infobox.icon, infobox.layout]]
                });
            })
            .catch(error => {
                alert(`Error: ${error.response.data.detail}`)
                console.error(error);
            });
        });
    }

    function displayFramesBySelectOptions({
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

    displayFramesBySelectOptions({
        selectSelector: "#forms-select",
        optionsToFrameSelectorsMapping: {
            users: '#users-frame',
            directories: '#directories-frame',
            infoboxes: '#infoboxes-frame',
        },
        unhideClass: "dashboard-frame-visible",
    });

    displayFramesBySelectOptions({
        selectSelector: "#template-select",
        optionsToFrameSelectorsMapping: {
            "online-service": "#online-service-infobox-fields",
            "international-passport": "#international-passport-infobox-fields",
            "bankcard": "#bankcard-infobox-fields",
        },
        unhideClass: "infobox-fields-visible",
    });

})();