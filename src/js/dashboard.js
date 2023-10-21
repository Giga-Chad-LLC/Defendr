const createTable = ({form, containerClass, headers, rows}) => {
    const container = form.querySelector(containerClass);

    console.log(container)

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

    container.appendChild(table)
}

createTable({
    form: document.querySelector("#get-users-form"),
    containerClass: ".frames-container__result",
    headers: ["id", "email"],
    rows: [[1, "email1@gmail.com"], [2, "email2@gmail.com"], [3, "email3@gmail.com"]]
})