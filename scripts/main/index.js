// Homepage for KnowledgeBytes

$(function(){
    var result, summary;
    $("#searchQuery").on("keyup ", function(key){
        if (key.which === 13) {
            ajaxReq(JSON.stringify({ "query": $(this).val()})).done(function(data){
                result = data;
                })
                summary = scrapeResults(result);   
                console.log(summary);
                $("#summary").html(summary);
        }
    });

    $("#searchSubmit").on('click', function (){
        ajaxReq(JSON.stringify({ "query": $(this).val()})).done(function(data){
            result = data;
            })
            summary = scrapeResults(result);   
            console.log(summary);
            $("#summary").html(summary);

        });
    });

function ajaxReq(data) {
    
    return $.ajax({
        url: "http:localhost:5000/search_query",
        contentType: 'application/json; charset=UTF-8',
        type: "POST",
        data: data,
        dataType: 'json'
    });
}

function scrapeResults(scrape)
{
   
var results = "";
for (prop in scrape)
{
    if(scrape.hasOwnProperty(prop) && scrape[prop])
        results += "<p>"+prop +": " +  scrape[prop] + "</p>";  
}``
return results;
}

