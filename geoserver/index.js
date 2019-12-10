var express = require("express");
var app = express();
var codegrid = require("codegrid-js");

grid = codegrid.CodeGrid();


app.listen(3000, () => {
 console.log("Server running on port 3000");
});

app.get("/countryCode", (req, res, next) => {
 if (!("lat" in req.query) || !("lng" in req.query)) {
  res.json({"code": null, "error": "lat or lng not specified"});
  return;
 }
 console.log(req.query.lat);
 console.log(req.query.lng);
 grid.getCode(parseFloat(req.query.lat), parseFloat(req.query.lng), function(error, code) {
  res.json({"code": code, "error": error});
 })
});
