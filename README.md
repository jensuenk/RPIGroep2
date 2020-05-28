# WarehouseAPI

WarehouseAPI is an ASP.NET Core API for warehouses. It is usable user, product and order management.
## Usage

The web API and database are hosted on an azure app service and database server with sql. You can access the api with the following url: https://warehouseapi20200528053515.azurewebsites.net
All requests are authorized and rely on a google authorization token.


#### User Requests
The users can be sorted on name and firstName in direction asc or desc.
```http
GET /api/v1/user
GET /api/v1/user/#
GET /api/v1/user?name=""&firstName=""&email=""&address=""&tel=""&sort=""&page=#&length=#dir=""
DELETE /api/v1/user/#
PUT /api/v1/user
POST /api/v1/user
```
The products can be sorted on name, number and location in direction asc or desc.
```http
GET /api/v1/product
GET /api/v1/product/#
GET /api/v1/product?name=""&number=""&location=""&sort=""&page=#&length=#dir=""
DELETE /api/v1/product/#
PUT /api/v1/product
POST /api/v1/product
```
The orders can be sorted on date in direction asc or desc.
```http
GET /api/v1/order
GET /api/v1/order/#
GET /api/v1/order?date=""&sort=""&page=#&length=#dir=""
DELETE /api/v1/order/#
PUT /api/v1/order
POST /api/v1/order
```

#### Database Model
The database structure consists of a usertable with a one to many relation to orders. And two tables for orders and products in many to many relation joined with a join table.
## Client
The client is an implementation on how the api could be used. It consists of a dashboard where an admin can view, edit, add all users, products and orders. The client is secuired with google oAuth.
There is also a third party API wich lets the admin check if a user has a valid email address in the client.
https://mailboxlayer.com/documentation

### Installation
The client is written in Angular can can be insalled with following commands.
```sh
$ npm install
$ npm run
```



License
----

MIT
