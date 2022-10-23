create table users
(
    userID int not null,
    apiKey varchar(255)
);

create table userSpaces
(
    userID    int,
    boardName varchar(255),
    boardID   int
);

create table userPerms
(
    userID int,
    status int
);

