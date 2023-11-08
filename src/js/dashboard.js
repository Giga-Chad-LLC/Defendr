import {
    getFormData,
    createTable,
    createTableFromInfoboxes,
    showNotificationError,
    displayFramesBySelectOptions,
    populateSelectsWithOptions,
    requestAuth,
} from './implementation.js';

(() => {
    // requests
    {
        const DEVELOPMENT = true;
        const host = DEVELOPMENT ? "http://127.0.0.1:8347" : "http://10.72.1.14:8347";

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
                    showNotificationError(error?.response?.data?.detail);
                    console.error(error);
                });
        })

        // getting user by id
        getFormData('#get-user-by-id-form', data => {
            if (data.id == null) {
                showNotificationError("Id field cannot be empty");
                return;
            }

            axios.get(`${host}/users/single/${data.id}`)
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
                showNotificationError(error?.response?.data?.detail);
                console.error(error);
            });
        })

        // creating user
        getFormData('#create-user-form', data => {
            console.log(data);

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
                showNotificationError(error?.response?.data?.detail);
                console.error(error);
            });
        });


        function rowClickHandler(row, data) {
            for (let i = 0; i < row.children.length && i < data.length; ++i) {
                const tableData = row.children[i];
                data[i].value = tableData.textContent;
            }

            const modalContent = document.querySelector('#modal-1-content');
            modalContent.innerHTML = "";

            for (const { label, value } of data) {
                const block = document.createElement('div');

                const labelElement = document.createElement('span');
                labelElement.innerText = label;
                labelElement.classList.add('modal__label');

                const valueElement = document.createElement('span');
                valueElement.innerText = value;
                valueElement.classList.add('modal__value');

                block.appendChild(labelElement);
                block.appendChild(valueElement);

                modalContent.appendChild(block);
            }

            MicroModal.show('modal-1');
        }

        getFormData('#users-infoboxes-count-form', data => {
            const layout = data.layout;

            axios.get(`${host}/users/layouts?layout=${layout}`)
                .then(response => createTable({
                    form: document.querySelector("#users-infoboxes-count-form"),
                    containerSelector: ".frames-container__result",
                    headers: ["user_id", "infobox_layout", "infobox_count"],
                    rows: response.data.data.map(data => [data.user_id, data.infobox_layout, data.infobox_count]),
                    onRowClick: row => rowClickHandler(row, [
                        { label: "User Id:" },
                        { label: "Infobox layout:" },
                        { label: "Infobox count:" }
                    ])
                }))
                .catch(error => {
                    showNotificationError(error?.response?.data?.detail);
                    console.error(error);
                });
        });

        getFormData('#top-users-by-infoboxes-count-form', data => {
            const {layout, limit} = data;
            axios.get(`${host}/users/top?layout=${layout}&limit=${limit}`)
                .then(response => createTable({
                    form: document.querySelector("#top-users-by-infoboxes-count-form"),
                    containerSelector: ".frames-container__result",
                    headers: ["user_id", "infobox_layout", "infobox_count"],
                    rows: response.data.data.map(data => [data.user_id, data.infobox_layout, data.infobox_count]),
                    onRowClick: row => rowClickHandler(row, [
                        { label: "User Id:" },
                        { label: "Infobox layout:" },
                        { label: "Infobox count:" }
                    ])
                }))
                .catch(error => {
                    showNotificationError(error?.response?.data?.detail);
                    console.error(error);
                });
        });




        // getting all directories
        getFormData('#get-directories-form', _ => {
            axios.get(`${host}/directories`)
                .then(response => createTable({
                        form: document.querySelector("#get-directories-form"),
                        containerSelector: ".frames-container__result",
                        headers: ["id", "user_id", "title", "icon"],
                        rows: response.data.directories.map(directory => [
                            directory.id,
                            directory.user_id,
                            directory.title,
                            directory.icon
                        ])
                    }))
                .catch(error => {
                    showNotificationError(error?.response?.data?.detail);
                    console.error(error);
                });
        });


        // getting directories by user id
        getFormData('#get-directories-by-user-id-form', data => {
            axios.get(`${host}/directories/${data.user_id}`)
                .then(response => createTable({
                        form: document.querySelector("#get-directories-by-user-id-form"),
                        containerSelector: ".frames-container__result",
                        headers: ["id", "user_id", "title", "icon"],
                        rows: response.data.directories.map(directory => [
                            directory.id,
                            directory.user_id,
                            directory.title,
                            directory.icon
                        ])
                    }))
                .catch(error => {
                    showNotificationError(error?.response?.data?.detail);
                    console.error(error);
                });
        });


        // create directory in db
        getFormData('#create-directory-form', data => {
            axios.post(`${host}/directories`, data)
                .then(response => {
                    console.log(response);

                    createTable({
                        form: document.querySelector("#create-directory-form"),
                        containerSelector: ".frames-container__result",
                        headers: ["id", "user_id", "title", "icon"],
                        rows: [[
                            response.data.id,
                            response.data.user_id,
                            response.data.title,
                            response.data.icon
                        ]]
                    });
                })
                .catch(error => {
                    showNotificationError(error?.response?.data?.detail);
                    console.error(error);
                });
        });



        // creating infobox

        // online service infobox
        getFormData('#online-service-infobox-fields', data => {
            data = {
                user_id: data.user_id,
                directory_id: null,
                fields: {
                    email: data.email,
                    password: data.password,
                    url: data.url,
                },
            };

            console.log(data);

            axios.post(`${host}/infoboxes/online-service`, data)
                .then(response => {
                    createTableFromInfoboxes({
                        form: document.querySelector("#online-service-infobox-fields"),
                        containerSelector: ".frames-container__result",
                        infoboxes: response.data.infoboxes
                    });
                })
                .catch(error => {
                    showNotificationError(error?.response?.data?.detail);
                    console.error(error);
                });
        });

        // international passport infobox
        getFormData('#international-passport-infobox-fields', data => {
            data = {
                user_id: data.user_id,
                directory_id: null,
                fields: {
                    number: data.number,
                    surname: data.surname,
                    name: data.name,
                    nationality: data.nationality,
                }
            };

            console.log(data);

            axios.post(`${host}/infoboxes/international-passport`, data)
                .then(response => {
                    createTableFromInfoboxes({
                        form: document.querySelector("#international-passport-infobox-fields"),
                        containerSelector: ".frames-container__result",
                        infoboxes: response.data.infoboxes
                    });
                })
                .catch(error => {
                    showNotificationError(error?.response?.data?.detail);
                    console.error(error);
                });
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

            axios.post(`${host}/infoboxes/bankcard`, data)
                .then(response => {
                    createTableFromInfoboxes({
                        form: document.querySelector("#bankcard-infobox-fields"),
                        containerSelector: ".frames-container__result",
                        infoboxes: response.data.infoboxes
                    });
                })
                .catch(error => {
                    showNotificationError(error?.response?.data?.detail);
                    console.error(error);
                });
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

    displayFramesBySelectOptions({
        selectSelector: "#query-forms-select",
        optionsToFrameSelectorsMapping: {
            infoboxesByLayout: "#users-infoboxes-count-frame",
            usersByInfoboxesCount: "#top-users-by-infoboxes-count-frame"
        },
        unhideClass: "dashboard-frame-visible",
    });

    populateSelectsWithOptions({
        selectSelector: ".layout-select",
        options: [
            {
                label: "Online service",
                value: "ONLINE_SERVICE"
            },
            {
                label: "International passport",
                value: "INTERNATIONAL_PASSPORT"
            },
            {
                label: "Bank card",
                value: "BANK_CARD"
            }
        ]
    });

    document.querySelector('#show-auth-modal-button').addEventListener('click', e => {
        e.preventDefault();
        requestAuth();
    });

})();