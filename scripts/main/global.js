// Scripts across all pages
var query;
function ajaxReq(data) {
    return $.ajax({
        url: "http:localhost:5000/sample",
        contentType: 'application/json; charset=utf-8',
        type: "POST",
        data: data
    });
    

}