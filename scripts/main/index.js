// Homepage for KnowledgeBytes

$(function(){

    $("#searchQuery").on("keypress", function(key){
        if (key.which === 13) {

            ajaxReq(JSON.stringify({ "query": $(this).val()}))
        }
    });
    $("#searchSubmit").on('click', function (){
        ajaxReq(JSON.stringify({ "query": $(this).val()}))
    });
});


function ajaxReq(data) {
console.log(data);

    
    
    return $.ajax({
        url: "http:localhost:5000/sample",
        contentType: 'application/json; charset=utf-8',
        type: "POST",
        data: data
    });
    

}