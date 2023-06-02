INSERT INTO User (address, phone, email, Bdate, password, is_seller) 
VALUES 
('1001 Oak Street, Cityville', '555-1234', 'johnsmith@example.com', '1995-09-15', 'Pass123!', 1),
('456 Elm Avenue, Townville', '555-5678', 'janesmith@example.com', '1992-07-02', 'JaneP@ssw0rd', 0);

INSERT INTO Locate (address, phone) 
VALUES 
('123 Main Street, Cityville', '555-1234'),('456 Elm Avenue, Townville', '555-5678'),('789 Maple Road, Villageland', '555-9876'),('321 Pine Lane, Hamletville', '555-4321');

INSERT INTO Type (name) 
VALUES 
('food'), ('cosmetic'), ('clothes');


INSERT INTO Product (seller_email, product_name, type_id, store, price, origin)
VALUES 
('johnsmith@example.com', 'Product A', 1, 100, 50, 'placeA'),('johnsmith@example.com', 'Product B', 2, 150, 75, 'placeB'),('johnsmith@example.com', 'Product C', 1, 80, 40, 'placeC'),('johnsmith@example.com', 'Product D', 3, 120, 60, 'placeD');

INSERT INTO Orders (user_id, product_id, price, locate_id, amount)
VALUES
(1, 1, 50, 1, 2),(2, 2, 75, 2, 1),(1, 3, 40, 1, 3),(1, 4, 60, 2, 1);


