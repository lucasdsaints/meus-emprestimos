
    FOREIGN KEY (user) REFERENCES user(id),
    UNIQUE(name, user)