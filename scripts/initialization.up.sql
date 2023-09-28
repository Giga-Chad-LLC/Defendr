/*
Implement:
    entities:
        User        +
        Directory   +
        Infobox
        Field

    relationships:
        Infobox   -> User
        Directory -> User   +

    ISA hierarchies:
        SelectionField -> Field
        TextField -> Field
*/

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(320) NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE directories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    icon TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
